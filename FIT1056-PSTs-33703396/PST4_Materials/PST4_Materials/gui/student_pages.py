# gui/student_pages.py
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Search Section (remains the same) ---
    st.subheader("Find a Student")
    student_id = st.number_input("Enter the id of the student you want to find",
                                 min_value=1,
                                 step=1)
    student = manager.find_student(student_id)
    if student:
        st.write(student.__dict__)
    else:
        st.write("There is no student match the requirements")    
    # ...

    # --- Registration Section (now works correctly) ---
    st.subheader("Register New Student")
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")
        find_button = st.form_submit_button("Find courses")
        
        if find_button:
            # This call now works because we implemented the method in PST3.
            # TODO: Add a check for blank name/instrument.
            if reg_name and reg_instrument:
                find_courses = manager.check_instrument_courses(reg_instrument)
                if find_courses:
                    st.session_state["find_courses"] = find_courses
                    st.session_state["reg_name"] = reg_name
                else:
                    if "find_courses" in st.session_state:
                        del st.session_state["find_courses"]
                    st.error(f"Could not register student. A teacher for {reg_instrument} might not be available.")    
            else:
                st.warning("Please enter both a name and an instrument.")
    if "find_courses" in st.session_state:
        with st.form("Choose course form"):
            selected_course = st.selectbox("Choose course", st.session_state["find_courses"], index=None, placeholder="Choose a course") 
            register_button = st.form_submit_button("Register Student")
            if register_button:
                if selected_course is None:
                    st.warning("Please choose a course")
                else:
                    new_student = manager.register_new_student(st.session_state["reg_name"], selected_course)   
                    if new_student:
                        st.success(f"Successfully registered {st.session_state['reg_name']}!")
                        del st.session_state["find_courses"]
                        del st.session_state["reg_name"]
                    else:
                        st.error("Could not register student.")    
                    # You can use st.balloons() for extra flair.
           