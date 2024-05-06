import param
import panel as pn

pn.extension()

class DropdownApp(param.Parameterized):
    first_choice = param.Selector(default="Fruits", objects=["Fruits", "Colors"])
    
    options = {
        "Fruits": ["Apple", "Banana", "Cherry"],
        "Colors": ["Red", "Blue", "Green"]
    }
    
    # Adding sub-options for each option in second_choice
    sub_options = {
        "Apple": ["Pie", "Juice", "Sauce"],
        "Banana": ["Bread", "Smoothie", "Split"],
        "Cherry": ["Jam", "Cobbler", "Ice Cream"],
        "Red": ["Rose", "Apple", "Car"],
        "Blue": ["Sky", "Berry", "Whale"],
        "Green": ["Grass", "Apple", "Alien"]
    }

    second_choice = param.Selector(default="Apple", objects=options["Fruits"])
    third_choice = param.Selector(default="Pie", objects=sub_options["Apple"])
    
    def view(self):
        print('v'*100)
        return pn.pane.Markdown(f"## You selected {self.first_choice}, {self.second_choice}, and {self.third_choice}")

    @param.depends('first_choice', watch=True)
    def _update_second_choice(self):
        print('2'*100)
        self.param.second_choice.objects = self.options[self.first_choice]
        self.second_choice = self.param.second_choice.objects[0]  # Reset to default
        self._update_third_choice()  # Also update the third_choice when the first_choice changes

    @param.depends('second_choice', watch=True)
    def _update_third_choice(self):
        print('3'*100)
        self.param.third_choice.objects = self.sub_options[self.second_choice]
        self.third_choice = self.param.third_choice.objects[0]  # Reset to default

    def panel(self):
        return pn.Column(
            pn.Param(self.param.first_choice),
            pn.Param(self.param.second_choice),
            pn.Param(self.param.third_choice),
            self.view
        )

# Create an instance of the app
app = DropdownApp()

# Serve the panel app
app.panel().servable()
