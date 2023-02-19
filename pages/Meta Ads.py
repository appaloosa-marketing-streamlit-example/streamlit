"""
# My first app
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

#SECRETS
meta_conversions_monthly = st.secrets["META_CONVERSIONS_MONTHLY"]
meta_conversions_mtd = st.secrets["META_CONVERSIONS_MTD"]
meta_actions_mtd = st.secrets["META_ACTIONS_MTD"]
compare_df = st.secrets["COMPARE_META"]
last_month_df = st.secrets["LAST_MONTH_META"]

#DATA
meta_conversions_monthly = pd.read_csv(meta_conversions_monthly)
meta_conversions_monthly = meta_conversions_monthly.groupby(by="Month").sum().reset_index()
meta_conversions_mtd = pd.read_csv(meta_conversions_mtd)
meta_actions_mtd = pd.read_csv(meta_actions_mtd)
compare_df = pd.read_csv(compare_df)
last_month_df = pd.read_csv(last_month_df)

st.title('Meta Ads')
st.markdown('Performance Metrics from Meta. Please remember that Meta tracking does not work on IOS. Revenue will always be under-reported.')


from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
# Create figure with secondary y-axis
df = meta_conversions_monthly
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.update_layout(template="plotly_white")

# Add traces


fig.add_trace(
    go.Scatter(x=df['Month'], y=df['Revenue'], name="Revenue"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=df['Month'], y=df['Spend'], name="Spend"),
    secondary_y=True,
)
# Add figure title
fig.update_layout(
    title_text="<b>Revenue & Spend Over Time</b>",
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

if st.checkbox('⬅ Click there for the data as a table'):
    colored_header(
        label="Conversions by Month",
        description="Spend & Revenue Over Time",
        color_name="green-70",
    )
    st.table(meta_conversions_monthly.style.set_precision(2))



# CSS to hide df indicies & tables
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)



colored_header(
    label="MTD Report",
    description="Month to Date Metrics.",
    color_name="blue-60",
)


def color_coding(row):
    return ['background-color: #fffdaf'] * len(
        row) if row.Adset == "TOTAL" else ['background-color:white'] * len(row)

st.table(meta_conversions_mtd.style.apply(color_coding, axis=1).set_precision(2))
#st.table(meta_conversions_mtd)


if st.checkbox('⬅ Click there for all tracked actions & engagement'):
    # Actions
    colored_header(
        label="Actions",
        description="All tracked actions.",
        color_name="violet-70",
    )

    st.table(meta_actions_mtd.style.set_precision(0))

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

    last_month_cost = last_month_df.query("Adset == 'TOTAL'")['Spend'].values[0].round(2)
    last_month_purchases = last_month_df.query("Adset == 'TOTAL'")['Purchases'].values[0].round(0)
    last_month_revenue = last_month_df.query("Adset == 'TOTAL'")['Revenue'].values[0].round(2)
    last_month_roas = last_month_df.query("Adset == 'TOTAL'")['ROAS'].values[0].round(2)


    compared_cost = compare_df['Cost'].astype(float).sum().round(2)
    compared_purchases = compare_df['Purchases'].astype(float).sum().round(2)
    compared_revenue = compare_df['Revenue'].astype(float).sum().round(2)
    compared_roas = compare_df['ROAS'].astype(float).sum().round(2)

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

    compared_cost = compare_df['Cost'].astype(float).sum().round(2)
    compared_clicks = compare_df['Clicks'].astype(float).sum().round(0)

    with col1:
        st.metric(label="Last Month Spend", value=f'${last_month_cost}', delta=compared_cost)
    with col2:
        st.metric(label="Last Month Purchases", value=last_month_clicks, delta=compared_clicks)




st.subheader('Last Month')
st.table(last_month_df.style.apply(color_coding, axis=1).set_precision(2))