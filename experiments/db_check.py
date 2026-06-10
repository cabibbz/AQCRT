"""results.db <-> docs drift detector (READ-ONLY).

Wired into loop.sh as a pre-sprint check. Catches the failure mode that produced the
Sprint-131 "q=5 alpha = 2.139" zombie: a headline number that lives in prose but has
NO ancestor in the database. Also reports the model-name fragmentation
('sq' vs 'sq_potts' vs 'S_q_Potts' ...) that makes query(model=...) silently incomplete.

Usage:  python db_check.py        (exit 0 = consistent, 1 = drift found)

It is intentionally conservative: it only flags a doc exponent when it is clearly tagged
to a q, in the alpha range, and matches NO results.db value for that q within tolerance.
"""
import sys, os, re, sqlite3
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # docs contain unicode
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, 'results.db')
SQ_MODELS = ('sq', 'sq_potts', 'S_q_potts', 'S_q_Potts')
TOL = 0.04           # how close a doc number must be to a DB value to count as "supported"
DOCS = ['STATE.md', 'KNOWLEDGE.md']
FLOAT = re.compile(r'([12]\.\d{2,4})')                    # alpha-range float 1.00-2.9999


def db_alpha_by_q():
    """{q: sorted list of distinct alpha_exact values across all S_q spellings}."""
    c = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    qmarks = ','.join('?' * len(SQ_MODELS))
    rows = c.execute(
        f"SELECT q, value FROM measurements WHERE quantity='alpha_exact' AND model IN ({qmarks})",
        SQ_MODELS).fetchall()
    out = {}
    for q, v in rows:
        out.setdefault(q, set()).add(round(v, 4))
    c.close()
    return {q: sorted(vs) for q, vs in out.items()}


def supported(q, val, db):
    return any(abs(val - dv) <= TOL for dv in db.get(q, []))


def _first_float(cell):
    m = FLOAT.search(cell)
    return float(m.group(1)) if m else None


def scan_docs(db):
    """Flag a doc S_q-alpha number tagged to a q that matches no DB alpha for that q.

    Source: the S_q-alpha COLUMN of any markdown exponent table -- precise and
    low-false-positive. Free-prose numbers are deliberately NOT scanned: prose carries
    incidental values (ln N, ratios) and intentionally discusses retracted numbers, so
    scanning it produces noise. Headline exponents live in the table; that is what we check."""
    drift = []
    for fn in DOCS:
        path = os.path.join(ROOT, fn)
        if not os.path.exists(path):
            continue
        lines = open(path, encoding='utf-8').read().splitlines()
        sq_col = q_col = None
        for ln, line in enumerate(lines, 1):
            # ---- (1) markdown table: track header to find the S_q-alpha column ----
            if line.lstrip().startswith('|'):
                cells = [c.strip() for c in line.split('|')]
                if any(re.search(r's_?q', c, re.I) and 'alpha' in c.lower() for c in cells):
                    # header row: locate q-column and the S_q-alpha column
                    q_col = next((i for i, c in enumerate(cells) if c.lower() == 'q'), None)
                    sq_col = next((i for i, c in enumerate(cells)
                                   if re.search(r's_?q', c, re.I) and 'alpha' in c.lower()), None)
                    continue
                if sq_col is not None and q_col is not None and len(cells) > max(sq_col, q_col):
                    if cells[q_col].isdigit():
                        q = int(cells[q_col]); val = _first_float(cells[sq_col])
                        if val is not None and q in db and not supported(q, val, db):
                            drift.append((fn, ln, q, val, db[q], line.strip()))
                continue
            else:
                sq_col = q_col = None       # table ended
    return drift


