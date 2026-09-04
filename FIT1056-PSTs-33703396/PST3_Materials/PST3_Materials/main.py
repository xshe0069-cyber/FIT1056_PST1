# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    # Notice: This code does not need to change. It doesn't care where the Course class lives.
    # It only talks to the manager.
    # TODO: Call a method on the manager to get the day's lessons and print them.
    roster = manager.get_daily_roster(day)

    if not roster:
        print("No lessons found")
        return

    for lesson in roster:
        print(
            f"{lesson['course_name']} |"
            f"{lesson['start_time']} |"
            f"{lesson['room']} |"
        )
    

def switch_course(manager, student_id, from_course_id, to_course_id):
    # TODO: Implement the logic to switch a student by calling methods on the manager.
    is_switched = manager.get_switch_course(student_id, from_course_id, to_course_id)
    if is_switched:
        print("Swith successfully")
    else:
        print("Switch not successful, please check your input")    

def list_users(users):
    if not users:
        print("No users found")
        return

    for user in users:
        print(user.get_details()) 

def front_desk_lookup(manager, term):
    students = manager.find_users(
        manager.students,
        term
    )

    teachers = manager.find_users(
        manager.teachers,
        term
    )

    print("\n--- Matching Students ---")
    list_users(students)

    print("\n--- Matching Teachers ---")
    list_users(teachers)

def front_desk_register(manager, name, course_id):
    student = manager.register_student(
        name,
        course_id
    )

    if student:
        print(
            f"Student '{student.name}' "
            f"registered successfully. "
            f"Student ID: {student.id}"
        )
    else:
        print(
            "Registration failed. "
            "Please check the course ID."
        )

def front_desk_add_teacher(
    manager,
    name,
    speciality
):
    teacher = manager.add_teacher(
        name,
        speciality
    )

    print(
        f"Teacher '{teacher.name}' "
        f"added successfully. "
        f"Teacher ID: {teacher.id}"
    )

def front_desk_update_student(
    manager,
    student_id,
    name
):
    success = manager.update_student(
        student_id,
        name = name
    )

    if success:
        print("Student updated successfully.")
    else:
        print("Student ID not found.")

def front_desk_update_teacher(
    manager,
    teacher_id,
    name,
    speciality
):
    success = manager.update_teacher(
        teacher_id,
        name=name,
        speciality=speciality
    )

    if success:
        print("Teacher updated successfully.")
    else:
        print("Teacher ID not found.")


def front_desk_remove_student(
    manager,
    student_id
):
    success = manager.remove_student(
        student_id
    )

    if success:
        print("Student removed successfully.")
    else:
        print("Student ID not found.")


def front_desk_remove_teacher(
    manager,
    teacher_id
):
    success = manager.remove_teacher(
        teacher_id
    )

    if success:
        print("Teacher removed successfully.")
    else:
        print(
            "Teacher could not be removed. "
            "Check the ID or assigned courses."
        )


def front_desk_print_card(
    manager,
    student_id
):
    success = manager.print_student_card(
        student_id
    )

    if success:
        print("Student card created successfully.")
    else:
        print("Student ID not found.")
           

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. View daily roster")
        print("2. Check in student")
        print("3. Switch course")
        print("4. Register new student")
        print("5. Lookup student / teacher")
        print("6. List all students")
        print("7. List all teachers")
        print("8. Add teacher")
        print("9. Update student")
        print("10. Update teacher")
        print("11. Remove student")
        print("12. Remove teacher")
        print("13. Print student card")
        print("Q. Quit")
        # TODO: Create a menu for the new PST3 functions.
        # Get user input and call the appropriate view function, passing 'manager' to it.
        choice = input("Enter choice: ")
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)
        elif choice == "2":
            student_id = int(input("Enter student ID: "))
            course_id = int(input("Enter course ID: "))
            manager.check_in(student_id, course_id)
        elif choice == "3":
            student_id = int(input("Enter student ID: "))
            from_course_id = int(input("Enter current course ID: "))
            to_course_id = int(input("Enter new course ID: "))
            switch_course(
                manager,
                student_id,
                from_course_id,
                to_course_id
            )
        elif choice == "4":
            name = input(
                "Enter student name: "
            )
            course_id = int(
                input("Enter course ID: ")
            )
            front_desk_register(
                manager,
                name,
                course_id
            ) 
        elif choice == "5":
            term = input(
                "Enter search term: "
            )
            front_desk_lookup(
                manager,
                term
            )
        elif choice == "6":
            print("\n--- Student List ---")
            list_users(manager.students)
        elif choice == "7":
            print("\n--- Teacher List ---")
            list_users(manager.teachers)
        elif choice == "8":
            name = input(
                "Enter teacher name: "
            )
            speciality = input(
                "Enter teacher speciality: "
            )
            front_desk_add_teacher(
                manager,
                name,
                speciality
            )
        elif choice == "9":
            student_id = int(
                input("Enter student ID: ")
            )
            name = input(
                "Enter new name: "
            )
            front_desk_update_student(
                manager,
                student_id,
                name
            )
        elif choice == "10":
            teacher_id = int(
                input("Enter teacher ID: ")
            )
            name = input(
                "Enter new name: "
            )
            speciality = input(
                "Enter new speciality: "
            )
            front_desk_update_teacher(
                manager,
                teacher_id,
                name,
                speciality
            )
        elif choice == "11":
            student_id = int(
                input("Enter student ID: ")
            )
            front_desk_remove_student(
                manager,
                student_id
            )
        elif choice == "12":
            teacher_id = int(
                input("Enter teacher ID: ")
            )
            front_desk_remove_teacher(
                manager,
                teacher_id
            )
        elif choice == "13":
            student_id = int(
                input("Enter student ID: ")
            )
            front_desk_print_card(
                manager,
                student_id
            )
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice.")

        
if __name__ == "__main__":
    main()