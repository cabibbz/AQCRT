"""Sprint 142a: publication figures for the S136-141 thermal-gap-EP / walking-crossover arc.

Reads only existing results/*.json; writes unresolved/figures/fig{1..4}.png (+ .pdf).
Usage:  python exp_142a_figures.py
"""
import numpy as np
import json, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
FIG = os.path.join(HERE, '..', 'unresolved', 'figures')
os.makedirs(FIG, exist_ok=True)

XI = {6: 158.9, 7: 48.1, 8: 23.9, 10: 10.56}
SRC = {6: 'sprint_137b_crossover_q6.json', 7: 'sprint_138b_crossover_q7.json',
       8: 'sprint_141b_crossover_q8.json', 10: 'sprint_139b_crossover_q10.json'}
COL = {6: '#2c7fb8', 7: '#41ae76', 8: '#ef6548', 10: '#88419d'}
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'figure.dpi': 150,
                     'savefig.bbox': 'tight'})


def load(q):
    d = json.load(open(os.path.join(RES, SRC[q])))
    s = {int(k): v for k, v in d['sizes'].items()}
    ns = np.array(sorted(s), float)
    return {'n': ns,
            'dm': np.array([s[int(n)]['gap_min'] for n in ns]),
            'im': np.array([s[int(n)]['im_gEP'] for n in ns])}


D = {q: load(q) for q in XI}


def save(fig, name):
    for ext in ('png', 'pdf'):
        fig.savefig(os.path.join(FIG, f'{name}.{ext}'))
    plt.close(fig)
    print(f'  wrote {name}.png/.pdf')


# ---------------- Fig 1: the crossover ----------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))
for q in [6, 7, 8, 10]:
    d = D[q]; x = d['n'] / XI[q]
    ax1.plot(x, d['dm'] * d['n'], 'o-', ms=4.5, color=COL[q], label=f'q={q}  (ξ={XI[q]:g})')
ax1.axvline(1.0, color='0.6', lw=0.8, ls=':')
ax1.set_xlabel(r'$L/\xi_d^{\rm cl}(q)$'); ax1.set_ylabel(r'$\Delta_{\min}\,L$')
ax1.set_xscale('log'); ax1.legend(frameon=False, fontsize=9)
ax1.set_title('(a) gap amplitude: CFT-flat below ξ, decay beyond', fontsize=10)
for q in [6, 7, 8, 10]:
    d = D[q]; n, im = d['n'], d['im']
    sl = [(np.sqrt(n[i] * n[i+1]) / XI[q],
           (np.log(im[i+1]) - np.log(im[i])) / (np.log(n[i+1]) - np.log(n[i])))
          for i in range(len(n) - 1)]
    ax2.plot(*zip(*sl), 's-', ms=4, color=COL[q], label=f'q={q}')
ax2.axvline(1.0, color='0.6', lw=0.8, ls=':')
ax2.set_xlabel(r'$L_{\rm mid}/\xi_d^{\rm cl}(q)$')
ax2.set_ylabel(r'local slope  $d\ln {\rm Im}(g_{EP})/d\ln L$')
ax2.set_xscale('log'); ax2.legend(frameon=False, fontsize=9)
ax2.set_title('(b) EP local slopes: runaway sets in at L ~ ξ', fontsize=10)
fig.suptitle('Walking crossover of the thermal-gap exceptional point (open-BC $Z_q$ DMRG)', y=1.02)
save(fig, 'fig1_crossover')

# ---------------- Fig 2: the blind q=7 prediction ----------------
fig, ax = plt.subplots(figsize=(5.2, 4.0))
# S137 fitted onset coefficients (Im channel), S138 q=7 free fit
pts = {8: (1.59, None), 10: (1.71, None), 7: (1.64, 0.52)}
ax.axhspan(1.65 - 0.09, 1.65 + 0.09, color='#41ae76', alpha=0.18,
           label='registered prediction (from q=8,10): 1.65±0.09')
for q, (v, e) in pts.items():
    if q == 7:
        ax.errorbar([q], [v], yerr=[e], fmt='*', ms=16, color='#d7301f', capsize=4,
                    label='q=7 measured AFTER registration: 1.64±0.52', zorder=5)
    else:
        ax.plot([q], [v], 'o', ms=9, color='0.25')
ax.plot([], [], 'o', ms=9, color='0.25', label='q=8, 10 (S137, inputs to the prediction)')
ax.set_xlabel('q'); ax.set_ylabel(r'$\Lambda_{\rm Im}/\xi_d^{\rm cl}$')
ax.set_xticks([7, 8, 9, 10]); ax.set_xlim(6.4, 10.6); ax.set_ylim(0.8, 2.6)
ax.legend(frameon=False, fontsize=8.5, loc='lower right')
ax.set_title('Blind test of Λ ∝ ξ: the q=7 prediction', fontsize=11)
save(fig, 'fig2_blind_prediction')