def main():
    if not os.path.exists(DB):
        print("db_check: results.db not found"); return 1
    db = db_alpha_by_q()
    print("=" * 70)
    print("DB<->DOCS DRIFT CHECK (alpha_exact, S_q family)")
    print("=" * 70)
    print("DB canonical alpha_exact by q:")
    for q in sorted(db):
        print(f"  q={q}: {db[q]}")

    # CHECK A: zombie numbers in docs
    drift = scan_docs(db)
    print("\n[A] doc exponents with no DB ancestor:")
    if not drift:
        print("  none -- docs consistent with results.db")
    else:
        for fn, ln, q, val, dbvals, text in drift:
            print(f"  DRIFT {fn}:{ln}  q={q} doc={val} not in DB {dbvals}")
            print(f"        > {text[:90]}")

    # CHECK B: model-name fragmentation -- now a HARD FAIL (audit 2026-06-09: the DB was
    # migrated to one spelling per family and db_utils.record() canonicalizes on write,
    # so any reappearance of a second spelling is a regression, not history).
    c = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    models = [r[0] for r in c.execute("SELECT DISTINCT model FROM measurements").fetchall()]
    maxs = c.execute("SELECT MAX(sprint) FROM measurements").fetchone()[0]
    sq_variants = [m for m in models if m and m.lower().replace('_', '').startswith('sqpotts') or m in SQ_MODELS]
    frag = []
    if len(sq_variants) > 1:
        frag.append(f"S_q family has {len(sq_variants)} spellings: {sq_variants}")
    hyb2 = [m for m in models if m and m.lower() == 'hybrid_2d']
    if len(hyb2) > 1:
        frag.append(f"hybrid_2d family has {len(hyb2)} spellings: {hyb2}")
    print("\n[B] model-name fragmentation (one canonical spelling per family):")
    if frag:
        for f in frag:
            print(f"  FRAGMENTED: {f}")
    else:
        print(f"  ok -- canonical: {sq_variants}")

    # CHECK D: method-conflict detector (audit 2026-06-09). A (quantity,model,q,n) group
    # whose values disagree by >1% across methods is a collision like the old c_eff one.
    # Legacy groups (all rows sprint<=136) are HISTORY: count only. New rows (sprint>=137)
    # that create/extend a conflict FAIL the gate.
    conf = c.execute("""
        SELECT quantity, model, q, n, MIN(value), MAX(value), MAX(sprint),
               COUNT(DISTINCT method)
        FROM measurements
        WHERE value IS NOT NULL AND quantity NOT LIKE 'g_c%'
        GROUP BY quantity, model, q, n
        HAVING COUNT(DISTINCT method) > 1
           AND ABS(MAX(value) - MIN(value)) > 0.01 * MAX(ABS(MAX(value)), ABS(MIN(value)))
    """).fetchall()
    c.close()
    new_conf = [r for r in conf if (r[6] or 0) >= 137]
    print(f"\n[D] cross-method value conflicts >1% (same quantity/model/q/n): "
          f"{len(conf)} legacy group(s) [informational]")
    for r in new_conf:
        print(f"  NEW CONFLICT (sprint {r[6]}): {r[0]} {r[1]} q={r[2]} n={r[3]} "
              f"values {r[4]:.6g}..{r[5]:.6g} across {r[7]} methods")

    # CHECK C: provenance / freshness
    sprint_reports = [f for f in os.listdir(os.path.join(ROOT, 'sprints')) if re.match(r'sprint_\d+', f)]
    latest_report = max(int(re.search(r'\d+', f).group()) for f in sprint_reports) if sprint_reports else 0
    print(f"\n[C] freshness: DB max sprint = {maxs}; latest sprint report = {latest_report}")
    if latest_report > (maxs or 0):
        print(f"  note: sprints {(maxs or 0)+1}..{latest_report} wrote no DB rows -- "
              "DB may lag the latest doc framing (check retractions by hand).")

    print("\n" + "=" * 70)
    problems = []
    if drift:
        problems.append(f"doc drift ({len(drift)})")
    if frag:
        problems.append(f"model fragmentation ({len(frag)})")
    if new_conf:
        problems.append(f"new method conflicts ({len(new_conf)})")
    print(f"DB-CHECK: {'FAIL: ' + ', '.join(problems) if problems else 'consistent'}")
    print("=" * 70)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
