import numpy as np

a = np.array([[1,2,3],[1,2,3],[-np.Inf,np.NAN,np.Inf]])
a[a>=np.Inf] = 0
a[a<=-np.Inf] = 0



print(a)

print(np.mean(a))
print(np.nanmean(a))