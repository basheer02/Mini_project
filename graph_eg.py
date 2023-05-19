import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

mydb = mysql.connector.connect(host = "localhost", username = "root", password = "", database = "example")

mycursor = mydb.cursor()
mycursor.execute("select * from main_tab")
result = mycursor.fetchall()

data = {}
data['Male'] = {}
data['Female'] = {}

age_cat = []
male_cat = []
female_cat = []

for i in result:
    data[i[0]][i[1]] = int(i[2])
    if i[1] not in age_cat:
        age_cat.append(i[1])

age_cat.sort()

for x in age_cat:
    if x in data["Male"].keys() and x in data["Female"].keys():
        male_cat.append(data["Male"][x])
        female_cat.append(data["Female"][x])
    elif x in data["Male"].keys():
        male_cat.append(data["Male"][x])
        female_cat.append(0)
    else:
        male_cat.append(0)
        female_cat.append(data["Female"][x])

gender = list(data.keys())
count = [sum(male_cat),sum(female_cat)]

sns.set_style("darkgrid")
plt.ylabel("Count")
sns.barplot(x = gender, y = count)
plt.show()

# Set the width of the bars
bar_width = 0.35

# Set the positions of the x-axis ticks
bar_positions = np.arange(len(age_cat))

plt.bar(bar_positions, male_cat, width = bar_width, label = 'Male')
plt.bar(bar_positions + bar_width, female_cat, width = bar_width, label = 'Female')

plt.xlabel('Age Categories')
plt.ylabel('Count')
plt.title('Comparison of Male and Female Counts by Age Categories')

# Set the x-axis tick positions and labels
plt.xticks(bar_positions + bar_width/2, age_cat)

# Add a legend
plt.legend()

# Display the plot
plt.show()