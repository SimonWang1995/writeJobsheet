from random import choice
import calendar
import os,re
import datetime,time


def get_dates(ym):
    worklist=[]
    year=int(ym.split('/')[0])
    month=int(ym.split('/')[1].lstrip("0"))
    num = calendar.monthlen(year,month)
    for day in range(1,num+1):
        if calendar.weekday(year,month,day) < 5:
            date = "%d/%02d/%02d" % (year,month,day)
            worklist.append(date)
    return worklist

def read_file(filename):
    list = []
    with open(filename,'r') as fd:
        while True:
            line = fd.readline()
            if line:
               # print(line)
                list.append(line.strip('\n'))
            else:
                break
        return list

def write_file(filename,values):
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename,'a') as file:
        for value in values:
            file.write(value+'\n')

def checkdate(ym):
    try:
        year = ym.split('/')[0]
        month = ym.split('/')[1]
        if re.match("\d{4}",year) and 0<int(month)<=12:
            return True
    except Exception as e:
        print(e)
        return  False

def formatdate(from_date):
    date_list=from_date.split('/')
    to_date = "%s/%s/%s" % (date_list[1],date_list[2],date_list[0])
    return to_date