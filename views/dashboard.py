
import streamlit as st


def display_dashboard():
    st.title("Horner Correction System")

    st.write(
        "A borehole temperature analysis system "
        "for calculating static formation temperature."
    )

    st.divider()

    st.subheader("Welcome")

    st.info(
        "Use this application to analyse borehole "
        "temperature measurements using the Horner method."
    )
