# tests/test_schedule_manager.py
import pytest
import os
from app.schedule import ScheduleManager
from app.student import StudentUser

# A pytest fixture creates a clean environment for each test function.
@pytest.fixture
def fresh_manager(tmp_path):
    """Creates a fresh ScheduleManager instance using a temporary test data file."""
    test_file = tmp_path / "test_data.json"
    return ScheduleManager(data_path=test_file)

def test_create_course(fresh_manager):
    # ARRANGE: We have a fresh manager from the fixture.
    # ACT: Call the method we want to test.
    fresh_manager.create_course("Beginner Piano", "Piano", 1)
    # ASSERT: Check if the outcome is what we expect.
    assert len(fresh_manager.courses) == 1
    assert fresh_manager.courses[0].name == "Beginner Piano"

def test_record_payment_and_history(fresh_manager):
    # ARRANGE: Add a dummy student to the manager for the test.
    # This test verifies the core financial logic you added in Fragment 5.1.
    # fresh_manager.students.append(...)
    student_id_to_test = 1
    fresh_manager.students.append(StudentUser(student_id_to_test, "shen"))
    # ACT: Record a payment for that student.
    fresh_manager.record_payment(student_id_to_test, 100.00, "Credit Card")
    
    # ACT 2: Get the payment history.
    history = fresh_manager.get_payment_history(student_id_to_test)

    # ASSERT: Check the results.
    assert len(history) == 1
    assert history[0]['amount'] == 100.00
    assert history[0]['method'] == "Credit Card"
    
def test_get_payment_history_no_results(fresh_manager):
    # TODO: Implement a test that checks if get_payment_history
    # returns an empty list for a student with no payments.
    student_id_to_test = 2
    fresh_manager.students.append(StudentUser(student_id_to_test, "lee"))
    
    history = fresh_manager.get_payment_history(student_id_to_test)
    assert history == []
# tests/test_schedule_manager.py
# ... (fixture setup) ...

def test_check_in_saves_attendance(fresh_manager):
    from datetime import datetime

    fresh_manager.create_course("Beginner Piano", "Piano", 1)
    student = fresh_manager.register_new_student("Shen", 1)

    assert fresh_manager.check_in(student.id, 1) is True
    saved_manager = ScheduleManager(fresh_manager.data_path)
    record = saved_manager.attendance[0]
    assert record["student_id"] == student.id
    assert record["course_id"] == 1
    assert datetime.fromisoformat(record["timestamp"])


@pytest.mark.parametrize("search_term", [1, "1", " 1 ", "Shen", " shEN "])
def test_find_student_by_name_or_id(fresh_manager, search_term):
    student = StudentUser(1, "Shen")
    fresh_manager.students.append(student)
    assert fresh_manager.find_students(search_term) is student


def test_find_student_no_match(fresh_manager):
    fresh_manager.students.append(StudentUser(1, "Shen"))
    assert fresh_manager.find_students("Unknown") is None
