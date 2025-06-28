import streamlit as st
from PIL import Image
import os
import glob

st.set_page_config(page_title = 'Cereal Trends 2025', layout = 'wide')
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

st.subheader("Plinth Quantitative Research Associates, LLC")
st.title("Cereal Trends 2025 Report")

st.markdown(
    """
    The official page for the 2025 Cereal Trend Report, commissioned by the Panel on Eating Trends, Exploratory Research (PETER) Division of
    Carb<sup>2</sup> Corp, a subsidiary of the Carbohydrates Commission for America. The Report leverages high-granularity, longitudinal
    consumption data for a curated set of brand-name cereals, chosen for their popularity in the Whittier Heights region.

    The Report is a value-add and information net-positive for high-impact individuals in the breakfast cereal space. Plinth Quantitative 
    Research Associates brings decades of consumer-side experience in the breakfast cereal market, with a special emphasis on cross-product 
    integration and cereal physics theory.

    Readers can expect both product-centric and consumer-centric insights from The Report, which is the first of its kind. Plinth
    Quantitative Research Associates thanks Carb<sup>2</sup> Corp and the PETER Division for their unwavering support of innovative
    cereal science. 

    © 2025, Carbohydrates Commission for America, all rights reserved.
    """,
    unsafe_allow_html=True
)