This application is a task management tool designed to help users organize and track tasks related to drawings, revisions, and items in a manufacturing or engineering context. It extracts information from drawings and converts it into a structured to-do list, allowing users to manage tasks efficiently. The application uses a graphical user interface (GUI) built with Tkinter and stores task data in a text file.

Features
Task Input:
Enter multiple job numbers (up to 10 at a time).
Input a drawing number and revision number.
Add up to 10 items, each with an item number and description.
Specify the start and end weeks for the tasks in the format yyyyww (e.g., 202342 for the 42nd week of 2023).
Live Preview:
As you enter data, a preview of the tasks is displayed in real-time, showing how they will appear in the task list.
Task List Display:
View all tasks with their details, including job number, drawing number, revision number, item number, item description, start week, and end week.
Tasks that are currently active (based on the current week) are marked with [In Progress].
Add Tasks:
Save the entered tasks to a file and update the task list display.
Delete Tasks:
Remove specific tasks by entering their task number.
Update Task List:
Refresh the task list display to reflect any changes.
Validation:
Ensures that the start and end weeks are in the correct format and that the start week is not after the end week.
Provides warnings and error messages for invalid or missing inputs.

How to Use
Input Data:
Job Numbers: Enter up to 10 job numbers in the grid provided (5 columns, 2 rows).
Drawing Number: Enter the drawing number in the designated field.
Revision Number: Enter the revision number in the designated field.
Start and End Weeks: Enter the start and end weeks for the tasks in the format yyyyww.
Items: Enter up to 10 items, each with an item number and description.
Preview:
As you type, the preview area below the input fields will display how the tasks will look once added. This helps you verify the data before saving.
Add Tasks:
Once all fields are filled correctly, click the "Add" button to save the tasks.
The input fields will be cleared, and the task list will be updated to include the new tasks.
Delete Tasks:
To delete a task, enter its number (as shown in the task list) in the "Job number to delete" field.
Click the "Delete" button to remove the task.
The task list will be updated accordingly.
Update Task List:
Click the "Update" button to refresh the task list display. This is useful if the task file has been modified externally.
Quit:
Click the "Quit" button to close the application.
