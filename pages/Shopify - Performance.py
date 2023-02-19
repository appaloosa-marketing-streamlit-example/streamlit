"""
# My first app
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#SECRETS
shopify_report = st.secrets["SHOPIFY_REPORT_MONTHLY"]
google_report = st.secrets["GOOGLE_CONVERSIONS_MONTHLY"]
meta_report = st.secrets["META_CONVERSIONS_MONTHLY"]

#DATA
shopify_report = pd.read_csv(shopify_report)
google_report = pd.read_csv(google_report)
meta_report = pd.read_csv(meta_report)

#PROCESSING
 # Shopify Splice
shopify_report_splice = shopify_report.copy()

shopify_report_splice = shopify_report_splice[['Month', 'Revenue']]

 # Spend dataframe from google & meta splice
google_report_splice = google_report.copy()
google_report_splice = google_report_splice[['Month', 'Spend']]

meta_report_splice = meta_report.copy()
meta_report_splice = meta_report_splice[['Month', 'Spend']]
meta_report_splice = meta_report_splice.groupby(by="Month").sum().reset_index()


spend_df = pd.merge(meta_report_splice,google_report_splice, on='Month')
spend_df['Spend'] = spend_df['Spend_x'] + spend_df['Spend_y']

 #Combined Dataframe for the bottom of the page
spend_df2 = spend_df.copy()
spend_df2.rename(columns={'Spend_x':'Meta', 'Spend_y':'Google', 'Spend':'Total Spend'},inplace=True)
df3 = pd.merge(spend_df2,shopify_report_splice)


 # Splicing spend_df for plotly graph...could have copied dataframe for better organization.
spend_df = spend_df[['Spend', 'Month']]

#st.markdown("Main Page")
#st.sidebar.markdown("Main Page")

st.title('Shopify Performance')
st.markdown('Shopify Revenue vs Total Ad Spend')


from streamlit_extras.colored_header import colored_header



# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.update_layout(template="plotly_white")

# Add traces


fig.add_trace(
    go.Scatter(x=spend_df['Month'], y=spend_df['Spend'], name="Spend"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=shopify_report_splice['Month'], y=shopify_report_splice['Revenue'], name="Revenue"),
    secondary_y=True,
)
# Add figure title
fig.update_layout(
    title_text="<b>Revenue & Spend Over Time</b>"
)

# Set x-axis title
fig.update_xaxes(title_text="<b>Month</b>")

#Get Max value from sales df to dynamically set a range for the graph (so the lines match up)
max_val = shopify_report_splice['Revenue'].max()

# Set y-axes titles
fig.update_yaxes(title_text="<b>Revenue</b>", secondary_y=False, tickformat = '000', separatethousands= True,tickprefix='$',range=[0,max_val])
fig.update_yaxes(title_text="<b>Cost</b>", secondary_y=True, tickformat = '000', separatethousands= True,tickprefix='$', overlaying='y',range=[0,max_val])


fig.data[0].marker.color = ('skyblue')
fig.data[1].marker.color = ('orange')
st.plotly_chart(fig)


st.header('Are ads causing sales?')
from sklearn.linear_model import LinearRegression

# initiate linear regression model
model = LinearRegression()

import numpy as np
# define predictor and response variables
spend_x = np.array(spend_df.Spend)
spend_x = spend_x.reshape(-1, 1)
X, y = spend_x, shopify_report_splice.Revenue


# fit regression model
model.fit(X, y)

# calculate R-squared of regression model
r_squared = round(model.score(X, y), 2)
r_squared_100 = round(r_squared * 100)
if r_squared >= .6:
    correlation = f"is likely to be a significant factor influencing " \
                  f" your sales. "
    yes_or_no = "It looks like it."
    reccomendation = "it makes sense to increase your budget, so long as the sales are profitable.\n\n" \
                     "Try increasing your budget next month to see if profit increases."
    st.balloons()
else:
    correlation = "does not appear to be a significant factor influencing sales.\n\nYou may need more data—especially if you just started running ads." \
                  " If you have sufficient data, consider cutting platforms with low tracked ROAS. \n"
    yes_or_no = "It's difficult to say."
    reccomendation = "it is not recommended to increase your budget, unless you are interested in KPI's " \
                     "other than digital sales.\n\n" \
                     "Reasses low performing channels, check for bottlenecks, consider demand, and investigate competition."

    # view R-squared value
st.markdown(f"{yes_or_no} The correlation between spend and revenue is {r_squared},"
            f" which means advertising {correlation}")

# add_vertical_space(3)

st.subheader('Will increasing spend increase profit?')
st.markdown(f'Based on your performance, {reccomendation}')

#tACOS

tacos_df = df3.copy()
total_revenue = tacos_df['Revenue'].astype(float).sum()
total_spend = tacos_df['Total Spend'].astype(float).sum()
taco = ((total_spend/total_revenue)*100).round(2)
tacos = f"{taco}%"
st.subheader('How do I know if sales are profitable?')
st.markdown('One way to determine if ad sales are profitiable is by using Total Advertising Cost of Sale (tACOS).'
            ' This is your (ad spend ÷ ad revenue) x 100.\n\n'
            f'Your tACOS is {tacos}, which means {tacos} of your revenue is spent on advertising.\n\n '
            f'You need to factor in other costs such as operating, shipping, legal, employees, etc, to'
            f' determine how much you can spend in order for your business to remain profitable. '
            f'This is a question specific to you & your business. ')



hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)






#Column Layout & other neat features.
colored_header(
    label="Spend & Revenue",
    description="Spend & Revenue by Month.",
    color_name="blue-60",
)

st.table(df3)