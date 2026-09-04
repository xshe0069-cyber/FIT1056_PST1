import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course


class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # TODO: Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        # ... (next_id counters) ...
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # TODO: Load students, teachers, and courses as before.
                # ...
                self.students = []
                for student_data in data.get("students", []):
                    student = StudentUser(student_data["id"], student_data["name"])
                    student.enrolled_course_ids = student_data.get("enrolled_course_ids", [])
                    self.students.append(student)

                self.teachers = []
                for teacher_data in data.get("teachers", []):
                    teacher = TeacherUser(teacher_data["id"], teacher_data["name"], teacher_data["speciality"])
                    self.teachers.append(teacher)

                self.courses = []
                for course_data in data.get("courses", []):
                    course = Course(course_data["id"], course_data["name"], course_data["instrument"], course_data["teacher_id"])
                    course.enrolled_student_ids = course_data.get("enrolled_student_ids", [])
                    course.lessons = course_data.get("lessons", [])
                    self.courses.append(course)        
                # TODO: Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't exist.
                self.attendance_log = data.get("attendance", [])
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            # TODO: Add the attendance_log to the dictionary to be saved.
            # Since it's already a list of dicts, no conversion is needed.
            "attendance": self.attendance_log,
            # ... (next_id counters) ...
        }
        # TODO: Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def check_in(self, student_id, course_id):
    # This implementation remains the same, but it will now function correctly.
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
    
        if not student or not course:
           print("Error: Check-in failed. Invalid Student or Course ID.")
           return False
        
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
    
    # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

# TODO: Also implement find_student_by_id and find_course_by_id helper methods.

    def _find_by_id(self, item, target_id):
        for item in item:
            if item.id == target_id:
               return item
        return None

    def find_student_by_id(self, student_id):
        return self._find_by_id(self.students, student_id)

    def find_course_by_id(self, course_id):
        return self._find_by_id(self.courses, course_id)

    def find_teacher_by_id(self, teacher_id):
        return self._find_by_id(self.teachers, teacher_id)
    
    def find_users(self, users, term):
        results = []

        for user in users:
            if user.matches(term):
                results.append(user)
        return results                   

    def get_daily_roster(self, day):
        roster = []

        for course in self.courses:
            for lesson in course.lessons:
                if lesson["day"].lower() == day.lower():
                    roster.append({"course_name": course.name, "start_time": lesson["start_time"], "room": lesson["room"]})
        return roster

    def get_switch_course(self, student_id, from_course_id, to_course_id):
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student or not from_course or not to_course:
            return False
        if from_course_id not in student.enrolled_course_ids:
            return False
        if student_id not in from_course.enrolled_student_ids:
            return False
        if to_course_id in student.enrolled_course_ids:
            return False

        student.enrolled_course_ids.remove(from_course_id)
        from_course.enrolled_student_ids.remove(student_id)

        student.enrolled_course_ids.append(to_course_id)
        if student_id not in to_course.enrolled_student_ids:
            to_course.enrolled_student_ids.append(student_id)

        self._save_data()

        return True

    def _get_next_id(self, item):
        if item:
            return max(item.id for item in item) + 1

        return 1
 
    def register_student(self, name, course_id):
        course = self.find_course_by_id(course_id)
        if not course:
            return None
        new_id = self._get_next_id(self.students)

        student = StudentUser(new_id, name)
        student.enrolled_course_ids.append(course_id)
        course.enrolled_student_ids.append(new_id)

        self.students.append(student)
        self._save_data()

        return student        

    def update_student(self, student_id, **fields):
        student = self.find_student_by_id(student_id)
        if not student:
            return False
        if "name" in fields:
            student.name = fields["name"]
        self._save_data()
        return True

    def remove_student(self, student_id):
        student = self.find_student_by_id(student_id)

        if not student:
            return False
        for course in self.courses:
            if student_id in course.enrolled_student_ids:
                 course.enrolled_student_ids.remove(student_id)

        self.students.remove(student)
        self._save_data()
        return True

    def add_teacher(self, name, speciality):
        new_id = self._get_next_id(self.teachers)

        teacher = TeacherUser(
         new_id,
         name,
         speciality)

        self.teachers.append(teacher)

        self._save_data()

        return teacher

    def update_teacher(self, teacher_id, **fields):
        teacher = self.find_teacher_by_id(teacher_id)

        if not teacher:
           return False

        if "name" in fields:
           teacher.name= fields["name"]

        if "speciality" in fields:
           teacher.speciality = fields["speciality"]

        self._save_data()

        return True 

    def remove_teacher(self, teacher_id):
        teacher = self.find_teacher_by_id(teacher_id)

        if not teacher:
           return False

        for course in self.courses:
            if course.teacher_id == teacher_id:
               return False

        self.teachers.remove(teacher)
        self._save_data()

        return True 

    def print_student_card(self, student_id):
        student = self.find_student_by_id(student_id)

        if not student:
           return False

        filename = f"student_{student.id}_card.txt"

        with open(filename, "w") as file:
           file.write("===== STUDENT CARD =====\n")
           file.write(f"ID: {student.id}\n")
           file.write(f"Name: {student.name}\n")
           file.write("Courses:\n")

           for course_id in student.enrolled_course_ids:
            course = self.find_course_by_id(course_id)

            if course:
                file.write(
                    f"{course.id}: {course.name}\n"
                )

        return True         
