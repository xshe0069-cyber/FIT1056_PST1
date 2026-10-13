# Music School Management System (MSMS)

FIT1056 individual problem-solving tasks (PST1-PST5). Student ID: 33703396.

This repository records the development of a music school management system from an in-memory prototype to an object-oriented Streamlit application with financial records, logging, backups, and automated tests. **PST5 is the latest application.** Earlier directories preserve previous stages and supplied materials.

## Development stages

All stage directories are under `FIT1056-PSTs-33703396/`.

| Stage | Directory | Purpose |
| --- | --- | --- |
| PST1 | `PST1/` | In-memory student and teacher management, enrolment, and console interaction fragments. |
| PST2 | `PST2/` | JSON persistence and procedural application logic in `pst2_main.py`. |
| PST3 | `PST3_Materials/PST3_Materials/` | Object-oriented models and a central `ScheduleManager`, with a console view. |
| PST4 | `PST4_Materials/PST4_Materials/` | Streamlit student management, daily roster, and check-in pages. |
| PST5 | `PST5/` | Finance and reporting, administrative utilities, and pytest tests, building on the GUI. |

The `Fragment*.py` files are development templates or individual task fragments; use `PST5/main.py` to run the latest integrated application.

## Setup and run PST5

Prerequisites: Git and Python. The current application has been tested with Python 3.14. Dependencies are Streamlit, pandas, and pytest.

Clone the repository and enter the latest application directory:

```powershell
git clone --branch individual https://github.com/xshe0069-cyber/FIT1056_PST1.git
cd FIT1056_PST1/FIT1056-PSTs-33703396/PST5
```

Create a virtual environment and install dependencies on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install streamlit pandas pytest
.\.venv\Scripts\python.exe -m streamlit run main.py
```

Open the local URL printed by Streamlit. Stop the server with `Ctrl+C`. If using an existing environment, run `python -m streamlit run main.py` instead.

**Run commands from the PST5 directory.** Data, log, and backup paths are relative to the working directory. The app writes to the supplied data file, so use a copy when experimenting with sample records.

## Using the application

- **Student Management:** search by numeric ID or full name. Search ignores case and leading/trailing spaces. To register, enter a name and instrument, click **Find courses**, select a matching course ID, then click **Register Student**.
- **Daily Roster:** select a weekday to view lesson names, instruments, start times, and rooms. Select a student and course to check in. The student must already be enrolled in that course.
- **Payments (stub):** despite the retained navigation label, this opens the implemented finance page. Select a student, enter an amount and payment method, and submit. Select a student in the history section to view their transactions.

Courses and teachers are loaded from the JSON file. The GUI does not provide every controller operation, such as teacher maintenance or CSV export.

## PST5 structure and responsibilities

```text
PST5/
  main.py                       # Logging, backup, and GUI startup
  app/
    user.py                     # Base user model
    student.py                  # Student model and course IDs
    teacher.py                  # Teacher and Course models
    schedule.py                 # Business logic, persistence, and CSV reports
    admin_utils.py              # Logger configuration and timestamped backups
  gui/
    main_dashboard.py           # Navigation and session-state manager
    student_pages.py            # Search and registration
    roster_pages.py             # Weekday roster and check-in
    finance_pages.py            # Payment recording and history
  data/
    msms.json                   # Application records
    backups/                    # Generated backup files
  tests/
    test_schedule_manager.py    # Automated controller tests
```

### Finance and reporting

`ScheduleManager` stores payments in `finance_log`. Each record contains `student_id`, `amount`, `method`, and an ISO-formatted timestamp. `get_payment_history(student_id)` filters these records for one student. Finance and attendance records are included in JSON saving and loading.

CSV export is available through the controller rather than a GUI button. From PST5, start `python` (or `.\.venv\Scripts\python.exe`) and run:

```python
from app.schedule import ScheduleManager

manager = ScheduleManager()
manager.export_report("finance", "finance_report.csv")
manager.export_report("attendance", "attendance_report.csv")
```

The files are written to the current directory. Finance columns are `student_id, amount, method, timestamp`; attendance columns are `student_id, course_id, timestamp`.

### Logging and backups

`init_logger()` configures `msms.log` with timestamps, severity levels, and messages. Payment recording and lesson cancellation produce log entries. `backup_data()` copies `data/msms.json` to a timestamped file in `data/backups/` and logs success or failure.

Both utilities are called in `main.py` before launching the GUI. Streamlit reruns the entry script during interactions, so backup creation can run more than once during a browser session. Backups are not automatically rotated or restored.

## Automated tests

From the PST5 directory, run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

With dependencies already installed in your active Python environment:

```powershell
python -m pytest tests -q
```

Tests use pytest's `tmp_path` fixture to isolate JSON files from real application data. They follow Arrange, Act, Assert and currently cover:

- Course creation.
- Payment recording and history retrieval, including empty history.
- Successful check-in and attendance persistence after reloading.
- Student lookup by numeric ID, string ID, and case-insensitive full name.
- Missing-student search results.

The current suite reports **10 passed**; five cases come from a parameterized lookup test. This does not mean every function or error condition is tested. CSV exports, logging, backups, and further invalid-input cases still need dedicated automated coverage.

For a manual demonstration, search for an existing student, register a student into an available course, check in to that course, record a payment, inspect its history, and export both CSV reports. Restart the app to check persistence, and inspect the log and backup directory. Manual operations change application data.

## Design choices and assumptions

- Models represent students, teachers, and courses. `ScheduleManager` owns business rules and persistence; GUI functions call the manager instead of directly editing JSON.
- The manager is stored in Streamlit session state so it survives page changes within a session.
- Students and courses are connected by integer IDs. Check-in requires a valid student, a valid course, and enrolment.
- JSON is used for readable, lightweight local storage. This is a single-user teaching application; concurrent browser sessions are not coordinated and can overwrite one another's changes.
- Timestamps use the computer's local time without timezone information.
- Student lookup returns the first exact full-name or ID match, not partial-name results. Name-based dropdown dictionaries assume distinct student names; duplicate names can hide an entry.
- Data files are expected to contain valid JSON with the required student, teacher, and course fields. Malformed JSON, inaccessible paths, and write failures are not comprehensively handled.
- Monetary amounts use Python numbers rather than a dedicated decimal currency model. The application is an educational prototype, not a production accounting system.

## Git workflow

Work is tracked on the `individual` branch with commits for the development stages. After reviewing and testing a change, stage the intended files, commit with a descriptive message, and push to `origin individual`. Generated bytecode, logs, backups, and unrelated local files are not needed to explain source changes.
