import panel as pn
import pandas as pd
import altair as alt
import param

pn.extension("plotly", "vega")

data = pd.DataFrame([
    ('Monday', 7), ('Tuesday', 4), ('Wednesday', 9), ('Thursday', 4),
    ('Friday', 4), ('Saturday', 5), ('Sunday', 4)], columns=['Day', 'Wind Speed (m/s)']
)

class Plot(param.Parameterized):
    slider = param.Integer(default=7, bounds=(1, 7))
    slider2 = param.Integer(default=7, bounds=(1, 7))

    def data_plot(self):
        print('in data_plot')
        fig = (
            alt.Chart(data.head(self.slider))
            .mark_line(point=True)
            .encode(
                x="Day",
                y=alt.Y("Wind Speed (m/s)", scale=alt.Scale(domain=(0, 10))),
                tooltip=["Day", "Wind Speed (m/s)"],
            )
            .properties(width="container", height="container", title="Wind Speed Over the Week")
        )
        return fig

    def view(self): 
        print('in view  ')
        return pn.Column(
            self.param.slider,
            self.param.slider2,
            self.data_plot
        )
    
plot = Plot()
plot.view().servable()
