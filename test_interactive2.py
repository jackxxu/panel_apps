import panel as pn
import param
import hvplot.pandas
import holoviews as hv
from bokeh.sampledata.autompg import autompg_clean as df

pn.extension('tabulator', sizing_mode="stretch_width")
hv.extension('bokeh')

class InteractiveDashboard(param.Parameterized):
    cylinders = param.Integer(default=6, bounds=(4, 8))
    mfr = param.ListSelector(default=['ford', 'chevrolet', 'honda', 'toyota', 'audi'],
                             objects=['ford', 'chevrolet', 'honda', 'toyota', 'audi'])
    yaxis = param.ObjectSelector(default='hp', objects=['hp', 'weight'])

    PALETTE = ["#ff6f69", "#ffcc5c", "#88d8b0"]

    def __init__(self, **params):
        super(InteractiveDashboard, self).__init__(**params)
        self.idf = df.interactive()
        self.pipeline = None
        self.table = None
        self.hvplot = None
        self.template = None
        self._init_components()

    def _init_components(self):
        self.pipeline = (
            self.idf[
                (self.idf.cyl == self.param.cylinders) &
                (self.idf.mfr.isin(self.param.mfr))
            ]
            .groupby(['origin', 'mpg'])[self.param.yaxis].mean()
            .to_frame()
            .reset_index()
            .sort_values(by='mpg')
            .reset_index(drop=True)
        )
        self.table = self.pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size=10)
        self.hvplot = self.pipeline.hvplot(x='mpg', y=self.param.yaxis, by='origin', color=self.PALETTE, line_width=6, height=400)

        self.template = pn.template.FastListTemplate(
            title='Interactive DataFrame Dashboards with hvplot .interactive',
            sidebar=[self.param.cylinders, 'Manufacturers', self.param.mfr, 'Y axis', self.param.yaxis],
            main=[self.hvplot.panel(), self.table.panel()],
            accent_base_color="#88d8b0",
            header_background="#88d8b0",
        )

    @param.depends('cylinders', 'mfr', 'yaxis', watch=True)
    def update_view(self):
        self._init_components()
        self.template.main[0] = self.hvplot.panel()
        self.template.main[1] = self.table.panel()

    def view(self):
        return self.template

# Usage
app = InteractiveDashboard()
app.view().servable()
