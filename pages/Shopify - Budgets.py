import pandas as pd
import streamlit as st
from streamlit_extras.colored_header import colored_header

#SECRETS
meta_budgets = st.secrets["META_BUDGETS"]
google_budgets = st.secrets["GOOGLE_BUDGETS"]

#DATA
meta_budgets = pd.read_csv(meta_budgets)
google_budgets = pd.read_csv(google_budgets)


# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)


st.title('Shopify Budget Report')
st.markdown('Total Daily Budget and Spend Month to Date.')

#Remove campaigns including 'Amazon'
#meta_budgets = meta_budgets.query("Campaign != 'Amazon'")
#meta_budgets.fillna(" ",inplace=True)

#Get only Total rows of each df, then combine them into a df
# google_budgets.fillna(" ",inplace=True)
# google_total = google_budgets.loc[google_budgets['Campaign'] == 'TOTAL']
# google_total.replace('TOTAL', 'Google', inplace=True)
#
# meta_total = meta_budgets.loc[meta_budgets['Campaign'] == 'TOTAL']
# meta_total.replace('TOTAL', 'Meta', inplace=True)
#
#
# total_budgets = pd.concat([google_total, meta_total], ignore_index= True)
# total_budgets.rename(columns={'Campaign': 'Channel'}, inplace=True)
# total_budgets.drop(columns='Status', inplace=True)
# total_totals = total_budgets.sum(axis=0)
# total_budgets.loc['TOTAL'] = total_totals
# total_budgets.replace('GoogleMeta', 'TOTAL', inplace=True)

#st.table(total_budgets)

colored_header(
    label="Google Budgets",
    description="Current Google Ads Campaigns",
    color_name="yellow-80",
)
def color_coding(row):
    return ['background-color: #fffdaf'] * len(
        row) if row.Campaign == "TOTAL" else ['background-color:white'] * len(row)

st.table(google_budgets.style.apply(color_coding, axis=1).format(precision=2))

colored_header(
    label="Meta Budgets",
    description="Current Meta Campaigns",
    color_name="blue-60",
)

#Replace n.a with blanks, then create table


st.table(meta_budgets.style.apply(color_coding, axis=1).format(precision=2))