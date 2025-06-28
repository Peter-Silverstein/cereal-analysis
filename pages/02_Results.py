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
    cereal_ts['change_per_day_naed'] = cereal_ts['change_per_day']
    cereal_ts.loc[cereal_ts['change_per_day_naed'] > 0, 'change_per_day_naed'] = None
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
cereal_pivot = cereal_ts.pivot(index = 'date', columns = 'name', values = 'change_per_day_naed')
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
         title='Correlation',
         legend=None
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
    1. **Cheerios + Life (correlation = 0.61):** Experts agree, there are few better textural combinations than the squares and circles.
            Though Honey Nut Cheerios are perhaps the more iconic combination, these data indicate that Life benefits from a more pedestrian 
            partner.
    2. **Corn Flakes + Frosted Mini Wheats (correlation = 0.61):** This combination isn't backed up by a lot of theory in the literature,
            but the principles of sweetness spillover certainly apply. Anytime Corn Flakes are brought closer to Frosted Flakes by a 
            combination, good things happen.
    3. **Chex + Honey Nut Chex (correlation = 0.57):** Perhaps an indication that the correlation is not the end-all-be-all of cereal combination
            theory. Or, perhaps this blended variety of Chex provides balance that only an experienced palette could truly appreciate.
            
    ### Like Oil and Water, These Don't Mix:
    1. **Corn Flakes + Cheerios (correlation = -0.31):** Cheerios were the least-combinatory cereal out there, boasting all three of the
            lowest correlation coefficients. This tops the lot: two boring cereals don't add up to a less boring cereal.
    2. **Cheerios + Raisin Bran (correlation = -0.23):** Again, bland meet bland. Though Raisin Bran is highly popular, its raisin
            component requires a highly-tuned pairing for proper success. Cheerios are simply too sensible to be a good pairing.
    3. **Frosted Mini Wheats + Raisin Bran (correlation = -0.14):** Though not one of the top 3, the a priori beliefs about this combination 
            are strong enough so as to make it mention-worthy by Bayesian process. Testurally and flavor-wise a poor mix, and these are
            two of the least sog-resistant cereals out there.

    ### The Paragon of Friendship
    Life is the amiable customer in the fridge-top lineup. It shows positive correlation coefficients with all other brands, save Raisin Bran.
            From the iconic Chex and Life power duo to the cloyingly-sweet yet overpoweringly delicious Honey Nut Cheerios combination,
            Life lends excellent flavor, unique and compatible texture, and a sog profile that complements both sog winners and losers. It's
            also an excellent weight cereal, making it perfect to combine with typical floaters such as Cheerios.
""")

