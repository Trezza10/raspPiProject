import matplotlib.pyplot as plt

plt.plot([3,9,7], [8,2,0])
plt.plot([7,1,3], [1,3,6])
var = 'test'
plt.savefig('demo.png', transparent=True)

plt.show()