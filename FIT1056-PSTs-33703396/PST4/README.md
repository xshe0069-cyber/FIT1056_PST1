\# Music School Management System (MSMS)



\## Overview



This project is a Music School Management System developed for FIT1056 PST4.



PST4 extends the previous object-oriented version of the system by replacing the text-based console interface with a graphical user interface built using Streamlit.



The system separates the graphical user interface from the application logic. The GUI communicates with the `ScheduleManager`, which is responsible for managing students, teachers, courses, lessons, attendance, and JSON data storage.



\---



\## Features



\### Student Management



The Student Management page allows the receptionist to:



\- Search for a student using their student ID.

\- View student information.

\- Register a new student.

\- Select the student's first instrument.

\- Automatically enrol the student into a course that matches the selected instrument.

\- Display appropriate success or error messages.



Student registration is handled through:



`ScheduleManager.register\_new\_student(name, instrument)`



\---



\### Daily Roster



The Daily Roster page allows the receptionist to:



\- Select a weekday.

\- View all lessons scheduled for the selected day.

\- View the course name.

\- View the instrument.

\- View the lesson start time.

\- View the room.



The roster is displayed using a Streamlit dataframe for clearer presentation.



\---



\### Student Check-In



The check-in section allows the receptionist to:



\- Select a student.

\- Select a course.

\- Check the student into the selected course.

\- Receive success or error feedback.



The application verifies that the selected student is enrolled in the selected course before completing the check-in.



Check-in logic is handled through:



`ScheduleManager.check\_in(student\_id, course\_id)`



Attendance information is stored in the JSON data file.



\---



\## Project Structure



```text

PST4\_Materials/

│

├── main.py

│

├── README.md

│

├── app/

│   ├── user.py

│   ├── student.py

│   ├── teacher.py

│   └── schedule.py

│

├── data/

│   └── msms.json

│

└── gui/

&#x20;   ├── main\_dashboard.py

&#x20;   ├── student\_pages.py

&#x20;   └── roster\_pages.py

