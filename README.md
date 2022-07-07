
# Project Overwiev

The scope is to visualize number of direct trains running daily between given cities in Poland
Using  https://rozklad-pkp.pl  - web Polish Railways timetable, list of cities (see file cities.csv) and Selenium library for browsing timetable and Pandas for preparing output for visualization (Orignation, Destination, trains count)  processing is done - see the PKP_graf.py script. Results are saved in graf.csv file to be an input for visualization.
Visualization (PKP_graf.py) is done in two ways:
  as a heatmap by Seaborn library and
  as a Plotly scattergeo plot
