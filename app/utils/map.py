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
                    <img src="data:image/jpeg;base64,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" width="70" height="70"><br/>
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