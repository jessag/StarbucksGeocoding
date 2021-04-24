# -*- coding: utf-8 -*-
"""Assignment5_JessaGariepy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ar6wEtZOcSf0JXKfQTWro7dGruL78n4E

**Module 5 - Assignment 5**
- Student: Jessa Gariepy
- Instructor: Professor Li
- Class: GIS 322
- Date: 04/06/2021

---

First, import all the needed modules:
"""

# Commented out IPython magic to ensure Python compatibility.
# Import needed modules.

!pip install geopandas
!sudo apt install python3-rtree

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geopandas.tools import geocode
import pygeos
import rtree

# %matplotlib inline

"""The following line of code was utilized as a recommendation from a classmate that was also having issues with an ImportModule Error. The code install the most updated version of geopandas"""

!pip install git+git://github.com/geopandas/geopandas.git

"""## Step 1: Import the data into Python using the proper function.

*starbucks* is name of all Starbucks stores in Arizona.
*az_zips* is shapefile file of all Arizona zip codes.

After files are imported, the files are viewed using the head() function.
"""

# Step 1: Import the data into Python using the proper function

starbucks = pd.read_csv("/content/starbucks_address.csv")
az_zips = gpd.read_file("/content/AZ_zipcodes.shp")

starbucks.head()

az_zips.head()

"""## Step 2: Geocode each of Starbucks address to longitude and latitude.


- The for loop is designed to go through each entry within the starbucks dataframe and to combine the street address, city, and state into one column named "address".

- Then, geocoding is finalized and each geocoded starbucks location is placed in starbucks_loc GeoDataFrame.

"""

# Step 2: Geocode each of the Starbucks address to longitude and latitude.
# Hints: Use loops and concatenate each address with city/state names
# KEY = AswUwe1UpCxEOAzwfwDwZn5IjWPKhTFLsqXMsV4HTRcIX2zO88Nv6R8LwXiOfIMB

# Loop 1: To create a concatenated version of each SB address
for i in starbucks:
  starbucks['Address'] = starbucks['Street Address'] + " " + starbucks['City'] + " " + starbucks['State/Province']

# Get the longtiude and latitude of each location. 
starbucks_loc = gpd.tools.geocode(starbucks["Address"], provider = 'bing', api_key = 'AswUwe1UpCxEOAzwfwDwZn5IjWPKhTFLsqXMsV4HTRcIX2zO88Nv6R8LwXiOfIMB')

#Check to make sure it worked properly
starbucks_loc.head()

"""- The following code is used to determine the coordinate reference system (CRS) for each data frame. Then, the starbucks_loc GDF is converted to the same CRS that az_zips has."""

#find CRS of Arizona Zip code data = 4269
az_zips.crs

#find CRS of starbucks GDF = 4326
starbucks_loc.crs

starbucks_loc= starbucks_loc.to_crs(epsg ='4269')

starbucks_loc.crs

"""## Step 3: Import the zipcode boundary map into Python

The following code simply visualizes the zipcode data from az_zips (a shapefile).
"""

#Step 3: Import the zipcode boundary map into Python 
az_zips.plot()

"""## Step 4: Count number of Starbuck locations within each zip code using proper "spatial overlay" function.

- The following code performs a spatial merge between the az_zips GeoDataFrame and starbucks_loc GeoDataFrame.
- Index from az_zips is used for the new GDF, and the attributes are joined depending on if Starbucks locations fully contained in zipcodes.

- The count is performed using the groupby() function. For each zipcode, it counts the number of Starbuck addresses contained within.
"""

#Step 4: Count the number of Starbuck location within each zip code using proper
# "spatial overlay" function


starbucks_zips_merged = gpd.sjoin(az_zips,starbucks_loc, how = 'left', op = 'contains')

#The number of Starbuck locations within each zipcode.
sb_by_zip = starbucks_zips_merged.groupby("Zipcode").count()[["address"]]
print(sb_by_zip)

starbucks_zips_merged.head()

#Here, we do an attribute merge of the total number of Starbucks in each zipcode (sb_by_zip) and GDF (starbucks_zips_merged)

merged_starbucks_total = pd.merge(starbucks_zips_merged, sb_by_zip,
                             left_on= "Zipcode", right_on = 'Zipcode')

merged_starbucks_total.head()

# Change column name to be more intuitive:
merged_starbucks_total.rename(columns = {'address_y':'SB_in_zip'}, inplace = True)

merged_starbucks_total.head()

"""## Step 5: Export the zip code map with color representing numbers of Starbucks locations.

- The plot below was learned from the module 5 example code.

"""

#Define figure size and subplot

fig, ax = plt.subplots(1, figsize=(12, 12))
merged_starbucks_total.plot(column="SB_in_zip",figsize=(10,10), ax=ax, 
                           cmap='PuRd',edgecolor='black', linewidth=0.2)

# Set the plot's title
plt.title("Starbucks Stores per Arizona Zipcode",fontsize=20)

#Prepare the legend.
vmin = merged_starbucks_total["SB_in_zip"].min()
vmax = merged_starbucks_total["SB_in_zip"].max()
sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax),cmap='PuRd')
sm._A = []
cax = fig.add_axes([1, 0.15, 0.03, 0.65])
fig.colorbar(sm, cax=cax)

#Turn off the axis increments
ax.axis('off')


#Save and export image
plt.savefig("starbucks.png",dpi=400,bbox_inches='tight')

# This is the same map as above, except with Starbucks location pinpointed on the map.
# I was not sure if required, so I included in case.


fig, ax = plt.subplots(1, figsize=(12, 12))
merged_starbucks_total.plot(column="SB_in_zip",figsize=(10,10), ax=ax, 
                           cmap='Reds',edgecolor='black', linewidth=0.2)
starbucks_loc.plot(ax=ax,color="black")

# Set the plot's title
plt.title("Starbucks Stores per Arizona Zipcode",fontsize=20)

#Prepare the legend.
vmin = merged_starbucks_total["SB_in_zip"].min()
vmax = merged_starbucks_total["SB_in_zip"].max()
sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax),cmap='Reds')
sm._A = []
cax = fig.add_axes([1, 0.15, 0.03, 0.65])
fig.colorbar(sm, cax=cax)

#Turn off the axis increments
ax.axis('off')