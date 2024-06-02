# %%

import param, random
import panel as pn

pn.extension()

class P(param.Parameterized):
    i = param.Integer(2)
    j = param.Integer(5)
    k = param.Integer(8)
    x = param.Number(-13.6)

p = P(i=6, x=9.8)

# %%
p.i
# %%
p_dynamic = P(i=lambda: random.randint(35,99), x=lambda: random.random())
p_dynamic

print(p_dynamic.i, p_dynamic.i)
# %%
print(p_dynamic.x, p_dynamic.x)
# %%
p.param.inspect_value('x'), p.param.inspect_value('x'), p.param.inspect_value('x')

# %%
# display p_dynamic.x as a slider
pn.Param(
    p_dynamic.param.x, 
    widgets={'x': pn.widgets.FloatSlider}
)

p.param.inspect_value('x')
# %%
pn.Param(
    p_dynamic.param.x, 
    widgets={'x': pn.widgets.FloatSlider}
)

# %%

class A(param.Parameterized):
    x = param.Selector(default='a', objects=[])

A = A()

# %%
import param
import random 
class DynamicSelector(param.Selector):
    def __get__(self, obj, objtype):
        print(obj, objtype)
        if obj is not None:
            self.objects = obj.dynamic_objects()
        return super().__get__(obj, objtype)

class DynamicSelectorExample(param.Parameterized):
    dynamic_selector = DynamicSelector(default=None, objects=[])
    i = param.Integer(default=0)

    option_groups = [
        ['Option 1', 'Option 2', ],
        ['Option A', 'Option A1', ],
        ['Option B', 'Option B2'],
        ['Option C', 'Option C2'],
        ['Option D', 'Option D2'],
    ]

    def dynamic_objects(self):
        s = random.choice(self.option_groups) 
        print('1'*10, s)
        return s

    def view(self):
        # Dummy view function to display the current state
        return f"Current selection: {self.dynamic_selector}, Available options: {self.param.dynamic_selector.objects} {self.i}"

# Example usage
dynamic_selector_example = DynamicSelectorExample()
print(dynamic_selector_example.view())  # Outputs: Current selection: None, Available options: ['Option 1', 'Option 2', 'Option 3']

# %%

pn.Param(
    dynamic_selector_example
) 

# %%

pn.Param(
    dynamic_selector_example
) 
# %%
import param
import random

class DynamicSelector(param.Selector):
    def __get__(self, obj, objtype):
        if obj is not None:
            self.objects = obj.generate_random_options()
            print(self.objects)
        return super().__get__(obj, objtype)

class DynamicSelectorExample(param.Parameterized):
    def generate_random_options(self):
        return [f"Option {i}" for i in random.sample(range(1, 10), 3)]

    @property
    def dynamic_selector(self):
        return param.Selector(default=None, objects=self.generate_random_options())

    def view(self):
        # Dummy view function to display the current state
        selector_param = self.param.dynamic_selector
        return f"Current selection: {self.dynamic_selector}, Available options: {selector_param.objects}"

# Example usage
dynamic_selector_example = DynamicSelectorExample()
print(dynamic_selector_example.view())  # Outputs the current selection and available options

# Re-accessing the dynamic_selector to see the dynamic update in action
print(dynamic_selector_example.view())  # Outputs the current selection and available options

# %%
