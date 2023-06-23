import dash_bootstrap_components as dbc
from dash import html

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
    text_with_linebreak = []
    for line in text.split('\n'):
        text_with_linebreak.append(line)
        text_with_linebreak.append(html.Br())
    text_with_linebreak.pop()
        
    return dbc.Card([
        html.P(
            text_with_linebreak,
            className="card-text",
        ),], style=style, body=True, color=color)