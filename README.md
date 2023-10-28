# PetroDash

## About the Project

The aim of this project is to shed light on a topic of public interest (such as weather, environment, politics, public life, finance, transportation, culture, health, sports, economy, agriculture, ecology, etc.) that I have chosen. I have utilized unaltered, publicly available Open Data.

I have chosen to focus on the price of fuels in France. You will find a "**data**" directory where all the downloaded CSV files are located, the "**get_data.py**" script that allows you to fetch a new CSV for more up-to-date data, and the scrip to launch the dashboard for visualizing the data in various formats.

### Installation

In order to use our program, you have to clone the repo :

```bash
git clone https://github.com/GuillaumeDupuy/PetroDash.git
cd PetroDash
```

Then run this command to install all the libraries used :

```bash
pip install -r requirements.txt
```

### Execute

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
│   │
│   └── app.py
│
├── get_data.py
│
├── requirements.txt
│
├── data/
│    ├── data.csv
│    └── new_data.csv
│
```

If you wish to modify or extend the code, here's a brief overview:

- app/app.py: This file contains the code for the dashboard. You can customize the visualization and interaction components here.

- get_data.py: Use this script to fetch new data. You can modify it to collect data from different sources or update the existing data retrieval process.

- requirements.txt: This file lists all the Python libraries and dependencies required for the project. If you add new libraries, make sure to update this file accordingly.

Feel free to explore and enhance the code as needed.