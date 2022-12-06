#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import numpy as np
import pandas as pd
import base64
from bs4 import BeautifulSoup
import requests
import json
from pandas.core.frame import DataFrame

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


merge6_withoutUSA = pd.read_csv("merge6_withoutUSA.csv")
merge9 = pd.read_csv("merge9.csv")

## Read in geojson
all_country = json.load(open("all_country.geojson","r"))

#---------------------------------#
# Chart Layout
# merge6_withoutUSA_filtered = merge6_withoutUSA.filter(["Country Name","UN Region","Amount","Population","Population Date"])

# st.dataframe(data=merge6_withoutUSA_filtered)



#################### sec viz#############



fig3 = px.choropleth_mapbox(merge9,
                    locations = "id",
                    geojson = all_country,
                    color="log_FY2022 Grants Amount",
                   hover_name = "Country Name",
                   hover_data = merge9.columns,
                     mapbox_style = "carto-positron",
                     zoom= 0.57,opacity = 0.3,
                    center = {"lat": 23.8859,"lon":45.0792},
                    title = "Distribution of USA Grants Spending around the world in FY2022",
                    height=700, width=800)
#fig3.update_layout(height=500, width=700, margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig3) 

