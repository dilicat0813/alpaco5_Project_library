import dash_bootstrap_components as dbc

def bot_textbox(text, box="other"):
    style = {
        "max-width": "55%",
        "width": "max-content",
        "padding": "10px 15px",
        "border-radius": "25px",
    }
    color = "primary"
    
    return dbc.Card(text, style=style, body=True, color=color)