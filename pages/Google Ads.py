"""
# My first app
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

#SECRETS
shoc_google_conversions_monthly = st.secrets["GOOGLE_CONVERSIONS_MONTHLY"]
shoc_google_conversions_mtd = st.secrets["GOOGLE_CONVERSIONS_MTD"]
last_month_df = st.secrets["LAST_MONTH_GOOGLE"]
compare_df = st.secrets["COMPARE_GOOGLE"]

#DATA
google_conversions_monthly = pd.read_csv(shoc_google_conversions_monthly)
google_conversions_mtd = pd.read_csv(shoc_google_conversions_mtd)
last_month_df = pd.read_csv(last_month_df)
compare_df = pd.read_csv(compare_df)


# #Rounding
# # columns to round to 2 decimal places
# cols_2dp = ['Purchases', 'Revenue', 'Cost']
#
# # columns to round to whole number
# cols_whole = ['Clicks', 'Impressions']
#
# # function to round the values of the columns
# def round_values(col):
#     if col.name in cols_2dp:
#         return round(col, 2)
#     elif col.name in cols_whole:
#         return round(col)
#
# # apply the function to the specified columns
# google_conversions_mtd[cols_2dp + cols_whole] = google_conversions_mtd[cols_2dp + cols_whole].apply(round_values)
#
# # google_conversions_mtd.style.set_precision(2)
# # google_conversions_mtd= google_conversions_mtd.round(2)
#CSS
#— Hide Index from df
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
# Define a styling function that checks if a row contains "TOTAL" in the "Name" column


#st.markdown("Main Page")
#st.sidebar.markdown("Main Page")

st.title('Google Ads')
st.markdown('Performance Metrics')


from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

# colored_header(
#     label="Total Performance over Time",
#     description="Combined performance metrics from all channels.",
#     color_name="blue-60",
# )



df = google_conversions_monthly




# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.update_layout(template="plotly_white")

# Add traces


fig.add_trace(
    go.Scatter(x=df['Month'], y=df['Spend'], name="Spend"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=df['Month'], y=df['Revenue'], name="Revenue"),
    secondary_y=True,
)
# Add figure title
fig.update_layout(
    title_text="<b>Revenue & Spend Over Time</b>"
)

# Set x-axis title
fig.update_xaxes(title_text="<b>Date</b>")

#Get Max value from sales df to dynamically set a range for the graph (so the lines match up)
max_val = df['Revenue'].max()

# Set y-axes titles
fig.update_yaxes(title_text="<b>Revenue</b>", secondary_y=False, tickformat = '000', separatethousands= True,tickprefix='$',range=[0,max_val])
fig.update_yaxes(title_text="<b>Cost</b>", secondary_y=True, tickformat = '000', separatethousands= True,tickprefix='$', overlaying='y',range=[0,max_val])


fig.data[0].marker.color = ('skyblue')
fig.data[1].marker.color = ('orange')


st.plotly_chart(fig)



#Column Layout & other neat features.
colored_header(
    label="MTD Performance",
    description="Month to Data Metrics",
    color_name="blue-60",
)

def color_coding(row):
    return ['background-color: #fffdaf'] * len(
        row) if row.Campaign == "TOTAL" else ['background-color:white'] * len(row)

st.table(google_conversions_mtd.style.apply(color_coding, axis=1).set_precision(2))
#st.dataframe(google_conversions_mtd.style.format(float))

#Comparison
today = datetime.today()
if today.month > 1:
    last_month = datetime(today.year, today.month-1, 1).strftime("%B")
elif today.month == 1:
    last_month = datetime(today.year-1, 12, 1).strftime("%B")


colored_header(
    label=last_month,
    description=f"{last_month} performance compared to the previous month.",
    color_name="light-blue-70",
)


if 'Revenue' in last_month_df.columns:


    col1, col2, col3, col4 = st.columns(4)

    last_month_cost = last_month_df.query("Campaign == 'TOTAL'")['Cost'].reset_index()['Cost'][0].astype(float).round(2)
    last_month_purchases = last_month_df.query("Campaign == 'TOTAL'")['Purchases'].values[0].round(0)
    last_month_revenue = last_month_df.query("Campaign == 'TOTAL'")['Revenue'].values[0].round(2)
    last_month_roas = last_month_df.query("Campaign == 'TOTAL'")['ROAS'].values[0].round(2)


    compared_cost = compare_df['Cost'][0].astype(float)
    compared_purchases = compare_df['Purchases'][0].astype(float)
    compared_revenue = compare_df['Revenue'][0].astype(float)
    compared_roas = compare_df['ROAS'][0]

    with col1:
        st.metric(label="Last Month Spend", value=f'${last_month_cost}', delta=compared_cost)
    with col2:
        st.metric(label="Last Month Purchases", value=last_month_purchases, delta=compared_purchases)
    with col3:
        st.metric(label="Last Month Revenue", value=f'${last_month_revenue}', delta=compared_revenue)
    with col4:
        st.metric(label="Last Month ROAS", value=last_month_roas, delta=compared_roas)



else:

    col1, col2 = st.columns(2)

    last_month_cost = last_month_df.query("Adset == 'TOTAL'")['Spend'].values[0].round(2)
    last_month_clicks = last_month_df.query("Adset == 'TOTAL'")['Clicks'].values[0].round(0)

    compared_cost = compare_df['Cost'].sum().round(2)
    compared_clicks = compare_df['Clicks'].sum().round(0)

    with col1:
        st.metric(label="Last Month Spend", value=f'${last_month_cost}', delta=compared_cost)
    with col2:
        st.metric(label="Last Month Purchases", value=last_month_clicks, delta=compared_clicks)




st.subheader('Last Month')
st.table(last_month_df.style.apply(color_coding, axis=1).set_precision(2))