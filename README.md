The scope is to visualize number of direct trains running daily between given cities in Poland using:

1. [https://rozklad-pkp.pl](https://rozklad-pkp.pl/) - web Polish Railways timetable,
2. list of cities (see file cities.csv)
3. Selenium library for browsing timetable
4. Pandas for preparing output
5. Seaborn, Plotly, Geopy libraries for visualization

Script PKP\_SCRAP.py uses Selenium as a main tool for timetable browsing. It checks if direct connection between cities exists (from file cities.csv). If so, it counted the number and store the value. Finally output data (graf.csv) is saved and ready to be visualized. List of cities is editable – you provide city names you are interested in.

Visualization is done by PKP\_graf.py. It creates pivot table for Seaborn heatmap, generates it and saves as a jpg file. It also geocodes names to Lat, Lon, and using Plotly plot on the map cities and a graph of direct trains connections.

Running the tool you can easily visualize and understand train traffic volume - in terms of number of trains not passengers

Usage:

1. Input city names in cities.csv
2. Run PKP\_SCRAP.py
3. Run PKP\_graf.py
