import sys

import matplotlib
from PyQt6.QtCore import QSize, QDateTime, QTimer
from PyQt6.QtGui import QFont, QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QDateTimeEdit, QPushButton, QDialog, QWidget, \
    QVBoxLayout
import mysql.connector
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("数据录入")
        self.setGeometry(200, 400, 400, 300)

        # 时间
        self.label1 = QLabel("时间：", self)
        self.label1.move(50, 50)# 设置位置
        # 设置默认时间为当前时间
        current_time = QDateTime.currentDateTime()
        self.time_edit = QDateTimeEdit(current_time,self)
        self.time_edit.setFixedSize(QSize(200, 30))
        self.time_edit.setDisplayFormat("yyyy-MM-dd")
        self.time_edit.setCalendarPopup(True)
        self.time_edit.move(100, 50)

        # 输入章节
        self.label4 = QLabel("输入章节：", self)
        self.label4.move(50, 100)
        self.chapter = QLineEdit(self)
        self.chapter.setFixedSize(QSize(200, 30))
        self.chapter.move(100, 100)

        # 做题量
        self.label2 = QLabel("做题量：", self)
        self.label2.move(50, 150)
        self.question_num = QLineEdit(self)
        self.question_num.setFixedSize(QSize(200, 30))
        self.question_num.move(100, 150)

        # 错题数
        self.label3 = QLabel("错题数：", self)
        self.label3.move(50, 200)
        self.error_num = QLineEdit(self)
        self.error_num.setFixedSize(QSize(200, 30))
        self.error_num.move(100, 200)

        # 保存数据
        self.save_button = QPushButton("保存", self)
        self.save_button.move(150, 250)
        self.save_button.clicked.connect(self.save_data)

        # 回车键保存数据
        self.save_shortcut = QShortcut(QKeySequence("Return"), self)
        self.save_shortcut.activated.connect(self.save_data)





    def save_data(self):
        time = self.time_edit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        chapter = self.chapter.text()
        question_num = self.question_num.text()
        error_num = self.error_num.text()
        accuracy = round((1 - int(error_num) / int(question_num))*100,2)
        print("时间：", time,"正在连接数据库......")
        # 数据库连接
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wxw020601.",
            port="3308",
            database="rate_408"
        )
        print("数据库连接成功！")
        # 数据库游标
        mycursor = mydb.cursor()
        # 插入数据
        insert_query = "INSERT INTO rate (time, chapter, q_num, error_num, correct_rate) VALUES (%s, %s, %s, %s, %s)"
        insert_value = (time, chapter, question_num, error_num, accuracy)
        mycursor.execute(insert_query, insert_value)


        # 数据库提交
        mydb.commit()
        print("数据插入成功！")

        # 关闭数据库
        mycursor.close()
        mydb.close()
        print("数据库连接已关闭！")

        # 清空输入框
        self.chapter.clear()
        self.question_num.clear()
        self.error_num.clear()


        # 关闭当前窗口
        # self.close()

        # 新窗口显示正确率
        self.result_window = ResultWindow(accuracy = accuracy)
        self.result_window.exec()
        self.rate_window = RateWindow()
        self.rate_window.exec()


        print("今日做题正确率为：", accuracy)
        print("数据保存成功！")

# 新1窗口显示正确率
class ResultWindow(QDialog):
    def __init__(self, accuracy):
        super().__init__()

        self.setWindowTitle("正确率")
        self.setGeometry(300, 400, 200, 100)

        self.accuracy_label = QLabel(self)
        font = QFont()
        font.setPointSize(11) #
        self.accuracy_label.setFont(font)
        self.accuracy_label.setStyleSheet("color: red;")
        self.accuracy_label.setText(f"今日做题正确率为：{accuracy:.2f}%")
        self.accuracy_label.move(15, 20)

        self.label = QLabel("数据已存入数据库！", self)
        self.label.move(20, 50)

        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close_window)
        self.timer.start(2000)

    def close_window(self):
        self.timer.stop()
        self.close()

# 新2窗口显示折线图
class RateWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("正确率变化")
        self.setGeometry(300, 400, 800, 400)
        # 创建垂直布局管理器
        layout = QVBoxLayout(self)
        # 创建 MatplotlibWidget 实例并添加到布局中
        self.matplotlib_widget = MatplotlibWidget(self)
        layout.addWidget(self.matplotlib_widget)
        # 设置布局管理器
        self.setLayout(layout)
        # 重新绘制折线图以适应窗口大小的变化
        self.matplotlib_widget.plot_data_from_database()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close_window)
        self.timer.start(3000)

    def close_window(self):
        self.timer.stop()
        self.close()



class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.axes = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.setStretch(1, 1)  # 设置第二个部件的拉伸因子为1
        self.canvas.setFixedSize(1200, 400)  # 设置折线图的固定大小

    def plot_data_from_database(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wxw020601.",
            port="3308",
            database="rate_408"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT time, correct_rate FROM rate ORDER BY time")
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()

        time = []
        rate = []
        for x in myresult:
            time.append(x[0].strftime("%m-%d"))
            rate.append(x[1])
        average_accuracy = sum(rate) / len(rate)

        # 设置matplotlib正常显示中文和负号
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号


        self.axes.clear()
        self.axes.plot(time, rate)
        self.axes.set_xlabel("时间")
        self.axes.set_ylabel("正确率")
        self.axes.set_title("正确率变化")
        self.axes.text(0.95, 0.95, f"平均正确率: {average_accuracy:.2f}%",
                       verticalalignment='top', horizontalalignment='right',
                       transform=self.axes.transAxes,
                       bbox=dict(facecolor='white', alpha=0.5))
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())