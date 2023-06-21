import numpy as np
from collections import defaultdict

""" This module is modified from https://sidsite.com/posts/autodiff/ and https://github.com/sradc/SmallPebble """

class Variable:
    def __init__(self, value, gradients=None, name=''):
        self.value = value
        # If no gradients are given we assume it is a variable with gradient 1
        # which corresponds to the derivative with respect to itself (dx/dx)
        self._gradients = gradients if gradients is not None else ((self, np.sign(value)),)
        self.name = name
        self._stored_gradients = None
    
    def __add__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        return add(self, other)

    def __radd__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        return add(self, other)
    
    def __mul__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        return mul(self, other)

    def __rmul__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        return mul(self, other)
    
    def __sub__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        return add(self, neg(other))

    def __rsub__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        return add(other, neg(self))

    def __truediv__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        return mul(self, inv(other))

    def __rtruediv__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        return mul(other, inv(self))

    def __pow__(self, exponent):
        return pow(self, exponent)

    def __rpow__(self, exponent):
        return pow(exponent, self)

    def __neg__(self):
        return neg(self)

    def __repr__(self):
        return f'{self.name}' if self.name else f'{self.value}'
    
    @property
    def gradients(self):
        if self._stored_gradients is None:
            self._stored_gradients = dict(compute_gradients(self))
        return self._stored_gradients
    
def add(a, b):
    value = a.value + b.value    
    gradients = (
        (a, 1),
        (b, 1)
    )
    return Variable(value, gradients)

def mul(a, b):
    value = a.value * b.value
    gradients = (
        (a, b.value),
        (b, a.value)
    )
    return Variable(value, gradients)

def neg(a):
    value = -1 * a.value
    gradients = (
        (a, -1),
    )
    return Variable(value, gradients)

def inv(a):
    value = 1. / a.value
    gradients = (
        (a, -1 / a.value**2),
    )
    return Variable(value, gradients)   

def pow(a, n):
    value = a.value**n
    gradients = (
        (a, n * a.value),
    )
    return Variable(value, gradients)   

def exp(a):
    a = a if isinstance(a, Variable) else Variable(a)
    value = np.exp(a.value)
    gradients = (
        (a, value),
    )
    return Variable(value, gradients)


def compute_gradients(variable):
    """ Compute the first derivatives of `variable` 
    with respect to child variables.
    """
    gradients = defaultdict(lambda: 0)
    
    def _compute_gradients(variable, total_gradient):
        for child_variable, child_gradient in variable._gradients:
            # "Multiply the edges of a path":
            gradient = total_gradient * child_gradient
            # "Add together the different paths":
            gradients[child_variable] += gradient
            # if the child variable only has itself as a gradient 
            # we have reached the end of recursion
            criteria = (
                len(child_variable._gradients) == 1 and 
                child_variable._gradients[0][0] is child_variable
            )
            if not criteria:
                # recurse through graph:
                _compute_gradients(child_variable, gradient)
    
    _compute_gradients(variable, total_gradient=1)
    # (total_gradient=1 is from `variable` differentiated w.r.t. itself)
    return gradients


if __name__=='__main__':
    print('testing ...')

    def f(a, b):
        return (a / b - a) * (b / a + a + b) * (a - b)

    a = Variable(230.3)
    b = Variable(33.2)
    y = f(a, b)

    gradients = compute_gradients(y)

    delta = Variable(1e-8)
    numerical_grad_a = (f(a + delta, b) - f(a, b)) / delta
    numerical_grad_b = (f(a, b + delta) - f(a, b)) / delta

    def isclose(a, b):
        a = a if not isinstance(a, Variable) else a.value
        b = b if not isinstance(b, Variable) else b.value
        return np.isclose(a, b)

    assert isclose(gradients[a], numerical_grad_a)
    assert isclose(y.gradients[b], numerical_grad_b)

    def loss(y, y_hat):
        return 0.5 * (y - y_hat)**2

    def sigma(x):
        return 1. / (1. + exp(-x))

    def y_hat(w_0, w_1, x_1):
        return sigma(w_0 + w_1*x_1)

    def dy_hat_dw_1(w_0, w_1, x_1):
        return x_1*y_hat(w_0, w_1, x_1) * (1 - y_hat(w_0, w_1, x_1))

    def dloss_dw_1(y, w_0, w_1, x_1):
        return (y_hat(w_0, w_1, x_1) - y) * dy_hat_dw_1(w_0, w_1, x_1)
    
    def linear_y_hat(w_0, w_1, x_1):
        return w_0 + w_1*x_1
    
    def linear_dL_dw0(y, y_hat):
        return y_hat - y

    def linear_dL_dw1(y, y_hat, x_1):
        return x_1*(y_hat - y)
    
    x_1 = Variable(0.1, name='x_1')
    w_0 = Variable(4, name='w_0')
    w_1 = Variable(3, name='w_1')
    y = Variable(10, name='y')

    
    assert isclose(compute_gradients(
        loss(y, y_hat(w_0, w_1, x_1)))[y], y - y_hat(w_0, w_1, x_1)
        )
    assert isclose(
        compute_gradients(y_hat(w_0, w_1, x_1))[w_1], dy_hat_dw_1(w_0, w_1, x_1)
        )
    assert isclose(
        compute_gradients(loss(y, y_hat(w_0, w_1, x_1)))[w_1], dloss_dw_1(y, w_0, w_1, x_1)
        )
    assert isclose(
        compute_gradients(loss(y, linear_y_hat(w_0, w_1, x_1)))[w_1], linear_dL_dw1(y, linear_y_hat(w_0, w_1, x_1), x_1)
        )
    assert isclose(
        compute_gradients(loss(y, linear_y_hat(w_0, w_1, x_1)))[w_0], linear_dL_dw0(y, linear_y_hat(w_0, w_1, x_1))
        )
    
    print('all tests were succsessful')