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

    def check_instrument_courses(self, student_instrument):
         find_courses = []
         for course in self.courses:
              if course.instrument.lower() == student_instrument.strip().lower():
                   find_courses.append(course.id)
         return find_courses
                        
    def register_new_student(self, student_name, selected_course_id):
        student = StudentUser(0, "") 
        if self.students:
           student.id = max(s.id for s in self.students) + 1
        else:
           student.id = 1
        student.name = student_name
        if selected_course_id != None:
                for course in self.courses:
                     if course.id == selected_course_id:       
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

    def daily_roster(self, day):
        roster_data = []
        for course in self.courses:
                 for lesson in course.lessons:
                     if lesson["day"] == day:
                         roster_data.append({"name": course.name,
                                             "instrument": course.instrument,
                                             "start_time": lesson["start_time"],
                                             "room": lesson["room"]})
        return roster_data                 
         

    def _find_by_id(self, item, target_id):
            for item in item:
                if item.id == target_id:
                   return item
            return None

    def _get_next_id(self, items):
        if items:
           return max(item.id for item in items) + 1
        return 1

    def find_student_by_id(self, student_id):
            return self._find_by_id(self.students, student_id)
    
    def find_course_by_id(self, course_id):
            return self._find_by_id(self.courses, course_id)
    
    def find_teacher_by_id(self, teacher_id):
            return self._find_by_id(self.teachers, teacher_id)
        
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
