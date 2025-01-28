## Overview

**SA_Water_Quality_Map** is a project designed to visualise and interact with **SA Water Quality Reports**. This allows users to view detailed water quality reports provided by SA Water.

The data provided only provides location names and not coordinates (lat/long) required for mapping. Utilising the **GeoPy** Python package, the location is converted to a lat/long coordinate. Along with **Folium** and **Pandas** packages, this map was made possible.

**The dataset used is provided by Data SA**.

---

**NOTE:** Not all data is available due to location names not being recorded constistantly in the datasets. Some efforts have been made to include them anyway, but the inconsistancies in the dataset can change.

### **View the interactive map here: https://jameson-dev.github.io/SA_Water_Quality_Map/**

## Planned

It is planned to utilise a Choropleth map to better visualise the water quality of the locations available on the map.
