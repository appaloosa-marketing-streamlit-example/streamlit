"""
ROAS by Channel
"""

import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header

#SECRETS
meta_conversions_mtd = st.secrets["META_CONVERSIONS_MTD"]
google_conversions_mtd = st.secrets["GOOGLE_CONVERSIONS_MTD"]


#DATA
meta_conversions_mtd = pd.read_csv(meta_conversions_mtd)
google_conversions_mtd = pd.read_csv(google_conversions_mtd)

#PROCESSING
# for ROAS Table
meta_total_row = meta_conversions_mtd.loc[meta_conversions_mtd.eq('TOTAL').any(1)].replace('TOTAL', 'Meta')
meta_total_row.rename(columns={'Adset':'Channel'}, inplace=True)
meta_total_row = meta_total_row[['Channel','ROAS']]

google_total_row = google_conversions_mtd.loc[google_conversions_mtd.eq('TOTAL').any(1)].replace('TOTAL','Google')
google_total_row.rename(columns={'Campaign':'Channel'}, inplace=True)
google_total_row = google_total_row[['Channel','ROAS']]

total_rows = pd.concat([meta_total_row,google_total_row])

# for graph
meta_total_splice = meta_conversions_mtd.copy()
meta_total_splice = meta_total_splice.loc[meta_total_splice.eq('TOTAL').any(1)].replace('TOTAL','Meta')
meta_total_splice = meta_total_splice[['Revenue', 'Spend','Adset']]
meta_total_splice.rename(columns={'Adset':'Channel'}, inplace=True)

google_total_splice = google_conversions_mtd.copy()
google_total_splice = google_total_splice.loc[google_total_splice.eq('TOTAL').any(1)].replace('TOTAL','Google')
google_total_splice = google_total_splice[['Revenue', 'Cost','Campaign']]
google_total_splice.rename(columns={'Cost':'Spend','Campaign':'Channel'}, inplace=True)

splice_df = pd.concat([meta_total_splice,google_total_splice])

# for bottom tables
meta_bottom = meta_conversions_mtd.copy()
meta_bottom = meta_bottom[['Adset','Revenue','Spend']]

google_bottom = google_conversions_mtd.copy()
google_bottom = google_bottom[['Campaign','Revenue','Cost']].rename(columns={'Cost':'Spend'})

#Title
st.title('Tracked ROAS MTD')
st.markdown('Revenue tracked by pixels this month. Note: FB cannot track conversions from Apple/IOS. '
            'For Total Ad Spend vs. Sales, see Shopify/Amazon Performance.')


st.header('ROAS by Channel')
st.table(total_rows.style.set_precision(2))

#Column Layout & other neat features.
colored_header(
    label="Spend & Revenue",
    description="Compare spend vs revenue by channel.",
    color_name="blue-60",
)

import plotly.graph_objects as go

fig = go.Figure(data=[
    go.Bar(name='Spend', x=splice_df['Channel'], y=splice_df['Spend']),
    go.Bar(name='Revenue', x=splice_df['Channel'], y=splice_df['Revenue'])
])
# Change the bar mode
fig.update_layout(barmode='group')
st.plotly_chart(fig)

col1, col2 = st.columns(2)

def color_coding(row):
    return ['background-color: #fffdaf'] * len(
        row) if row.Campaign == "TOTAL" else ['background-color:white'] * len(row)

def color_coding2(row):
    return ['background-color: #fffdaf'] * len(
        row) if row.Adset == "TOTAL" else ['background-color:white'] * len(row)

col1.subheader('Google')
col1.table(google_bottom.style.apply(color_coding, axis=1).set_precision(2))

col2.subheader('Meta')
col2.table(meta_bottom.style.apply(color_coding2, axis=1).set_precision(2))



