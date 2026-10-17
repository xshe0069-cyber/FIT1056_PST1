# Music School Management System - PST5

FIT1056 - Introduction to Software Engineering, Semester 2, 2026  
Student ID: 33703396

## Overview

This individual project develops a Music School Management System (MSMS) through five stages. PST1 introduces an in-memory prototype; PST2 adds file storage and validation; PST3 introduces object-oriented models; PST4 adds a Streamlit GUI; PST5 adds finance, CSV reporting, logging, backups, and automated tests. This directory contains the integrated PST5 application based on the revised materials.

## Features and assignment parts

| Part | Implementation |
| --- | --- |
| Finance and reporting (5.1) | `ScheduleManager` initializes, loads, and saves `finance_log`; records payments; retrieves a student's payment history; exports finance or attendance records to CSV. |
| Finance GUI (5.2) | The Payments page records payments and displays payment history. The dashboard connects this page to the navigation menu. |
| Admin utilities (5.3) | `init_logger()` configures timestamped file logging; `backup_data()` creates timestamped copies of the JSON data. |
| Lifecycle integration (5.4) | `main.py` initializes logging and attempts one startup backup per Streamlit session before launching the GUI. Registration, payments, check-ins, and lesson cancellations produce log entries. The sidebar includes a Backup Now button. |
| Automated tests (also labelled 5.4 in the revised PDF) | pytest tests cover course creation, payments and history, empty history, attendance persistence, student searches, CSV exports, backup success/failure, and Streamlit backup lifecycle. |

Earlier functionality remains available: searching for students by name or ID, registering a student into an available instrument course, viewing the daily roster, and checking enrolled students into courses.

## Project structure

```text
main.py                       Application entry point
app/
    schedule.py               Business logic and JSON persistence
    student.py                Student model
    teacher.py                Teacher and course models
    user.py                   Shared user model
    admin_utils.py            Logging and backup utilities
gui/
    main_dashboard.py         Navigation and manual backup button
    student_pages.py          Student search and registration
    roster_pages.py           Daily roster and attendance check-in
    finance_pages.py          Payment recording and history
data/
    msms.json                 Application data
    backups/                  Generated backup files
tests/
    test_schedule_manager.py  Automated unit tests
pytest.ini                    Project import path and test discovery settings
package_submission.py         Builds a clean submission ZIP
Fragment5_1.py                Supplied finance reference fragment
Fragment5_2.py                Supplied logging reference fragment
```

## Installation and running

Use Python 3 and install Streamlit, pandas, and pytest. Run all commands below from this directory (the directory containing this README and `main.py`). Paths containing spaces must be quoted in PowerShell.

```powershell
cd "C:\homework\FIT1056_Works\FIT1056-PSTs-33703396\PST5 Material\PST5 Material"
python -m pip install streamlit pandas pytest
python -m streamlit run main.py
```

Open the local URL printed by Streamlit. Stop the server with Ctrl+C. Launch the integrated application through `main.py`; the fragment files are reference material rather than the application entry point.

## Using the application

1. **Student Management:** search by a student's name or ID. To register, enter a name and instrument, click Find courses, select a course, and click Register Student.
2. **Daily Roster:** choose a weekday to view lessons. Select an enrolled student and course, then click Check-in Student.
3. **Payments:** select a student, enter a positive amount and a nonblank payment method, then click Record Payment. Select a student in the history section to view recorded payments.
4. **Backup Now:** click the sidebar button to copy the saved JSON file into `data/backups/`. The page displays a success or failure message.

### Exporting CSV reports

CSV export is a backend method; the current GUI has no export button. From the project directory, use:

```powershell
python -c "from app.schedule import ScheduleManager; m = ScheduleManager(); m.export_report('finance', 'finance_report.csv'); m.export_report('attendance', 'attendance_report.csv')"
```

Finance CSV columns are `student_id`, `amount`, `method`, and `timestamp`. Attendance CSV columns are `student_id`, `course_id`, and `timestamp`.

## Automated tests

```powershell
pytest
```

