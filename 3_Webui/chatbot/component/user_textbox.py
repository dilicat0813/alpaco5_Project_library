import dash_bootstrap_components as dbc

def user_textbox(text, box="other"):
    style = {
        "width": "max-content",
        "padding": "10px 15px",
        "border-radius": "25px",
        "font-size":"large",
        "font-family":"sans-serif",
        "margin-bottom":"25px",
        "font-weight":"bold",
        "transform":"translate(0%, 18%)"
    }

    color = "yellow"
    
    return dbc.Card(text, style=style, body=True, color=color)