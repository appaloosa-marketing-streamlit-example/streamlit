import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from streamlit_extras.colored_header import colored_header

#AMAZON
sellercentral_monthly = st.secrets["AMAZON_SALES_MONTHLY"]
sellercentral_mtd = st.secrets["AMAZON_SALES_MTD"]
amazonads_mtd = st.secrets["AMAZON_ADS_MTD"]
amazon_meta_budgets = st.secrets["AMAZON_META_BUDGETS"]

# SHOPIFY
shopify_report = st.secrets["SHOPIFY_REPORT_MTD"]

#META
meta_conversions_mtd = st.secrets["META_CONVERSIONS_MTD"]
last_month_meta_df = st.secrets["LAST_MONTH_META"]

#GOOGLE
google_conversions_mtd = st.secrets["GOOGLE_CONVERSIONS_MTD"]



#DATA
try:
    sellercentral_monthly = pd.read_csv(sellercentral_monthly)
except:
    print('sellercentral_monthly df is empty.')

try:
    meta_conversions_mtd = pd.read_csv(meta_conversions_mtd)

except:
    print('meta_conversions_mtd is empty or does not exist')


sellercentral_mtd = pd.read_csv(sellercentral_mtd)
amazonads_mtd = pd.read_csv(amazonads_mtd)

last_month_meta_df = pd.read_csv(last_month_meta_df)

google_conversions_mtd = pd.read_csv(google_conversions_mtd)


amazon_meta_budgets = pd.read_csv(amazon_meta_budgets)


shopify_report = pd.read_csv(shopify_report)

## STYLING
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)


def color_coding(row):
    return ['background-color: #fffdaf'] * len(
        row) if row.Channel == "TOTAL" else ['background-color:white'] * len(row)



st.title('Executive Summary')
# st.markdown('Quick Performance Metrics')



colored_header(
    label="Sales This Month (MTD)",
    description="Amazon and Shopify",
    color_name="green-70",
)

# AMAZON SALES #
sellercentral_mtd['Platform'] = 'Amazon'
sellercentral_mtd.rename(columns={"unitCount":"Units Ordered","orderCount":"Orders","Total Sales":"Revenue"}, inplace=True)
sellercentral_mtd.drop(columns={"month"}, inplace=True)
sellercentral_mtd = sellercentral_mtd[['Platform', 'Revenue', 'Orders', 'Units Ordered', 'Avg. Unit Price']]
#st.table(sellercentral_mtd.style.set_precision(2))

# SHOPIFY #
total_revenue = shopify_report['totalPrice'].astype(float).sum()
total_tax = shopify_report['totalTax'].astype(float).sum()
total_refund = shopify_report['totalRefunded'].astype(float).sum()
total_revenue_adjusted = total_revenue - total_tax - total_refund

data = {'Platform': ['Shopify'], 'Revenue': [total_revenue_adjusted]}
shopify_mtd = pd.DataFrame(data)

mtd_sales = pd.concat([sellercentral_mtd, shopify_mtd], axis=0).fillna('')

st.table(mtd_sales.style.set_precision(2))

# ADVERTISING #
colored_header(
    label="Advertising This Month (MTD)",
    description="Performance This Month",
    color_name="blue-70",
)

# AMAZON ADS #
amazonads_mtd.rename(columns={'Campaign': 'Channel', 'Sales':'Revenue'}, inplace=True)
amazonads_mtd_total = amazonads_mtd[['Channel', 'Cost', 'Revenue', 'Purchases']]
amazonads_mtd_total = (amazonads_mtd_total.iloc[-1:]).replace('TOTAL', 'Amazon Ads')
amazonads_mtd_total['ROAS'] = amazonads_mtd_total['Revenue']/amazonads_mtd_total['Cost']
#amazonads_mtd_total = amazonads_mtd_total.reset_index().
#st.table(amazonads_mtd_total.style.set_precision(2))

# FB ADS - Ammazon #
amazon_meta_budgets = amazon_meta_budgets[['Spent', 'Campaign']]

# Create the new columns with values set to 0
for column_name in ['Purchases', 'Revenue', 'ROAS']:
    amazon_meta_budgets[column_name] = 0

# Reorder the columns
amazon_meta_budgets = amazon_meta_budgets[['Campaign', 'Spent', 'Revenue', 'Purchases','ROAS']]

