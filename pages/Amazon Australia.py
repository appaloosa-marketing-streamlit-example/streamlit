"""
# Amazon Australia
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from streamlit_extras.colored_header import colored_header


#SECRETS
sellercentral_monthly = st.secrets["AMAZON_SALES_MONTHLY_AU"]
sellercentral_mtd = st.secrets["AMAZON_SALES_MTD_AU"]
amazonads_mtd = st.secrets["AMAZON_ADS_AU_MTD"]
last_month_df = st.secrets["AMAZON_ADS_AU_LAST_MONTH"]
compare_df = st.secrets["AMAZON_AU_COMPARE"]
budgets = st.secrets["AMAZON_AU_BUDGETS"]
amazon_meta_monthly = st.secrets["AMAZON_AU_META_MONTHLY"]
amazon_meta_budgets = st.secrets["AMAZON_AU_META_BUDGETS"]

#DATA
sellercentral_monthly = pd.read_csv(sellercentral_monthly)
sellercentral_mtd = pd.read_csv(sellercentral_mtd)
amazonads_mtd = pd.read_csv(amazonads_mtd)
budgets = pd.read_csv(budgets)
last_month_df = pd.read_csv(last_month_df)
compare_df = pd.read_csv(compare_df)
amazon_meta_monthly = pd.read_csv(amazon_meta_monthly)
amazon_meta_budgets = pd.read_csv(amazon_meta_budgets)

# PROCESSING
amazonads_mtd.drop(columns={'startDate','endDate'}, inplace=True)
amazon_meta_monthly = amazon_meta_monthly.groupby(by="Month").sum().reset_index()

#Get only Total rows of each df, then combine them into a df
amazon_meta_budgets.rename(columns={'Spent':'Cost'}, inplace=True)
budgets.fillna(" ",inplace=True)
amazon_total = budgets.loc[budgets['Campaign'] == 'TOTAL']
amazon_total.replace('TOTAL', 'Amazon', inplace=True)

meta_total = amazon_meta_budgets.loc[amazon_meta_budgets['Campaign'] == 'TOTAL']
meta_total.replace('TOTAL', 'Meta', inplace=True)


total_budgets = pd.concat([amazon_total, meta_total], ignore_index= True)
total_budgets.rename(columns={'Campaign': 'Channel'}, inplace=True)
total_budgets.drop(columns='Status', inplace=True)
total_totals = total_budgets.sum(axis=0)
total_budgets.loc['TOTAL'] = total_totals
total_budgets.replace('AmazonMeta', 'TOTAL', inplace=True)




def color_coding2(row):
    return ['background-color: #fffdaf'] * len(
        row) if row.Channel == "TOTAL" else ['background-color:white'] * len(row)



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



st.title('Amazon Australia 🇦🇺')



df = sellercentral_monthly




# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.update_layout(template="plotly_white")

# Add traces


fig.add_trace(
    go.Scatter(x=df['month'], y=df['Total Sales'], name="Sales"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=amazon_meta_monthly['Month'], y=amazon_meta_monthly['Spend'], name="FB Spend"),
    secondary_y=True,
)
# Add figure title
fig.update_layout(
    title_text="<b>Revenue vs FB Ad Spend  Over Time</b>"
)

# Set x-axis title
fig.update_xaxes(title_text="<b>Date</b>")

#Get Max value from sales df to dynamically set a range for the graph (so the lines match up)
max_val = df['Total Sales'].max()

# Set y-axes titles
fig.update_yaxes(title_text="<b>Revenue</b>", secondary_y=False, tickformat = '000', separatethousands= True,tickprefix='$',range=[0,max_val])
fig.update_yaxes(title_text="<b>Cost</b>", secondary_y=True, tickformat = '000', separatethousands= True,tickprefix='$', overlaying='y',range=[0,max_val])


fig.data[0].marker.color = ('skyblue')
#fig.data[1].marker.color = ('orange')


st.plotly_chart(fig)
if st.checkbox('⬅ Click there for table of monthly data'):
    st.subheader('Seller Central Sales Over Time')
    sellercentral_monthly
    st.subheader('Meta Spend Over Time')
    amazon_meta_monthly

# Budgets
colored_header(
    label="Budget Caps (AUD, $)",
    description="Current budgets with month-to-date spend. Take note of current spend to approximate if budgets will spend close to their cap.",
    color_name="green-60",
)
st.table(total_budgets.style.apply(color_coding2, axis=1).set_precision(2))


if st.checkbox('⬅ Click for breakdown of budgets'):
    st.subheader('Meta Budgets')
    st.table(amazon_meta_budgets.style.set_precision(2))

    st.subheader('Amazon Ads Budgets')
    st.table(budgets.style.set_precision(2))

# MTD
colored_header(
    label="MTD Performance",
    description="Month to Data Metrics",
    color_name="blue-60",
)

def color_coding(row):
    return ['background-color: #fffdaf'] * len(
        row) if row.Campaign == "TOTAL" else ['background-color:white'] * len(row)

st.subheader('Seller Central MTD')
st.table(sellercentral_mtd.style.set_precision(2))
st.subheader('Amazon Ads MTD')

# MTD TOTAL METRICS
mtd_revenue = amazonads_mtd.iloc[-1, amazonads_mtd.columns.get_loc("Sales")].round(2)
mtd_spend = amazonads_mtd.iloc[-1, amazonads_mtd.columns.get_loc("Cost")].round(2)
mtd_roas = amazonads_mtd.iloc[-1, amazonads_mtd.columns.get_loc("ROAS")].round(2)
mtd_clicks = amazonads_mtd.iloc[-1, amazonads_mtd.columns.get_loc("Clicks")].round(0)


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Revenue",value=f'${mtd_revenue}')

with col2:
    st.metric(label="Spend",value=f'${mtd_spend}')

with col3:
    st.metric(label="ROAS",value=mtd_roas)

with col4:
    st.metric(label="Clicks",value=mtd_clicks)

if st.checkbox('⬅ Click there for more data'):
    st.table(amazonads_mtd.style.apply(color_coding, axis=1).set_precision(2))

#st.dataframe(google_conversions_mtd.style.format(float))

#Comparison
today = datetime.today()
if today.month > 1:
    last_month = datetime(today.year, today.month-1, 1).strftime("%B")
elif today.month == 1:
    last_month = datetime(today.year-1, 12, 1).strftime("%B")


colored_header(
    label=f"{last_month}",
    description=f"{last_month} performance compared to the previous month.",
    color_name="light-blue-70",
)



if 'Sales' in last_month_df.columns:

    col1, col2, col3, col4 = st.columns(4)

    last_month_cost = last_month_df.query("Campaign == 'TOTAL'")['Cost'].values[0].round(2)
    last_month_purchases = last_month_df.query("Campaign == 'TOTAL'")['Purchases'].reset_index()['Purchases'][0]
    last_month_revenue = last_month_df.query("Campaign == 'TOTAL'")['Sales'].values[0].round(2)
    last_month_roas = last_month_df.query("Campaign == 'TOTAL'")['ROAS'].values[0].round(2)


    compared_cost = compare_df['Cost'].astype(float).sum().round(2)
    compared_purchases = compare_df['Purchases'].astype(float).sum().round(2)
    compared_revenue = compare_df['Revenue'].astype(float).sum().round(2)
    compared_roas = compare_df['ROAS'].sum().round(2)
    #compared_clicks = compare_df['Clicks'].astype(float).sum().round(2)

    with col1:
        st.metric(label=f"{last_month} Cost", value=f'${last_month_cost}', delta=compared_cost)
    with col2:
        st.metric(label=f"{last_month} Purchases", value=last_month_purchases, delta=compared_purchases)
    with col3:
        st.metric(label=f"{last_month} Revenue", value=f'${last_month_revenue}', delta=compared_revenue)
    with col4:
        st.metric(label=f"{last_month} ROAS", value=last_month_roas, delta=compared_roas)



else:

    col1, col2 = st.columns(2)

    last_month_cost = last_month_df.query("Campaign == 'TOTAL'")['Cost'].values[0].round(2)
    last_month_clicks = last_month_df.query("Campaign == 'TOTAL'")['Clicks'].values[0].round(0)

    compared_cost = compare_df['Cost'].sum().round(2)
   # compared_clicks = compare_df['Clicks'].sum().round(0)

    with col1:
        st.metric(label=f"{last_month} Cost", value=f'${last_month_cost}', delta=compared_cost)
    with col2:
        st.metric(label=f"{last_month} Purchases", value=last_month_clicks, delta=compared_clicks)



if st.checkbox('⬅ Click there'):
    st.table(last_month_df.style.apply(color_coding, axis=1).set_precision(2))