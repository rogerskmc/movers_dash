#######################
# DSTP Cohort 6 Capstone Team A23 Movers Dashboard - Streamlit
# 2023 ACS PUMS 1-Yr Data
# Kathleen created 5/30/25
# Last edited 6/13/25

# After running the following code in a .py file, you will see some warning/thread messages. You can disregard them. There will also be a message saying...
# "Warning: to view this Streamlit app on a browser, run it with the following command: streamlit run file_location/file_name.py [ARGUMENTS]"
# Copy and paste that command into your Terminal application to run the dashboard app locally.

# View the public dashboard created using the following code here: https://a3moversdash.streamlit.app/

#######################
# Import libraries
import streamlit as st # provides the web app framework
import pandas as pd # for data manipulation
import plotly.express as px # for choropleth maps

#######################
# Page configuration
st.set_page_config(
    page_title="DSTP 2025 Team A3 Movers Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

#######################
# Load data
inbound = pd.read_csv('inbound.csv')
outbound = pd.read_csv('outbound.csv')

#######################
# Sidebar
with st.sidebar:
    st.title("DSTP '25 Capstone Team A3 Movers Dashboard")
    
    # Create drop-down menus for filtering data
    # Choose just inbound or just outbound, if you only want one set of drop-downs to filter both datasets simultaneously
    sex_list = list(outbound.sex.unique())
    age_list = list(outbound.age_group.unique())
    education_list = list(outbound.education.unique())
    marital_list = list(outbound.marital_status.unique())
    
    # Establish possible values for each drop-down
    selected_sex = st.selectbox('Select Sex', options=outbound["sex"].unique())
    selected_age = st.selectbox('Select Age Group', options=outbound["age_group"].unique())
    selected_education = st.selectbox('Select Highest Level of Education', options=outbound["education"].unique())
    selected_marital = st.selectbox('Select Marital Status', options=outbound["marital_status"].unique())

    # Define how to filter the inbound and outbound datasets based on the drop-down selections
    df_in_selected = inbound[(inbound["sex"] == selected_sex) & (inbound["age_group"] == selected_age) & (inbound["education"] == selected_education) & (inbound["marital_status"] == selected_marital)]
    df_in_selected_sorted = df_in_selected.sort_values(by="count", ascending=False)

    df_out_selected = outbound[(outbound["sex"] == selected_sex) & (outbound["age_group"] == selected_age) & (outbound["education"] == selected_education) & (outbound["marital_status"] == selected_marital)]
    df_out_selected_sorted = df_out_selected.sort_values(by="count", ascending=False)

#######################
# Plots

# Choropleth map configuration
def make_choropleth(input_df, input_id, input_column):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale="reds",
                               scope="usa",
                               labels={'count':'Count'}
                              )
    return choropleth

#######################
# Dashboard Main Panel
col = st.columns((4, 2.5), gap='medium') # 2 columns with a 4:2.5 ratio

# First column: choropleth maps showing counts of inbound and outbound movers by state
with col[0]:
    st.markdown('#### Count of Inbound Movers by Select Characteristics')
    
    choropleth = make_choropleth(df_in_selected, 'current_state_code', 'count')
    st.plotly_chart(choropleth, use_container_width=True)

    st.markdown('#### Count of Outbound Movers by Select Characteristics')
    
    choropleth = make_choropleth(df_out_selected, 'previous_state_code', 'count')
    st.plotly_chart(choropleth, use_container_width=True)

# Second column: Sorted bar charts showing inbound and outbound mover counts by state
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
                        format="compact"
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
                        format="compact"
                     )}
                 )
    
    # Footer with additional information
    with st.expander('About', expanded=True):
        st.write('''
            - :orange[**Data**]: [U.S. Census Bureau. American Community Survey Public Use Microdata Sample (PUMS) 1-Year, 2023. Accessed via the ACS API.](<https://www.census.gov/programs-surveys/acs/microdata/access.html>)
            - :orange[**Note**]: The inbound and outbound components above are independent of each other. Migration flows are not visualized in this dashboard.
            - :orange[**Disclaimer**]: The data presented in this dashboard is for educational purposes only and should not be used for decision-making without further analysis.
            - :orange[**Questions? Suggestions?**] contact DSTP Cohort 6 Capstone Team A3 member, Kathleen Rogers (EWD)
            ''')