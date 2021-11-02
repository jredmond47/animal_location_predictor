import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style('dark_grid')
import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas as gpd
# import contextily as ctx
import pandas as pd
import numpy as np

# def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
#     xmin, xmax, ymin, ymax = ax.axis()
#     basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
#     ax.imshow(basemap, extent=extent, interpolation='bilinear')
#     # restore original x/y limits
#     ax.axis((xmin, xmax, ymin, ymax))

path = os.path.join('data','movebank','gps_events_s21231406_i24563363_ss653.csv')

data = pd.read_csv(path)

data[['year','week','weekday']] = pd.to_datetime(data.timestamp).dt.isocalendar()
data['week_year'] = data.year.astype(str) + '-' + data.week.astype(str)
data['weekday_year'] = data.year.astype(str) + '-' + data.weekday.astype(str)

# scatter and line plot
temp = data.groupby('week_year')['ground_speed'].median().reset_index().rename(columns={'ground_speed':'agg_speed'})

fig, ax = plt.subplots(figsize=(15,9))
plt.scatter(temp.week_year, temp.agg_speed)
plt.plot(temp.week_year, temp.agg_speed)
plt.show()

# coordinates plot
# temp = data.groupby(['weekday','week','year'])[['location_lat','location_long']].mean().reset_index()
#
# _temp = temp[temp.year == '2014']
#
# df = _temp
#
# df['coords'] = list(zip(df.location_long, df.location_lat))
#
# # ... turn them into geodataframe, and convert our
# # epsg into 3857, since web map tiles are typically
# # provided as such.
# geo_df = gpd.GeoDataFrame(
#     df, crs  ={'init': 'epsg:4326'},
#     geometry = df['coords'].apply(Point)
# ).to_crs(epsg=3857)
#
# # ... and make the plot
# ax = geo_df.plot(
#     figsize= (5, 5),
#     alpha  = 1
# )
# add_basemap(ax, zoom=20)
# ax.set_axis_off()
# plt.title('We made a thing')
# plt.show()