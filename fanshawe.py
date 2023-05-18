import numpy
import streamlit as st
import pandas as pd
import plotly.express as px
import pdb as pdb

# Define the UI
def app():
####################       Setup        #############################    
    # Set the tcp itle of the application
    st.title("Fanshawe Analytics")    
    # Load the data into a DataFrame
    df = pd.read_csv("AprilMayAllocsTurndowns.csv")   
    # Rename the column names
    df.columns = ['ckid', 'resource', 'rtype', 'status', 'startdatetime', 'endatatime', 'otherdatetime']
    # Convert the date string to datetime object
    df['converted_startdatetime'] = pd.to_datetime(df['startdatetime'], format="%m/%d/%Y %H:%M %p")
    tddf = pd.read_csv("Turndowns.csv")
    tddf.columns = ['rtype', 'ttime', 'cocenter'];
    tddf['converted_startdatetime'] = pd.to_datetime(tddf['ttime'], format="%m/%d/%Y %H:%M")

#####################     End Setup      #############################

#####################  Resource by DOW  #############################
    # Create a new column 'dow' to store the day of week
    df['dow'] = df['converted_startdatetime'].dt.day_name()
    # Get the unique resources
    resources = df['resource'].unique().tolist()
    # Create the selectbox for resources
    selected_resources = st.selectbox("Select Resources:", resources)
    # Filter the data for the selected resource
    resource_data = df[df['resource'] == selected_resources]
    # Create a new DataFrame to store the counts of reservations by day of week
    dow_data = resource_data.groupby(['dow', 'status']).size().reset_index(name='counts')
    # Reorder the days of week
    dow_data['dow'] = pd.Categorical(dow_data['dow'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    empty_data = {'dow': ['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
         'status': ['CHECKOUT-COMPLETED','CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED' ],
         'counts': [0, 0, 0, 0, 0, 0,0]}
    emptyDF = pd.DataFrame(empty_data)
    dow_data = pd.merge(dow_data, emptyDF, on=['dow', 'status', 'counts'], how='outer')

    fig = px.bar(dow_data, x='dow', y='counts', title='Reservation Start Time by Day of Week', barmode='group', color='status')
    fig.update_xaxes(title='Day of Week', categoryorder='array', categoryarray=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    fig.update_xaxes(type ='category')
    fig.update_layout(yaxis = dict(tickmode='linear', tickformat=",d"), title=dict(font=dict(size=24)))
    fig.update_layout(title={'x':0.5, 'xanchor':'center'})
    fig.update_yaxes(title='Number of Checkouts')
    # Render the chart
    st.plotly_chart(fig)
#####################  End Resources by DOW  #############################

#####################  Resources by TOD  #############################

#    df['startHour'] = df['startdatetime'].dt.hour.head()
 #   df['hourStr'] = df['startHour'].to_string()
    df['hour_str'] = df['converted_startdatetime'].dt.strftime('%H')+":00"

    selectedr_data = df[df['resource'] == selected_resources]
    # Create a new DataFrame to store the counts of reservations by day of week                                                                      
    tod_data = selectedr_data.groupby(['hour_str', 'status']).size().reset_index(name='counts')

    empty_tod_data = {'hour_str': ['01:00','02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
         'status': ['CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED','CHECKOUT-COMPLETED','CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED' ],
         'counts': [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}

    empty_todDF = pd.DataFrame(empty_tod_data)
    tod_data = pd.merge(tod_data, empty_todDF, on=['hour_str', 'status', 'counts'], how = "outer")


#    fig_tod_resource = px.bar(tod_data, x='hour_str', y='counts', width=600, height=600, title='Completed Reservations by Start Time', barmode='group', color='status')
    fig_tod_resource = px.bar(tod_data, x='hour_str', y='counts', title='Completed Reservations by Start Time', barmode='group', color='status')
    fig_tod_resource.update_xaxes(type='category') 
    fig_tod_resource.update_xaxes(categoryorder='array', categoryarray=["1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]) 
    fig_tod_resource.update_yaxes(title='Number of Checkouts')
    fig_tod_resource.update_layout(barmode='group', bargap=0.25, bargroupgap=0.1)
    # Render the chart                                                                                         
    fig_tod_resource.update_layout(yaxis = dict(tickmode='linear', tickformat=",d"), title=dict(font=dict(size=24)))
    fig_tod_resource.update_layout(title={'x':0.5, 'xanchor':'center'})

    st.plotly_chart(fig_tod_resource)
    
#####################  End Resources by TOD  #############################

#########################  Rtype of DOW  #################################

    rtypes = df['rtype'].unique().tolist()
    # Create the selectbox for resources                                                                                                                                            
    selected_rtypes = st.selectbox("Select Types:", rtypes)
    # Filter the data for the selected resource                                                                                                                                     
    rtype_data = df[df['rtype'] == selected_rtypes]
    # Create a new DataFrame to store the counts of reservations by day of week                                                                                                     
    dow_rtype_data = rtype_data.groupby(['dow', 'status']).size().reset_index(name='counts')
    # Reorder the days of week
    #dow_rtype_data['dow'] = pd.Categorical(dow_rtype_data['dow'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    empty_rtype_data = {'dow': ['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                                               'status': ['CHECKOUT-COMPLETED','CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED'],
                                               'counts': [0, 0, 0, 0, 0, 0,0]}
    empty_rtypeDF = pd.DataFrame(empty_rtype_data)
    dow_rtype_data = pd.merge(dow_rtype_data, empty_rtypeDF, on=['dow', 'status', 'counts'], how='outer')
    dow_rtype_data = dow_rtype_data.sort_values('dow')
    # Create the bar chart
    fig_rtype = px.bar(dow_rtype_data, x='dow', y='counts', title='Usage by Resource Type', barmode='group', color='status')
    fig_rtype.update_xaxes(title='Start Time', tickmode="array", ticktext=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    fig_rtype.update_yaxes(title='Number of Checkouts')
    fig_rtype.update_layout(yaxis = dict(tickmode='linear', tickformat=",d"), title=dict(font=dict(size=24)))
    fig_rtype.update_layout(title={'x':0.5, 'xanchor':'center'})
    st.plotly_chart(fig_rtype)
################################ RTYPES DOW ##################################


#####################  Resources by TOD  #############################                                                                                                  
#    df['startHour'] = df['startdatetime'].dt.hour.head()                                                                                                               
 #   df['hourStr'] = df['startHour'].to_string()                                                                                                                        
    df['hour__rtype_str'] = df['converted_startdatetime'].dt.strftime('%H')+":00"
    selected_type_data = df[df['rtype'] == selected_rtypes]
    # Create a new DataFrame to store the counts of reservations by day of week                                                                                         
    tod_rtype_data = selected_type_data.groupby(['hour_str', 'status']).size().reset_index(name='counts')

    empty_tod_data = {'hour_str': ['1:00','2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
         'status': ['CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED','CHECKOUT-COMPLETED','CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 'CHECKOUT-COMPLETED', 
'CHECKOUT-COMPLETED' ],
         'counts': [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}

    empty_todDF = pd.DataFrame(empty_tod_data)
    tod_rtype_data = pd.merge(tod_rtype_data, empty_todDF, on=['hour_str', 'status', 'counts'], how = "outer")
#    fig_tod_resource = px.bar(tod_data, x='hour_str', y='counts', width=600, height=600, title='Completed Reservations by Start Time', barmode='group', color='status'\
                                                                                                                                                                       
    fig_tod_rtype = px.bar(tod_rtype_data, x='hour_str', y='counts', title='Completed Reservations by Start Time', barmode='group', color='status')

    fig_tod_rtype.update_yaxes(title='Number of Checkouts')
    fig_tod_rtype.update_layout(barmode='group', bargap=0.25, bargroupgap=0.1)
    fig_tod_rtype.update_layout(yaxis = dict(tickmode='linear', tickformat=",d"), title=dict(font=dict(size=24)))
    fig_tod_rtype.update_layout(title={'x':0.5, 'xanchor':'center'})
    st.plotly_chart(fig_tod_rtype)

#########################  End TOD RType ##########################

#########################  Start Turndown  ########################

    turndown_data = tddf.groupby(['rtype']).size().reset_index(name='counts')

    fig_turndowns = px.bar(turndown_data, x='rtype', y='counts', title='Turndown Report')

    fig_turndowns.update_layout(yaxis = dict(tickmode='linear', tickformat=",d"), title=dict(font=dict(size=24)))
    fig_turndowns.update_layout(title={'x':0.5, 'xanchor':'center'})
    st.plotly_chart(fig_turndowns)



    
    
# Run the application
if __name__ == "__main__":
    app()


    
