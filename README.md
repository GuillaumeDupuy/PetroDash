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

Now, you can see the dashboard on the IP Address in the terminal or you can click [here](https://petrodash.streamlit.app/)