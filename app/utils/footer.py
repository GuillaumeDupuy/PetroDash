# ------------------------------------------------------------------------------
# Description: This script defines the footer content of the web page.
# ------------------------------------------------------------------------------

# Import libraries
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
import streamlit as st

# Define a function to create an image element with optional styles
def image(src_as_string, **style):
    """
    Build an image element with `src` and optional `style`
    Args:
        src_as_string: image source url
        style: Dictionary of styles
    Returns:
        An HtmlElement object containing the image
    """
    return img(src=src_as_string, style=styles(**style))

# Define a function to create a hyperlink element with optional styles
def link(link, text, **style):
    """
    Build a hyperlink element with `src` and optional `style`
    Args:
        link: Hyperlink
        text: Text to display
        style: Dictionary of styles
    Returns:
        An HtmlElement object containing the hyperlink
    """
    return a(_href=link, _target="_blank", style=styles(**style))(text)

# Define the main layout function that assembles the web page
def layout(*args):
    """
    Build a streamlit web page with a header, footer and variable number of content blocks in between
    Args:
        *args: Variable length argument list of HtmlElement objects
    Returns:
        An HtmlElement object containing the entire web page
    """

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        margin=px(0, 0, 0, 0),
        width=percent(100),
        height="auto",
        color="white",
        text_align="center",
        font_family="Arial, sans-serif",
        opacity=1,
        position="fixed",
        left=0,
        bottom=0,
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2),
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

# Define a function to create the footer content
def footer():
    """
    Build the footer content
    Args:
        None
    Returns:
        An HtmlElement object containing the footer content
    """

    myargs = [
        "Made in ",
        image('https://avatars.githubusercontent.com/u/56391911?v=4',
              width=px(25), height=px(25)),
        " with ❤️ by ",
        link("https://github.com/GuillaumeDupuy/", "@GuillaumeDupuy", color="red"),
        br(),
        "Learn more about this dashboard and the methodology behind its development. The data sources used to create this application are available on ",
        link("data.gouv.fr","data.gouv.fr", color="red"), 
        " and can be explored ",
        link("https://www.data.gouv.fr/fr/datasets/prix-des-carburants-en-france-flux-instantane-v2-amelioree/#/resources)", "here.", color="red"),
        br(),
        " These data sources are provided by the Ministry of Economy, Finance, and Digital Sovereignty. ",
        br(),
        "For more information, please visit the official website. ",
        br(),
        "This visualization was created by GuillaumeDupuy, and its source code is open-source. You can find it on ",
        link("https://github.com/GuillaumeDupuy/PetroDash","GitHub.", color="red")
    ]
    layout(*myargs)