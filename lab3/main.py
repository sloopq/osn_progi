from PyQt5.QtWidgets import (QApplication, QWidget, QTableView, QVBoxLayout,
                             QDialog, QLineEdit, QComboBox, QSpinBox, QPushButton,
                             QFormLayout, QDialogButtonBox)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5 import uic


class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("QtWidget.ui", self)  # Ensure you have a valid QtWidget.ui file
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('films_db.sqlite')
        self.db.open()

        self.mainModel = QSqlQueryModel()
        self.updateModel()

        self.tableView.setModel(self.mainModel)
        self.tableView.setColumnHidden(0, True)  # Hide the ID column
        self.tableView.resizeColumnsToContents()
        self.tableView.doubleClicked.connect(self.doubleClick)

    def updateModel(self):
        query_string = """SELECT
            f.id,
            f.title AS [Название],
            g.title AS [Жанр],
            f.year AS [Год выпуска],
            f.duration AS [Длительность]
        FROM films f 
        JOIN genres g on f.genre = g.id;"""
        self.mainModel.setQuery(query_string, self.db)

    def doubleClick(self, index):
        film_id = self.mainModel.data(self.mainModel.index(index.row(), 0))
        dialog = DialogForm(film_id, self.db)
        if dialog.exec() == QDialog.Accepted:
            self.updateModel()


class DialogForm(QDialog):
    def __init__(self, film_id, db):
        super().__init__()
        self.film_id = film_id
        self.db = db

        self.setWindowTitle("Edit Film")
        self.resize(400, 200)

        self.titleEdit = QLineEdit()
        self.genreBox = QComboBox()
        self.yearEdit = QSpinBox()
        self.yearEdit.setRange(1888, 2100)
        self.durationEdit = QSpinBox()
        self.durationEdit.setRange(1, 1000)

        self.loadGenres()
        self.loadFilmData()

        formLayout = QFormLayout()
        formLayout.addRow("Название:", self.titleEdit)
        formLayout.addRow("Жанр:", self.genreBox)
        formLayout.addRow("Год выпуска:", self.yearEdit)
        formLayout.addRow("Длительность:", self.durationEdit)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def loadGenres(self):
        query = QSqlQuery("SELECT title FROM genres", self.db)
        while query.next():
            self.genreBox.addItem(query.value(0))

    def loadFilmData(self):
        query = QSqlQuery(f"SELECT title, year, genre, duration FROM films WHERE id = {self.film_id}", self.db)
        if query.next():
            self.titleEdit.setText(query.value(0))
            self.yearEdit.setValue(query.value(1))
            genre_id = query.value(2)
            self.durationEdit.setValue(query.value(3))

            genre_query = QSqlQuery(f"SELECT title FROM genres WHERE id = {genre_id}", self.db)
            if genre_query.next():
                genre_title = genre_query.value(0)
                self.genreBox.setCurrentText(genre_title)

    def accept(self):
        title = self.titleEdit.text()
        year = self.yearEdit.value()
        duration = self.durationEdit.value()
        genre = self.genreBox.currentText()

        if not title or not genre:
            print("Error: All fields must be filled.")
            return

        query = QSqlQuery(self.db)
        query.prepare("""UPDATE films
                         SET title = ?, year = ?, genre = (SELECT id FROM genres WHERE title = ?), duration = ?
                         WHERE id = ?""")
        query.addBindValue(title)
        query.addBindValue(year)
        query.addBindValue(genre)
        query.addBindValue(duration)
        query.addBindValue(self.film_id)

        if not query.exec():
            print("Error:", query.lastError().text())
        else:
            super().accept()


if __name__ == '__main__':
    app = QApplication([])
    window = MainForm()
    window.show()
    app.exec()
