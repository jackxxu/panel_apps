import panel as pn
import pandas as pd
import altair as alt
import param
import random 


data = pd.DataFrame([
    ('Monday', 7), ('Tuesday', 4), ('Wednesday', 9), ('Thursday', 4),
    ('Friday', 4), ('Saturday', 5), ('Sunday', 4)], columns=['Day', 'Wind Speed (m/s)']
)

class Plot(param.Parameterized):
    slider = param.Integer(default=7, bounds=(1, 7))

    def data_plot(self):
        print('1'*100)

        # generate a random integer between 1 and 7
        random_integer = random.randint(1, 7)

        fig = (
            alt.Chart(data.head(random_integer))
            .mark_line(point=True)
            .encode(
                x="Day",
                y=alt.Y("Wind Speed (m/s)", scale=alt.Scale(domain=(0, 10))),
                tooltip=["Day", "Wind Speed (m/s)"],
            )
            .properties(width="container", height="container", title="Wind Speed Over the Week")
        )

        return pn.panel(fig, sizing_mode="stretch_width", height=400)

    def view(self): 
        return pn.Column(
            pn.Param(self.param.slider), 
            self.data_plot, # self.data_plot()
        )
    

Plot().view().servable()