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
    Data were collected on a semi-weekly schedule using standard field equipment (kitchen scale). Collection began in March 2025 and 
    continued through June of the same year. Plinth Quantitative Research Associates, LLC employs field researchers of the highest 
    caliber, and places a special emphasis on quality and length of experience in the hiring process. The Field Operations Lead for 
    this project, Laura Silverstein, is well-versed in kitchen scale management as well as in-field observation and data collection.

    Data were manually entered to a cloud-hosted database service (Google Sheets) and accessed by the quantitative research team from 
    there. Due to the relative simplicity of the research design, no major issues with collection or data parsing occurred.
    """,
    unsafe_allow_html=True
)

st.subheader("Quantitative Methods")

st.markdown(
    """
    Because this research was performed with a *longitudinal panel* design, special consideration was necessary to ensure that time 
    series data were treated correctly. If not properly accounted for in the analysis, time series data can be subject to spurious (COYS) 
    correlations and non-stationarity. To address this, a lag procedure was implemented and the large majority of the analysis was 
    based on *change from prior measurement* rather than the raw weight of the cereal box. This choice is further justified because 
    cereal box weight differ by brand, so comparison across study units at the raw weight level is problematic.
    """,
    unsafe_allow_html=True
)

st.subheader("Analysis Approach")

st.markdown(
    """
    Plinth Quantitative Research Associates, LLC does not focus on statistical significance or arbitrary KPI milestones. Rather, we
    prefer an approach grounded in prior beliefs and insights derived directly from the data. This approach returns the art to the 
    science of statistical analysis, which Plinth Associates is readily able to leverage with our highly capable research staff.
    """,
    unsafe_allow_html=True
)