# ---------------- Fig 3: the universal constant ----------------
fig, ax = plt.subplots(figsize=(6.2, 4.2))
for q in [8, 10]:
    d = D[q]; n, dm = d['n'], d['dm']
    lnR = np.log(dm * n)
    sl = [(np.sqrt(n[i] * n[i+1]) / XI[q],
           -(lnR[i+1] - lnR[i]) / (n[i+1] - n[i]) * XI[q]) for i in range(len(n) - 1)]
    ax.plot(*zip(*sl), 'o-' if q == 10 else 's-', ms=5, color=COL[q],
            label=f'q={q}   (ξ = {XI[q]:g})')
ax.axhline(0.25, color='k', lw=1.4, label=r'$1/4$  (= $\sigma_{od}^{\rm cl}\,\xi_d^{\rm cl}/2$, exact)')
ax.axhline(0.50, color='0.4', lw=1.0, ls='--', label=r'$1/2$ (classical duality) — excluded $9.9\sigma$')
ax.axhline(0.40, color='0.4', lw=1.0, ls=':', label=r'$0.40$ (onset frozen) — excluded $6.4\sigma$')
ax.annotate(r'joint shared-$s$ fit: $0.213\pm0.029$', xy=(0.45, 0.06),
            xycoords='axes fraction', fontsize=9.5)
ax.set_xlabel(r'$L_{\rm mid}/\xi_d^{\rm cl}(q)$')
ax.set_ylabel(r'$\sigma_{\rm loc}\,\xi_d^{\rm cl} = -\xi_d^{\rm cl}\, d\ln(\Delta_{\min}L)/dL$')
ax.set_ylim(-0.05, 0.62); ax.legend(frameon=False, fontsize=8.5, loc='upper left')
ax.set_title('The q-independent decay constant (S139 + S141)', fontsize=11)
save(fig, 'fig3_universal_constant')

# ---------------- Fig 4: two lengths + shadow validity ----------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.0))
d40 = json.load(open(os.path.join(RES, 'sprint_140a_xi_q10.json')))
run = next(r for r in d40['runs'] if r['n'] == 64 and abs(r['g'] - 0.1) < 1e-9)
r = np.array(run['r'], float); C = np.array(run['C'], float)
keep = C > 1e-14
ax1.semilogy(r[keep], C[keep], 'o', ms=4, color='#88419d', label=r'$C(r)$ at $g_c$, $n=64$')
xi_oz = run['xi_OZ']
rr = np.linspace(2, 30, 100)
C0 = C[2] * np.sqrt(r[2])
ax1.semilogy(rr, C0 * np.exp(-rr / xi_oz) / np.sqrt(rr), '-', color='0.3', lw=1,
             label=f'OZ fit, $\\xi_x = {xi_oz:.1f}$')
ax1.axvline(10.56, color='#d7301f', lw=1.2, ls='--')
ax1.text(10.9, 2e-3, r'$\xi_d^{\rm cl} = 10.56$', color='#d7301f', fontsize=9, rotation=90)
ax1.set_xlabel('r (sites)'); ax1.set_ylabel(r'$\langle Z_i Z^\dagger_{i+r}\rangle$')
ax1.set_xlim(0, 32); ax1.legend(frameon=False, fontsize=9)
ax1.set_title('(a) the quantum chain\'s own ξ is microscopic (q=10)', fontsize=10)

CG_Q = np.linspace(4.01, 10.5, 200)
def y_t(Q):
    th = (2 / np.pi) * np.arccosh(np.sqrt(Q) / 2)
    return 3 * (2 + th**2) / (4 + th**2)
ax2.plot(CG_Q, [y_t(Q) for Q in CG_Q], '-', color='0.3', lw=1.4,
         label=r'Re$(1/\nu_{\rm complex})$ — Coulomb-gas continuation')
meas = {5: 1.505, 6: 1.648, 7: 1.775}
ax2.plot(list(meas), list(meas.values()), 'D', ms=8, color='#ef6548',
         label=r'measured effective $1/\nu$ (S136 ED, $L<\xi$)')
ax2.axhline(2.0, color='0.6', lw=0.9, ls=':')
ax2.text(4.3, 2.02, 'first-order value  d = 2', fontsize=8.5, color='0.4')
ax2.set_xlabel('q'); ax2.set_ylabel(r'$1/\nu$')
ax2.set_ylim(1.4, 2.1); ax2.legend(frameon=False, fontsize=9, loc='lower right')
ax2.set_title('(b) "conformal shadow" reading holds only at q=5', fontsize=10)
save(fig, 'fig4_two_lengths_shadow')

print('DONE ->', FIG)
