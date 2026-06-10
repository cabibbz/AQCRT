#!/usr/bin/env python3
"""Pretty-print Claude Code `--output-format stream-json` into a verbose, readable live view.

Reads NDJSON on stdin, prints a human-readable running transcript of the sprint: model/tools
banner, assistant text, thinking, every tool call WITH its inputs, tool-result previews, and
per-turn + final token/cost usage. The raw .jsonl (saved by tee in loop.sh) stays intact for
forensics; this is purely the on-screen view.

Usage (loop.sh):
    claude ... --output-format stream-json --verbose | tee sprint.jsonl | python format_stream.py

Env toggles:
    STREAM_FULL=1     show thinking/results untruncated (default: generous truncation)
    NO_COLOR=1        disable ANSI color
"""
import sys, os, json, shutil

try:
    # sprint content is full of unicode (chi, nu, alpha, arrows) and we print emoji markers;
    # force utf-8 so it never crashes on a cp1252 console (Git Bash renders it correctly).
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FULL = os.environ.get("STREAM_FULL") == "1"
COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") != "1"
WIDTH = min(shutil.get_terminal_size((100, 20)).columns, 120)

# generous limits -- this view is meant to be VERBOSE
T_THINK = 10 ** 9 if FULL else 2000
T_RESULT = 10 ** 9 if FULL else 700
T_ARG = 10 ** 9 if FULL else 400


def c(code, s):
    return f"\033[{code}m{s}\033[0m" if COLOR else s


def trunc(s, n):
    s = str(s)
    return s if len(s) <= n else s[:n] + c("2", f" …(+{len(s)-n} chars)")


def rule(ch="-"):
    return ch * WIDTH


def fmt_input(inp):
    if not isinstance(inp, dict):
        return trunc(inp, T_ARG)
    out = []
    for k, v in inp.items():
        v = str(v).replace("\n", "\\n")
        out.append(f"{c('36', k)}={trunc(v, T_ARG)}")
    return "\n      ".join(out)


def emit(ev):
    t = ev.get("type")
    if t == "system" and ev.get("subtype") == "init":
        print(c("1;44", rule("=")))
        print(c("1", f"  session {str(ev.get('session_id',''))[:8]} | model {ev.get('model','?')} "
                      f"| {len(ev.get('tools',[]))} tools | cwd {ev.get('cwd','')}"))
        print(c("1;44", rule("=")))
    elif t == "assistant":
        msg = ev.get("message", {})
        for b in msg.get("content", []):
            bt = b.get("type")
            if bt == "text" and b.get("text", "").strip():
                print("\n" + c("1;37", "💬 ") + b["text"].strip())
            elif bt == "thinking" and b.get("thinking", "").strip():
                print("\n" + c("35", "🤔 thinking: ") + c("2", trunc(b["thinking"].strip(), T_THINK)))
            elif bt == "tool_use":
                print("\n" + c("1;33", f"🔧 {b.get('name','?')}"))
                print("      " + fmt_input(b.get("input", {})))
        u = msg.get("usage") or {}
        if u.get("output_tokens"):
            print(c("2", f"   · in {u.get('input_tokens',0)} / out {u.get('output_tokens',0)}"
                         f" / cache {u.get('cache_read_input_tokens',0)}"))
    elif t == "user":
        for b in (ev.get("message", {}).get("content") or []):
            if isinstance(b, dict) and b.get("type") == "tool_result":
                cc = b.get("content")
                if isinstance(cc, list):
                    cc = " ".join(x.get("text", "") for x in cc if isinstance(x, dict))
                tag = c("1;31", "↳ ERROR ") if b.get("is_error") else c("32", "↳ ")
                print("   " + tag + trunc(str(cc).strip(), T_RESULT))
    elif t == "result":
        ok = ev.get("subtype", "done")
        print("\n" + c("1;42" if ok == "success" else "1;41", rule("=")))
        print(c("1", f"  {ok} | {ev.get('num_turns','?')} turns | "
                     f"{ev.get('duration_ms',0)/1000:.1f}s | ${ev.get('total_cost_usd',0):.4f}"))
        u = ev.get("usage") or {}
        if u:
            print(c("1", f"  tokens: in {u.get('input_tokens',0)} / out {u.get('output_tokens',0)}"
                         f" / cache_read {u.get('cache_read_input_tokens',0)}"))
        print(c("1;42" if ok == "success" else "1;41", rule("=")))


def main():
    # readline iteration (not `for line in sys.stdin`) avoids read-ahead buffering, so the
    # view streams live as the sprint runs rather than appearing all at once at the end.
    for line in iter(sys.stdin.readline, ""):
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            # not a JSON event (e.g. a stray stderr line) -- show it raw, don't crash
            print(c("2", line))
            sys.stdout.flush()
            continue
        if not isinstance(ev, dict):
            # valid JSON but not an event object (e.g. a bare string/number) -- the old
            # handler crashed HERE on ev.get and killed the live view (audit 2026-06-09)
            print(c("2", line))
            sys.stdout.flush()
            continue
        try:
            emit(ev)
        except Exception as e:
            et = ev.get("type") if isinstance(ev, dict) else type(ev).__name__
            print(c("2", f"[format_stream: {type(e).__name__} on {et}: {e}]"))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
