import streamlit as st

st.set_page_config(page_title = 'CT2025 - Methods', layout = 'wide')
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

st.title("Methods")
st.subheader("Data Collection")

st.markdown(
    """
    """,
    unsafe_allow_html=True
)

st.subheader("Key Metrics")

st.markdown(
    """
    """,
    unsafe_allow_html=True
)