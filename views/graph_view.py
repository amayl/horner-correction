import streamlit as st
import matplotlib.pyplot as plt
from controllers.horner_controller import HornerController

def display_graph():

    st.title("Horner Plot")
    
    st.write(
        "Visualisation of measured temperatures against "
        "the logarithm of the Horner ratio."
    )

    st.divider()
    
    if "controller" not in st.session_state:
        st.session_state.controller = HornerController()

    controller = st.session_state.controller

    if controller.analysis_run is None:
        st.info("Please submit measurements before viewing the graph.")
        return

    if "results" not in st.session_state:
        st.info("Please run the Horner analysis first.")
        return

    x_values, y_values = controller.horner_engine.prepare_regression_data()

    results = st.session_state.results    

    slope = results["slope"]
    intercept = results["intercept"]

    fig, ax = plt.subplots(figsize=(5,2))

    # Plot measured temperature values
    ax.scatter(
        x_values,
        y_values,
        label="Measured temperatures"
    )

    # Calculate regression line
    regression_y = [
        slope * x + intercept for x in x_values
    ]

    ax.plot(
        x_values,
        regression_y,
        label="Regression line"
    )

    ax.set_xlabel("Log Horner Ratio")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Horner Correction Plot")

    ax.legend()
    ax.grid(True)

    st.pyplot(fig, use_container_width=False)

    plt.close(fig)