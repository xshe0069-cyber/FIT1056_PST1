# PST5 - Music School Management System

**FIT1056 - Introduction to Software Engineering**  
**Student ID: 33703396**

## Overview

PST5 implements the Quality & Finance Gate for the Music School Management System (MSMS). It provides financial tracking and CSV reporting, a Streamlit finance interface, logging, timestamped backups, and automated tests. Student registration, lookup, daily rosters, and attendance check-in are also available in the integrated application.

## PST5 components

| Component | Implementation |
| --- | --- |
| Finance and reporting engine | `app/schedule.py`: payment records, payment history, JSON persistence, and CSV export. |
| Finance GUI | `gui/finance_pages.py`: payment entry and student payment history. `gui/main_dashboard.py` connects the page to navigation. |
| Automated test suite | `tests/test_schedule_manager.py`: pytest fixtures and tests for controller behavior. |
| Administrative utilities | `app/admin_utils.py`: file logging and timestamped JSON backups, called from `main.py`. |

## Folder structure

```text
PST5/
  README.md
  main.py
  app/
    user.py
    student.py
    teacher.py
    schedule.py
    admin_utils.py
  gui/
    main_dashboard.py
    student_pages.py
    roster_pages.py
    finance_pages.py
  data/
    msms.json
  tests/
    test_schedule_manager.py
```

`Fragment5_1.py` and `Fragment5_2.py` are reference/development fragments. The integrated application starts from `main.py`. Running the application also generates `msms.log` and files in `data/backups/`.

## Installation and startup

Requirements: Python, Streamlit, pandas, and pytest. The current test suite has been run with Python 3.14.

From the repository root, enter this folder:

```powershell
cd FIT1056-PSTs-33703396/PST5
```

Create a virtual environment, install dependencies, and start the application:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install streamlit pandas pytest
.\.venv\Scripts\python.exe -m streamlit run main.py
```

If your current Python environment already has the dependencies installed, use:

```powershell
python -m streamlit run main.py
```

Open the URL printed in the terminal. Press `Ctrl+C` to stop the server.

Run the app from **this PST5 directory** because data, backup, and log paths are relative to the working directory. Registration, check-in, and payment operations update `data/msms.json`; make a copy before experimenting with the supplied records.

## Using the pages

### Student Management

- Search using a student ID or full name. Search ignores capitalization and surrounding spaces and returns the first exact match.
- To register, enter a name and instrument and click **Find courses**.
- Choose a matching course ID and click **Register Student**. Registration adds the student to that course and saves the data.

### Daily Roster

- Select Monday to Friday to view scheduled lessons, including course name, instrument, start time, and room.
- Select a student and course, then click **Check-in Student**.
- Check-in succeeds only when both records exist and the student is enrolled in the selected course. Attendance records include a timestamp and are saved to JSON.

### Finance & Payments

The navigation currently calls this page **Payments (stub)**, but it opens the implemented finance interface.

- Select a student, enter a payment amount and method, and click **Record Payment**.
- Use the history selector to view transactions for one student.
- Payment records contain `student_id`, `amount`, `method`, and an ISO-formatted timestamp.

`record_payment(student_id, amount, method)` handles payment recording and `get_payment_history(student_id)` retrieves matching transactions. The local implementation rejects nonpositive amounts, blank methods, and unknown students, returns a success flag, and prevents payment entry when no students exist.

## CSV reports

Reports are exported through `ScheduleManager`; there is currently no export button in the GUI. From the PST5 directory, open Python using `python` or `.\.venv\Scripts\python.exe`, then run:

```python
from app.schedule import ScheduleManager

manager = ScheduleManager()
manager.export_report("finance", "finance_report.csv")
manager.export_report("attendance", "attendance_report.csv")
```

- Finance columns: `student_id`, `amount`, `method`, `timestamp`.
- Attendance columns: `student_id`, `course_id`, `timestamp`.

Relative output paths create files in the current directory. These commands overwrite existing files with the same names.

## Logging and backups

- `init_logger()` configures `msms.log` with timestamps, severity levels, and messages.
- Successful payments are logged at INFO level; lesson cancellations are logged at WARNING level.
- `backup_data()` copies the JSON data into `data/backups/msms_backup_YYYY-MM-DD_HH-MM-SS.json` and logs the outcome.
- `main.py` calls these utilities before launching the dashboard. Because Streamlit reruns the entry script during interactions, backups may be created repeatedly within a session. Backup rotation and automatic restoration are not implemented.

## Running the tests

From this directory:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

Or, with your active Python environment:

```powershell
python -m pytest tests -q
```

The tests use Arrange, Act, Assert and pytest's `tmp_path` fixture. Temporary JSON files keep tests separate from the application's real data.

Current coverage includes:

- Course creation.
- Payment recording and history retrieval.
- Empty payment history.
- Check-in and attendance persistence after reloading.
- Lookup by integer ID, string ID, and case-insensitive full name.
- A search with no matching student.

The suite currently reports **10 passed**, including five parameterized search cases. Dedicated automated tests for CSV export, backups, logging, and additional invalid-input conditions remain to be added.

## Suggested demonstration

1. Search for an existing student by ID and name.
2. Register a student into an available course.
3. Check that student into the enrolled course.
4. Record a payment and view the student's payment history.
5. Export finance and attendance CSV files using the controller.
6. Restart the app and check that saved records remain available.
7. Inspect `msms.log` and a generated backup file.

These steps change application data. Automated tests use separate temporary files.

## Design choices and assumptions

- `User`, `StudentUser`, `TeacherUser`, and `Course` represent domain data. `ScheduleManager` manages business operations and persistence. Streamlit pages call the controller rather than writing JSON directly.
- The manager is stored in Streamlit session state so page changes preserve the current session's objects.
- Students and courses are linked through integer IDs. JSON stores students, teachers, courses, attendance, and finance records in a readable local file.
- This is a single-user educational application. Concurrent sessions are not synchronized and can overwrite changes.
- Timestamps use local computer time without timezone information. Monetary values use Python numbers rather than decimal currency arithmetic.
- Name-based dropdown dictionaries assume unique student names. Duplicate names can hide an entry; lookup by name returns only the first match.
- The data file is expected to contain valid JSON and the required fields. Corrupted data, filesystem failures, and concurrent writes are not comprehensively handled.
- Some controller operations, including teacher maintenance and CSV export, are not exposed through the GUI.

## Version control

PST5 work is tracked on the repository's `individual` branch. Review and test source changes before committing and pushing. This README documents the local PST5 implementation; source edits must also be committed and pushed for GitHub to contain those changes.
