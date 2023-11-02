# IMPORT LIBRAIRIES
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os
import altair as alt
import pydeck as pdk
import pyproj
from PIL import Image

# GET PWD
cwd = os.getcwd()

# DOWNLOAD DATA IN CACHE
@st.cache_data
def load_data_df():
    """Load dataset in cache"""
    cwd = os.getcwd()
    df_price = pd.read_csv(cwd + '/data/prix-des-carburants-en-france-flux-instantane-v2.csv', sep=';')
    return df_price

st.set_page_config(
    page_title="PetroDash", page_icon="⛽", initial_sidebar_state="collapsed"
)

# LOAD DATAFRAME
df_price = load_data_df()

# PAGE

st.title('Price of fuels in France')

# if st.checkbox("See all dataframe", False):
#     st.dataframe(df_price)

# PRE-PROCESSING

# Un tableau contenant tous les noms de région
name_regions = df_price['region'].unique()
name_regions = name_regions[~pd.isna(name_regions)]
name_regions = sorted(name_regions)

# Un tableau contenant tous les noms de ville

name_villes = df_price['ville'].unique()
name_villes = name_villes[~pd.isna(name_villes)]
name_villes = sorted(name_villes)

# Un tableau contenant tous les noms de carburants

name_carburants = df_price['carburants_disponibles'].str.split(',').explode().unique()
name_carburants = name_carburants[~pd.isna(name_carburants)]

# Dictionnaire contenant le nombre de stations par carburant
summary = [
    {'Carburant': 'E10', 'Number of stations': len(df_price[df_price['e10_prix'].notnull()])},
    {'Carburant': 'Gazole', 'Number of stations': len(df_price[df_price['gazole_prix'].notnull()])},
    {'Carburant': 'SP95', 'Number of stations': len(df_price[df_price['sp95_prix'].notnull()])},
    {'Carburant': 'SP98', 'Number of stations': len(df_price[df_price['sp98_prix'].notnull()])},
    {'Carburant': 'E85', 'Number of stations': len(df_price[df_price['e85_prix'].notnull()])},
    {'Carburant': 'GPLC', 'Number of stations': len(df_price[df_price['gplc_prix'].notnull()])},
]

df_summary = pd.DataFrame(summary)

# GRAPHIC

# Affichage du nombre de stations par carburant

st.title('Number of stations per fuel')

bar_chart = alt.Chart(df_summary).mark_bar().encode(
    x='Carburant:O',
    y='Number of stations:Q',
)

st.altair_chart(bar_chart, use_container_width=True)

# Affichage du prix moyen par carburant

summary_price = []

for carburant in name_carburants:
    summary_price.append({
        'Carburant': carburant,
        'Average price': df_price[carburant.lower() + '_prix'].mean(),
    })

df_summary_price = pd.DataFrame(summary_price)

st.title('Average price per fuel')

bar_chart = alt.Chart(df_summary_price).mark_bar().encode(
    x=alt.X('Carburant:O', title='Carburant'),
    y=alt.Y('Average price:Q', title='Average price'),
)

st.altair_chart(bar_chart, use_container_width=True)

# Affichage du nombre de stations par carburant par région

summary_region = []

for region in name_regions:
    summary_region.append({
        'Region': region,
        'E10': len(df_price[(df_price['e10_prix'].notnull()) & (df_price['region'] == region)]),
        'Gazole': len(df_price[(df_price['gazole_prix'].notnull()) & (df_price['region'] == region)]),
        'SP95': len(df_price[(df_price['sp95_prix'].notnull()) & (df_price['region'] == region)]),
        'SP98': len(df_price[(df_price['sp98_prix'].notnull()) & (df_price['region'] == region)]),
        'E85': len(df_price[(df_price['e85_prix'].notnull()) & (df_price['region'] == region)]),
        'GPLC': len(df_price[(df_price['gplc_prix'].notnull()) & (df_price['region'] == region)]),
    })

df_summary_region = pd.DataFrame(summary_region)

st.title('Number of stations per fuel per region')

bar_chart = alt.Chart(df_summary_region).transform_fold(
    ['E10', 'Gazole', 'SP95', 'SP98', 'E85', 'GPLC']
).mark_bar().encode(
    x=alt.X('Region:O', title='Region'),
    y=alt.Y('value:Q', title='Number stations'),
    color=alt.Color('key:N', title='Carburant'),
)

