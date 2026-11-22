
import streamlit as st
from views.dashboard import display_dashboard
from views.data_upload import display_data_upload
from views.results_view import display_results
from views.graph_view import display_graph

def main():
    st.set_page_config(
        page_title="Horner Correction System",
        page_icon="🌡️",
        layout="wide"
    )

    st.markdown("""
<style>
    /* Main content area */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1500px;
    }

    /* Make sidebar narrower */
    [data-testid="stSidebar"] {
        min-width: 240px;
        max-width: 240px;
    }

    /* Reduce heading spacing */
    h1 {
        font-size: 36px !important;
        margin-bottom: 0.5rem;
    }

    h2 {
        font-size: 29px !important;
    }

    h3 {
        font-size: 25px !important;
    }

    /* Reduce vertical gaps between elements */
    [data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }

    /* Buttons */
    .stButton button {
        padding: 8px 18px;
        font-size: 16px;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
</style>
""", unsafe_allow_html=True)

    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Select a page",
        ["Dashboard", "Data Input", "Results", "Graph"]
    )

    if page == "Dashboard":
        display_dashboard()

    elif page == "Data Input":
        display_data_upload()

    elif page == "Results":
        display_results()

    elif page == "Graph":
        display_graph()

if __name__ == "__main__":
    main()
