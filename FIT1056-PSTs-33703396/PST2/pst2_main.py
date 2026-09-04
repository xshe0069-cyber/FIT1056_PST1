# pst2_main.py - The Persistent Application

import json
import datetime

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            # TODO: Use json.load(f) to load the file's content into the global 'app_data' variable.
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        # TODO: If the file doesn't exist, initialize 'app_data' with a default dictionary.
        # It should have keys like: "students", "teachers", "attendance", "next_student_id", "next_teacher_id".
        # The lists should be empty and the IDs should start at 1.
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    # TODO: Open the file at 'path' in write mode ('w').
    # Use json.dump() to write the global 'app_data' dictionary to the file.
    # Use the 'indent=4' argument in json.dump() to make the file readable.
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")

def find_students_by_id(student_id):
    for student in app_data['students']:
        if student_id == student['id']:
            return student
    return None

def front_desk_register(name, instrument):
    student_id = app_data['next_student_id'] 

    new_student = {"id": student_id, "name": name, "enrolled_in": [instrument]} 
    app_data['students'].append(new_student)
    app_data['next_student_id'] += 1  
    print(f"Front Desk: Successfully registered "
          f"'{name}' and enrolled them in '{instrument}'.") 

def list_students():
    print("\n--- Student List ---")

    if not app_data['students']:
        print("No students in the system")
        return

    for student in app_data['students']:
        print(
            f"ID: {student['id']}, "
            f"Name: {student['name']}, "
            f"Enrolled in: {student['enrolled_in']}")

def list_teachers():
    print("\n--- Teacher List ---")

    if not app_data['teachers']:
        print("No teachers in the system.")
        return

    for teacher in app_data['teachers']:
        print(
            f"ID: {teacher['id']}, "
            f"Name: {teacher['name']}, "
            f"Speciality: {teacher['speciality']}")                          

def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store."""
    # TODO: Get the next teacher ID from app_data['next_teacher_id'].
    teacher_id = app_data['next_teacher_id']
    # TODO: Create a new teacher dictionary with 'id', 'name', and 'speciality' keys.
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    # TODO: Append the new dictionary to the app_data['teachers'] list.
    app_data['teachers'].append(new_teacher)
    # TODO: Increment the 'next_teacher_id' in app_data.
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    # TODO: Loop through the app_data['teachers'] list.
    for teacher in app_data['teachers']:
        # TODO: If a teacher's 'id' matches teacher_id:
        if teacher['id'] == teacher_id:
            # Use the .update() method on the teacher dictionary to apply the 'fields'.
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def remove_student(student_id):
    """Removes a student from the data store."""
    # TODO: Find the student dictionary in app_data['students'] with the matching ID.
    for student in app_data['students']:
        if student_id == student['id']:
            app_data['students'].remove(student)
            print(f"Remove successfully")
            return

    print(f"Error: Student with ID {student_id} not found.")    
    # If found, use the .remove() method on the list to delete it.
    # A list comprehension is a clean way to do this:
    # app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
    pass

def remove_teacher(teacher_id):
    for teacher in app_data['teachers']:
        if teacher_id == teacher['id']:
            app_data['teachers'].remove(teacher)
            print(f"Remove successfully")
            return

    print(f"Error: Teacher with ID {teacher_id} not found.")  

def update_student(student_id, **fields):
    for student in app_data['students']:

        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return

    print(f"Error: Student with ID {student_id} not found.")    

def check_in(student_id, instrument, timestamp=None):
    """Records a student's attendance for a course."""
    if timestamp is None:
        # TODO: Get the current time as a string using datetime.datetime.now().isoformat()
        timestamp = datetime.datetime.now().isoformat()
    
    # TODO: Create a check-in record dictionary.
    # It should contain 'student_id', 'instrument', and 'timestamp'.
    check_in_record = {
        "student_id": student_id,
        "instrument": instrument,
        "timestamp": timestamp
    }
    # TODO: Append this new record to the app_data['attendance'] list.
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {instrument}.")

def print_student_card(student_id):
    """Creates a text file badge for a student."""
    # TODO: Find the student dictionary in app_data['students'].
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    
    if student_to_print:
        # TODO: Create a filename, e.g., f"{student_id}_card.txt".
        filename = f"{student_id}_card.txt"
        # TODO: Open the file in write mode ('w').
        with open(filename, 'w') as f:
            # Write the student's details to the file in a nice format.
            f.write("========================\n")
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")

def main():
    """Main function to run the MSMS application."""
    load_data() # Load all data from file at startup.

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Check-in Student")
        print("2. Print Student Card")
        print("3. Update Teacher Info")
        print("4. Remove Student")
        print("5. Register new student")
        print("6. Add teacher")
        print("7. List All students")
        print("8. List All teachers")
        print("9. Update Student Info")
        print("10. Remove Teacher")
        print("q. Quit and Save")
        
        choice = input("Enter your choice: ")
        
        made_change = False # A flag to track if we need to save
        if choice == '1':
            # TODO: Get student_id and instrument from user, then call check_in().
            student_id = int(input("Enter student ID: "))
            instrument = int(input("Enter course ID: "))
            check_in(student_id, instrument)
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

            speciality = input("Enter new speciality: ")

            update_teacher(
                teacher_id,
                speciality=speciality)
            made_change = True
        elif choice == '4':
            # TODO: Get student_id, then call remove_student().
            student_id = int(
                input("Enter student ID: ")
            )

            remove_student(student_id)
            made_change = True
        elif choice == '5':
            name = input("Enter student name: ")
            instrument = input("Enter student's instrument: ")
            front_desk_register(name, instrument)
            made_change = True
        elif choice == '6':
            name = input("Enter teacher name: ")
            speciality = input("Enter teacher's speciality: ")
            add_teacher(name, speciality)
            made_change = True
        elif choice == '7':
            list_students()
        elif choice == '8':
            list_teachers()
        elif choice == '9':
            student_id = int(input("Enter student ID: "))
            new_name = input("Enter the new student name: ")
            new_instrument = input("Student's instrument: ")
            update_student(student_id, name = new_name, enrolled_in = [new_instrument])
            made_change = True
        elif choice == '10':
            teacher_id = int(input("Enter teacher id: "))
            remove_teacher(teacher_id)
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