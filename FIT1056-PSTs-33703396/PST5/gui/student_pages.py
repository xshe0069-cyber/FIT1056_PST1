# gui/student_pages.py
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Section 1: Search for a Student ---
    st.subheader("Find a Student")
    search_term = st.text_input("Search by Name or ID")
    if search_term:
        # Call a find method on your manager and display results.
        # results = manager.find_students(search_term)
        # st.dataframe(results)
        result = manager.find_students(search_term)
        if result:
            st.dataframe([{
                "ID": result.id,
                "Name": result.name,
                "Enrolled Course IDs": result.enrolled_course_ids,
            }])
        else:
            st.write("Can not find the student")    
        

    # --- Section 2: Register a New Student ---
    st.subheader("Register a New Student")
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
