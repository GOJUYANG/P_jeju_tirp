#background-color:qlineargradient(spread:pad,
# x1:0.971591, y1:0.636, x2:1, y2:1,
# stop:0 rgba(85, 255, 127, 255), stop:1 rgba(255, 255, 255, 255))

#이것을 큐티디자이너에서 단독으로 할 수 없다고한다.
#따로 클래스와 함수를 통해 호출하여 사용해야한다.
#아래는 지피티 선생님이 짜주신 코드다

# from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
# from PyQt5.QtGui import QLinearGradient, QPalette, QColor

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.stackedWidget = QStackedWidget(self)
#         self.setCentralWidget(self.stackedWidget)
#
#         # 페이지 0
#         page0 = QWidget(self.stackedWidget)
#         self.stackedWidget.addWidget(page0)
#
#         # 페이지 1
#         page1 = QWidget(self.stackedWidget)
#         self.stackedWidget.addWidget(page1)
#
#         self.setPagePalette(0)  # 초기 페이지의 배경 설정
#
#         self.stackedWidget.setCurrentIndex(0)  # 초기 페이지 설정
#
#     def setPagePalette(self, index):
#         palette = self.stackedWidget.palette()
#         gradient = QLinearGradient(self.stackedWidget.rect().topLeft(), self.stackedWidget.rect().bottomLeft())
#         gradient.setColorAt(0, QColor(255, 0, 0))
#         gradient.setColorAt(1, QColor(0, 255, 0))
#         gradient.setSpread(QGradient.ReflectSpread)  # spread 스타일 설정
#
#         palette.setBrush(QPalette.Background, gradient)
#         self.stackedWidget.widget(index).setPalette(palette)
#
# if __name__ == "__main__":
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec()
