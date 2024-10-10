from tkinter import *
from tkinter import ttk
import tkinter 
import random
from tkinter import messagebox
import pymysql
import csv
from datetime import datetime
import numpy as np

# Create the main window for the application
window = tkinter.Tk() 
window.title("Student Record") 
window.geometry("1009x640")  
myTable = ttk.Treeview(window, show='headings', height=20)  
style = ttk.Style()  

# An array to hold placeholders (StringVars) for student data input fields
placeholderArray = ['', '', '', '', '', '']


# Initialize each element as a tkinter StringVar.
for i in range(0, 6):
    placeholderArray[i] = tkinter.StringVar()  


def connection():
    conn=pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='studentsrecorddb'
    )
    return conn

    conn = connection()
    cursor = conn.cursor()

def read():
    conn = connection()
    cursor = conn.cursor()

    cursor.connection.ping()
    sql = f"SELECT `ID`, `NAME`, `COURSE / PROGRAM`, `YEAR LEVEL`, `AGE`, `SEX` FROM `studentsrecorddb`.`students`;"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

# Table Start

def refreshTable():
    # Clear the table before inserting new data
    for data in myTable.get_children():
        myTable.delete(data)
    
    # Insert each array from dummydata into the Treeview
    for array in read():
        myTable.insert(parent='', index='end', iid=array[0], text="", values=(array), tag='orow')
    
    myTable.tag_configure('orow', background="white")
    myTable.pack()


