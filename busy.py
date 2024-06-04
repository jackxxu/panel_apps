import time
import panel as pn
pn.extension() # for notebook

def processing(event):
    # Some longer running task
    time.sleep(2)

button = pn.widgets.Button(name='Click me!')
button.on_click(processing)

pn.Row(
    button, 
    pn.indicators.LoadingSpinner(value=True, color='primary', size=50, visible=pn.state.param.busy),
    pn.pane.Markdown('busy', visible=pn.state.param.busy)
).servable()