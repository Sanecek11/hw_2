"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6 import QtWidgets
from ui import c_signals_events_form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = c_signals_events_form.Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButtonMoveCoords.clicked.connect(self.moveWindow)
        self.ui.pushButtonGetData.clicked.connect(self.getScreenData)
        self.ui.plainTextEdit.appendPlainText("Начало работы")

    def moveWindow(self):
        x = self.ui.spinBoxX.value()
        y = self.ui.spinBoxY.value()
        self.move(x, y)
        self.ui.plainTextEdit.appendPlainText(f"Окно перемещено в координаты: {x}, {y}")

    def getScreenData(self):
        screen = QtWidgets.QApplication.screens()[0]
        screen_data = {
            "Кол-во экранов": len(QtWidgets.QApplication.screens()),
            "Текущее основное окно": self,
            "Разрешение экрана": screen.geometry(),
            "На каком экране окно находится": self.screen(),
            "Размеры окна": self.size(),
            "Минимальные размеры окна": self.minimumSize(),
            "Текущее положение (координаты) окна": self.geometry(),
            "Координаты центра приложения": self.geometry().center(),
            "Отслеживание состояния окна": "активно" if self.isActiveWindow() else "неактивно"
        }
        for key, value in screen_data.items():
            self.ui.plainTextEdit.appendPlainText(f"{key}: {value}")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
