import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

st.set_page_config(page_title = 'CT2025 - Results', layout = 'wide')

st.markdown(
    """
    <style>
    /* Basic styling for superscript, makes it slightly smaller and positioned correctly */
    sup {
        font-size: 0.75em;
        vertical-align: super;
        line-height: 0;
    }
    </style>
    """, 
    unsafe_allow_html=True
    )

# CACHE DATA
@st.cache_data
def get_data():
    cereal_ts = pd.read_csv("cereal-time-data.csv")
    cereal_ts['grams'] = cereal_ts['grams'].fillna(value = 0).replace(' ', 0)
    cereal_ts['date'] = pd.to_datetime(cereal_ts['date'], format = '%m/%d/%y')
    cereal_ts = cereal_ts.astype({'name':'string', 'grams':'int'})
    cereal_ts['percentage'] = cereal_ts['grams'] / cereal_ts.groupby('name')['grams'].transform('max')
    cereal_ts = cereal_ts.sort_values(by = ['name', 'date']).reset_index(drop = True)
    cereal_ts['gram_lag_1'] = cereal_ts.groupby('name')['grams'].shift(1).fillna(0)
    cereal_ts['gram_change'] = cereal_ts['gram_lag_1'] - cereal_ts['grams']
    cereal_ts['date_lag_1'] = pd.to_datetime(cereal_ts.groupby('name')['date'].shift(1), format = '%m/%d/%y')
    cereal_ts['day_change'] = (cereal_ts['date_lag_1'] - cereal_ts['date']).dt.days
    cereal_ts['change_per_day'] = cereal_ts['gram_change'] / cereal_ts['day_change']
    cereal_ts['change_per_day_zeroed'] = cereal_ts['change_per_day']
    cereal_ts.loc[cereal_ts['change_per_day_zeroed'] > 0, 'change_per_day_zeroed'] = 0
    return cereal_ts

def name_filter(df, names = None):
    filtered_df = df
    if names:
        filtered_df = filtered_df[filtered_df['name'].isin(names)]

    return filtered_df

cereal_ts = get_data()
name_order = ["Cheerios", "Honey Nut Cheerios", 
              "Chex", "Honey Nut Chex", 
              "Corn Flakes", "Frosted Mini Wheats", 
              "Life", "Raisin Bran"]

st.title("Results")
st.subheader("Overall Trends")
# INSERT A TIMELINE GRAPH WITH SELECTOR MENU (POSSIBLE TO INCLUDE BOX IMAGES?)

names = st.multiselect(
    "Select cereal brand(s):",
    name_order,
    default = None
)

cereal_ts_filtered = name_filter(cereal_ts, names)

ts_chart_raw = alt.Chart(cereal_ts_filtered).mark_line().encode(
    x=alt.X('date:T', title = 'Date'),
    y=alt.Y('grams:Q', title = 'Weight (Grams)'),
    color=alt.Color('name:N', title = "Brand Name")
).properties(
    width = 1000,
    title = "Cereal Box Weights Over Time",

)

ts_chart_change = alt.Chart(cereal_ts_filtered).mark_line().encode(
    x=alt.X('date:T', title = 'Date'),
    y=alt.Y('change_per_day_zeroed:Q', title = 'Change in Weight (Grams)'),
    color=alt.Color('name:N', title = "Brand Name")
).properties(
    width = 1000,
    title = "Change in Weight From Prior Measurement Across Time",

)

st.altair_chart(ts_chart_raw, use_container_width=True)
st.altair_chart(ts_chart_change, use_container_width=True)

st.subheader("Trendmakers")
# INSERT BAR GRAPHS: TOTAL CONSUMPTION, SINGLE WEEK CHANGE, NUMBER OF REFILLS, AVERAGE WEEK CONSUMPTION

tot_consumption_df = cereal_ts.groupby('name')['change_per_day_zeroed'].sum().reset_index(name='tot_consumption')
tot_consumption_df['tot_consumption'] = tot_consumption_df['tot_consumption'].abs()
with st.expander("Total Consumption"):
    tot_consumption_chart = alt.Chart(tot_consumption_df).mark_bar().encode(
                x=alt.X('tot_consumption:Q', title = 'Total Consumption (Grams)'),
                y=alt.Y('name', title=None, sort = '-x'),
                tooltip=['name', 'tot_consumption'],
            ).configure_bar(
                color="red"
                ).properties(
                width=150
            )
    st.altair_chart(tot_consumption_chart, use_container_width=True)

biggest_bowl_df = cereal_ts[cereal_ts['change_per_day_zeroed'] != 0]
biggest_bowl_df = biggest_bowl_df.groupby('name')['change_per_day_zeroed'].mean().reset_index(name='mean_consumption')
biggest_bowl_df['mean_consumption'] = biggest_bowl_df['mean_consumption'].abs()
with st.expander("Biggest Average Bowl"):
    bowl_chart = alt.Chart(biggest_bowl_df).mark_bar().encode(
                x=alt.X('mean_consumption:Q', title = 'Averge Bowl Size'),
                y=alt.Y('name', title=None, sort = '-x'),
                tooltip=['name', 'mean_consumption'],
            ).configure_bar(
                color="red"
                ).properties(
                width=150
            )
    st.altair_chart(bowl_chart, use_container_width=True)

max_consumption_df = cereal_ts.groupby('name')['change_per_day_zeroed'].min().reset_index(name='max_consumption')
max_consumption_df['max_consumption'] = max_consumption_df['max_consumption'].abs()
with st.expander("Biggest Single-Week Change"):
    max_consumption_chart = alt.Chart(max_consumption_df).mark_bar().encode(
                x=alt.X('max_consumption:Q', title = 'Max Consumption (Grams)'),
                y=alt.Y('name', title=None, sort = '-x'),
                tooltip=['name', 'max_consumption'],
            ).configure_bar(
                color="red"
                ).properties(
                width=150
            )
    st.altair_chart(max_consumption_chart, use_container_width=True)

positive_changes_df = cereal_ts[cereal_ts['gram_change'] < -10]
positive_counts = positive_changes_df[positive_changes_df['gram_change'] < -10].groupby('name').size().to_frame(name='positive_count').reset_index()
with st.expander("Number of Boxes"):
    refill_chart = alt.Chart(positive_counts).mark_bar().encode(
                x=alt.X('positive_count:Q', title = 'Number of Boxes'),
                y=alt.Y('name', title=None, sort = '-x'),
                tooltip=['name', 'positive_count'],
            ).configure_bar(
                color="red"
                ).properties(
                width=150
            )
    st.altair_chart(refill_chart, use_container_width=True)

st.subheader("Dynamic Duos")
# INSERT CORRELATION/HEAT MAP