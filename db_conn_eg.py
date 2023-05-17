import mysql.connector

mydb = mysql.connector.connect(host = "localhost", username = "root", password = "", database = "example")

mycursor = mydb.cursor()
mycursor.execute("select name,age from main_tab")
result = mycursor.fetchall()
result = result[0]

#for x in result:
#    result = x
#    break

sql = "select count from main_tab where name = %s and age = %s"
val = ("Male","21-30") 
gender = "Male"
age = "21-30"
mycursor.execute(sql,val)
res = mycursor.fetchone()
res = int(res[0]) + 1
if result == val:
    #res += 1
    sql = "update main_tab set count = count + 1 where name = %s and age = %s"
    val = [gender,age]
    mycursor.execute(sql,val)
    mydb.commit()

mydb.commit()
#for x in result:
#    #for i in x:
#    print(type(x))