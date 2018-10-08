import numpy as  np
from matplotlib import pyplot as plt



x = [[0,-1],[1,0],[3,2],[4,3],[2,2],[2,0],[1.5,1.5],[1,1],[3.5,0.5],[2,1]]

y = [[0, i*i] for i in range(10)]


y = np.array(y)
x = np.array(x)


x = x-x.mean(axis=0)
# fig = plt.figure()
# print(x)
# plt.scatter(x[:,0],x[:,1])
#plt.show()
print(x[:,1])
print(np.cov(x[:,1]*x[:,0]))
print(x[:,1]*x[:,0])
print(np.var(x[:,1]*x[:,0]))