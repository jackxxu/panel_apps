# %%

import param


# %%
class C(param.Parameterized):
    t1 = param.Number(default=2)
    t2 = param.Number(default=3)
    s = param.String(default='a string')

    # @param.depends('t1', 't2', watch=True)
    # def updating_on_t(self):
    #     print(f'New value of t1 and t2: {self.t1}, {self.t2}')

    # @param.depends('s', watch=True)
    # def updating_on_s(self):
    #     print(f'New value of s: {self.s}')

c = C()

def callback(event):
    print(event)
    print(f'Old value of s: {event.old}')
    print(f'New value of s: {event.new}')

c.param.watch(callback, ['s', 't1'], queued=True)

c.s = 'new string'
c.t1 = 4

# Watcher(
#     inst=C(name='C00007', s='a string', t1=2, t2=3), 
#     cls=<class '__main__.C'>, 
#     fn=<function callback at 0x10e744af0>, 
#     mode='args', 
#     onlychanged=True, 
#     parameter_names=('s',), 
#     what='value', 
#     queued=False, 
#     precedence=0)

# %%

import param

class C(param.Parameterized):
    _countries = {'Africa': ['Ghana', 'Togo', 'South Africa'],
                  'Asia'  : ['China', 'Thailand', 'Japan', 'Singapore'],
                  'Europe': ['Austria', 'Bulgaria', 'Greece', 'Switzerland']}
    
    continent = param.Selector(default='Asia', objects=list(_countries.keys()))
    country = param.Selector(objects=_countries['Asia'])
    
    @param.depends('continent', watch=True)
    def _update_countries(self):
        countries = self._countries[self.continent]
        self.param['country'].objects = countries
        if self.country not in countries:
            self.country = countries[0]

c = C()
c.country, c.param.country.objects

# %%
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

d = D()
d
# %%

d.param.method_dependencies('cb1')
# %%
