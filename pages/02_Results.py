import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

st.set_page_config(page_title = 'CT2025 - Results', layout = 'wide')
def sidebar_title_above_nav():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "Navigation";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 20px;
                font-weight: bold;
                position: relative;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

sidebar_title_above_nav()

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

st.markdown("""
    #### The Tortoise, the Hare, and the Electric Bicycle
    Corn Flakes are the perfect definition of methodical consistency, with steady consumption numbers across the whole study. Compare 
    that with the hare, Frosted Mini Wheats. Frosted Mini Wheats are hot-streak merchants, relying on Big Weeks to get through the box. 
    But, the fable sort of falls apart when someone pulls out the electric bike: fast *and* consistent. Looking at Raisin Bran's chart
    is a bit like watching Eliud Kipchoge run the marathon: he won't just rinse you in the 26.2, but even over 100m (or 200m, or 5k, or 10k).
""")

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

# Set up table 
cereal_pivot = cereal_ts.pivot(index = 'date', columns = 'name', values = 'change_per_day')
corr = cereal_pivot.corr('pearson')
corr_reset = corr.reset_index()
corr_long = pd.melt(corr_reset, id_vars='name', var_name = 'name2', value_name='corr')

corr_chart = alt.Chart(corr_long).mark_rect().encode(
    x=alt.X('name:O', axis=alt.Axis(title='',
                                    orient = 'top',
                                    labelAngle = 45,
                                    labelSeparation=-10,
                                    labelLimit=200)),
    y=alt.Y('name2:O', axis=alt.Axis(title='',
                                     labelLimit=200)),
    color=alt.Color('corr:Q',
         scale=alt.Scale(domain=[-1, -0.5, 0, 0.5, 1], range=['blue', 'lightblue', 'white', 'pink', 'red']),
         title='Correlation'
     ),
    tooltip=[
        alt.Tooltip('name', title='Cereal 1:'),
        alt.Tooltip('name2', title='Cereal 2:'),
        alt.Tooltip('corr', title='Correlation: ', format='.2f')
    ]
).properties(
    title='',
    width=alt.Step(25),
    height=alt.Step(75)
)

st.altair_chart(corr_chart, use_container_width=True)

st.markdown("""
    ### Top Dynamic Duos: 
    #### Corn Flakes + Honey Nut Cheerios (correlation = 0.47)
    Simultaneously innovative and expectable--this was not a top combination identified a priori but, in retrospect, it is a natural 
    pairing. The heavy-hitting sweetness of the Honey Nut Cheerios is balanced by the effortless flavor and refreshing texture of 
    the Corn Flakes. This is a top milk-retention combination.
    #### Cheerios + Life (correlation = 0.42)
    Pedestrian? Perhaps, but there are few, if any, texture combinations better than the circles and squares. While experts have lauded 
    the powerful combination of Life and Honey Nut Cheerios, these real-world observations identify Honey Nut's older, more mature 
    brother as the second component of this dynamic duo.
            
    ### Paragons of Insularity:
    #### Raisin Bran
    Despite its astronomical popularity, Raisin Bran does not play well with others. Like Einstein, Newton, and Dickinson before it, 
    the Bran prefers to exist in solitary excellence. The controversial raisins require a highly-tuned pairing. Though the bran flakes 
    are this tuned partner, other additions to the bowl only serve to disrupt majesty.
    #### Chex
    Though part of perhaps the all-time most notorious combination (Chex and Life), Chex was not a popular mixing choice (or, really, 
    a popular individual choice...). Its single positive pairing was Honey Nut Chex, which seems more likely to be coincidence than a 
    true pattern.
""")

