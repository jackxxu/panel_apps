# %%
import panel as pn
import pandas as pd
import altair as alt

pn.extension("plotly", "vega")


# data = pd.DataFrame([
#     ('Monday', 7), ('Tuesday', 4), ('Wednesday', 9), ('Thursday', 4),
#     ('Friday', 4), ('Saturday', 5), ('Sunday', 4)], columns=['Day', 'Wind Speed (m/s)']
# )
# component = pn.panel(data)
# print(component)
# component.servable()

data = pd.DataFrame([
    ('Monday', 7), ('Tuesday', 4), ('Wednesday', 9), ('Thursday', 4),
    ('Friday', 4), ('Saturday', 5), ('Sunday', 4)], columns=['Day', 'Wind Speed (m/s)']
)


# create an integer slider
slider = pn.widgets.IntSlider(name="Rows", start=1, end=7, step=1, value=7)


def data_plot(rows=7):
    print('1'*100)
    fig = (
        alt.Chart(data.head(rows))
        .mark_line(point=True)
        .encode(
            x="Day",
            y=alt.Y("Wind Speed (m/s)", scale=alt.Scale(domain=(0, 10))),
            tooltip=["Day", "Wind Speed (m/s)"],
        )
        .properties(width="container", height="container", title="Wind Speed Over the Week")
    )

    return pn.panel(fig, sizing_mode="stretch_width", height=400)


pn.Column(
    slider,
    pn.bind(data_plot, slider),
    pn.panel(data)
).servable()
