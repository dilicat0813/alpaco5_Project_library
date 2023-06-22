import dash_bootstrap_components as dbc

def bot_textbox(text, box="other"):
    style = {
        "width":"fit-content",
        "max-width":"50vw",
        "padding": "10px 15px",
        "border-radius": "25px",
        "font-size":"large",
        "font-family":"sans-serif",
        "margin-bottom":"25px",
        "font-weight":"bold",
        "transform":"translate(0%, 0%)",
        "color":"white"
    }

    color = "royalblue"
    
    return dbc.Card(text, style=style, body=True, color=color)