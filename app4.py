import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import param

# Define constants
PRIMARY_COLOR = "#0072B5"
SECONDARY_COLOR = "#B54300"
CSV_FILE = "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"

# Extend the param.Parameterized class
class MyPanelApp(param.Parameterized):
    # Define parameters
    variable = param.Selector(default="Temperature", objects=["Temperature", "Humidity", "Light", "CO2", "HumidityRatio"])
    window = param.Integer(default=30, bounds=(1, 60))
    sigma = param.Integer(default=10, bounds=(0, 20))
    
    # Data loading and caching
    @pn.depends('variable')
    def get_data(self):
        return pd.read_csv(CSV_FILE, parse_dates=["date"], index_col="date")

    def transform_data(self):
        """Calculates the rolling average and identifies outliers"""
        data = self.get_data()
        avg = data[self.variable].rolling(window=self.window).mean()
        residual = data[self.variable] - avg
        std = residual.rolling(window=self.window).std()
        outliers = np.abs(residual) > std * self.sigma
        return avg, avg[outliers]

    @pn.depends('variable', 'window', 'sigma')
    def get_plot(self):
        """Plots the rolling average and the outliers"""
        avg, highlight = self.transform_data()
        return avg.hvplot(
            height=300, legend=False, color=PRIMARY_COLOR
        ) * highlight.hvplot.scatter(color=SECONDARY_COLOR, padding=0.1, legend=False)

    def panel(self):
        return pn.template.MaterialTemplate(
            site="Panel",
            title="Getting Started App",
            sidebar=[pn.Param(self.param.variable),
                     pn.Param(self.param.window),
                     pn.Param(self.param.sigma)],
            main=[self.get_plot]
        ).servable()

# Activate Panel extension
pn.extension(design="material", sizing_mode="stretch_width")

# Create an instance of the app and serve it
app = MyPanelApp()
app.panel()
