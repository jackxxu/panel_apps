import param
import panel as pn
from datetime import date, timedelta

class DateRangeSelector(param.Parameterized):
    selector = param.Selector(objects=['Option 1', 'Option 2'], default='Option 1')
    date_range = param.DateRange()

    value_dependence = {
        'Option 1':  (date.today() - timedelta(days=7), date.today()),
        'Option 2':  (date.today() - timedelta(days=30), date.today()),
    }

    @param.depends('selector', watch=True, on_init=True)
    def update_date_range(self):
        self.date_range = self.value_dependence[self.selector]

    @param.depends('selector', 'date_range')
    def view(self):
        print('v'*100)
        return pn.pane.Markdown(f"""
        ### Selected Values
        - Selector: {self.selector}
        - Date Range: {self.date_range[0].strftime('%Y-%m-%d')} to {self.date_range[1].strftime('%Y-%m-%d')}
        """)
    
    @param.depends('selector')
    def controls(self):
        print('c'*100)
        date_range_slider = pn.widgets.DateRangeSlider(
            name='Date Range',
            start=self.value_dependence['Option 2'][0],
            end=self.value_dependence['Option 2'][1] + timedelta(days=365),
            value=self.date_range
        )
        date_range_panel = pn.Param(self.param.date_range, widgets={'date_range': date_range_slider})
        return pn.Column(self.param.selector, date_range_panel)


# Create an instance of the class
date_range_selector = DateRangeSelector()

# Create the FastListTemplate
template = pn.template.FastListTemplate(
    title="Date Range Selector Example",
    sidebar=date_range_selector.controls,
    main=date_range_selector.view
)

# Serve the template
template.servable()
