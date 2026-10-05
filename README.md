# User Database Management System

A simple desktop **User Database Management System** built with **Python, Tkinter, Pandas, and Excel**.

This project was created as a practical Python project to practice working with GUI applications, data management, CRUD operations, and Excel files.

## Features

* ➕ Add new users
* 🔍 Search users by ID, name, phone, or address
* ✏️ Update user information
* 🗑️ Delete users
* 📋 Display all users
* 🔄 Refresh the database
* 💾 Save all data directly to an Excel file
* 📊 Display users in a structured table using Tkinter Treeview

## Technologies Used

* **Python**
* **Tkinter** – Desktop GUI
* **Pandas** – Data manipulation
* **Excel** – Data storage
* **OS** – File handling

## How It Works

The application uses an Excel file as a simple database.

When the application starts, it checks if the Excel file exists:

* If it exists, the existing data is loaded.
* If it does not exist, a new database structure is created.

Users can then add, search, update, and delete records through the graphical interface.

All changes are saved back to the Excel file.

## Project Structure

```text
User-Database-Management-System/
│
├── main.py
├── database.xlsx
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/user-database-management-system.git
```

### 2. Open the project folder

```bash
cd user-database-management-system
```

### 3. Install the required libraries

```bash
pip install pandas openpyxl
```

> Tkinter is usually included with standard Python installations on Windows.

### 4. Run the application

```bash
python main.py
```

## What I Learned

Through this project, I practiced:

* Building a desktop GUI with Tkinter
* Working with Pandas DataFrames
* Reading and writing Excel files
* Implementing CRUD operations
* Searching and filtering data
* Connecting a GUI with stored data
* Improving the user experience of a Python application

## Future Improvements

Some possible improvements for the project:

* Add user login and authentication
* Move from Excel to SQLite
* Add sorting and filtering options
* Add data validation
* Add better error handling
* Improve the UI and user experience

## Author

**Ghazi Shatnawi**

Computer Science Student @ Yarmouk University

---

⭐ If you find this project useful, feel free to explore the code and give it a star.
