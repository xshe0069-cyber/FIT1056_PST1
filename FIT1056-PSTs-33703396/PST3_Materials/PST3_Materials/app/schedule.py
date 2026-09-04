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

    def find_student_by_id(self, student_id):
        for student in self.students:
            if student.id == student_id:
               return student
        return None 

    def find_course_by_id(self, course_id):
        for course in self.courses:
            if course.id == course_id:
               return course
        return None 

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

        student.enrolled_course_ids.remove(from_course_id)
        from_course.enrolled_student_ids.remove(student_id)

        student.enrolled_course_ids.append(to_course_id)
        to_course.enrolled_student_ids.append(student_id)

        self._save_data()

        return True