Alternatively, use the current Python interpreter explicitly:

```powershell
python -m pytest tests/test_schedule_manager.py -q
```

The suite produces 20 test cases, including parameterized report and backup lifecycle checks. Tests follow Arrange, Act, Assert and use pytest's `tmp_path` fixture for isolated data files rather than modifying `data/msms.json`.

`pytest.ini` sets `pythonpath = .` and `testpaths = tests`, so both `pytest` and `python -m pytest` work from this directory. The optional pytest cache is disabled. `tests/conftest.py` chooses a fresh project-local `.pytest_tmp_<unique ID>` directory on each run, avoiding system Temp permissions and reuse of directories owned by another Windows account. An explicit `--basetemp` still takes precedence. These generated test directories are excluded from Git and the submission ZIP; remove your own old test directories when no longer needed. A successful run reports `20 passed`. Tests use temporary files and mock backup calls in the Streamlit lifecycle test.

### Manual verification

- Register a student and find them by both name and ID.
- View a day's roster and check in an enrolled student.
- Record a valid payment, verify its history, and restart the application to check persistence.
- Try a blank payment method and confirm that the payment is rejected.
- Export both CSV report types and inspect their headers and records.
- Verify that one backup is attempted on launch, ordinary interactions create no additional backups, and Backup Now still creates a backup.
- Check `msms.log` for registration, payment, check-in, and backup entries. Lesson cancellation logging can be verified through the backend method.

## Logging and backups

Logs append to `msms.log` with a timestamp, severity, and message. Registration, payments, check-ins, and successful backups use INFO; lesson cancellation currently uses WARNING; failed file-copy operations use ERROR.

Backups use names such as `msms_backup_2026-10-15_14-30-00_123456.json`. To restore one, stop the application, preserve the current JSON file, copy the selected backup over `data/msms.json`, and restart the application.

A session-state flag limits startup backup to one attempt per session, including when the attempt fails. Use Backup Now to retry manually. A new browser session or browser reload can trigger a new startup backup. Filenames include microseconds to reduce same-second filename collisions.

## Design choices and assumptions

- **Separation of responsibilities:** model classes represent users and courses, `ScheduleManager` handles business rules and storage, and GUI modules handle display and input.
- **JSON storage:** students, teachers, courses, attendance, and finance records are stored together. Missing optional attendance or finance lists default to empty lists. Existing JSON must have the expected student, teacher, and course structure.
- **Session state:** Streamlit keeps one manager in session state across page reruns. Successful data-changing operations save to JSON.
- **Local execution:** relative paths assume execution from this project directory. This is a local coursework application; concurrent writes from multiple users or processes are not coordinated.
- **Student identity:** backend operations use IDs. Search matches an exact ID or an exact name, ignoring name case and surrounding search whitespace. GUI dropdowns use names as dictionary keys, so unique student names are assumed.
- **Payments:** amounts must be positive, payment methods must contain text, and the student must exist. Monetary values currently use Python numeric values without a separate currency or decimal-accounting model.
- **Scope:** CSV exports and lesson cancellation are available through backend methods; they do not have dedicated GUI controls. Tests cover selected core behaviour, not all error cases. Malformed JSON and some filesystem errors are not handled comprehensively.

## Submission

Complete the manual checks and automated tests, then commit and push the intended source files on the individual branch. Include this README and `pytest.ini`; avoid adding generated temporary directories, Python caches, or logs unintentionally. Follow the required Moodle submission process as well as GitHub submission, and be prepared to explain and modify the code during the demonstration.

The assignment requests one main README at the repository root. This document describes the revised PST5 directory; ensure the repository-root README also points to this version and explains the other PST stages before final submission.

### Clean submission ZIP

Run `python package_submission.py` from this directory. It creates `../PST5_submission.zip`, excluding Python caches, pytest caches and temporary directories, logs, generated backups, macOS metadata, virtual environments, and ZIP files. Source code, tests, configuration, README, supplied PDFs/fragments, and `data/msms.json` are retained. Local runtime files are left in place.
