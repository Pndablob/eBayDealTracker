import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-whitegrid')

fig = plt.figure()
ax = plt.axes()

x = [0, 2, 5]
y = [0, 8, 10]

plt.scatter(x, y)
plt.plot(x, y)

plt.show()
