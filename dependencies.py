# %%

import param

class C(param.Parameterized):
    _countries = {'Africa': ['Ghana', 'Togo', 'South Africa'],
                  'Asia'  : ['China', 'Thailand', 'Japan', 'Singapore'],
                  'Europe': ['Austria', 'Bulgaria', 'Greece', 'Switzerland']}
    
    continent = param.Selector(default='Asia', objects=list(_countries.keys()))
    country = param.Selector(objects=[])
    
    @param.depends('continent', watch=True, on_init=True)
    def _update_countries(self):
        print('updating c')
        countries = self._countries[self.continent]
        self.param['country'].objects = countries
        if self.country not in countries:
            self.country = countries[0]

c = C()
c.country, c.param.country.objects

class D(param.Parameterized):
    x = param.Number(7)
    s = param.String("never")
    i = param.Integer(-5)
    o = param.Selector(objects=['red', 'green', 'blue'])
    n = param.ClassSelector(default=c, class_=param.Parameterized, instantiate=False)                    
    
    @param.depends('x', 's', 'n.country', 's:constant', watch=True)
    def cb1(self):
        print(f"cb1 x={self.x} s={self.s} "
              f"param.s.constant={self.param.s.constant} n.country={self.n.country}")

    @param.depends('n.param', watch=True)
    def cb2(self):
        print(f"cb2 n={self.n}")

    @param.depends('x', 'i', watch=True)
    def cb3(self):
        print(f"cb3 x={self.x} i={self.i}")

    @param.depends('cb3', watch=True)
    def cb4(self):
        print(f"cb4 x={self.x} i={self.i}")

    @param.depends('x', watch=True)
    def cb5(self):
        print(f"cb4 x={self.x} ")

    def cb6(self):
        print(f"cb4 x={self.x} ")

    @param.depends('n', watch=True)
    def cb7(self):
        print(f"cb4 x={self.x} ")

d = D()
d
import panel as pn
pn.extension()
# pn.Column(c.param.continent, c.param.country, d.param.x, d.param.s, d.param.i, d.param.o, d.param.n)
pn.Column(c, d)

# %%
c.param.continent.__slots__

# %%

d.param.method_dependencies('cb1')
# %%
dependencies = d.param.method_dependencies('cb5')
[f"{o.inst.name}.{o.pobj.name}:{o.what}" for o in dependencies]

# %%
dependencies = d.param.method_dependencies('cb6')
[f"{o.inst.name}.{o.pobj.name}:{o.what}" for o in dependencies]

# %%
class Mul(param.Parameterized):
    a = param.Number(5,  bounds=(-100, 100))
    b = param.Number(-2, bounds=(-100, 100))

    @param.depends('a', 'b')
    def view(self):
        return str(self.a*self.b)

    def view2(self):
        return str(self.a*self.b)

prod = Mul(name='Multiplier')

pn.Row(prod.param, prod.view2)

# %%
