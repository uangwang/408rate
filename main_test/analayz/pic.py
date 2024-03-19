import mysql
import mysql.connector
import matplotlib.pyplot as plt

def show():
    # 从数据库读取数据(时间，正确率)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Wxw020601.",
        port="3308",
        database="rate_408"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT time, correct_rate FROM rate")
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    time = []
    rate = []
    for x in myresult:
        time.append(x[0])
        rate.append(x[1])
    # 画图
    plt.plot(time, rate)
    plt.xlabel("时间")
    plt.ylabel("正确率")
    plt.title("正确率变化")
    plt.show()
show()

