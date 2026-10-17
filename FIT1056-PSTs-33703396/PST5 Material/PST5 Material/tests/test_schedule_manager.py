# tests/test_schedule_manager.py
import pytest
import csv
import logging
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest
from app.admin_utils import backup_data
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


@pytest.mark.parametrize("kind,headers", [
    ("finance", ["student_id", "amount", "method", "timestamp"]),
    ("attendance", ["student_id", "course_id", "timestamp"]),
])
@pytest.mark.parametrize("empty", [False, True])
def test_export_report(tmp_path, kind, headers, empty):
    manager = ScheduleManager(tmp_path / "missing.json")
    record = {"student_id": 1, "timestamp": "2026-10-17T12:00:00"}
    if kind == "finance":
        record.update(amount=100.5, method='银行卡, "Card"')
    else:
        record["course_id"] = 2
    records = [] if empty else [record]
    setattr(manager, "finance_log" if kind == "finance" else "attendance", records)
    output = tmp_path / "report.csv"
    manager.export_report(kind, output)
    with output.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        assert reader.fieldnames == headers
        assert list(reader) == [{key: str(value) for key, value in row.items()} for row in records]


def test_unknown_report_does_not_overwrite_file(tmp_path):
    output = tmp_path / "report.csv"
    output.write_text("keep this", encoding="utf-8")
    ScheduleManager(tmp_path / "missing.json").export_report("unknown", output)
    assert output.read_text(encoding="utf-8") == "keep this"


def test_backup_creates_directory_and_preserves_snapshots(tmp_path):
    source = tmp_path / "msms.json"
    destination = tmp_path / "nested" / "backups"
    source.write_bytes(b'{"students": []}')
    assert backup_data(source, destination) is True
    first = next(destination.glob("msms_backup_*.json"))
    assert first.read_bytes() == source.read_bytes()
    source.write_bytes(b'{"students": [{"id": 1}]}')
    assert backup_data(source, destination) is True
    backups = list(destination.glob("msms_backup_*.json"))
    assert len(backups) == 2
    assert first.read_bytes() == b'{"students": []}'
    assert next(path for path in backups if path != first).read_bytes() == source.read_bytes()


def test_missing_backup_source_returns_false(tmp_path, caplog):
    with caplog.at_level(logging.ERROR):
        assert backup_data(tmp_path / "missing.json", tmp_path / "backups") is False
    assert "Failed to create backup" in caplog.text


def test_backup_directory_error_returns_false(tmp_path, caplog):
    blocked = tmp_path / "file"
    blocked.write_text("not a directory")
    with caplog.at_level(logging.ERROR):
        assert backup_data(tmp_path / "msms.json", blocked / "backups") is False
    assert "Failed to create backup" in caplog.text


@pytest.mark.parametrize("success", [True, False])
def test_startup_backup_once_per_session_and_manual_retry(success):
    main = Path(__file__).resolve().parents[1] / "main.py"
    with patch("app.admin_utils.init_logger"), patch("app.admin_utils.backup_data", return_value=success) as backup, patch("gui.main_dashboard.backup_data", return_value=True) as manual_backup:
        app = AppTest.from_file(str(main), default_timeout=15).run()
        assert not app.exception
        assert backup.call_count == 1
        app.run()
        assert not app.exception
        assert backup.call_count == 1
        app.sidebar.button[0].click().run()
        assert not app.exception
        assert backup.call_count == 1
        assert manual_backup.call_count == 1