# Change TOTAL row
amazon_meta_budgets = (amazon_meta_budgets.iloc[-1:]).replace('TOTAL', 'Amazon - FB Ads')
amazon_meta_budgets.rename(columns={"Spent":"Cost", 'Campaign':'Channel'}, inplace=True)

#st.table(amazon_meta_budgets.style.set_precision(2))



# FB ADS #
try:
    meta_conversions_mtd.fillna('', inplace=True)
    #st.table(meta_conversions_mtd.style.apply(axis=1).set_precision(2))
except:
    pass

try:
    meta_conversions_mtd = meta_conversions_mtd[meta_conversions_mtd['Adset'].str.contains('TOTAL')]
    meta_conversions_mtd.rename(columns={'Adset': 'Channel', 'Spend':'Cost'}, inplace=True)
    meta_conversions_mtd = meta_conversions_mtd[['Channel', 'Cost', 'Revenue', 'Purchases', 'ROAS']]

    meta_conversions_mtd = (meta_conversions_mtd.iloc[-1:]).replace('TOTAL', 'Shopify - Meta Ads')
except:
    print('No data for meta_conversions_mtd.')

#st.table(meta_conversions_mtd.style.set_precision(2))


# GOOGLE
google_conversions_mtd = google_conversions_mtd[google_conversions_mtd['Campaign'].str.contains('TOTAL')]

if 'Revenue' in google_conversions_mtd.columns and (google_conversions_mtd['Revenue'] > 0).any():
    try:
        google_conversions_mtd = google_conversions_mtd.iloc[-1:].replace('TOTAL', 'Shopify - Google Ads')
        google_conversions_mtd = google_conversions_mtd.rename(columns={'Campaign': 'Channel'})
    #     st.table(google_conversions_mtd.style.apply(axis=1).set_precision(2))
    #
    except:
        print('No purchase data or something is broken.')
    pass
else:
    # If there's no purchase data, create empty purchase metric columns & set val = 0
    for column_name in ['Purchases', 'Revenue', 'ROAS']:
        if column_name not in google_conversions_mtd.columns:
            google_conversions_mtd[column_name] = 0
    try:
        google_conversions_mtd = google_conversions_mtd.iloc[-1:].replace('TOTAL', 'Shopify - Google Ads')
        google_conversions_mtd = google_conversions_mtd.drop(columns=['Clicks', 'Impressions'])
        google_conversions_mtd = google_conversions_mtd.rename(columns={'Campaign': 'Channel'})
        #st.table(google_conversions_mtd.style.set_precision(2))
    except:
        'Something wrong (Line 92)'

try:
    combined_df = pd.concat([amazonads_mtd_total, amazon_meta_budgets, meta_conversions_mtd, google_conversions_mtd], axis=0, ignore_index=True)
    combined_df = combined_df.drop(columns=['Clicks', 'Impressions'])
except:
    combined_df = pd.concat([amazonads_mtd_total, amazon_meta_budgets, google_conversions_mtd], axis=0, ignore_index=True)
    combined_df = combined_df.drop(columns=['Clicks', 'Impressions'])
# Calculate sums and mean

st.subheader('Amazon')
# select rows where 'Channel' contains 'Amazon'
amazon_df = combined_df[combined_df['Channel'].str.contains('Amazon')]
amazon_df.loc['TOTAL'] = amazon_df.sum(numeric_only=True)
amazon_df.loc['TOTAL', 'ROAS'] = amazon_df['ROAS'].mean()
amazon_df.iloc[-1, amazon_df.columns.get_loc('Channel')] = 'TOTAL'

# Format as currency
amazon_df[['Cost', 'Revenue']] = amazon_df[['Cost', 'Revenue']].applymap(lambda x: f'${x:,.2f}')
st.table(amazon_df.style.apply(color_coding, axis=1).set_precision(2))


st.subheader('Shopify')
# select rows where 'Channel' contains 'Amazon'
shopify_df = combined_df[combined_df['Channel'].str.contains('Shopify')]
shopify_df.loc['TOTAL'] = shopify_df.sum(numeric_only=True)
shopify_df.loc['TOTAL', 'ROAS'] = shopify_df['ROAS'].mean()
shopify_df.iloc[-1, shopify_df.columns.get_loc('Channel')] = 'TOTAL'

# Format as currency
shopify_df[['Cost', 'Revenue']] = shopify_df[['Cost', 'Revenue']].applymap(lambda x: f'${x:,.2f}')
st.table(shopify_df.style.apply(color_coding, axis=1).set_precision(2))

