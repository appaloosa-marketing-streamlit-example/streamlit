"""
# Home!
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#SECRETS
logo = st.secrets['LOGO']


#DATA
col1, col2, col3 = st.columns(3)
with col1:
    st.text("")
with col2:
    st.image(logo)
with col3:
    st.text("")



st.title("Streamlit for Marketing!")

st.write('Use the menu (left-side on desktop, top left > on Mobile) to navigate to different reporting pages.')

st.subheader('The data')
st.write('is all made up. This imaginary company has a peak month in February & runs sucessful Black Friday/Holiday marketing campaigns each year. ')



if st.checkbox('⬅ Click there for an overview on each page.'):

    st.subheader('Amazon')
    st.markdown('• A graph with monthly revenue vs FB Spend + report with more data\n'
                '• Current budget cap and spend MTD for Amazon Ads & Meta Ads\n'
                '• Seller Central performance MTD\n'
                '• Amazon Ads performance MTD + report with more data\n'
                '• Last month\'s Amazon Ads Report + month over month change (from 2 months ago) + report with more data.')

    st.subheader('Google Ads')
    st.markdown('• A graph with tracked revenue & spend from Google Ads\n'
                '• Google Ads performance MTD\n'
                '• Last month\'s Google Ads Report + month over month change (from 2 months ago) + report with more data.')

    st.subheader('Meta Ads')
    st.markdown('• A graph with tracked revenue & spend from Meta Ads\n'
                '• Meta Ads performance MTD + data on all actions from ads MTD\n'
                '• Last month\'s Meta Ads Report + month over month change (from 2 months ago) + report with more data.')

    st.subheader('Shopify - Budgets')
    st.markdown('Budget details for ads running to Shopify.')

    st.subheader('Shopify - Performance')
    st.markdown('• A graph of combined spend from FB & Google vs Shopify Sales\n,'
                '• Analysis of your ad operations, which includes updated total advertising cost of sale (tACOS) & your r squared value of spend vs sales.\n'
                '• A table of the data from the graph')

    st.subheader('Shopify - ROAS by Channel')
    st.markdown('• Your MTD ROAS of Google & FB\n'
                '• A graph of tracked spend vs revenue for Google & FB + a table with that info below.\n')

# st.write(' Warning! Some pages may not be available for your account. Additionally, recommendations may be limited for new accounts.')


st.subheader('Message')
st.write('This dashboard was designed to make it easy for you to find'
             ' your data in one place so you can make decisions fast.\n\n'
             'Made with Python, APIs, and Streamlit.\n\n'
         'Enjoy!\n\n Michael, [Appaloosa Marketing](https://appaloosa-marketing.com)')


if st.checkbox('⬅ Developers, Click there for tips!'):
    st.subheader('Built with AWS')
    st.write('All 22 csv files used to create this dashboard are served using AWS Cloudfront with S3 bucket origins. This was done to avoid running a streamlit dashboard perpetually with EC2, Elastic Beanstalk, Heroku, or something else. While those are viable options, my aim was to spend the least amount of money as humanly possible. 😉')

    st.subheader('Drawbacks')
    st.write('There are serious drawbacks of using a public app & CDN to host the spreadsheets instead of running a perpetual Streamlit App on a private server. \n\n'
             '• The app will turn off if not used which will require the client reboot it\n'
             '• Streamlit may update libraries which can cause issues with dependencies or methods that are deprecated. In other words, your app might break occasionally. ')

    st.subheader('API Access Requirements')
    st.subheader('• Create a Google Ads Manager account & apply for a Google Ads API Developer token\n'
                 '• Create a Facebook Developer account & apply for Marketing API access.\n'
                 '• Create an Amazon Advertising account & apply for Advertising API Access\n'
                 '• Create an Amazon Developer account, read security requirements, & apply for SP-API Access\n'
                 '• Develop a private app on Shopify, get an access token')

    st.subheader('More Recommendations')
    st.subheader('For running real-life streamlit apps for marketing clients, here are some methods I use:\n'
                 '• Invalidate the S3 cache after each upload to ensure fresh data is shown!\n'
                 '• Use Shopify GraphQL API for bulk operations! Saves a lot of time.\n')

