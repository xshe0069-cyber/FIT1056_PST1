# main.py
from gui.main_dashboard import launch
# TODO: Import the new admin utilities.
from app.admin_utils import init_logger, backup_data
import streamlit as st

if __name__ == "__main__":
    # TODO: Initialize the logger as the very first step.
    init_logger()
    
    # TODO: Perform a data backup before starting the application session.
    # Streamlit reruns this file on interactions; attempt startup backup once per session.
    if "startup_backup_attempted" not in st.session_state:
        st.session_state.startup_backup_attempted = True
        if not backup_data():
            st.warning("Startup backup failed. Check msms.log or try Backup Now.")

    # TODO: Launch the GUI as before.
    launch()
