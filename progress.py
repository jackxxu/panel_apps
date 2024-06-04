import panel as pn
import time     

run = pn.widgets.Button(name="Press to run calculation", align='center')

def runner(run):
    if not run:
        yield "Calculation did not run yet"
        return
    for i in range(101):
        time.sleep(0.01) # Some calculation
        yield pn.Column(
            f'Running ({i}/100%)', pn.indicators.Progress(value=i)
        )
    yield "Success ✅︎"

pn.Row(run, pn.bind(runner, run)).servable()
