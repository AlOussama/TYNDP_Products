"""Reproducible analytical N-1 demonstrator. NOT a real IoSN dataset."""
import numpy as np
from tyndp_reduce.dc import DetailedDC
from tyndp_reduce.security_projection import (
    cnec_operator,zonal_security,bilateral_transfer_limit,
    lodf_from_ptdf,dual_cycle_lodf,robust_uniform_derating,
)


def run():
    d=DetailedDC(('A','B','C'), ('A-B','B-C','C-A'),
                 np.array([0,1,2]), np.array([1,2,0]),
                 np.ones(3), np.array([100.,100.,80.]))
    H,A=d.ptdf(),d.incidence()
    C=cnec_operator(H,A,d.limit)
    mod=zonal_security(H,np.eye(3),np.eye(3),np.zeros(3),C)
    tau,limiting=bilateral_transfer_limit(mod,0,1)
    D,bad=lodf_from_ptdf(H,A)
    Ddual,baddual=dual_cycle_lodf(A,d.x)
    assert not bad and not baddual and np.allclose(D,Ddual)
    alpha=robust_uniform_derating(D,d.limit)
    print('Synthetic 3-bus triangle (not TYNDP data)')
    print(f'A->B N-1-safe incremental transfer: {tau:.3f} MW; binding CNEC: {limiting}')
    print(f'Conservative uniform N-0 derating factor: {alpha:.6f}')
    print(f'Dual/primal LODF max error: {np.max(abs(D-Ddual)):.2e}')

if __name__ == '__main__':
    run()
