import panel as pn
pn.serve({
    'markdown': '# This is a Panel app',
    'json': pn.pane.JSON({'abc': 123})
})