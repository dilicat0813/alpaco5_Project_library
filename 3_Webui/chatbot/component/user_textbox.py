import dash_bootstrap_components as dbc

def user_textbox(text, box="other"):
    style = {
        "max-width": "55%",
        "width": "max-content",
        "padding": "10px 15px",
        "border-radius": "25px",
    }
    color = "light"
    
    return dbc.Card(text, style=style, body=True, color=color)