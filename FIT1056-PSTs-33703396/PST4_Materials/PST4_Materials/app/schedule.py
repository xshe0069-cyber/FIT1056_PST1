import json
from app.student import StudentUser
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course
from datetime import datetime

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance = []
        self.next_lesson_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # The logic here remains the same, but the source of the Course class has changed.
                # TODO: For each dictionary in data['students'], create a StudentUser object and append to self.
                #students.
                for student_data in data["students"]:
                    student = StudentUser(student_data["id"], student_data["name"])
                    student.enrolled_course_ids.extend(student_data["enrolled_course_ids"])
                    self.students.append(student)
                # TODO: Do the same for teachers (creating TeacherUser objects).
                for teacher_data in data["teachers"]:
                    teacher = TeacherUser(teacher_data["id"], teacher_data["name"], teacher_data["speciality"])
                    self.teachers.append(teacher)
                # TODO: Do the same for courses (creating Course objects).
                for course_data in data["courses"]:
                    course = Course(course_data["id"], course_data["name"], course_data["instrument"], course_data["teacher_id"])
                    course.enrolled_student_ids.extend(course_data["enrolled_student_ids"])
                    course.lessons.extend(course_data["lessons"])
                    self.courses.append(course)
                self.attendance = data.get("attendance", [])
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # The logic here remains the same.
        # TODO: Create a 'data_to_save' dictionary.
        # Convert self.students, self.teachers, and self.courses into lists of dictionaries.
        # Write the result to the JSON file.
        data_to_save = {
            "students": [],
            "teachers": [],
            "courses": [],
            "attendance": []
        }
        for student in self.students:
            student_dic = {
                "id": student.id,
                "name": student.name,
                "enrolled_course_ids": student.enrolled_course_ids
            }
            data_to_save["students"].append(student_dic) 
        for teacher in self.teachers:
            teacher_dic = {
                "id": teacher.id,
                "name": teacher.name,
                "speciality": teacher.speciality
            }
            data_to_save["teachers"].append(teacher_dic)
        for course in self.courses:
            course_dic = {
                "id": course.id,
                "name": course.name,
                "instrument": course.instrument,
                "teacher_id": course.teacher_id,
                "enrolled_student_ids": course.enrolled_student_ids,
                "lessons": course.lessons
            }
            data_to_save["courses"].append(course_dic)
        data_to_save["attendance"] = self.attendance        

        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4)

    def find_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student        
        return

    def register_new_student(self, student_name, student_instrument):
        student = StudentUser(0, "") 
        if self.students:
           student.id = max(s.id for s in self.students) + 1
        else:
           student.id = 1
        student.name = student_name
        for course in self.courses:
            if course.instrument.lower() == student_instrument.strip().lower():
                student.enrolled_course_ids.append(course.id)
                course.enrolled_student_ids.append(student.id)
                self.students.append(student)
                self._save_data()
                return student
        return 

    def check_in(self, student_id, course_id):
        student = None
        course = None

        for s in self.students:
            if s.id == student_id:
                student = s
        for c in self.courses:
            if c.id == course_id:
                course = c
        if student is None or course is None:
            return False
        if course_id not in student.enrolled_course_ids:
            return False

        attendance_record = {
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": datetime.now().isoformat()
        }
        self.attendance.append(attendance_record)
        self._save_data()
        return True

