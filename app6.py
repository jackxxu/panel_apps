import panel as pn
import param
import numpy as np


class AppOne(param.Parameterized):
    shared_param = param.Number(default=5, bounds=(0, 10))

    def view(self):
        return pn.pane.Markdown(f"# App One\nThe shared value is {self.shared_param}")

class AppTwo(param.Parameterized):
    shared_param = param.Number(default=5, bounds=(0, 10))

    def view(self):
        return pn.pane.Markdown(f"# App Two\nThe shared value is {self.shared_param}")


class MainApp(param.Parameterized):
    app_selector = param.ObjectSelector(default="App One", objects=["App One", "App Two"])
    shared_param = param.Number(default=5, bounds=(0, 10))

    apps = {'App One': AppOne(), 'App Two': AppTwo()}

    @pn.depends('app_selector', watch=True)
    def _update_app(self):
        # Update the shared parameter in the selected app
        self.apps[self.app_selector].shared_param = self.shared_param

    @pn.depends('app_selector')
    def view(self):
        return self.apps[self.app_selector].view()

    @pn.depends('shared_param', watch=True)
    def update_shared_param(self):
        # Update shared_param in all apps when it changes
        for app in self.apps.values():
            app.shared_param = self.shared_param

# Create the main Panel application
main_app = MainApp()

# Create the layout
layout = pn.Column(
    pn.Param(main_app.param.app_selector, widgets={'app_selector': {'type': pn.widgets.RadioButtonGroup}}),
    pn.Param(main_app.param.shared_param),
    main_app.view
)

layout.servable(title="Switchable Panel Apps with Shared Control")
