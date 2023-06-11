import mysql.connector

mydb = mysql.connector.connect(host = "localhost", username = "root", password = "", database = "example")

mycursor = mydb.cursor()

import datetime

date_data = {
    'Mon' : [6,1],
    'Tue' : [5,2],
    'Wed' : [4,3],
    'Thu' : [3,4],
    'Fri' : [2,5],
    'Sat' : [1,6],
    'Sun' : [0,0]
}

year, month, day = 2023,6,28

today = datetime.date(year,month,day)
cur_day = today.strftime("%a")
day = int(today.strftime("%d")) + date_data[cur_day][0]
month = int(today.strftime("%m"))
year = int(today.strftime("%Y"))

if day > 30:
    day = day % 10
    month += 1
    
today = datetime.date(year,month,day)
date = today.strftime('%d-%m-%Y')

print(date)

#v = [date]
#mycursor.execute("select gender,age,count from gender_data where date = %s",v)
#result = mycursor.fetchall()
#
#for x in result:
#    print(x)

sql = "insert into gender_data(date,gender,age,count) values(%s,%s,%s,%s)"
val = (date,'Female','10-15',str(5))
mycursor.execute(sql,val)
mydb.commit()