def save():
    # Get the input values
    StudentID = str(idField.get())
    StudentNAME = str(nameField.get())
    StudentPROGRAM = str(courseField.get())
    StudentYEARLVL = str(yearField.get())
    StudentAGE = str(ageField.get())
    StudentSEX = str(sexField.get())

    # Validate the ID for being a 6-digit number
    if len(StudentID) != 6 or not StudentID.isdigit():
        messagebox.showwarning("Error", "ID must be exactly 6 digits.")
        return

    try:
        # Establish a connection to the database
        conn = connection()
        cursor = conn.cursor()

        # Updated SQL query to insert data with correct column names
        sql = """
        INSERT INTO students (id, name, `COURSE / PROGRAM`, `YEAR LEVEL`, age, sex)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (StudentID, StudentNAME, StudentPROGRAM, StudentYEARLVL, StudentAGE, StudentSEX)

        # Execute the SQL query and commit to the database
        cursor.execute(sql, values)
        conn.commit()

        # Display a success message
        messagebox.showinfo("Success", "Record saved successfully!")

        # Refresh the table to show the new record
        refreshTable()

        # Clear the text fields after saving
        clear_fields()

    except pymysql.Error as e:
        # Handle any errors with the database interaction
        messagebox.showerror("Database Error", f"Failed to insert record into database: {e}")

    finally:
        # Close the database connection
        conn.close()

# Function to clear all text fields
def clear_fields():
    idField.delete(0, 'end')
    nameField.delete(0, 'end')
    courseField.set('')
    yearField.set('')
    ageField.delete(0, 'end')
    sexField.set('')
    # Restore the placeholder text in the name field
    nameField.insert(0, namePlaceholder)
    nameField.config(fg="grey")  # Set text color to grey to indicate it's a placeholder

def update_action():
    # Get the selected item from the Treeview
    selected_item = myTable.selection()
    
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a record to update.")
        return

    # Assuming only one item can be selected at a time
    item = selected_item[0]
    
    # Get the ID of the selected record for updating
    student_id = myTable.item(item, "values")[0]

    # Get the input values
    StudentNAME = str(nameField.get())
    StudentPROGRAM = str(courseField.get())
    StudentYEARLVL = str(yearField.get())
    StudentAGE = str(ageField.get())
    StudentSEX = str(sexField.get())

    # Validate the ID for being a 6-digit number
    if len(student_id) != 6 or not student_id.isdigit():
        messagebox.showwarning("Error", "ID must be exactly 6 digits.")
        return

    try:
        # Establish a connection to the database
        conn = connection()
        cursor = conn.cursor()

        # Updated SQL query to update the student record
        sql = """
        UPDATE students
        SET name = %s, `COURSE / PROGRAM` = %s, `YEAR LEVEL` = %s, age = %s, sex = %s
        WHERE id = %s
        """
        values = (StudentNAME, StudentPROGRAM, StudentYEARLVL, StudentAGE, StudentSEX, student_id)

        # Execute the SQL query and commit to the database
        cursor.execute(sql, values)
        conn.commit()

        # Display a success message
        messagebox.showinfo("Success", "Record updated successfully!")

        # Refresh the table to show the updated record
        refreshTable()

        # Clear the text fields after updating
        clear_fields()

    except pymysql.Error as e:
        # Handle any errors with the database interaction
        messagebox.showerror("Database Error", f"Failed to update record in database: {e}")

    finally:
        # Close the database connection
        conn.close()

def clear_fields():
    """ Clear all input fields """
    idField.delete(0, "end")
    nameField.delete(0, "end")
    nameField.insert(0, namePlaceholder)  # Restore placeholder
    nameField.config(fg="grey")  # Reset text color to grey
    courseField.set('')  # Clear ComboBox
    yearField.set('')    # Clear ComboBox
    ageField.delete(0, "end")
    sexField.set('')      # Clear ComboBox


# Function to delete a selected record from the table and database
def delete():
    # Get the selected item from the Treeview
    selected_item = myTable.selection()
    
    if not selected_item:
        messagebox.showwarning("Select a record", "Please select a record to delete.")
        return

    # Ask for confirmation before deleting
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    
    if confirm:  # If the user clicks "Yes"
        # Get the ID of the selected item
        selected_id = myTable.item(selected_item)['values'][0]

        try:
            # Establish a connection to the database
            conn = connection()
            cursor = conn.cursor()

            # SQL query to delete the record
            sql = "DELETE FROM students WHERE id = %s"
            cursor.execute(sql, (selected_id,))

            # Commit the changes
            conn.commit()
            messagebox.showinfo("Success", "Record deleted successfully!")

            # Refresh the table to show the updated records
            refreshTable()

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete record: {e}")

        finally:
            conn.close()
    else:
        messagebox.showinfo("Cancelled", "Delete operation cancelled.")

def select_action():
    # Get the selected item from the Treeview
    selected_item = myTable.selection()
    
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a record to display.")
        return

    # Assuming only one item can be selected at a time
    item = selected_item[0]
    
    # Retrieve values from the selected item
    values = myTable.item(item, "values")
    
    # Populate the entry fields with the selected values
    idField.delete(0, "end")  # Clear the field
    idField.insert(0, values[0])  # ID

    nameField.delete(0, "end")
    nameField.insert(0, values[1])  # NAME
    nameField.config(fg="black")  # Change the text color to black after selection

    courseField.set(values[2])  # COURSE / PROGRAM
    yearField.set(values[3])  # YEAR LEVEL
    ageField.delete(0, "end")
    ageField.insert(0, values[4])  # AGE

    sexField.set(values[5])  # SEX

# Define a variable for button color to maintain consistency
frameColor = "#800000"
btnColor = "#3B4D61"

# Create a Frame widget that will hold other widgets like buttons, labels, etc.
frame = tkinter.Frame(window, bg = frameColor) 
frame.pack()

formFrame = tkinter.LabelFrame(frame, text="Student Form", borderwidth=5, bg=frameColor, fg='white') 
formFrame.grid(row=0, column=0, sticky="w", padx=[10, 15], pady=20, ipadx=[6])

# ComboBox List
courseList = ['Bachelor of Science in Information Technology', 'Bachelor of Science in Computer Science', 'Bachelor of Science in Computer Engineering']
yearList = ['1st', '2nd', '3rd', '4th']
sexList = ['MALE', 'FEMALE']

# Place Holder 
idPlaceholder = "ID search"
namePlaceholder = "Last Name, First Name M.I."

# Form Label
idLabel = Label(formFrame, text="ID", anchor="e", width=20, background=frameColor, fg='white')
nameLabel = Label(formFrame, text="NAME", anchor="e", width=20, background=frameColor, fg='white')
courseLabel = Label(formFrame, text="COURSE / PROGRAM", anchor="e", width=20, background=frameColor, fg='white')
yearLabel = Label(formFrame, text="YEAR LEVEL", anchor="e", width=20, background=frameColor, fg='white')
ageLabel = Label(formFrame, text="AGE", anchor="e", width=20, background=frameColor, fg='white')
sexLabel = Label(formFrame, text="SEX", anchor="e", width=20, background=frameColor, fg='white')

idLabel.grid(row=0, column=0, padx=20)
nameLabel.grid(row=0, column=2, padx=20)
courseLabel.grid(row=1, column=0, padx=20)
yearLabel.grid(row=1, column=2, padx=20)
ageLabel.grid(row=2, column=0, padx=20)
sexLabel.grid(row=2, column=2, padx=20)

# Form Text Field
idField = Entry(formFrame, width=45, textvariable=placeholderArray[0])
nameField = Entry(formFrame, width=45, textvariable=placeholderArray[1])
courseField = ttk.Combobox(formFrame, width=42, textvariable=placeholderArray[2], values=courseList)
yearField = ttk.Combobox(formFrame, width=42, textvariable=placeholderArray[3], values=yearList)
ageField = Entry(formFrame, width=45, textvariable=placeholderArray[4])
sexField = ttk.Combobox(formFrame, width=42, textvariable=placeholderArray[5], values=sexList)

idField.grid(row=0, column=1, padx=10, pady=10)
nameField.grid(row=0, column=3, padx=10, pady=10)
courseField.grid(row=1, column=1, padx=10, pady=10)
yearField.grid(row=1, column=3, padx=10, pady=10)
ageField.grid(row=2, column=1, padx=10, pady=10)
sexField.grid(row=2, column=3, padx=10, pady=10)

# Insert the placeholder text initially
nameField.insert(0, namePlaceholder)
nameField.config(fg="grey")

# Define function for when the user clicks into the field
def on_name_entry_click(event):
    if nameField.get() == namePlaceholder:
        nameField.delete(0, "end")  # Clear the field
        nameField.config(fg="black")  # Change text color to black

# Define function for when the user leaves the field
def on_name_focus_out(event):
    if nameField.get() == "":  # If field is left empty, restore the placeholder
        nameField.insert(0, namePlaceholder)
        nameField.config(fg="grey")

# Bind the focus in and out events to the nameField
nameField.bind("<FocusIn>", on_name_entry_click)
nameField.bind("<FocusOut>", on_name_focus_out)

# Buttons 

saveBtn = Button(formFrame, text="SAVE", width=20, borderwidth=1, bg=btnColor, fg='white', command = save)
updateBtn = Button(formFrame, text="UPDATE", width=20, borderwidth=1, bg=btnColor, fg='white', command = update_action)
deleteBtn = Button(formFrame, text="DELETE", width=20, borderwidth=1, bg=btnColor, fg='white', command = delete)
selectBtn = Button(formFrame, text="SELECT", width=20, borderwidth=1, bg=btnColor, fg='white', command = select_action)

saveBtn.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
updateBtn.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
deleteBtn.grid(row=3, column=2, padx=10, pady=10, sticky="ew")
selectBtn.grid(row=3, column=3, padx=10, pady=10, sticky="ew")


# Search

# Search Section (new separate frame)
searchFrame = tkinter.Frame(frame, bg="white", bd=2, relief="solid")
searchFrame.grid(row=1, column=0, sticky='w', padx=10, pady=[5, 15])

# Create a separate StringVar for the search field
searchVar = tkinter.StringVar()

# Text Field
searchField = tkinter.Entry(searchFrame, textvariable=searchVar, font=("Arial", 14), bd=0)
searchField.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
searchField.insert(0, idPlaceholder)
searchField.config(fg="grey")

#search start
# Function to handle focus in event (when clicking in the search field)
def on_entry_click(event):
    if searchField.get() == idPlaceholder:
        searchField.delete(0, "end")
        searchField.config(fg="black")


# Function to handle focus out event (when leaving the search field)
def on_focus_out(event):
    if searchField.get() == "":
        searchField.insert(0, idPlaceholder)
        searchField.config(fg="grey")

# Functionality for Find button
def search_action():
    search_term = searchVar.get().strip()  # Get the search term from the search field

    if search_term == idPlaceholder or search_term == "":
        messagebox.showwarning("Warning", "Please enter an ID to search.")
    else:
        found = False
        
        # Clear any current selection
        for row in myTable.get_children():
            myTable.selection_remove(row)
        
        # Loop through the rows in myTable
        for row in myTable.get_children():
            # Get the ID of the current row (first column) as a string
            row_data = str(myTable.item(row)["values"][0])  
            
            # Compare the row's ID with the search term
            if row_data == search_term:
                # Highlight the matching row
                myTable.selection_set(row)
                myTable.see(row)  # Scroll to the matched row
                messagebox.showinfo("Found", "ID Found!")  # Simplified message
                found = True
                break

        if not found:
            messagebox.showwarning("Not Found", f"No match found for ID: {search_term}")

#search ends

# Bind the focus in and out events to the entry field
searchField.bind("<FocusIn>", on_entry_click)
searchField.bind("<FocusOut>", on_focus_out)    

# Find button
findBtn = tkinter.Button(searchFrame, text="Find", font=("Arial", 10), bg="#3B4D61", fg="white", padx=10, pady=5, bd=0, command = search_action)
findBtn.grid(row=0, column=1, padx=10, pady=5)

style.configure(window) # end of the frame


# Table

myTable['columns'] = ("ID", "NAME", "COURSE / PROGRAM", "YEAR LEVEL", "AGE", "SEX")

myTable.column("#0", width=0, stretch=NO)
myTable.column("ID", anchor=CENTER, width=110)  # Center text
myTable.column("NAME", anchor=CENTER, width=220)  # Center text
myTable.column("COURSE / PROGRAM", anchor=CENTER, width=290)  # Center text
myTable.column("YEAR LEVEL", anchor=CENTER, width=130)  # Center text
myTable.column("AGE", anchor=CENTER, width=129)  # Center text
myTable.column("SEX", anchor=CENTER, width=128)  # Center text

myTable.heading("ID", text="ID", anchor=CENTER)  # Center heading
myTable.heading("NAME", text="NAME", anchor=CENTER)  # Center heading
myTable.heading("COURSE / PROGRAM", text="COURSE / PROGRAM", anchor=CENTER)  # Center heading
myTable.heading("YEAR LEVEL", text="YEAR LEVEL", anchor=CENTER)  # Center heading
myTable.heading("AGE", text="AGE", anchor=CENTER)  # Center heading
myTable.heading("SEX", text="SEX", anchor=CENTER)  # Center heading

myTable.tag_configure('orow', background="#FFFFFF")
myTable.pack()

refreshTable()

# Prevent resizing of the window
window.resizable(False,False)
window.mainloop()