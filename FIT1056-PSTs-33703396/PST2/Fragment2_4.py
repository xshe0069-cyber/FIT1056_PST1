# --- Main Application Loop ---
def main():
    """Main function to run the MSMS application."""
    load_data() # Load all data from file at startup.

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Check-in Student")
        print("2. Print Student Card")
        print("3. Update Teacher Info")
        print("4. Remove Student")
        print("q. Quit and Save")
        
        choice = input("Enter your choice: ")
        
        made_change = False # A flag to track if we need to save
        if choice == '1':
            # TODO: Get student_id and course_id from user, then call check_in().
            student_id = int(input("Enter student ID: "))
            course_id = int(input("Enter course ID: "))
            check_in(student_id, course_id)
            made_change = True
        elif choice == '2':
            # TODO: Get student_id, then call print_student_card().
            student_id = int(input("Enter student ID: "))
            print_student_card(student_id)
            pass # No change made, so no save needed
        elif choice == '3':
            # TODO: Get teacher_id and new details, then call update_teacher().
            # Example: update_teacher(1, speciality="Advanced Piano")
             teacher_id = int(
                input("Enter teacher ID: "))

            speciality = input(
                "Enter new speciality: "
            )

            update_teacher(
                teacher_id,
                speciality=speciality
            )
            made_change = True
        elif choice == '4':
            # TODO: Get student_id, then call remove_student().
            student_id = int(
                input("Enter student ID: ")
            )

            remove_student(student_id)
            made_change = True
        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break
        else:
            print("Invalid choice.")
            
        if made_change:
            save_data() # Save the data immediately after any change.

    save_data() # One final save on exit.

# --- Program Start ---
if __name__ == "__main__":
    main()