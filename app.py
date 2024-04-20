import panel as pn

# Ensure that the Panel extension is loaded for Jupyter environments
pn.extension()

def create_app():

    print('1'*100)
    # Define a reactive function that updates based on the slider's value
    def slider_display(value):
        return f'The current slider value is: {value}'

    # Create a slider widget
    slider = pn.widgets.IntSlider(name='Adjust Value', start=0, end=100, step=1, value=50)

    # Connect the slider to the display function using pn.bind
    display = pn.bind(slider_display, slider.value)

    # Create a Panel layout that includes the slider and the display label
    layout = pn.Column(slider, display)

    return layout

# # Serve the function directly without calling it here; Panel handles each session
# app = create_app

# # Make the app servable if running in an environment that requires it
# app().servable()


# Serve the function directly without calling it here; Panel handles each session
create_app().servable()
