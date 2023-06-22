import dash_bootstrap_components as dbc

def bot_textbox(text, box="other"):
    style = {
        "max-width": "55%",
        "width": "max-content",
        "padding": "10px 15px",
        "border-radius": "25px",
    }
    box == "self"
    style["margin-left"] = 0
    style["margin-right"] = "auto"
    color = "primary"
    inverse = True
    
    return dbc.Card(text, style=style, body=True, color=color, inverse=inverse)