st.altair_chart(bar_chart, use_container_width=True)

# Affichage du prix moyen par carburant par région

summary_price_region = []

for region in name_regions:
    summary_price_region.append({
        'Region': region,
        'E10': df_price[(df_price['e10_prix'].notnull()) & (df_price['region'] == region)]['e10_prix'].mean(),
        'Gazole': df_price[(df_price['gazole_prix'].notnull()) & (df_price['region'] == region)]['gazole_prix'].mean(),
        'SP95': df_price[(df_price['sp95_prix'].notnull()) & (df_price['region'] == region)]['sp95_prix'].mean(),
        'SP98': df_price[(df_price['sp98_prix'].notnull()) & (df_price['region'] == region)]['sp98_prix'].mean(),
        'E85': df_price[(df_price['e85_prix'].notnull()) & (df_price['region'] == region)]['e85_prix'].mean(),
        'GPLC': df_price[(df_price['gplc_prix'].notnull()) & (df_price['region'] == region)]['gplc_prix'].mean(),
    })

df_summary_price_region = pd.DataFrame(summary_price_region)

st.title('Average price per fuel per region')

bar_chart = alt.Chart(df_summary_price_region).transform_fold(
    ['E10', 'Gazole', 'SP95', 'SP98', 'E85', 'GPLC']
).mark_bar().encode(
    x=alt.X('Region:O', title='Region'),
    y=alt.Y('value:Q', title='Average price'),
    color=alt.Color('key:N', title='Carburant'),
)

st.altair_chart(bar_chart, use_container_width=True)

# SEARCH CITY

if st.checkbox("See the average price for a city",False):
    ville = st.selectbox("Write or choose the city for which you want to see the average price",name_villes)

    url = f"https://api.prix-carburants.2aaz.fr/pdv_liste/?opendata=v2&q={ville}"

    r = requests.get(url, allow_redirects=True)

    # Affichage du prix moyen par carburant de la ville

    summary_price_ville = []

    for carburant in name_carburants:
        summary_price_ville.append({
            'Carburant': carburant,
            'Average price': df_price[(df_price['ville'] == ville) & (df_price[carburant.lower() + '_prix'].notnull())][carburant.lower() + '_prix'].mean(),
        })

    df_summary_price_ville = pd.DataFrame(summary_price_ville)

    st.title(f'Average price per fuel in the city of {ville}')

    bar_chart = alt.Chart(df_summary_price_ville).mark_bar().encode(
        x=alt.X('Carburant:O', title='Carburant'),
        y=alt.Y('Average price:Q', title='Average price'),
    )

    st.altair_chart(bar_chart, use_container_width=True)

# SEARCH REGION

if st.checkbox("See the evolution of price of fuel per region",False):
    region = st.selectbox("Write or choose the region for which you want to see",name_regions)
    type_carburant = st.selectbox("Write or choose the carburant for you want to see",name_carburants)
    date_start = st.date_input("Date de début de recherche", datetime.date(2023, 1, 1))
    current_date = datetime.date.today()
    date_finish = st.date_input("Date de fin de recherche", current_date)

    df_price_ = df_price[(df_price[f'{type_carburant.lower()}_prix'].notnull()) & (df_price['region'] == f'{region}')][[f'{type_carburant.lower()}_maj', f'{type_carburant.lower()}_prix']]
    df_price_[f'{type_carburant.lower()}_maj'] = pd.to_datetime(df_price_[f'{type_carburant.lower()}_maj'])
    df_price_= df_price_.sort_values(by=[f'{type_carburant.lower()}_maj'])
    df_price_  = df_price_[(df_price_[f'{type_carburant.lower()}_maj'] >= f'{date_start}') & (df_price_[f'{type_carburant.lower()}_maj'] <= f'{date_finish}')]
    df_price_[f'{type_carburant.lower()}_maj'] = df_price_[f'{type_carburant.lower()}_maj'].dt.strftime('%B')

    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    y_min = 1.0 
    y_max = 3.0

    y_scale = alt.Scale(domain=[y_min, y_max])

    line_chart = alt.Chart(df_price_).mark_line().encode(
        x=alt.X(f'{type_carburant.lower()}_maj:N', title='Month', sort=months_order),
        y=alt.Y(f'{type_carburant.lower()}_prix:Q', title='Price', scale=y_scale),
    )

    st.title(f'Évolution du prix du {type_carburant} en fonction du temps et de la région {region}')

    st.altair_chart(line_chart, use_container_width=True)

