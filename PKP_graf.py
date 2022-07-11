import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from matplotlib.pyplot import figure

geopy_login = os.getenv("GEOPY_LOGIN")
if not geopy_login:
    print("Ustaw GEOPY_LOGIN")
    sys.exit(1)

geolocator = Nominatim(user_agent="YOURLOGIN")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
path = os.getcwd()
Trains = pd.read_csv(path + '/graf.csv')
Trains_piv = Trains.pivot("Origination", "Destination", "daily_trains")

figure(figsize=(12, 12), dpi=300)
size = 100 / Trains_piv.shape[0]
hm = sns.heatmap(data=Trains_piv, linewidths=.5, cbar=False, annot=True, annot_kws={"size": size, "color": 'blue'}, cmap="Oranges")
plt.xticks(fontsize=size)
plt.yticks(fontsize=size)
plt.title("Liczba bezpośrednich połączeń kolejowych pomiędzy miastami", fontsize=18)
plt.show()
hm.figure.savefig(path + '/heat.jpg', dpi=300)

cities = pd.read_csv(path + '/cities.csv')
cities['location'] = cities['City'].apply(geocode)
cities['point'] = cities['location'].apply(lambda loc: tuple(loc.point) if loc else None)
cities = cities.drop(columns=['location'])
coords = pd.DataFrame(cities['point'].to_list(), index=cities.index)
coords.columns = ['lat', 'lon', 'point']
coords = coords.drop(columns=['point'])
cities = cities.merge(coords, left_index=True, right_index=True)

Trains = Trains.merge(cities, left_on='Origination', right_on='City')
Trains = Trains[Trains['daily_trains'] != 0]
Trains = Trains.rename(columns={"lat": "o_lat", "lon": "o_lon"})
Trains = Trains.merge(cities, left_on='Destination', right_on='City')
Trains = Trains.rename(columns={"lat": "d_lat", "lon": "d_lon"})

Trains_by_cities = Trains.groupby(['Origination'], as_index=False).sum()
Trains_by_cities = Trains_by_cities.drop(columns=['o_lat', 'd_lat', 'o_lon', 'd_lon'])
cities = cities.merge(coords, left_index=True, right_index=True)
cities = cities.merge(Trains_by_cities, left_on='City', right_on='Origination')
fig = go.Figure()

for i in range(len(Trains)):
    fig.add_trace(
        go.Scattergeo(
            locationmode='country names',
            lon=[Trains['o_lon'][i], Trains['d_lon'][i]],
            lat=[Trains['o_lat'][i], Trains['d_lat'][i]],
            mode='lines',
            line=dict(width=float(Trains['daily_trains'][i] / 2), color='rgb(255, 95, 0)'),
            opacity=float(Trains['daily_trains'][i]) / float(Trains['daily_trains'].max()),
        )
    )

font_settings = dict(color='rgb(0, 0, 188)', size=14)
line_settings = dict(width=3, color='rgb(0, 0, 188,1)')

fig.add_trace(go.Scattergeo(
    locationmode='country names',
    lon=cities['lon_y'],
    lat=cities['lat_y'],
    hoverinfo='text',
    text=cities['City'],
    mode='markers+text',
    textposition='middle right',
    textfont=font_settings,
    marker=dict(
        size=cities['daily_trains'] / 8,
        opacity=1,
        color='rgb(0, 0, 188)',
        line=line_settings
    )))

fig.update_layout(
    title_text='Kolejowe połączenia bezpośrednie pomiędzy miastami',
    title_font_size=24,
    title_x=0.5,
    title_y=0.95,
    showlegend=False,
    geo=dict(
        scope='europe',
        center=dict(lat=52.1, lon=17.9),
        projection=dict(scale=10, type='transverse mercator'),
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(180, 180, 180)',
        resolution=50
    ),
)

fig.show()
