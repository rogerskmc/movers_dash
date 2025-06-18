#######################
# DSTP Cohort 6 Capstone Team A23 Movers Dashboard - Streamlit
# 2023 ACS PUMS 1-Yr Data
# Kathleen created 5/30/25
# Last edited 6/18/25

# After running the following code in a .py file, you will see some warning/thread messages. You can disregard them. There will also be a message saying...
# "Warning: to view this Streamlit app on a browser, run it with the following command: streamlit run file_location/file_name.py [ARGUMENTS]"
# Copy and paste that command into your Terminal application to run the dashboard app locally.

# View the public dashboard created using the following code here: https://a3moversdash.streamlit.app/

#######################
# Import libraries
import streamlit as st # provides the web app framework
import pandas as pd # for data manipulation
import plotly.express as px # for choropleth maps
from itables.streamlit import interactive_table # for tables with sort, copy, and download functionality

#######################
# Page configuration
st.set_page_config(
    page_title="DSTP 2025 Capstone Team A3 Interstate Movers Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

#######################
# Load data
inbound = pd.read_csv('inbound.csv')
outbound = pd.read_csv('outbound.csv')
flows1 = pd.read_csv('flows1.csv')
flows2 = pd.read_csv('flows2.csv')
flows3 = pd.read_csv('flows3.csv')
flows4 = pd.read_csv('flows4.csv')
flows5 = pd.read_csv('flows5.csv')
flows = pd.concat([flows1, flows2, flows3, flows4, flows5])

#######################
# Sidebar
with st.sidebar:
    st.title("DSTP '25 Capstone Team A3 Interstate Movers Dashboard")
    
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

    # Define how to filter all datasets based on the drop-down selections
    df_in_selected = inbound[(inbound["sex"] == selected_sex) & (inbound["age_group"] == selected_age) & (inbound["education"] == selected_education) & (inbound["marital_status"] == selected_marital)]
    df_in_selected_sorted = df_in_selected.sort_values(by="count", ascending=False)

    df_out_selected = outbound[(outbound["sex"] == selected_sex) & (outbound["age_group"] == selected_age) & (outbound["education"] == selected_education) & (outbound["marital_status"] == selected_marital)]
    df_out_selected_sorted = df_out_selected.sort_values(by="count", ascending=False)

    flows_selected = flows[(flows["sex"] == selected_sex) & (flows["age_group"] == selected_age) & (flows["education"] == selected_education) & (flows["marital_status"] == selected_marital)]
    flows_selected_sorted = flows_selected.sort_values(by="count", ascending=False)

#######################
# Plots

# Choropleth map configuration
def make_choropleth(input_df, input_id, input_column, input_color):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color,
                               scope="usa",
                               labels={'count':'Count'}
                              )
    return choropleth

#######################
# Dashboard Main Panel
# If you want rows to line up prcisely, create separate sets of columns

# First set of columns
col = st.columns((4, 2.5), gap='medium') # 2 columns with a 4:2.5 ratio

# First column: choropleth map showing counts of inbound movers by state
with col[0]:
    st.markdown('#### Count of Inbound Movers by Select Characteristics')
    
    choropleth = make_choropleth(df_in_selected, 'current_state_code', 'count', "reds")
    st.plotly_chart(choropleth, use_container_width=True)

# Second column: Sorted bar chart showing inbound mover counts by state
with col[1]:
    st.markdown('#### Destination States Ranked')

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

# Second set of columns        
col2 = st.columns((4, 2.5), gap='medium') # 2 columns with a 4:2.5 ratio

# First column: choropleth map showing counts of outbound movers by state
with col2[0]:
    st.markdown('#### Count of Outbound Movers by Select Characteristics')
    
    choropleth = make_choropleth(df_out_selected, 'previous_state_code', 'count', "reds")
    st.plotly_chart(choropleth, use_container_width=True)

# Second column: Sorted bar chart showing outbound mover counts by state
with col2[1]:
    st.markdown('#### Origin States Ranked')

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

# Third set of columns        
col3 = st.columns((4, 2.5), gap='medium') # 2 columns with a 4:2.5 ratio

# First column: Interactive table with top 10 migration flows
with col3[0]:
    st.markdown('#### Top 10 Interstate Migration Flows by Select Characteristics')

    interactive_table(flows_selected_sorted.head(10),
                  select=True,
                  showIndex=False,
                  labels={'flow':'Flow', 'count':'Count', 'sex':'Sex', 'age_group':'Age', 'education':'Education', 'marital_status':'Marital Status'},
                  buttons=['copyHtml5', 'csvHtml5', 'excelHtml5', 'colvis'])

# Second column: Footer with additional information
with col3[1]:
    with st.expander('About', expanded=True):
        st.write('''
            - :orange[**Data**]: [U.S. Census Bureau. American Community Survey Public Use Microdata Sample (PUMS) 1-Year, 2023. Accessed via the ACS API.](<https://www.census.gov/programs-surveys/acs/microdata/access.html>)
            - :orange[**Note**]: The inbound and outbound components above are independent of each other. Top ten direct migration flows are displayed in the table to the left.
            - :orange[**Disclaimer**]: This dashboard is for educational purposes only and should not be used for decision-making without further analysis.
            - :orange[**Questions? Suggestions?**] contact DSTP Cohort 6 Capstone Team A3 member, Kathleen Rogers (EWD)
            ''')