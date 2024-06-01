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

fig = (
    alt.Chart(data)
    .mark_line(point=True)
    .encode(
        x="Day",
        y=alt.Y("Wind Speed (m/s)", scale=alt.Scale(domain=(0, 10))),
        tooltip=["Day", "Wind Speed (m/s)"],
    )
    .properties(width="container", height="container", title="Wind Speed Over the Week")
)

component = pn.panel(fig, sizing_mode="stretch_width", height=400)
print(component)

component.servable()