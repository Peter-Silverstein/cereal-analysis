import streamlit as st

st.set_page_config(page_title = 'CT2025 - The Team', layout = 'wide')
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

st.title("Meet the Team")
st.subheader("Peter E. Silverstein, MA -- Principal Investigator")

st.markdown(
    """
    Mr. Silverstein brings over 2 decades of experience in cold cereal research and experimentation. His work focuses specifically on
    multi-cereal combination theory and, within that field, the principles of boyancy and textural properties of mixed varieties. He 
    is technically owed a master's degree in quantitative methods for the social sciences by Columbia University. Outside of the lab,
    Peter pursues his passion project: determining which grocery stores in his area carry All-Bran Flakes, rather than the Sticks or the Dots.

    """,
    unsafe_allow_html=True
)

st.subheader("Laura Silverstein, MSW -- Field Operations Lead")

st.markdown(
    """
    Ms. Silverstein has spent 30 years conducting highly-immersive fieldwork in the Whittier Heights area, observing cereal 
    eaters in their natural environment. She was listed as one of the world's top Cereal Ethnographers (2007, 2008, 2010) by the Fridge Top 
    Review and her natual-setting Dibble Lab has been lauded by the academic world. She holds an MSW from the University of Washington. 
    Laura enjoys a bowl of Frosted Mini Wheats for dessert, on occasion.
    """,
    unsafe_allow_html=True
)