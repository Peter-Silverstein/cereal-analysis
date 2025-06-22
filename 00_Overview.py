import streamlit as st

st.set_page_config(page_title = 'Cereal Trends 2025', layout = 'wide')

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

st.subheader("Plinth Quantitative Research Associates, LLC")
st.title("Cereal Trends 2025 -- Preliminary Report")

st.markdown(
    """
    The official page for the 2025 Cereal Trend Report, commissioned by the Panel on Eating Trends, Exploratory Research (PETER) Division of
    Carb<sup>2</sup> Corp, a subsidiary of the Carbohydrates Commission for America. The Report leverages high-granularity, longitudinal
    consumption data for a curated set of brand-name cereals, chosen for their popularity in the Whittier Heights region.

    The Report is a value-add and information net-positive for high-impact individuals in the breakfast cereal space. Plinth Quantitative 
    Research Associates brings decades of consumer-side experience in the breakfast cereal market, with a special emphasis on cross-product 
    integration and alternative-meal theory.

    As of June, 2025, the preliminary results for The Report are available. These initial results provide an early look at the 2025 trends, 
    alongside findings that give a sense of what the full results will look like. The preliminary report also provides an opporunity for 
    cross-team consultation and course-correction on the research design.

    Readers can expect both product-centric and consumer-centric insights from The Report, which is the first of its kind. Plinth
    Quantitative Research Associates thanks Carb<sup>2</sup> Corp and the PETER Division for their unwavering support of innovative
    cereal science. 

    © 2025, Carbohydrates Commission for America, all rights reserved.
    """,
    unsafe_allow_html=True
)