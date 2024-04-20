import panel as pn
import param

# Ensure Panel extensions are loaded
pn.extension()

class ReactiveControls(param.Parameterized):
    # Define a parameter: a slider for integers
    number = param.Integer(default=10, bounds=(0, 100))

    # Method to update some output based on the parameter's value
    @param.depends('number')
    def view(self):
        return f'The current number is: {self.number}'

    # Method to create the Panel layout
    def panel(self):
        return pn.Column(
            pn.Param(self.param, widgets={
                'number': {'type': pn.widgets.IntSlider, 'name': 'Select Number'}
            }),
            self.view
        )

# Create an instance of the class
app = ReactiveControls()

# Make the Panel layout servable
app.panel().servable()
