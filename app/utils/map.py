# ------------------------------------------------------------------------------
# Description: This file contains the function to generate the map
# ------------------------------------------------------------------------------

# Import libraries
import pydeck as pdk

# Function to generate the map
def generate_map(data):
    """
    Generate the map with the data
    Args:
        data (dataframe): Dataframe with the data to display on the map
    Returns:
        map_ (map): Map with the data
    """
    view_state = pdk.ViewState(
        latitude=48.8566,
        longitude=2.3522,
        zoom=4,
        pitch=0,
    )

    def custom_tooltip():
        """
        Generate the tooltip
        Args:
            None
            Returns:
                tooltip (html): Tooltip
        """
        return {
            "html": """
            <div style="display: flex; flex-direction: row;">
                <div style="flex: 1;">
                    <b>Address</b>: {adresse}<br/>
                    <b>City</b>: {cp} {ville}<br/>
                    <b>Brand</b>: {brand}<br/>
                    <img src="./image/brands/{brand_logo}.png" width="70" height="70"><br/>
                </div>
                <div style="flex: 1;">
                    <b> Image Gazole</b>: <img src="https://raw.githubusercontent.com/GuillaumeDupuy/PetroDash/main/image/fuels/b7.png" width="30" height="30"><br/>
                    <b>Price Gazole</b>: {gazole_prix} €<br/>
                    <b>Update on</b>: {gazole_maj}<br/>
                    <b> Image SP98</b>: <img src="https://raw.githubusercontent.com/GuillaumeDupuy/PetroDash/main/image/fuels/e5.png" width="30" height="30"><br/>
                    <b>Price SP98</b>: {sp98_prix} €<br/>
                    <b>Update on</b>: {sp98_maj}<br/>
                    <b> Image E85</b>: <img src="https://raw.githubusercontent.com/GuillaumeDupuy/PetroDash/main/image/fuels/e85.png" width="30" height="30"><br/>
                    <b>Price E85</b>: {e85_prix} €<br/>
                    <b>Update on</b>: {e85_maj}<br/>
                </div>
                <div style="flex: 1;">
                    <b> Image SP95</b>: <img src="https://raw.githubusercontent.com/GuillaumeDupuy/PetroDash/main/image/fuels/e10.png" width="30" height="30"><br/>
                    <b>Price SP95</b>: {sp95_prix} €<br/>
                    <b>Update on</b>: {sp95_maj}<br/> 
                    <b> Image E10</b>: <img src="https://raw.githubusercontent.com/GuillaumeDupuy/PetroDash/main/image/fuels/e10.png" width="30" height="30"><br/>
                    <b>Price E10</b>: {e10_prix} €<br/>
                    <b>Update on</b>: {e10_maj}<br/>
                    <b> Image GPLc</b>: <img src="https://raw.githubusercontent.com/GuillaumeDupuy/PetroDash/main/image/fuels/lpg.png" width="30" height="30"><br/>
                    <b>Price GPLc</b>: {gplc_prix} €<br/>
                    <b>Update on</b>: {gplc_maj}<br/>
                </div>
            </div>
            """,
            "style": {
                "backgroundColor": "white",
                "color": "black"
            }
        }
 

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position=["longitude", "latitude"],
        get_radius=2500,
        get_color=[255, 0, 0],
        pickable=True,
        auto_highlight=True,
    )

    map_ = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[layer],
        initial_view_state=view_state,
        tooltip=custom_tooltip()
    )

    return map_