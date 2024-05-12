"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings_form.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QComboBox, QDial, QLCDNumber, QSlider, QApplication, QWidget
from ui import d_eventfilter_settings_form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = d_eventfilter_settings_form.Ui_Form()
        self.ui.setupUi(self)
        # Инициализация QSettings
        self.settings = QSettings("MyCompany", "MyApp")

        # Подключение обработчиков событий
        self.ui.dial.valueChanged.connect(self.update_ui)
        self.ui.horizontalSlider.valueChanged.connect(self.update_ui)
        self.ui.lcdNumber.display(self.settings.value("lcdNumber", 0))
        self.ui.comboBox.currentTextChanged.connect(self.update_lcd_format)

        # Загрузка сохраненного режима отображения
        self.ui.comboBox.setCurrentText(self.settings.value("displayMode", "dec"))

        # Подключение обработчиков клавиш для QDial
        self.ui.dial.keyPressEvent = self.handle_key_press

    def update_ui(self):
        value = self.ui.dial.value()
        self.ui.horizontalSlider.setValue(value)
        self.ui.lcdNumber.display(value)
        self.settings.setValue("lcdNumber", value)

    def update_lcd_format(self):
        format = self.ui.comboBox.currentText()
        self.ui.lcdNumber.setDigitCount(4)
        if format == "oct":
            self.ui.lcdNumber.display("{0:o}".format(self.settings.value("lcdNumber", 0)))
        elif format == "hex":
            self.ui.lcdNumber.display("{0:x}".format(self.settings.value("lcdNumber", 0)))
        elif format == "bin":
            self.ui.lcdNumber.display("{0:b}".format(self.settings.value("lcdNumber", 0)))
        else:  # dec
            self.ui.lcdNumber.display(str(self.settings.value("lcdNumber", 0)))
        self.settings.setValue("displayMode", format)

    def handle_key_press(self, event):
        if event.key() == Qt.Key_Plus:
            self.ui.dial.setValue(self.ui.dial.value() + 1)
        elif event.key() == Qt.Key_Minus:
            self.ui.dial.setValue(self.ui.dial.value() - 1)
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
