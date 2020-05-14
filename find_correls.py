#RUNNING THE CHAIN
import numpy as np
def adder(a, b):
    return a+b, a

regcf = np.zeros(5000)

for kk in range(5000):
    zx = np.corrcoef(reg, np.roll(reg, kk))
    regcf[kk]=zx[0,1]
    
rmmcf = np.zeros(5000)


for kk in range(5000):
    zx = np.corrcoef(rmm, np.roll(rmm, kk))
    rmmcf[kk]=zx[0,1]
    
rswcf = np.zeros(5000)

for kk in range(5000):
    zx = np.corrcoef(rsw, np.roll(rsw, kk))
    rswcf[kk]=zx[0,1]
