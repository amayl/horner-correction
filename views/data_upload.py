from controllers.horner_controller import HornerController
import streamlit as st


def display_data_upload():
    if "controller" not in st.session_state:
        st.session_state.controller = HornerController()

    controller = st.session_state.controller

    st.title("Borehole Data Input")

    st.write(
        "Enter the borehole details and temperature "
        "measurements required for Horner analysis."
    )

    st.divider()

    st.subheader("Borehole Information")

    col1, col2 = st.columns(2)

    with col1:
        borehole_id = st.text_input(
            "Borehole ID",
            placeholder="e.g. BH001"
        )

        total_depth = st.number_input(
            "Total Borehole Depth (m)",
            min_value=1.0,
            value=3000.0
        )

    with col2:
        run_id = st.text_input(
            "Analysis Run ID",
            placeholder="e.g. RUN001"
        )

        circulation_time = st.number_input(
            "Circulation Time (hours)",
            min_value=0.1,
            value=3.0
        )

    st.divider()

    st.subheader("Temperature Measurements")

    st.write("Enter the temperature readings for this borehole.")

    measurements = st.data_editor(
        [
            {
                "Depth (m)": 3000.0,
                "Temperature (°C)": 90.0,
                "Shut-in Time (hours)": 1.0
            }
        ],
        num_rows="dynamic",
        use_container_width=True
    )

    st.divider()

    if st.button("Submit Measurements", type="primary"):

        try:
            if not borehole_id.strip():
                raise ValueError("Borehole ID cannot be empty")

            if not run_id.strip():
                raise ValueError("Analysis Run ID cannot be empty")

            if len(measurements) == 0:
                raise ValueError("At least one measurement is required")
            
            controller.create_analysis_run(
                run_id=run_id,
                borehole_id=borehole_id,
                depth=total_depth,
                circulation_time=circulation_time
            )

            measurement_data = []

            for index, row in enumerate(measurements, start=1):
                measurement_data.append({
                    "measurement_id": index,
                    "depth": row["Depth (m)"],
                    "temperature": row["Temperature (°C)"],
                    "measurement_time": None,
                    "time_since_circulation": row["Shut-in Time (hours)"]
                })

            controller.add_measurements(measurement_data)

            st.success("Measurements successfully submitted!")

        except ValueError as error:
            st.error(str(error))