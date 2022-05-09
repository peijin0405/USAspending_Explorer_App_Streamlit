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

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")

#---------------------------------#
# Title
st.title("Welcome to the USAspending Explorer!")

st.markdown("""
This app is designed to make federal spending data publicly available. It reveals the whole picture of government grant funding in a specific state. It shows the trend of federal spending data in a state in the course of 2012-2022 and it also serves as a tool to understand federal funding at the county level.

This mapping part of the explorer focuses on federal assistance in the form of grants and shows the total funding going to each county. Total grants are obtained by adding up every grant awarded by the federal government to the county. Blank means that the county has no grants in FY 2022 (2022 fiscal year is from Oct. 2021 to Sep. 2022). Alaska is not included because the county codes of Alaska extracted from USAspening API do not correspond to the ones provided by the United States Census Bureau.""")

#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** pandas, streamlit, numpy, plotly, BeautifulSoup, requests, json, base64 
* **Data source:** [USAspending API](https://www.usaspending.gov).USAspending is the official open data source of federal spending information. It tracks how federal maony is spent in communities accross America and beyond. 
* **Reference and Credit:** County codes collected from [United States Census Bureau](https://www.census.gov/library/reference/code-lists/ansi.html#county). State Population Data is from [Wikipedia](https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents). County GeoJSON files adapted from  [Johan Sundström's  github](https://github.com/johan/world.geo.json) repositories. State latitude and longitude data come from [LatLong.net](https://www.latlong.net/category/states-236-14.html). Combine GeoJSON files using [Find that Postcode](https://findthatpostcode.uk/tools/merge-geojson). 
""")
#---------------------------------#

# Make selectbox a sidebar
Select_state = st.selectbox('Select state',['Alabama','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island''South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'])

                             
#############load needed data#######################
###get supplementary data
State_Latitude_Longitude = pd.read_csv("State_Latitude_Longitude.csv")

FIPS_code_state = pd.read_csv("FIPS_code_state.csv")
FIPS_code_state["FIPS"] = FIPS_code_state["FIPS"].apply(lambda x:str(x).zfill(2))             

###get the grants data
def get_grants_dataset(Select_state):
    if Select_state == "New York":
        grants_data = pd.read_csv("grants_data/county_grants_NY.csv")
    elif Select_state == "Indiana":
        grants_data  = pd.read_csv("grants_data/county_grants_Indiana.csv")
    elif Select_state == "Tennessee":
        grants_data  = pd.read_csv("grants_data/county_grants_TN.csv")
    elif Select_state == "Alabama":
        grants_data  = pd.read_csv("grants_data/county_grants_Alabama.csv")
    elif Select_state == "Washington":
        grants_data  = pd.read_csv("grants_data/county_grants_Washington.csv")
    elif Select_state == "California":
        grants_data  = pd.read_csv("grants_data/county_grants_CA.csv")
    elif Select_state == "Pennsylvania":
        grants_data  = pd.read_csv("grants_data/county_grants_PA.csv")
    elif Select_state == "Illinois":
        grants_data  = pd.read_csv("grants_data/county_grants_IL.csv")
    elif Select_state == "Maryland":
        grants_data  = pd.read_csv("grants_data/county_grants_Maryland.csv")
    elif Select_state == "Texas":
        grants_data  = pd.read_csv("grants_data/county_grants_TX.csv")
    elif Select_state == "Georgia":
        grants_data  = pd.read_csv("grants_data/county_grants_GA.csv")
    elif Select_state == "Michigan":
        grants_data  = pd.read_csv("grants_data/county_grants_MI.csv")
    elif Select_state == "Minnesota":
        grants_data  = pd.read_csv("grants_data/county_grants_MN.csv")
    elif Select_state == "Wyoming":
        grants_data  = pd.read_csv("grants_data/county_grants_WY.csv")
    elif Select_state == "Mississippi":
        grants_data  = pd.read_csv("grants_data/county_grants_MS.csv")
    elif Select_state == "Arizona":
        grants_data  = pd.read_csv("grants_data/county_grants_AZ.csv")
    elif Select_state == "Arkansas":
        grants_data  = pd.read_csv("grants_data/county_grants_AR.csv")
    elif Select_state == "Colorado":
        grants_data  = pd.read_csv("grants_data/county_grants_CO.csv")
    elif Select_state == "Connecticut":
        grants_data  = pd.read_csv("grants_data/county_grants_CT.csv")
    elif Select_state == "Delaware":
        grants_data  = pd.read_csv("grants_data/county_grants_DE.csv")
    elif Select_state == "Idaho":
        grants_data  = pd.read_csv("grants_data/county_grants_ID.csv")
    elif Select_state == "Iowa":
        grants_data  = pd.read_csv("grants_data/county_grants_IA.csv")
    elif Select_state == "Kansas":
        grants_data  = pd.read_csv("grants_data/county_grants_KS.csv")
    elif Select_state == "Kentucky":
        grants_data  = pd.read_csv("grants_data/county_grants_KY.csv")
    elif Select_state == "Louisiana":
        grants_data  = pd.read_csv("grants_data/county_grants_LA.csv")
    elif Select_state == "Maine":
        grants_data  = pd.read_csv("grants_data/county_grants_ME.csv")
    elif Select_state == "Massachusetts":
        grants_data  = pd.read_csv("grants_data/county_grants_MA.csv")
    elif Select_state == "Missouri":
        grants_data  = pd.read_csv("grants_data/county_grants_MO.csv")
    elif Select_state == "Montana":
        grants_data  = pd.read_csv("grants_data/county_grants_MT.csv")
    elif Select_state == "Nebraska":
        grants_data  = pd.read_csv("grants_data/county_grants_NE.csv")
    elif Select_state == "Nevada":
        grants_data  = pd.read_csv("grants_data/county_grants_NV.csv")
    elif Select_state == "New Hampshire":
        grants_data  = pd.read_csv("grants_data/county_grants_NH.csv")
    elif Select_state == "New Jersey":
        grants_data  = pd.read_csv("grants_data/county_grants_NJ.csv")
    elif Select_state == "New Mexico":
        grants_data  = pd.read_csv("grants_data/county_grants_NM.csv")
    elif Select_state == "North Carolina":
        grants_data  = pd.read_csv("grants_data/county_grants_NC.csv")
    elif Select_state == "North Dakota":
        grants_data  = pd.read_csv("grants_data/county_grants_ND.csv")
    elif Select_state == "Ohio":
        grants_data  = pd.read_csv("grants_data/county_grants_OH.csv")
    elif Select_state == "Oklahoma":
        grants_data  = pd.read_csv("grants_data/county_grants_OK.csv")
    elif Select_state == "Oregon":
        grants_data  = pd.read_csv("grants_data/county_grants_OR.csv")
    elif Select_state == "South Carolina":
        grants_data  = pd.read_csv("grants_data/county_grants_SC.csv")
    elif Select_state == "South Dakota":
        grants_data  = pd.read_csv("grants_data/county_grants_SD.csv")
    elif Select_state == "Utah":
        grants_data  = pd.read_csv("grants_data/county_grants_UT.csv")
    elif Select_state == "Vermont":
        grants_data  = pd.read_csv("grants_data/county_grants_VT.csv")
    elif Select_state == "Virginia":
        grants_data  = pd.read_csv("grants_data/county_grants_VA.csv")
    elif Select_state == "West Virginia":
        grants_data  = pd.read_csv("grants_data/county_grants_WV.csv")
    elif Select_state == "Wisconsin":
        grants_data  = pd.read_csv("grants_data/county_grants_WI.csv")
    elif Select_state == "Hawaii":
        grants_data  = pd.read_csv("grants_data/county_grants_HI.csv")
    elif Select_state == "Rhode Island":
        grants_data  = pd.read_csv("grants_data/county_grants_RI.csv")
    else:
        grants_data  = pd.read_csv("grants_data/county_grants_Florida.csv")
    return grants_data
        
###get the geojson data
def get_geojson_dataset(Select_state):
    if Select_state == "New York":
        geojson_data = json.load(open("geojson_data/mergedfile_new_york_36.geojson","r"))
    elif Select_state == "Indiana":
        geojson_data  = json.load(open("geojson_data/mergedfile_indiana.geojson","r"))
    elif Select_state == "Tennessee":
        geojson_data  =json.load(open("geojson_data/mergedfile_TN.geojson","r"))
    elif Select_state == "Alabama":
        geojson_data  =json.load(open("geojson_data/mergedfile_AL.geojson","r")) 
    elif Select_state == "Washington":
        geojson_data  =json.load(open("geojson_data/mergedfile_WA.geojson","r")) 
    elif Select_state == "California":
        geojson_data  =json.load(open("geojson_data/mergedfile_California.geojson","r")) 
    elif Select_state == "Pennsylvania":
        geojson_data  =json.load(open("geojson_data/mergedfile_PA.geojson","r"))    
    elif Select_state == "Illinois":
        geojson_data  =json.load(open("geojson_data/mergedfile_IL.geojson","r"))  
    elif Select_state == "Maryland":
        geojson_data  =json.load(open("geojson_data/mergedfile Maryland.geojson","r")) 
    elif Select_state == "Texas":
        geojson_data  =json.load(open("geojson_data/mergedfile_TX.geojson","r")) 
    elif Select_state == "Georgia":
        geojson_data  =json.load(open("geojson_data/mergedfile_GA.geojson","r")) 
    elif Select_state == "Michigan":
        geojson_data  =json.load(open("geojson_data/mergedfile_MI.geojson","r")) 
    elif Select_state == "Minnesota":
        geojson_data  =json.load(open("geojson_data/mergedfile_MN.geojson","r")) 
    elif Select_state == "Wyoming":
        geojson_data  =json.load(open("geojson_data/mergedfile_WY.geojson","r")) 
    elif Select_state == "Mississippi":
        geojson_data  =json.load(open("geojson_data/mergedfile_MS.geojson","r")) 
    elif Select_state == "Arizona":
        geojson_data  =json.load(open("geojson_data/mergedfile_AZ.geojson","r")) 
    elif Select_state == "Arkansas":
        geojson_data  =json.load(open("geojson_data/mergedfile_AR.geojson","r")) 
    elif Select_state == "Colorado":
        geojson_data  =json.load(open("geojson_data/mergedfile_CO.geojson","r"))
    elif Select_state == "Connecticut":
        geojson_data  =json.load(open("geojson_data/mergedfile_CT.geojson","r"))   
    elif Select_state == "Delaware":
        geojson_data  =json.load(open("geojson_data/mergedfile_DE.geojson","r")) 
    elif Select_state == "Idaho":
        geojson_data  =json.load(open("geojson_data/mergedfile_ID.geojson","r"))
    elif Select_state == "Iowa":
        geojson_data  =json.load(open("geojson_data/mergedfile_IA.geojson","r"))
    elif Select_state == "Kansas":
        geojson_data  =json.load(open("geojson_data/mergedfile_KS.geojson","r"))
    elif Select_state == "Kentucky":
        geojson_data  =json.load(open("geojson_data/mergedfile_KY.geojson","r"))
    elif Select_state == "Louisiana":
        geojson_data  =json.load(open("geojson_data/mergedfile_LA.geojson","r"))
    elif Select_state == "Maine":
        geojson_data  =json.load(open("geojson_data/mergedfile_ME.geojson","r")) 
    elif Select_state == "Massachusetts":
        geojson_data  =json.load(open("geojson_data/mergedfile_MA.geojson","r"))  
    elif Select_state == "Missouri":
        geojson_data  =json.load(open("geojson_data/mergedfile_MO.geojson","r")) 
    elif Select_state == "Montana":
        geojson_data  =json.load(open("geojson_data/mergedfile_MT.geojson","r"))
    elif Select_state == "Nebraska":
        geojson_data  =json.load(open("geojson_data/mergedfile_NE.geojson","r"))
    elif Select_state == "Nevada":
        geojson_data  =json.load(open("geojson_data/mergedfile_NV.geojson","r"))
    elif Select_state == "New Hampshire":
        geojson_data  =json.load(open("geojson_data/mergedfile_NH.geojson","r"))
    elif Select_state == "New Jersey":
        geojson_data  =json.load(open("geojson_data/mergedfile_NJ.geojson","r"))
    elif Select_state == "New Mexico":
        geojson_data  =json.load(open("geojson_data/mergedfile_NM.geojson","r"))
    elif Select_state == "North Carolina":
        geojson_data  =json.load(open("geojson_data/mergedfile_NC.geojson","r"))
    elif Select_state == "North Dakota":
        geojson_data  =json.load(open("geojson_data/mergedfile_ND.geojson","r"))
    elif Select_state == "Ohio":
        geojson_data  =json.load(open("geojson_data/mergedfile_OH.geojson","r"))
    elif Select_state == "Oklahoma":
        geojson_data  =json.load(open("geojson_data/mergedfile_OK.geojson","r"))
    elif Select_state == "Oregon":
        geojson_data  =json.load(open("geojson_data/mergedfile_OR.geojson","r"))
    elif Select_state == "South Carolina":
        geojson_data  =json.load(open("geojson_data/mergedfile_SC.geojson","r"))
    elif Select_state == "South Dakota":
        geojson_data  =json.load(open("geojson_data/mergedfile_SD.geojson","r"))
    elif Select_state == "Utah":
        geojson_data  =json.load(open("geojson_data/mergedfile_UT.geojson","r"))
    elif Select_state == "Vermont":
        geojson_data  =json.load(open("geojson_data/mergedfile_VT.geojson","r"))
    elif Select_state == "Virginia":
        geojson_data  =json.load(open("geojson_data/mergedfile_VA.geojson","r"))
    elif Select_state == "West Virginia":
        geojson_data  =json.load(open("geojson_data/mergedfile_WV.geojson","r"))
    elif Select_state == "Wisconsin":
        geojson_data  =json.load(open("geojson_data/mergedfile_WI.geojson","r"))
    elif Select_state == "Hawaii":
        geojson_data  =json.load(open("geojson_data/mergedfile_HI.geojson","r"))
    elif Select_state == "Rhode Island":
        geojson_data  =json.load(open("geojson_data/mergedfile_RI.geojson","r"))
    else:
        geojson_data  = json.load(open("geojson_data/mergedfile_Florida.geojson","r"))  
    return geojson_data

###get the Latitude_Longitude of a state
#clean the data
State_Latitude_Longitude['Place Name'] = State_Latitude_Longitude['Place Name'].str.split(r',').str[0]
def get_Latitude_Longitude(Select_state):
    state_row = State_Latitude_Longitude.loc[State_Latitude_Longitude["Place Name"] == Select_state]
    for state in State_Latitude_Longitude["Place Name"]:
        if Select_state == state:
            lat = state_row.iloc[0]['Latitude']
            lon = state_row.iloc[0]['Longitude']
    return lat,lon

###get the FIPS code of a state  
def get_FIPS(Select_state):
    state_row = FIPS_code_state.loc[FIPS_code_state["Name"] == Select_state]
    for state in FIPS_code_state["Name"]:
        if Select_state == state:
            FIPS_code0 = state_row.iloc[0]['FIPS']
            FIPS_code = str(FIPS_code0)
    return FIPS_code

####################Recall####################
grants_data = get_grants_dataset(Select_state)
geojson_data = get_geojson_dataset(Select_state)
lat,lon = get_Latitude_Longitude(Select_state)
FIPS_code = get_FIPS(Select_state)

########################################the first result #######################################   
#Customize fonts
st.markdown(""" <style> .font {
font-size:24px ; font-family: 'Cooper Black';} 
</style> """, unsafe_allow_html=True)
st.markdown('<p class="font">All Federal Grant Funding Received by County, FY 2022</p>', unsafe_allow_html=True)

county_grants_NY_vis = grants_data.filter(["County","Award_Amount","grants_per_capita"])
county_grants_NY_vis = county_grants_NY_vis.rename(columns={"County":"County Name","Award_Amount":"Total Federal Grant Funding Amount","grants_per_capita":"Total Per Capita Federal Grant Funding"})


county_grants_NY_vis=county_grants_NY_vis.sort_values(by='Total Per Capita Federal Grant Funding',ascending=False,axis=0)
                             
County_Name_list = []
for ii in county_grants_NY_vis["County Name"]:
    County_Name_list.append(ii)
    
total_list = []
for ii in county_grants_NY_vis["Total Federal Grant Funding Amount"]:
    currency_form = "${:,.2f}".format(ii)
    total_list.append(currency_form )
    
per_list = []
for ii in county_grants_NY_vis["Total Per Capita Federal Grant Funding"]:
    currency_form_2 = "${:,.2f}".format(ii)
    per_list.append(currency_form_2)

cc={"total_list":total_list,"per_list":per_list,"County_Name_list":County_Name_list}
NY_county_grants_vis = DataFrame(cc)                              
                              
NY_county_grants_vis = NY_county_grants_vis.rename(columns={"County_Name_list":"County Name",
                                          "total_list":"Total Federal Grant Funding Amount",
                                           "per_list":"Total Per Capita Federal Grant Funding"})
NY_county_grants_vis = NY_county_grants_vis.filter(["County Name","Total Federal Grant Funding Amount",
                                                    "Total Per Capita Federal Grant Funding"])                              
st.dataframe(data=NY_county_grants_vis)  
                              
#---------------------------------#
# Chart Layout

columns = st.columns((1,1))
    
##############the second result visualization################                           

with columns[0]:
    
    state_id_map = {}
    for feature in geojson_data["features"]:
        feature["id"] = feature["properties"]['name']
        state_id_map[feature["properties"]['name']] = feature["id"]

    grants_data["id"] = grants_data["County"].apply(lambda x:state_id_map[x])                              
    grants_data["grants_per_capita"]=round(grants_data["grants_per_capita"],3)
    #set the value under 0 to be 1 (log10(1) ==0)
    grants_data["grants_per_capita"][grants_data.grants_per_capita< 0]=1
    grants_data["grants_per_capita_scale"] = np.log10(grants_data["grants_per_capita"])

    grants_data = grants_data.merge(NY_county_grants_vis, how = "left", left_on='County', right_on='County Name')
    grants_data = grants_data.rename(columns={"grants_per_capita_scale":"Per Capita Scale"})  
    #plot                               
    fig1 = px.choropleth_mapbox(grants_data,
                        locations = "id",
                        geojson = geojson_data,
                        color="Per Capita Scale",
                       hover_name = "County Name",
                       hover_data = ["Total Per Capita Federal Grant Funding"],
                         mapbox_style = "carto-positron",
                         center = {"lat": lat ,"lon":lon},
                         zoom= 4.7,opacity = 0.3,
                         title="2022 Grant Funding of " + Select_state,
                         width=700, height=500,
                        )
    st.plotly_chart(fig1)                                                       
##########################the third result visualization################                   
##form the url              

with columns[1]:
    
    year_list = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
    year_list_1 = [ str(x) for x in year_list]

    one_state = []

    for year in year_list_1:
        url = "https://api.usaspending.gov/api/v2/recipient/state/" + FIPS_code + "/" + "?year=" + year
        one_state.append(url)                            

    ##request the annual data of one state(2012-2022)                               
    info_one_state = []
    for ii in one_state:
        r = requests.get(ii)
        print(ii)
        r0_1=r.json()
        info_one_state.append(r0_1) 

    ##data wrangling                               
    info_one_state = pd.DataFrame(info_one_state)
    info_one_state0 = info_one_state.filter(["code","fips","total_prime_amount",'population'])
    info_one_state0["award_per_capita"]  = round(info_one_state0["total_prime_amount"]/info_one_state0["population"],2)
    info_one_state0["year"] = year_list                              


    ##create figure with secondary y-axis
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    ## add traces
    fig2.add_trace(
        go.Scatter(
            x=[2012, 2013, 2014, 2015, 2016, 2017, 2018,2019, 2020, 2021, 2022],
            y=info_one_state0['award_per_capita'],
            name="award_amount_per_capita",
            mode='lines+markers', 
            marker=dict(size=9,
                    symbol = 'diamond',
                    color ='RGB(251, 177, 36)',
                    line_width = 2),
            line = dict(color='firebrick', width=3)),
            secondary_y=True
        )

    fig2.add_trace(
        go.Bar(
            x=[2012, 2013, 2014, 2015, 2016, 2017, 2018,2019, 2020, 2021, 2022],
            y=info_one_state0['total_prime_amount'],
            name="total_prime_amount",
            text = info_one_state0['total_prime_amount'],
            textposition='outside',
            textfont=dict(
            size=13,
            color='#1f77b4'),
            marker_color=["#f3e5f5", '#e1bee7', '#ce93d8', '#ba68c8','#ab47bc',
                         '#9c27b0','#8e24aa','#7b1fa2','#6a1b9a','#4a148c','#3c0a99'], 
            marker_line_color='rgb(17, 69, 126)',
            marker_line_width=1, 
            opacity=0.7),
            secondary_y=False
        )

    # strip down the rest of the plot
    fig2.update_traces(texttemplate='%{text:.2s}')

    fig2.update_layout(
        showlegend=True,
        plot_bgcolor="rgb(240,240,240)",
        margin=dict(t=50,l=10,b=10,r=10),
        title_text='2012-2022 Prime Amount of ' + Select_state,
        title_font_family='Times New Roman',
        legend_title_text='Dollars Obligated',
        title_font_size = 25,
        title_font_color="darkblue",
        title_x=0.5,
        xaxis=dict(
        tickfont_size=14,
        tickangle = 270,
        showgrid = True,
        zeroline = True,
        showline = True,
        showticklabels = True,
        dtick=1
        ),
        legend=dict(
        x=0.01,
        y=0.99,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
        ),
        bargap=0.15
    )

    ## set y-axes titles
    fig2.update_yaxes(title_text='Total Prime Amount  USD', 
                     titlefont_size=16, 
                     tickfont_size=14,
                     secondary_y=False)
    fig2.update_yaxes(title_text='Award Amount Per Capita  USD', 
                     titlefont_size=16, 
                     tickfont_size=14, 
                     secondary_y=True)


    st.plotly_chart(fig2)                               
                              
                              



                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              