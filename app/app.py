# ---------------------------------------------------------------------------------------------------------------
# Import libraries
# ---------------------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import numpy as np
import os
import altair as alt
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

# ---------------------------------------------------------------------------------------------------------------
# Import modules
# ---------------------------------------------------------------------------------------------------------------
from utils.footer import footer
from utils.map import generate_map

# ---------------------------------------------------------------------------------------------------------------
# Get the current working directory
# ---------------------------------------------------------------------------------------------------------------
cwd = os.getcwd()

# ---------------------------------------------------------------------------------------------------------------
# Download data in cache
# ---------------------------------------------------------------------------------------------------------------
@st.cache_data
def load_data_df():
    """
    Load dataset in cache
    Args:
        None
    Returns:
        df_price (dataframe): Dataframe with the data
    """
    cwd = os.getcwd()
    df_price = pd.read_csv(cwd + '/data/prix-des-carburants-en-france-flux-instantane-v2.csv', sep=';')
    return df_price

# ---------------------------------------------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="PetroDash", page_icon="⛽", initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------------------------------------------
df_price = load_data_df()

# ---------------------------------------------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------------------------------------------

st.sidebar.image(cwd + '/image/station-service.jpg', width=100)
st.sidebar.title('Navigation')

# Pages
pages = [
    'Home',
    'Number of stations per fuel',
    'Average price per fuel',
    'Number of stations per fuel per region',
    'Average price per fuel per region',
    'Number of stations per brand',
    'Search city',
    'Search region',
    'Gas Station Map',
    'Machine Learning',
    'Reinforcement learning',
]

# Page selection
page = st.sidebar.selectbox('Select a page', pages)

# ---------------------------------------------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------------------------------------------

st.header('PetroDash')

st.title('Price of fuels in France')