# MAP

df_price['latitude'] /= 100000
df_price['longitude'] /= 100000

columns_to_format = ['gazole_maj', 'sp95_maj', 'sp98_maj', 'e10_maj', 'e85_maj', 'gplc_maj']

for column in columns_to_format:
    df_price[column] = pd.to_datetime(df_price[column]).dt.strftime('%d/%m %H:%M')

df_price = df_price.fillna({
    "gazole_prix": "Not available in station",
    "gazole_maj": "",
    "sp95_prix": "Not available in station",
    "sp95_maj": "",
    "sp98_prix": "Not available in station",
    "sp98_maj": "",
    "e10_prix": "Not available in station",
    "e10_maj": "",
    "e85_prix": "Not available in station",
    "e85_maj": "",
    "gplc_prix": "Not available in station",
    "gplc_maj": "",
})

for column in columns_to_format:
    df_price[column] = df_price[column].astype(str)
    df_price[column] = df_price[column].apply(lambda x: "{:%d/%m at %H:%M}".format(datetime.strptime(x, '%d/%m %H:%M')) if x else '')
    df_price[column] = df_price[column].replace('', 'No Update')

df_brand = pd.read_csv(cwd + '/data/brand.csv')

# Ajoutez la liste brand_list comme colonne "brand" au DataFrame
df_price['brand'] = df_brand['brand']
df_price['brand'] = df_price['brand'].replace('Marque inconnue', 'No Brand')

# dupliquer la colonne "brand" dans une nouvelle colonne "brand_logo"
df_price['brand_logo'] = df_price['brand']

# Remplacez les valeurs de la colonne "brand_logo" par des valeurs sans espace, sans point, sans accent & en minuscule
df_price['brand_logo']  = df_price['brand_logo'].str.replace(' ', '')
df_price['brand_logo']  = df_price['brand_logo'].str.replace('.', '')
df_price['brand_logo']  = df_price['brand_logo'].str.replace('à', 'a')
df_price['brand_logo']  = df_price['brand_logo'].str.replace('é', 'e')
df_price['brand_logo']  = df_price['brand_logo'].str.replace('è', 'e')       
df_price['brand_logo'] = df_price['brand_logo'].str.lower()

# replace in brand_logo column the value 'Nobrand' by 'autre'
df_price['brand_logo'] = df_price['brand_logo'].replace('nobrand', 'autre')
df_price['brand_logo'] = df_price['brand_logo'].replace('totalenergies', 'total')
df_price['brand_logo'] = df_price['brand_logo'].replace('totalenergiesaccess', 'totalaccess')
df_price['brand_logo'] = df_price['brand_logo'].replace('marqueinconnue', 'autre')
df_price['brand_logo'] = df_price['brand_logo'].replace('supermarchesspar', 'spar')
df_price['brand_logo'] = df_price['brand_logo'].replace('supercasino', 'supermarchecasino')
df_price['brand_logo'] = df_price['brand_logo'].replace('intermarchecontact', 'intermarche')

# Fonction pour générer la carte

def generate_map(data):
    view_state = pdk.ViewState(
        latitude=48.8566,
        longitude=2.3522,
        zoom=4,
        pitch=0,
    )

    def custom_tooltip():
        return {
            "html": """
            <div style="display: flex; flex-direction: row;">
                <div style="flex: 1;">
                    <b>Address</b>: {adresse}<br/>
                    <b>City</b>: {cp} {ville}<br/>
                    <b>Brand</b>: {brand}<br/>
                    <b>Image brand</b>: <img src="https://raw.githubusercontent.com/GuillaumeDupuy/PetroDash/main/image/brands/{brand_logo}.png" width="30" height="30"><br/>
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

st.title('Gas Station Map')

# Générez la carte
map_ = generate_map(df_price)

# Affichez la carte dans l'application Streamlit
st.pydeck_chart(map_)
