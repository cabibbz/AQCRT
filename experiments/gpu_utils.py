"""GPU-accelerated eigensolver — drop-in replacement for scipy.sparse.linalg.eigsh.

Usage: Replace `from scipy.sparse.linalg import eigsh` with `from gpu_utils import eigsh`
That's it. Same API. Automatically uses GPU when beneficial, falls back to CPU.

    from gpu_utils import eigsh
    evals, evecs = eigsh(H, k=4, which='SA')

Observability (added after the audit): GPU availability is NOT silent. If CuPy fails to
import, the reason is recorded in CUPY_IMPORT_ERROR and a one-time warning is printed the
first time a large matrix has to run on CPU — so a broken GPU can no longer masquerade as
a working one (which previously left results.db with unreproducible "GPU" entries).
Check `from gpu_utils import GPU_ENABLED, gpu_status`.
"""
import sys
import numpy as np
from scipy.sparse.linalg import eigsh as cpu_eigsh

_has_cupy = False
CUPY_IMPORT_ERROR = None
try:
    import cupy as cp
    from cupyx.scipy.sparse import csr_matrix as cp_csr
    from cupyx.scipy.sparse.linalg import eigsh as _cp_eigsh
    _has_cupy = True
except Exception as e:                       # ImportError, ABI mismatch, missing DLL, ...
    CUPY_IMPORT_ERROR = f"{type(e).__name__}: {e}"

GPU_ENABLED = _has_cupy
# Use GPU when matrix dimension exceeds this threshold
GPU_THRESHOLD = 50000

_warned = set()


def _warn_once(key, msg):
    if key not in _warned:
        _warned.add(key)
        print(f"[gpu_utils] {msg}", file=sys.stderr, flush=True)


def gpu_status():
    """One-line backend status (call it / log it at sprint start)."""
    if _has_cupy:
        try:
            name = cp.cuda.runtime.getDeviceProperties(0)['name']
            name = name.decode() if isinstance(name, bytes) else name
            return f"GPU enabled (CuPy {cp.__version__}, device {name})"
        except Exception as e:
            return f"GPU import OK but device query failed: {e}"
    return f"GPU DISABLED -> CPU only. CuPy unavailable: {CUPY_IMPORT_ERROR}"


def eigsh(A, k=6, which='SA', return_eigenvectors=True, **kwargs):
    """Drop-in replacement for scipy.sparse.linalg.eigsh.
    Uses GPU (CuPy) when matrix dimension > 50k and CuPy is available.
    Falls back to CPU otherwise or on GPU error -- and SAYS SO (once) when it does.

    NOTE on ordering: with return_eigenvectors=False, raw scipy returns eigenvalues
    DESCENDING while CuPy returns them ASCENDING -- a silent sign-flip trap at the
    50k backend switch. This wrapper therefore normalizes that path to ASCENDING
    order on BOTH backends (audit 2026-06-09). The eigenvector path is unchanged
    (callers index/sort as before)."""
    n = A.shape[0]

    if n > GPU_THRESHOLD and not _has_cupy:
        _warn_once('no_cupy',
                   f"dim={n} > {GPU_THRESHOLD} but running on CPU (CuPy unavailable: "
                   f"{CUPY_IMPORT_ERROR}). Large/GPU-sized work will be slow or infeasible.")

    if _has_cupy and n > GPU_THRESHOLD:
        try:
            A_gpu = cp_csr(A)
            if return_eigenvectors:
                evals_gpu, evecs_gpu = _cp_eigsh(A_gpu, k=k, which=which, **kwargs)
                return cp.asnumpy(evals_gpu), cp.asnumpy(evecs_gpu)
            else:
                evals_gpu = _cp_eigsh(A_gpu, k=k, which=which,
                                       return_eigenvectors=False, **kwargs)
                return np.sort(cp.asnumpy(evals_gpu))
        except Exception as e:
            # Do NOT silently swallow: a GPU error that falls back to CPU must be visible.
            _warn_once(f'gpu_err_{type(e).__name__}',
                       f"GPU eigsh failed at dim={n} ({type(e).__name__}: {e}); "
                       f"falling back to CPU.")

    if return_eigenvectors:
        return cpu_eigsh(A, k=k, which=which, return_eigenvectors=True, **kwargs)
    return np.sort(cpu_eigsh(A, k=k, which=which, return_eigenvectors=False, **kwargs))
