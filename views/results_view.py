import streamlit as st
from controllers.horner_controller import HornerController

def display_results():
    if "controller" not in st.session_state:
        st.session_state.controller = HornerController()

    controller = st.session_state.controller

    st.title("Horner Analysis Results")

    st.write(
        "Run the Horner correction analysis and view "
        "the calculated static formation temperature."
    )

    st.divider()

    if st.button("Run Horner Analysis", type="primary"):

        try:
            results = controller.perform_analysis()

            st.session_state.results = results

            st.success("Horner analysis completed successfully!")

        except ValueError as error:
            st.error(str(error))

    if "results" in st.session_state:

        results = st.session_state.results

        st.divider()

        st.subheader("Analysis Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Static Formation Temperature",
                f"{results['static_formation_temperature']:.2f} °C"
            )

        with col2:
            st.metric(
                "Regression Slope",
                f"{results['slope']:.4f}"
            )

        with col3:
            st.metric(
                "Regression Intercept",
                f"{results['intercept']:.2f} °C"
            )      