if page == 'Home':
    st.write('<br><br>', unsafe_allow_html=True)
    st.write('This application allows you to visualize the price of fuels in France.')
    st.write('First, i have analyzed the data in the entire dataset. To see, the number of stations per fuel, the average price per fuel, the number of stations per fuel per region and the average price per fuel per region.')
    st.write('Then, you can filter the data by city or by region. You can also filter by fuel. Finally, you can see the evolution of the price of a fuel over time in a city or a region.')
    st.write('I have also added a map that allows you to see the location of the stations in France. You can filter the data by city or by region. You can also filter by fuel.')
    st.write('<strong>Warning:</strong> The data is updated every 15 minutes. The data is not updated in real time.', unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------------------------------
# Pre-processing
# ---------------------------------------------------------------------------------------------------------------

# Array containing all the names of the regions
name_regions = df_price['region'].unique()
name_regions = name_regions[~pd.isna(name_regions)]
name_regions = sorted(name_regions)

# Array containing all the names of the cities
name_villes = df_price['ville'].unique()
name_villes = name_villes[~pd.isna(name_villes)]
name_villes = sorted(name_villes)

# Array containing all the names of the fuels
name_carburants = df_price['carburants_disponibles'].str.split(',').explode().unique()
name_carburants = name_carburants[~pd.isna(name_carburants)]

# Dictionary containing the number of stations per fuel
summary = [
    {'Carburant': 'E10', 'Number of stations': len(df_price[df_price['e10_prix'].notnull()])},
    {'Carburant': 'Gazole', 'Number of stations': len(df_price[df_price['gazole_prix'].notnull()])},
    {'Carburant': 'SP95', 'Number of stations': len(df_price[df_price['sp95_prix'].notnull()])},
    {'Carburant': 'SP98', 'Number of stations': len(df_price[df_price['sp98_prix'].notnull()])},
    {'Carburant': 'E85', 'Number of stations': len(df_price[df_price['e85_prix'].notnull()])},
    {'Carburant': 'GPLC', 'Number of stations': len(df_price[df_price['gplc_prix'].notnull()])},
]

df_summary = pd.DataFrame(summary)

# ---------------------------------------------------------------------------------------------------------------
# GRAPHICS

if page == 'Number of stations per fuel':
    # ---------------------------------------------------------------------------------------------------------------
    # Display the number of stations per fuel
    # ---------------------------------------------------------------------------------------------------------------

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Number of stations per fuel')

    bar_chart = alt.Chart(df_summary).mark_bar().encode(
        x='Carburant:O',
        y='Number of stations:Q',
    )

    st.altair_chart(bar_chart, use_container_width=True)

    st.write("The bar chart above displays the number of fuel stations for each type of fuel in France. It offers a visual representation of the availability of different fuel options across the country. This information can be valuable for understanding the distribution of fuel options and their accessibility to consumers in different regions.")

if page == 'Average price per fuel':
    # ---------------------------------------------------------------------------------------------------------------
    # Display the average price per fuel
    # ---------------------------------------------------------------------------------------------------------------

    summary_price = []

    for carburant in name_carburants:
        summary_price.append({
            'Carburant': carburant,
            'Average price': df_price[carburant.lower() + '_prix'].mean(),
        })

    df_summary_price = pd.DataFrame(summary_price)

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Average price per fuel')

    bar_chart = alt.Chart(df_summary_price).mark_bar().encode(
        x=alt.X('Carburant:O', title='Carburant'),
        y=alt.Y('Average price:Q', title='Average price'),
    )

    st.altair_chart(bar_chart, use_container_width=True)

    st.write("The bar chart above illustrates the average prices for different types of fuels in France. It provides valuable insights into the cost of different fuels, helping consumers make informed decisions about their fuel choices. This data can also be useful for tracking price trends and comparing fuel prices between regions and cities.")

if page == 'Number of stations per fuel per region':
    # ---------------------------------------------------------------------------------------------------------------
    # Display the number of stations per fuel per region
    # ---------------------------------------------------------------------------------------------------------------

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

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Number of stations per fuel per region')

    bar_chart = alt.Chart(df_summary_region).transform_fold(
        ['E10', 'Gazole', 'SP95', 'SP98', 'E85', 'GPLC']
    ).mark_bar().encode(
        x=alt.X('Region:O', title='Region'),
        y=alt.Y('value:Q', title='Number stations'),
        color=alt.Color('key:N', title='Carburant'),
    )

    st.altair_chart(bar_chart, use_container_width=True)

    st.write("The bar chart above presents the number of fuel stations for each type of fuel in various regions of France. It allows you to compare the availability of different fuel options across different regions. This information can be helpful for residents or travelers looking for specific fuel types in particular areas. The chart provides a clear visual representation of the regional distribution of fuel stations for each fuel type.")

if page == 'Average price per fuel per region':
    # ---------------------------------------------------------------------------------------------------------------
    # Display the average price per fuel per region
    # ---------------------------------------------------------------------------------------------------------------

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

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Average price per fuel per region')

    bar_chart = alt.Chart(df_summary_price_region).transform_fold(
        ['E10', 'Gazole', 'SP95', 'SP98', 'E85', 'GPLC']
    ).mark_bar().encode(
        x=alt.X('Region:O', title='Region'),
        y=alt.Y('value:Q', title='Average price'),
        color=alt.Color('key:N', title='Carburant'),
    )

    st.altair_chart(bar_chart, use_container_width=True)

    st.write("The bar chart above provides insights into the average prices of different fuels in different regions of France. It allows you to compare the cost of various fuels within specific regions. This information can be valuable for budget-conscious consumers or businesses looking to optimize their fuel expenses. By visualizing the regional price differences, users can make more informed decisions about where to refuel based on their fuel preferences and budget.")

if page == 'Number of stations per brand':
    # ---------------------------------------------------------------------------------------------------------------
    # Display the number of stations per brand
    # ---------------------------------------------------------------------------------------------------------------

    # Read brand.txt & get number of stations per brand
    with open(cwd + '/data/brand.txt', 'r', encoding='ISO-8859-1') as file:
        brand_list = file.read().splitlines()

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Number of stations per brand')

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

    st.write("The bar chart above presents the number of fuel stations for different brands in France. It provides insights into the distribution of fuel stations among various brands, helping consumers identify popular and widely available brands. This information can be valuable for consumers looking for fuel stations associated with specific brands or for businesses considering brand partnerships for their fleet's fueling needs.")

if page == 'Search city':
    # ---------------------------------------------------------------------------------------------------------------
    # Search city
    # Display graphics on a city by a call API
    # ---------------------------------------------------------------------------------------------------------------

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Search city')

    st.write("Now, you have the ability to narrow down your analysis to a specific city using the parameters of your choice. You can explore the average fuel prices in a selected city and track the evolution of fuel prices over time within that city. To begin, then choose a city from the dropdown menu. This will display the average fuel prices for different fuel types in your selected city. Additionally, you can further refine your analysis by specifying a fuel type and a date range to examine how the fuel prices have changed over time. The line chart will show you the price trend for your chosen fuel type in the selected city.")

    st.write('<br>', unsafe_allow_html=True)

    ville = st.selectbox("Write or choose the city for which you want to see the average price",name_villes)

    url = f"https://api.prix-carburants.2aaz.fr/pdv_liste/?opendata=v2&q={ville}"

    r = requests.get(url, allow_redirects=True)

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

    # ---------------------------------------------------------------------------------------------------------------
    # Display the evolution of the price of fuel per city
    # ---------------------------------------------------------------------------------------------------------------

    type_carburant = st.selectbox("Write or choose the carburant for you want to see",name_carburants)
    date_start = st.date_input("Date de début de recherche", datetime(2023, 1, 1))
    current_date = datetime.now().date()
    date_finish = st.date_input("Date de fin de recherche", current_date)

    df_price_ = df_price[(df_price[f'{type_carburant.lower()}_prix'].notnull()) & (df_price['ville'] == f'{ville}')][[f'{type_carburant.lower()}_maj', f'{type_carburant.lower()}_prix']]
    df_price_[f'{type_carburant.lower()}_maj'] = pd.to_datetime(df_price_[f'{type_carburant.lower()}_maj'])
    df_price_= df_price_.sort_values(by=[f'{type_carburant.lower()}_maj'])
    df_price_  = df_price_[(df_price_[f'{type_carburant.lower()}_maj'] >= f'{date_start}') & (df_price_[f'{type_carburant.lower()}_maj'] <= f'{date_finish}')]
    df_price_[f'{type_carburant.lower()}_maj'] = df_price_[f'{type_carburant.lower()}_maj'].dt.strftime('%B')

    # Formatting of the months in letters
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    y_min = 1.0 
    y_max = 3.0

    y_scale = alt.Scale(domain=[y_min, y_max])

    line_chart = alt.Chart(df_price_).mark_line().encode(
        x=alt.X(f'{type_carburant.lower()}_maj:N', title='Month', sort=months_order),
        y=alt.Y(f'{type_carburant.lower()}_prix:Q', title='Price', scale=y_scale),
    )

    st.title(f'Evolution of the price of {type_carburant} according to time on {ville}')

    st.altair_chart(line_chart, use_container_width=True)

if page == 'Search region':
    # ---------------------------------------------------------------------------------------------------------------
    # Search region
    # Display graphics on a region by filtering the dataframe
    # ---------------------------------------------------------------------------------------------------------------

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Search region')

    st.write("In this section, you can focus your analysis on a specific region by filtering the data accordingly. First, select a region from the dropdown menu, and then choose a fuel type that you want to investigate. You can further refine your analysis by specifying a date range to observe how fuel prices have evolved over time in the selected region. The line chart will visualize the price trend for the chosen fuel type in the chosen region, allowing you to gain insights into the price fluctuations in that area.")

    st.write('<br>', unsafe_allow_html=True)

    region = st.selectbox("Write or choose the region for which you want to see",name_regions, key="region_selectbox")
    type_carburant = st.selectbox("Write or choose the carburant for you want to see",name_carburants, key="carburant_selectbox")
    date_start = st.date_input("Date de début de recherche", datetime(2023, 1, 1), key="date_start_selectbox")
    current_date = datetime.now().date()
    date_finish = st.date_input("Date de fin de recherche", current_date, key="date_finish_selectbox")

    df_price_ = df_price[(df_price[f'{type_carburant.lower()}_prix'].notnull()) & (df_price['region'] == f'{region}')][[f'{type_carburant.lower()}_maj', f'{type_carburant.lower()}_prix']]
    df_price_[f'{type_carburant.lower()}_maj'] = pd.to_datetime(df_price_[f'{type_carburant.lower()}_maj'])
    df_price_= df_price_.sort_values(by=[f'{type_carburant.lower()}_maj'])
    df_price_  = df_price_[(df_price_[f'{type_carburant.lower()}_maj'] >= f'{date_start}') & (df_price_[f'{type_carburant.lower()}_maj'] <= f'{date_finish}')]
    df_price_[f'{type_carburant.lower()}_maj'] = df_price_[f'{type_carburant.lower()}_maj'].dt.strftime('%B')

    # Formatting of the months in letters
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    y_min = 1.0 
    y_max = 3.0

    y_scale = alt.Scale(domain=[y_min, y_max])

    line_chart = alt.Chart(df_price_).mark_line().encode(
        x=alt.X(f'{type_carburant.lower()}_maj:N', title='Month', sort=months_order),
        y=alt.Y(f'{type_carburant.lower()}_prix:Q', title='Price', scale=y_scale),
    )

    st.title(f'Evolution of the price of {type_carburant} according to time on {region}')

    st.altair_chart(line_chart, use_container_width=True)

# ---------------------------------------------------------------------------------------------------------------
# Pre-processing for the map
# ---------------------------------------------------------------------------------------------------------------

# Convert the coordinates of the stations from degrees to decimal
df_price['latitude'] /= 100000
df_price['longitude'] /= 100000


# Formatting of the update dates and times of the station by type of fuel
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

# Add the column "brand" to the dataframe "df_price"
df_brand = pd.read_csv(cwd + '/data/brand.csv')
df_price['brand'] = df_brand['brand']
df_price['brand'] = df_price['brand'].replace('Marque inconnue', 'No Brand')

# Duplicate the values of the "brand" column in the "brand_logo" column
df_price['brand_logo'] = df_price['brand']

# Replace the values of the "brand_logo" column with values without space, without point, without accent & in lowercase
df_price['brand_logo']  = df_price['brand_logo'].str.replace(' ', '')
df_price['brand_logo']  = df_price['brand_logo'].str.replace('à', 'a')
df_price['brand_logo']  = df_price['brand_logo'].str.replace('é', 'e')
df_price['brand_logo']  = df_price['brand_logo'].str.replace('è', 'e')       
df_price['brand_logo'] = df_price['brand_logo'].str.lower()

# Replace in brand_logo column the value 'Nobrand' by 'autre'
df_price['brand_logo'] = df_price['brand_logo'].replace('nobrand', 'autre')
df_price['brand_logo'] = df_price['brand_logo'].replace('totalenergies', 'total')
df_price['brand_logo'] = df_price['brand_logo'].replace('totalenergiesaccess', 'totalaccess')
df_price['brand_logo'] = df_price['brand_logo'].replace('marqueinconnue', 'autre')
df_price['brand_logo'] = df_price['brand_logo'].replace('supermarchesspar', 'spar')
df_price['brand_logo'] = df_price['brand_logo'].replace('supercasino', 'supermarchecasino')
df_price['brand_logo'] = df_price['brand_logo'].replace('intermarchecontact', 'intermarche')
df_price['brand_logo'] = df_price['brand_logo'].replace('e.leclerc', 'eleclerc')

df_price['Autoroute'] = df_price['pop'].apply(lambda x: 'Yes' if x == 'A' else 'No')

if page == 'Gas Station Map':
    # ---------------------------------------------------------------------------------------------------------------
    # Map
    # ---------------------------------------------------------------------------------------------------------------

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Gas Station Map')

    st.write("In the 'Gas Station Map' section, you can visualize the location of fuel stations across France on a map. You have the option to filter the stations based on your preferences. You can filter by fuel type(s), and choose whether you want to filter by city or region. This interactive map allows you to explore the geographic distribution of fuel stations and their availability based on the selected filters. You can focus on specific areas and discover the locations that match your fuel preferences.")

    st.write('<br>', unsafe_allow_html=True)

    # Create a checkbox to filter the map

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

            ville = st.selectbox("Write or choose the city for which you want to see",name_villes, key="ville_map_selectbox")
            df_price_ = df_price[(df_price['ville'] == ville)]

            if gazole:
                df_price_ = df_price_.loc[(df_price_['gazole_prix'] != 'Not available in station') & (df_price_['ville'] == ville)]
            if sp98:
                df_price_ = df_price_.loc[(df_price_['sp98_prix'] != 'Not available in station') & (df_price_['ville'] == ville)]
            if sp95:
                df_price_ = df_price_.loc[(df_price_['sp95_prix'] != 'Not available in station') & (df_price_['ville'] == ville)]
            if e10:
                df_price_ = df_price_.loc[(df_price_['e10_prix'] != 'Not available in station') & (df_price_['ville'] == ville)]
            if e85:
                df_price_ = df_price_.loc[(df_price_['e85_prix'] != 'Not available in station') & (df_price_['ville'] == ville)]
            if gplc:
                df_price_ = df_price_.loc[(df_price_['gplc_prix'] != 'Not available in station') & (df_price_['ville'] == ville)]

        else:
            region = st.selectbox("Write or choose the region for which you want to see",name_regions, key="region_map_selectbox")
            df_price_ = df_price[(df_price['region'] == region)]

            if gazole:
                df_price_ = df_price_.loc[(df_price_['gazole_prix'] != 'Not available in station') & (df_price_['region'] == region)]
            if sp98:
                df_price_ = df_price_.loc[(df_price_['sp98_prix'] != 'Not available in station') & (df_price_['region'] == region)]
            if sp95:
                df_price_ = df_price_.loc[(df_price_['sp95_prix'] != 'Not available in station') & (df_price_['region'] == region)]
            if e10:
                df_price_ = df_price_.loc[(df_price_['e10_prix'] != 'Not available in station') & (df_price_['region'] == region)]
            if e85:
                df_price_ = df_price_.loc[(df_price_['e85_prix'] != 'Not available in station') & (df_price_['region'] == region)]
            if gplc:
                df_price_ = df_price_.loc[(df_price_['gplc_prix'] != 'Not available in station') & (df_price_['region'] == region)]  
    else:
        df_price_ = df_price

    # Generate the map
    map_ = generate_map(df_price_)

    # Display the map
    st.pydeck_chart(map_)

# ---------------------------------------------------------------------------------------------------------------
# Machine Learning
# ---------------------------------------------------------------------------------------------------------------

if page == 'Machine Learning':

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Machine Learning')

    st.markdown('''
    In the 'Predict the price of fuel' section, we are using machine learning techniques to predict the price of a specific type of fuel in a chosen city in France. Here's how it works:

    1. **Select Your Preferences**: You can choose the type of fuel (e.g., diesel, e10, sp98) and the city for which you want to predict the fuel price. 
    2. **Data Preparation**: We extract relevant data, including the timestamp, latitude, longitude, and the price of the selected fuel type. We remove any missing values from the dataset.
    3. **Training the Model**: We split the data into training and test sets. Then, we create a machine learning pipeline that standardizes the data and uses linear regression to build a predictive model.
    4. **Model Evaluation**: We evaluate the model's performance by calculating the Mean Square Error (MSE) on the test set, which provides an indication of how well the model predicts fuel prices.
    5. **Making Predictions**: We use the trained model to make predictions for the selected city's coordinates and the current timestamp. This allows us to estimate the fuel price for the chosen location and type.
    6. **Visualization**: We create a scatter plot to compare actual prices against predicted prices, providing a visual representation of the model's accuracy.
                
    In the 'Clustering of gas stations' section, we use clustering techniques to group gas stations based on their geographical location and fuel prices. Here's a summary of this section:
    1. **Data Selection**: We use the latitude, longitude, and prices of different fuel types for the clustering task.
    2. **Data Preprocessing**: Any missing values are replaced with zeros, and the data is standardized using the StandardScaler.
    3. **K-Means Clustering**: We apply K-Means clustering to group gas stations into clusters. You can choose the number of clusters to create.
    4. **Cluster Visualization**: We create a scatter plot on a map, with each cluster represented by a different color. You can see the distribution of gas stations in France and how they are grouped based on their attributes.
                
    These sections allow you to explore fuel price predictions and the clustering of gas stations in France, providing valuable insights into the fuel market across different regions.''')

    st.write('<br>', unsafe_allow_html=True)

    data = pd.read_csv(cwd + '/data/prix-des-carburants-en-france-flux-instantane-v2.csv', sep=';',parse_dates=['gazole_maj', 'sp95_maj', 'sp98_maj', 'e10_maj', 'e85_maj', 'gplc_maj'])

    # ---------------------------------------------------------------------------------------------------------------
    # Linear regression
    # ---------------------------------------------------------------------------------------------------------------

    st.title('Predict the price of fuel')

    type_carburant = st.selectbox("Write or choose the carburant for you want to see",name_carburants, key="carburant_selectbox")

    ville = st.selectbox("Write or choose the city for which you want to see the average price",name_villes)

    # Select the data for the machine learning
    data_fuels = data[[f'{type_carburant.lower()}_maj', 'latitude', 'longitude', f'{type_carburant.lower()}_prix']].copy()

    # Delete the rows with missing values
    data_fuels.dropna(inplace=True)

    # Convert the date to a timestamp
    data_fuels.loc[:, f'{type_carburant.lower()}_maj'] = data_fuels[f'{type_carburant.lower()}_maj'].apply(lambda x: x.timestamp())


    # Split the data into training and test sets
    X = data_fuels[[f'{type_carburant.lower()}_maj', 'latitude', 'longitude']]
    y = data_fuels[f'{type_carburant.lower()}_prix']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Standardize the data
        ('regressor', LinearRegression())  # Fit a linear regression model
    ])

    # Fit the pipeline to the training data
    pipeline.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = pipeline.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    st.write(f'{type_carburant} mean square error : {mse}')

    # Recover the city coordinates
    latitude = data[data['ville'] == ville]['latitude'].iloc[0]
    longitude = data[data['ville'] == ville]['longitude'].iloc[0]

    # Make predictions on new data
    nouvelles_donnees = pd.DataFrame({
        f'{type_carburant.lower()}_maj': [datetime.now().timestamp()],
        'latitude': [latitude],
        'longitude': [longitude]
    })

    prix_predits = pipeline.predict(nouvelles_donnees)
    # take prix_predits to convert array into float
    prix_predits = prix_predits[0]
    # round the price
    prix_predits = round(prix_predits, 3)
    st.write(f'Predicted {type_carburant} prices in {ville}: {prix_predits}')

    # Plot the predictions
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred)
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')
    st.pyplot(fig)

    # ---------------------------------------------------------------------------------------------------------------
    # Clustering
    # ---------------------------------------------------------------------------------------------------------------

    st.title('Clustering of gas stations')

    # Select the data for the machine learning
    selected_features = data[["latitude", "longitude", "gazole_prix", "e10_prix", "sp98_prix", "sp95_prix", "e85_prix", "gplc_prix"]].copy()

    # Replace missing values with 0
    selected_features.fillna(0, inplace=True)

    # Normalize the data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(selected_features)

    # Apply K-Means clustering to group gas stations
    k = 6 # Number of clusters
    kmeans = KMeans(n_clusters=k, random_state=0)
    data["cluster"] = kmeans.fit_predict(scaled_features)

    # Create a scatter plot for each cluster
    fig, ax = plt.subplots()
    colors = ['b', 'g', 'r', 'c', 'm', 'y']  # Define colors for clusters

    col1, col2 = st.columns(2)

    # Display the number of stations in each cluster
    for cluster_id in range(k):
        cluster_data = data[data["cluster"] == cluster_id]
        with col1:
            if cluster_id < 3:
                st.write(f"Cluster {cluster_id}: {len(cluster_data)} stations-service")
        with col2:
            if cluster_id > 3:
                st.write(f"Cluster {cluster_id}: {len(cluster_data)} stations-service")
        ax.scatter(cluster_data["longitude"], cluster_data["latitude"], c=colors[cluster_id], label=f"Cluster {cluster_id}")

    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.legend()

    # Display the scatter plot in the Streamlit app
    st.pyplot(fig)

