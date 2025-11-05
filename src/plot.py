import matplotlib.pyplot as plt
import numpy as np
import sympy
from sympy.abc import x, y

curve = sympy.Eq(y**2,x**3 + 486662*x**2+x)
for_y = sympy.solve(curve, y)
f = sympy.lambdify(x, for_y)

x = np.linspace(-10**-5, 10**-5, 100)

_ = [plt.plot(x, y) for y in f(x)]
plt.show()
