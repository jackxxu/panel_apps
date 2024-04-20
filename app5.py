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

    def __init__(self, **params):
        super(MainApp, self).__init__(**params)
        self.template = pn.template.MaterialTemplate(title='Switchable Panel Apps')
        self.setup_template()

    def setup_template(self):
        # Setup the sidebar with the app selector
        app_selector_widget = pn.Param(
            self.param.app_selector,
            widgets={'app_selector': {'type': pn.widgets.RadioButtonGroup}}
        )

        # Add sidebar and main area components
        self.template.sidebar.append(app_selector_widget)
        self.template.main.append(pn.Row(self.view))

    @pn.depends('app_selector')
    def view(self):
        return self.apps[self.app_selector].view()

# Create the main application instance
main_app = MainApp()

# Serve the application
main_app.template.servable()
