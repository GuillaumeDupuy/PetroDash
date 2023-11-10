# PetroDash

## About the Project

The aim of this project is to shed light on a topic of public interest (such as weather, environment, politics, public life, finance, transportation, culture, health, sports, economy, agriculture, ecology, etc.) that I have chosen. I have utilized unaltered, publicly available Open Data.

I have chosen to focus on the price of fuels in France. You will find a "**data**" directory where all the downloaded CSV files are located, the "**get_data.py**" script that allows you to fetch a new CSV for more up-to-date data, and the script "**app.py**" to launch the dashboard for visualizing the data in various formats.

### About the Data

The data is provided by data.gouv and is available [here](https://www.data.gouv.fr/fr/datasets/prix-des-carburants-en-france-flux-instantane-v2-amelioree/).

The data is updated every 10 minutes.

The data is about the price of fuels in France in every gas station. 

### About the Dashboard

The dashboard is made with Streamlit. You can find the documentation [here](https://docs.streamlit.io/en/stable/).

## Installation

In order to use our program, you have to clone the repo :

```bash
git clone https://github.com/GuillaumeDupuy/PetroDash.git
cd PetroDash
```

Then run this command to install all the libraries used :

```bash
pip install -r requirements.txt
```

## Execute

Finally, once the installation is complete, you should run this command to launch the dashboard :

```python
streamlit run app/app.py 
```

or 

```python
cd app
streamlit run app/app.py 
```

If you want to update the data, you should run this command :

```python
python get_data.py
```

Now, you can see the dashboard on the IP Address in the terminal or you can click [here](https://petrodash.streamlit.app/)

## Architecture of the project

```
├── app/
│   ├── utils/
│   │   ├── footer.py
│   │   └── map.py
│   │
│   └── app.py
│
├── get_data.py
│
├── requirements.txt
│
├── image/
│   ├── brand/
│   │   └── all_images_of_brand
│   └── fuels/
│       └── all_images_of_fuel
│
├── data/
│    ├── data.csv
│    ├── brand.txt
│    └── brand.csv
│
```

If you wish to modify or extend the code, here's a brief overview:

- app/app.py: This file contains the code for the dashboard. You can customize the visualization and interaction components here.

- app/utils/: This directory contains the code for the map and footer components. You can customize the map and footer here.

- get_data.py: Use this script to fetch new data. You can modify it to collect data from different sources or update the existing data retrieval process.

- image/: This directory contains all the images used in the dashboard.

- data/: This directory contains the data used in the dashboard.

- requirements.txt: This file lists all the Python libraries and dependencies required for the project. If you add new libraries, make sure to update this file accordingly.

Feel free to explore and enhance the code as needed.

## Analysis Report

We observe that among the seven largest brands with the highest number of fuel stations in France, four of them are supermarket brands. Therefore, it can be inferred that supermarkets are the largest fuel distributors in France. Consequently, three fuel-specialized companies dominate the market: Total Energies (with the highest number of stations in France), Total Energies Access, and Avia. Only two of these belong to the same company, Total Energies. It can be concluded that Total Energies is the largest fuel distributor in France.

Analyzing fuel prices, we note that diesel, E10, SP98, and SP95 are around €1.85 - €1.95 on average in mainland France and Corsica, while E85 and GPLc are around €1 on average. A more in-depth analysis of the average price by region reveals that the overall average for all types of fuel is roughly the same, with a difference of 0.5 cents €. However, in Corsica, the average price is higher by 0.10 cents €, reaching 0.30 - 0.80 € for some. It can be deduced that fuel prices are higher in Corsica than in mainland France due to the importation of fuels, which increases costs.

Examining the number of stations per region, Corsica stands out as the region with the fewest stations in France. It can also be inferred that fuel prices are higher in Corsica because there are fewer stations and, consequently, less competition. This leads to the need to travel further to find a station, and stations are more prone to running out of stock, contributing to an increase in fuel prices.