import panel as pn
import param
import duckdb

class AppOne(param.Parameterized):
    shared_param = param.Number(default=5, bounds=(0, 10))
    db = duckdb.connect(database=':memory:')  # Create an in-memory DuckDB database

    def view(self):
        return pn.pane.Markdown(f"# App One\nThe shared value is {self.shared_param} db id: {id(self.db)}; app id:{id(self)}")

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

    @pn.depends('app_selector', watch=True)
    def view(self):
        return self.apps[self.app_selector].view()

    @pn.depends('shared_param', watch=True)
    def update_shared_param(self):
        # Update shared_param in all apps when it changes
        for app in self.apps.values():
            app.shared_param = self.shared_param

    def panel(self):
        template = pn.template.MaterialTemplate(title="Switchable Panel Apps with Shared Control")

        # Create a panel for the shared parameter and app selector
        settings_panel = pn.Param(
            self.param,
            parameters=['app_selector', 'shared_param'],
            widgets={'app_selector': {'type': pn.widgets.RadioButtonGroup}}
        )

        # Add to the MaterialTemplate
        template.sidebar.append(settings_panel)
        template.main.append(self.view)  # Here we append the view directly

        return template


# Create the main Panel application and serve it
main_app = MainApp()
main_app.panel().servable()
