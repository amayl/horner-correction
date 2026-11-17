
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
