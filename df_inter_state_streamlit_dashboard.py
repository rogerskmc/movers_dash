# 2023 ACS 1-YR PUMS Dashboard
# Kathleen created 5/30/25
# Last edited 6/4/25


# #######################
# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px


#######################
# Page configuration
st.set_page_config(
    page_title="Team A3 Movers Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")


#######################
# Load data
inbound = pd.read_csv('inbound.csv')
outbound = pd.read_csv('outbound.csv')


#######################
# Sidebar
with st.sidebar:
    st.title("Team A3 Movers Dashboard")
    
    sex_list = list(outbound.sex.unique())
    age_list = list(outbound.age_group.unique())
    education_list = list(outbound.education.unique())
    marital_list = list(outbound.marital_status.unique())
    
    selected_sex = st.selectbox('Select Sex', options=outbound["sex"].unique())
    selected_age = st.selectbox('Select Age Group', options=outbound["age_group"].unique())
    selected_education = st.selectbox('Select Highest Level of Education', options=outbound["education"].unique())
    selected_marital = st.selectbox('Select Marital Status', options=outbound["marital_status"].unique())

    df_in_selected = inbound[(inbound["sex"] == selected_sex) & (inbound["age_group"] == selected_age) & (inbound["education"] == selected_education) & (inbound["marital_status"] == selected_marital)]
    df_in_selected_sorted = df_in_selected.sort_values(by="count", ascending=False)

    df_out_selected = outbound[(outbound["sex"] == selected_sex) & (outbound["age_group"] == selected_age) & (outbound["education"] == selected_education) & (outbound["marital_status"] == selected_marital)]
    df_out_selected_sorted = df_out_selected.sort_values(by="count", ascending=False)


#######################
# Plots

# Choropleth map
def make_choropleth(input_df, input_id, input_column):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale="reds",
                               scope="usa",
                               labels={'count':'Count'}
                              )
    return choropleth


#######################
# Dashboard Main Panel
col = st.columns((4.5, 2), gap='medium')


with col[0]:
    st.markdown('#### Count of Inbound Movers by Select Characteristics')
    
    choropleth = make_choropleth(df_in_selected, 'current_state_code', 'count')
    st.plotly_chart(choropleth, use_container_width=True)

    st.markdown('#### Count of Outbound Movers by Select Characteristics')
    
    choropleth = make_choropleth(df_out_selected, 'previous_state_code', 'count')
    st.plotly_chart(choropleth, use_container_width=True)


with col[1]:
    st.markdown('#### Top Inbound States')

    st.dataframe(df_in_selected_sorted,
                 column_order=("current_state", "count"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "current_state": st.column_config.TextColumn(
                        "Inbound State",
                    ),
                    "count": st.column_config.ProgressColumn(
                        "Count",
                        format="%f"
                     )}
                 )
    
    st.markdown('#### Top Outbound States')

    st.dataframe(df_out_selected_sorted,
                 column_order=("previous_state", "count"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "previous_state": st.column_config.TextColumn(
                        "Outbound State",
                    ),
                    "count": st.column_config.ProgressColumn(
                        "Count",
                        format="%f"
                     )}
                 )
    
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [U.S. Census Bureau](<https://www.census.gov/programs-surveys/acs/microdata/access.html>).
            - :orange[**Note Title**]: insert note
            - :orange[**Note Title**]: insert note
            ''')