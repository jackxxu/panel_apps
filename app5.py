import panel as pn
import param
import numpy as np

pn.extension(design="material", sizing_mode="stretch_width")

class AppOne(param.Parameterized):
    a = param.Number(default=5, bounds=(0, 10))

    @pn.depends('a')
    def view(self):
        return pn.pane.Markdown(f"# App One\nThe value of 'a' is {self.a}")

class AppTwo(param.Parameterized):
    b = param.Number(default=3, bounds=(1, 5))

    @pn.depends('b')
    def view(self):
        return pn.pane.Markdown(f"# App Two\nThe value of 'b' is {self.b}")


class MainApp(param.Parameterized):
    app_selector = param.ObjectSelector(default="App One", objects=["App One", "App Two"])
    apps = {'App One': AppOne(), 'App Two': AppTwo()}

    @pn.depends('app_selector', watch=True)
    def _update_app(self):
        # This method could be used to perform additional logic when switching apps
        pass

    @pn.depends('app_selector')
    def view(self):
        return self.apps[self.app_selector].view()

# Create the main Panel application
main_app = MainApp()

# Create the layout
layout = pn.Column(
    pn.Param(main_app.param.app_selector, widgets={'app_selector': {'type': pn.widgets.RadioButtonGroup}}),
    main_app.view
)

layout.servable(title="Switchable Panel Apps")
