from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox, QLabel, QListWidget, 
                             QDialog, QLineEdit, QDateEdit, QHBoxLayout, QVBoxLayout, QDialogButtonBox)
import json
import os

#sihirli bir şekilde json olmadan çalışıyo anlamadım



app = QApplication([])
window = QWidget()
window.setWindowTitle("Library")
window.setWindowIcon(QIcon("icon.png"))
window.resize(900, 600)

# Default data in case of an empty or invalid file
default_data = {}

# Load data from JSON file
def load_data(filename):
    if not os.path.exists(filename):
        return default_data
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return default_data

# Save data to JSON file
def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, sort_keys=True, ensure_ascii=True)

# Load initial data
data = load_data("data.json")

# Widgets
text_late_persons = QLabel("Late Persons")
late_persons = QListWidget()

text_person_info = QLabel("Personal information")
person_infos = QListWidget()
button_add_book = QPushButton("Add Book")
button_del_book = QPushButton("Delete Book")

field_name = QLineEdit("")
field_name.setPlaceholderText("Personal name")
field_book = QLineEdit("")
field_book.setPlaceholderText("Book name")
field_info = QLineEdit("")
field_info.setPlaceholderText("Contact information")
text_date = QLabel("Date to be brought")
field_date = QDateEdit()

text_persons = QLabel("Persons")
persons = QListWidget()
button_add_person = QPushButton("Add person")
button_del_person = QPushButton("Delete person")
button_search_person = QPushButton("Search for a person")

# Layouts
col1 = QVBoxLayout()
col1.addWidget(text_late_persons)
col1.addWidget(late_persons)

col2 = QVBoxLayout()
col2.addWidget(text_persons)
col2.addWidget(persons)
row1 = QHBoxLayout()
row1.addWidget(button_add_person)
row1.addWidget(button_del_person)
col2.addLayout(row1)
col2.addWidget(button_search_person)
col2.addWidget(text_person_info)
col2.addWidget(person_infos)
row2 = QHBoxLayout()
row2.addWidget(button_add_book)
row2.addWidget(button_del_book)
col2.addLayout(row2)
base = QHBoxLayout()
base.addLayout(col1)
base.addLayout(col2)

