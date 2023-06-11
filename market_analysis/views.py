from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from .models import DataModel

from django.shortcuts import render
from django.contrib.auth import authenticate,login

import datetime


#def index(request):
#    return render(request,'index.html')

def loginn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('data_view')
        else:
            return redirect('login')
    return render(request, 'login.html')





def graph_data(date='',to_day=datetime.date.today().strftime('%d-%m-%Y')):

    result = DataModel.objects.all()

    data = {}
    data['Male'] = {}
    data['Female'] = {}
    age_cat = ['0-3', '4-9', '10-15', '16-20', '20-30', '31-40', '41-53', '55+']
    male_cat,female_cat = [],[]
    count = 0

    for object in result:
        cur_date = object.date

        if len(date) < 3:
            day,month,year = map(str,cur_date.split('-'))
            cur_date = month

        if cur_date == date or date == '':
            gender = object.gender
            age = object.age    
            count = int(object.count)

            if age in data[gender].keys():
                data[gender][age] += count
            else:
                data[gender][age] = count

    for x in age_cat:
        if x in data["Male"].keys() and x in data["Female"].keys():
            male_cat.append(data["Male"][x])
            female_cat.append(data["Female"][x])
        elif x in data["Male"].keys():
            male_cat.append(data["Male"][x])
            female_cat.append(0)
        elif x in data['Female'].keys():
            male_cat.append(0)
            female_cat.append(data["Female"][x])
        else:
            male_cat.append(0)
            female_cat.append(0)

    count = [sum(male_cat),sum(female_cat)]

    products = {}
    products['Male'] = {
        '0-3' : 'M0-3', 
        '4-9' : 'M3-9',
        '10-15' : 'M10-15' ,
        '16-20' : 'M16-20', 
        '20-30' : 'M21-30', 
        '31-40' : 'M31-40', 
        '41-53' : 'M41-53', 
        '55+' : 'M56-100'
    }

    products['Female'] = {
        '0-3' : 'M0-3', 
        '4-9' : 'M4-10',
        '10-15' : 'M11-15' ,
        '16-20' : 'M16-20', 
        '20-30' : 'M21-30', 
        '31-40' : 'M31-42', 
        '41-53' : 'M43-55', 
        '55+' : 'M56-100'
    }

    highestFemaleCat,highestMaleCat = '',''

    if len(data['Male']) > 0:
        highestMaleCat = max(data['Male'], key = data['Male'].get)
    if len(data['Female']) > 0:
        highestFemaleCat = max(data['Female'], key = data['Female'].get)

    maleProduct = '' if highestMaleCat == '' else products['Male'][highestMaleCat]
    femaleProduct = '' if highestFemaleCat == '' else products['Female'][highestFemaleCat]

    context = {
        'gender_count' : count,
        'age_cat' : age_cat,
        'male_cat' : male_cat,
        'female_cat' : female_cat,
        'maleProduct' : maleProduct,
        'femaleProduct' : femaleProduct,
        'cur_date' : to_day
    }

    return context





def data_view(request):

    date_data = {
        'Mon' : [6,1],
        'Tue' : [5,2],
        'Wed' : [4,3],
        'Thu' : [3,4],
        'Fri' : [2,5],
        'Sat' : [1,6],
        'Sun' : [0,7]
    }
    
    today = datetime.date.today()
    cur_day = today.strftime("%a")
    month = int(today.strftime("%m"))
    year = int(today.strftime("%Y"))
    day = int(today.strftime("%d")) + date_data[cur_day][0]

    if day > 30:
        day = day % 10
        month += 1

    if request.method == 'POST' and 'selectedGraph' in request.POST:
        
        which_date = request.POST.get('selectedGraph')

        if which_date == 'current':
            to_day = datetime.date(year,month,day)
            date = to_day.strftime('%d-%m-%Y')
            context = graph_data(date)
            print(context)
            return JsonResponse(context)

        elif which_date == 'week': 
            day = int(today.strftime("%d")) - date_data[cur_day][1]

            if day <= 0:
                day += 31
                month -= 1

            to_day = datetime.date(year,month,day)
            date = to_day.strftime('%d-%m-%Y')
            context = graph_data(date,date)
            return JsonResponse(context)
        
        elif which_date == 'month':
            to_day = datetime.date(year,month-1,day)
            date = to_day.strftime('%m')
            context = graph_data(date,date)
            return JsonResponse(context)

        else:
            context = graph_data()
            return JsonResponse(context)
        
    return render(request, 'graph.html')