# ---------------------------------------------------------------------------------------------------------------
# Reinforcement learning
# ---------------------------------------------------------------------------------------------------------------

if page == 'Reinforcement learning':

    st.write('<br><br>', unsafe_allow_html=True)

    st.title('Reinforcement learning')

    st.markdown('''
    Reinforcement Learning for Fuel Price Optimization

    In this section, we utilize the epsilon-greedy algorithm to optimize fuel prices effectively.

    The epsilon-greedy algorithm explores and exploits different fuel pricing strategies. Here's a brief overview:

    - We use the epsilon-greedy algorithm with incremental updates.
    - The algorithm dynamically adjusts its strategy to find the best fuel price.
    - We analyze the algorithm's performance with varying epsilon values (0.1, 0.5, and 1).
    ''')

    st.write('<br>', unsafe_allow_html=True)

    data = pd.read_csv(cwd + '/data/prix-des-carburants-en-france-flux-instantane-v2.csv', sep=';')

    # ---------------------------------------------------------------------------------------------------------------
    # Epsilon-greedy algorithm
    # ---------------------------------------------------------------------------------------------------------------

    st.title('Epsilon-greedy algorithm')

    class EpsilonGreedy():
        """
        Epsilon Greedy with incremental update.
        Based on Sutton and Barto pseudo-code, page. 24
        """
        def __init__(self, data, epsilon):
            self.data = data
            self.epsilon = epsilon
            self.arm_count = len(data)
            self.Q = np.zeros(self.arm_count)  # q-value of actions
            self.N = np.zeros(self.arm_count)  # action count

        @staticmethod
        def name():
            return 'epsilon-greedy'

        def get_action(self):
            if np.random.uniform(0, 1) > self.epsilon:
                action = self.Q.argmax()
            else:
                action = np.random.randint(0, self.arm_count)
            return action

        def get_reward_regret(self, data):
            reward = data['gazole_prix']  # reward is the price of the gazole
            regret = self.data['gazole_prix'].max() - reward
            return reward, regret

        def _update_params(self, arm, reward):
            self.N[arm] += 1  # increment action count
            self.Q[arm] += 1 / self.N[arm] * (reward - self.Q[arm])  # inc. update rule

    epsilon_01 = EpsilonGreedy(data, epsilon=0.1)

    # Run the algorithm
    for i in range(1000):
        action = epsilon_01.get_action()
        reward, regret = epsilon_01.get_reward_regret(data.iloc[i])
        epsilon_01._update_params(action, reward)

    epsilon_05 = EpsilonGreedy(data, epsilon=0.5)

    # Run the algorithm
    for i in range(1000):
        action = epsilon_05.get_action()
        reward, regret = epsilon_05.get_reward_regret(data.iloc[i])
        epsilon_05._update_params(action, reward)

    epsilon_1 = EpsilonGreedy(data, epsilon=1)

    # Run the algorithm
    for i in range(1000):
        action = epsilon_1.get_action()
        reward, regret = epsilon_1.get_reward_regret(data.iloc[i])
        epsilon_1._update_params(action, reward)

    # Plot the results for Number of times action was selected
    fig1, ax1 = plt.subplots()
    ax1.plot(epsilon_01.N, label='epsilon=0.1')
    ax1.plot(epsilon_05.N, label='epsilon=0.5')
    ax1.plot(epsilon_1.N, label='epsilon=1')
    ax1.set_xlabel('Action')
    ax1.set_ylabel('Number of times action was selected')
    ax1.legend()
    st.pyplot(fig1)

    # Plot the results for Value of the action
    fig2, ax2 = plt.subplots()
    ax2.plot(epsilon_01.Q, label='epsilon=0.1')
    ax2.plot(epsilon_05.Q, label='epsilon=0.5')
    ax2.plot(epsilon_1.Q, label='epsilon=1')
    ax2.set_xlabel('Action')
    ax2.set_ylabel('Value of the action')
    ax2.legend()
    st.pyplot(fig2)

    # Log scale plot of epsilon greedy
    fig3, ax3 = plt.subplots()
    ax3.plot(epsilon_01.N * epsilon_01.Q, label='epsilon=0.1')
    ax3.plot(epsilon_05.N * epsilon_05.Q, label='epsilon=0.5')
    ax3.plot(epsilon_1.N * epsilon_1.Q, label='epsilon=1')
    ax3.legend()
    ax3.set_xscale('log')
    ax3.set_xlabel('Action')
    ax3.set_ylabel('Value of the action')
    st.pyplot(fig3)

    # Plot moving average ctr
    fig4, ax4 = plt.subplots()
    ax4.plot(epsilon_01.N * epsilon_01.Q, label='epsilon=0.1')
    ax4.plot(epsilon_05.N * epsilon_05.Q, label='epsilon=0.5')
    ax4.plot(epsilon_1.N * epsilon_1.Q, label='epsilon=1')
    ax4.legend()
    ax4.set_xlabel('Action')
    ax4.set_ylabel('Value of the action')
    st.pyplot(fig4)

# ---------------------------------------------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------------------------------------------

footer()