# Functions
def error_screen(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("ERROR")
    msg.exec_()

def list_late_persons():
    late_persons.clear()
    list1 = []
    for i in data:
        for a in data[i]["Books"]:
            d = data[i]["Books"][a].split(".")
            d = QDate(int(d[2]), int(d[1]), int(d[0]))
            if d < QDate.currentDate():
                list1.append(i)
    late_persons.addItems(set(list1))

def show_person():
    if persons.selectedItems():
        person_infos.clear()
        person = persons.selectedItems()[0].text()
        person_infos.addItem("Name: " + person)
        person_infos.addItem("Communication: " + data[person]["Information"])
        for i in data[person]["Books"]:
            person_infos.addItem("Book: " + i + "  History: " + data[person]["Books"][i])

def show_person2():
    if late_persons.selectedItems():
        person_infos.clear()
        person = late_persons.selectedItems()[0].text()
        person_infos.addItem("Name: " + person)
        person_infos.addItem("Communication: " + data[person]["Information"])
        for i in data[person]["Books"]:
            person_infos.addItem("Book: " + i + "  History: " + data[person]["Books"][i])

def del_person():
    button_search_person.setText("Search for a person")
    if persons.selectedItems():
        person = persons.selectedItems()[0].text()
        del data[person]
        persons.clear()
        person_infos.clear()
        persons.addItems(data)
        list_late_persons()
        save_data("data.json", data)
    elif late_persons.selectedItems():
        person = late_persons.selectedItems()[0].text()
        del data[person]
        persons.clear()
        person_infos.clear()
        persons.addItems(data)
        list_late_persons()
        save_data("data.json", data)
    else:
        error_screen("Select the person to be deleted!")

class person_add():
    def __init__(self):
        self.window = QDialog()
        self.window.setWindowTitle("Add person")
        self.layout = QVBoxLayout()
        self.field_name = QLineEdit("")
        self.field_name.setPlaceholderText("Personal name")
        self.field_book = QLineEdit("")
        self.field_book.setPlaceholderText("Book name")
        self.field_info = QLineEdit("")
        self.field_info.setPlaceholderText("Contact information")
        self.text_date = QLabel("Date to be brought")
        self.field_date = QDateEdit()
        self.field_date.setDate(QDate.currentDate())
        self.btnBox = QDialogButtonBox()
        self.btnBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btnBox.accepted.connect(self.save)
        self.btnBox.rejected.connect(self.close1)

        for i in [self.field_name, self.field_info, self.field_book, self.text_date, self.field_date, self.btnBox]:
            self.layout.addWidget(i)
        
        self.window.setLayout(self.layout)
        self.window.exec_()

    def save(self):
        if self.field_name.text() and self.field_book.text() and self.field_info.text() and self.field_date.text() != "":
            if self.field_name.text() not in data:
                data[self.field_name.text()] = {"Books": {self.field_book.text(): self.field_date.text()}, "Information": self.field_info.text()}
                persons.addItem(self.field_name.text())
                save_data("data.json", data)
                list_late_persons()
                self.window.close()
            else:
                error_screen("Try a different name!")
        else:
            error_screen("You entered the missing information!")
    def close1(self):
        self.window.close()

def add_person():
    dig = person_add()

class book_add():
    def __init__(self, person):
        self.window = QDialog()
        self.window.setWindowTitle("Add Book")
        self.person = person
        self.layout = QVBoxLayout()
        self.field_book = QLineEdit("")
        self.field_book.setPlaceholderText("Book name")
        self.text_date = QLabel("Date to be brought")
        self.field_date = QDateEdit()
        self.field_date.setDate(QDate.currentDate())
        self.btnBox = QDialogButtonBox()
        self.btnBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btnBox.accepted.connect(self.save)
        self.btnBox.rejected.connect(self.close1)

        for i in [self.field_book, self.text_date, self.field_date, self.btnBox]:
            self.layout.addWidget(i)
        self.window.setLayout(self.layout)
        self.window.exec_()

    def save(self):
        if self.field_book.text() and self.field_date.text() != "":
            data[self.person]["Books"][self.field_book.text()] = self.field_date.text()
            person_infos.addItem("Book: " + self.field_book.text() + "  History: " + self.field_date.text())
            save_data("data.json", data)
            list_late_persons()
            self.window.close()
        else:
            error_screen("You entered the missing information!")
    def close1(self):
        self.window.close()

def add_book():
    if persons.selectedItems() or late_persons.selectedItems():
        try:
            person = persons.selectedItems()[0].text()
            book = book_add(person)
        except:
            person = late_persons.selectedItems()[0].text()
            book = book_add(person)
        save_data("data.json", data)
        list_late_persons()
    else:
        error_screen("Select Person!")

def del_book():
    if person_infos.selectedItems():
        name = person_infos.item(0).text()[6:]
        if person_infos.selectedItems()[0].text()[:4] == "Book":
            book = person_infos.selectedItems()[0].text().split("  History:")[0][6:]
 
            del data[name]["Books"][book]
            save_data("data.json", data)
            try:
                show_person()
            except:
                show_person2()
            list_late_persons()
        else:
            error_screen("Choose Book to delete!")
    else:
        error_screen("Choose Book to delete!")

class person_search():
    def __init__(self):
        self.window = QDialog()
        self.window.setWindowTitle("Search for a person")
        self.layout = QVBoxLayout()
        self.field_name = QLineEdit("")
        self.field_name.setPlaceholderText("Personal name")
        self.field_book = QLineEdit("")
        self.field_book.setPlaceholderText("Book name")
        self.field_info = QLineEdit("")
        self.field_info.setPlaceholderText("Contact information")
        self.text_date = QLabel("Date to be brought")
        self.field_date = QDateEdit()
        self.field_date.setDate(QDate.currentDate())
        self.btnBox = QDialogButtonBox()
        self.btnBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btnBox.accepted.connect(self.save)
        self.btnBox.rejected.connect(self.close1)

        for i in [self.field_name, self.field_info, self.field_book, self.text_date, self.field_date, self.btnBox]:
            self.layout.addWidget(i)
        
        self.window.setLayout(self.layout)
        self.window.exec_()
    def save(self):
        person_infos.clear()
        persons.clear()
        self.filtered_persons = []
        if self.field_name.text() != "":
            for i in data:
                if self.field_name.text().lower() in i.lower():
                    self.filtered_persons.append(i)

        if self.field_info.text() != "" and self.field_info.text().isnumeric():
            for i in data:
                if self.field_info.text() in data[i]["Information"]:
                    self.filtered_persons.append(i)

        if self.field_book.text() != "":
            for i in data:
                for a in data[i]["Books"]:
                    if self.field_book.text().lower() in a.lower():
                        self.filtered_persons.append(i)

        if self.field_date.text() != "":
            for i in data:
                for a in data[i]["Books"]:
                    if self.field_date.text() == data[i]["Books"][a]:
                        self.filtered_persons.append(i)
        persons.addItems(set(self.filtered_persons))
        button_search_person.setText("Reset the search")
        self.window.close()

    def close1(self):
        self.window.close()

def search_person():
    if button_search_person.text() == "Search for a person":
        search = person_search()
    elif button_search_person.text() == "Reset the search":
        persons.clear()
        persons.addItems(data)
        button_search_person.setText("Search for a person")

# Initialize UI
persons.addItems(data)
list_late_persons()

# Connect buttons to functions
persons.itemClicked.connect(show_person)
late_persons.itemClicked.connect(show_person2)
button_del_person.clicked.connect(del_person)
button_add_person.clicked.connect(add_person)
button_add_book.clicked.connect(add_book)
button_del_book.clicked.connect(del_book)
button_search_person.clicked.connect(search_person)

window.setLayout(base)
window.show()
app.exec_()
