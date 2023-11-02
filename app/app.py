# IMPORT LIBRAIRIES
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os
import altair as alt

# IMPORT FUNCTIONS
from utils.footer import footer, link, layout
from utils.map import generate_map

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

# Read brand.txt & get number of stations per brand

with open(cwd + '/data/brand.txt', 'r') as file:
    brand_list = file.read().splitlines()

st.write('Number of stations per brand')

summary_brand = []

for element in brand_list:
    element_dict = eval(element)
    name = element_dict['name']
    nb_stations = element_dict['nb_stations']
    summary_brand.append({
        'Brand': name,
        'Number of stations': nb_stations,
    })

df_summary_brand = pd.DataFrame(summary_brand)

bar_chart = alt.Chart(df_summary_brand).mark_bar().encode(
    x=alt.X('Brand:O', title='Brand'),
    y=alt.Y('Number of stations:Q', title='Number of stations'),
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
    date_start = st.date_input("Date de début de recherche", datetime(2023, 1, 1))
    current_date = datetime.now().date()
    date_finish = st.date_input("Date de fin de recherche", current_date)

    df_price_ = df_price[(df_price[f'{type_carburant.lower()}_prix'].notnull()) & (df_price['region'] == f'{region}')][[f'{type_carburant.lower()}_maj', f'{type_carburant.lower()}_prix']]
    df_price_[f'{type_carburant.lower()}_maj'] = pd.to_datetime(df_price_[f'{type_carburant.lower()}_maj'])
    df_price_= df_price_.sort_values(by=[f'{type_carburant.lower()}_maj'])
    df_price_  = df_price_[(df_price_[f'{type_carburant.lower()}_maj'] >= f'{date_start}') & (df_price_[f'{type_carburant.lower()}_maj'] <= f'{date_finish}')]
    df_price_[f'{type_carburant.lower()}_maj'] = df_price_[f'{type_carburant.lower()}_maj'].dt.strftime('%B')

    # Formatage des mois chiffres en mois lettres

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

# Conversion des coordonnées GPS en décimal

df_price['latitude'] /= 100000
df_price['longitude'] /= 100000

# Formatage des dates et heures de mise a jour de la staation par type de carburants

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

# Ajoutez la liste brand_list comme colonne "brand" au DataFrame

df_brand = pd.read_csv(cwd + '/data/brand.csv')

df_price['brand'] = df_brand['brand']
df_price['brand'] = df_price['brand'].replace('Marque inconnue', 'No Brand')

# dupliquer la colonne "brand" dans une nouvelle colonne "brand_logo"
df_price['brand_logo'] = df_price['brand']

# Remplacez les valeurs de la colonne "brand_logo" par des valeurs sans espace, sans point, sans accent & en minuscule
df_price['brand_logo']  = df_price['brand_logo'].str.replace(' ', '')
df_price['brand_logo'] = df_price['brand_logo'].str.replace('.', '', regex=True)
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

# MAP

st.title('Gas Station Map')

if st.checkbox("Filter",False):

    col1, col2 = st.columns(2)
    
    with col1:
        gazole = st.checkbox("Gazole",False)
        sp98 = st.checkbox("SP98",False)
        sp95 = st.checkbox("SP95",False)
    with col2:
        e10 = st.checkbox("E10",False)
        e85 = st.checkbox("E85",False)
        gplc = st.checkbox("GPLc",False)
    
    if st.checkbox("If you want to filter by City (if not, it will be by Region)",False):

        ville = st.selectbox("Write or choose the city for which you want to see",name_villes)
        df_price_ = df_price[(df_price['ville'] == ville)]

        if gazole:
            df_price_ = df_price_.loc[(df_price_['gazole_prix'] != 'Not available in station') & (df_price['ville'] == ville)]
        if sp98:
            df_price_ = df_price_.loc[(df_price_['sp98_prix'] != 'Not available in station') & (df_price['ville'] == ville)]
        if sp95:
            df_price_ = df_price_.loc[(df_price_['sp95_prix'] != 'Not available in station') & (df_price['ville'] == ville)]
        if e10:
            df_price_ = df_price_.loc[(df_price_['e10_prix'] != 'Not available in station') & (df_price['ville'] == ville)]
        if e85:
            df_price_ = df_price_.loc[(df_price_['e85_prix'] != 'Not available in station') & (df_price['ville'] == ville)]
        if gplc:
            df_price_ = df_price_.loc[(df_price_['gplc_prix'] != 'Not available in station') & (df_price['ville'] == ville)]

    else:
        region = st.selectbox("Write or choose the region for which you want to see",name_regions)
        df_price_ = df_price[(df_price['region'] == region)]

        if gazole:
            df_price_ = df_price_.loc[(df_price_['gazole_prix'] != 'Not available in station') & (df_price['region'] == region)]
        if sp98:
            df_price_ = df_price_.loc[(df_price_['sp98_prix'] != 'Not available in station') & (df_price['region'] == region)]
        if sp95:
            df_price_ = df_price_.loc[(df_price_['sp95_prix'] != 'Not available in station') & (df_price['region'] == region)]
        if e10:
            df_price_ = df_price_.loc[(df_price_['e10_prix'] != 'Not available in station') & (df_price['region'] == region)]
        if e85:
            df_price_ = df_price_.loc[(df_price_['e85_prix'] != 'Not available in station') & (df_price['region'] == region)]
        if gplc:
            df_price_ = df_price_.loc[(df_price_['gplc_prix'] != 'Not available in station') & (df_price['region'] == region)]
    
else:
    df_price_ = df_price

# Générez la carte
map_ = generate_map(df_price_)

# Affichez la carte dans l'application Streamlit
st.pydeck_chart(map_)

# FOOTER

footer()