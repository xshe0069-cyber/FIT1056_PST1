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
    

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. View daily roster")
        print("2. Check in student")
        print("3. Switch course")
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
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice.")

        
if __name__ == "__main__":
    main()