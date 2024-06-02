# %%
import param 
import panel as pn

class A(param.Parameterized):
    x = param.Number()

a1 = A()
a2 = A()

a1.x = 1

print(a1.x, a2.x, type(a1.param.x))

# %%

print(a1.x, A.x)


# %%

import param

class A(param.Parameterized):
    x = param.Number(default=0.0)

A.x = 2
# Accessing the descriptor
print(A().x)  # Outputs: <Number at ...>

# %%

class C(param.Parameterized):
    t1 = param.Number(default=2)
    t2 = param.Number(default=3)
    s = param.String(default='a string')

    @param.depends('t1', 't2', watch=True)
    def updating_on_t(self):
        print(f'New value of t1 and t2: {self.t1}, {self.t2}')

    @param.depends('s', watch=True)
    def updating_on_s(self):
        print(f'New value of s: {self.s}')

c = C()

c.t1 = 2
c.t2 = 3

# %%
type(A.x)
# %%
type(A.param.x)

# %%
# %%
isinstance(A.param.x, param.Parameterized)
# %%
isinstance(A.param.x, param.Parameter)

# %%
isinstance(A().param.x, param.Parameterized)
A().param.x
# %%
