import streamlit as st
import pandas as pd
import requests
import datetime
import os
import altair as alt

cwd = os.getcwd()

@st.cache_data
def load_data_df():
    """Load dataset in cache"""
    cwd = os.getcwd()
    df_price = pd.read_csv(cwd + '/data/prix-des-carburants-en-france-flux-instantane-v2_2023_10_27_12_33.csv', sep=';')
    return df_price

st.set_page_config(
    page_title="Fuels",
    layout="wide",
    initial_sidebar_state='collapsed',
    page_icon="⛽"
)

df_price = load_data_df()

# PAGE

st.title('Price of fuels in France')

# if st.checkbox("See all dataframe", False):
#     st.dataframe(df_price)

# Un tableau contenant tous les noms de région
name_regions = df_price['region'].unique()
name_regions = name_regions[~pd.isna(name_regions)]
name_regions = sorted(name_regions)

# Un tableau contenant tous les noms de ville

name_villes = df_price['ville'].unique()
name_villes = name_villes[~pd.isna(name_villes)]
name_villes = sorted(name_villes)

# Un tableau contenant tous les noms de carburants

name_carburants = df_price['carburants_disponibles'].str.split(';').explode().unique()
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

# Affichage du nombre de stations par carburant

st.title('Number of stations per fuel')

bar_chart = alt.Chart(df_summary).mark_bar().encode(
    x='Carburant:O',
    y='Number of stations:Q',
)

st.altair_chart(bar_chart, use_container_width=True)
# st.bar_chart(df_summary.set_index('Carburant'))

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
