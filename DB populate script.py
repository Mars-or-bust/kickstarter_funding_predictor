import sys
sys.path.append('/anaconda3/lib/python3.6/site-packages')

import pymongo
from pymongo import MongoClient
import csv
from datetime import datetime

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return abs((d2 - d1).days)


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["kickstarter"]


with open('/Users/Ben/Desktop/DS220/kickstarter-projects/ks-projects-201612.csv',encoding='cp1252') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for row in readCSV:
        ID = row[0]
        name = row[1]
        category = row[2]
        main_category = row[3]
        currency = row[4]
        deadline = row[5]
        goal= row[6]
        launched = row[7]
        pledged= row[8]
        state = row[9]
        backers = row[10]
        country = row[11]
        usd_pledged = row[12]
        try:
            length = days_between(launched,deadline)
        except:
            length = None

        mydict = { "ID": ID, "name": name, "category":category,
                   "main_category": main_category, "currency":currency,
                   "deadline": deadline, "goal": goal, "launched": launched,
                   "pledged": pledged, "state": state, "backers": backers,
                   "country": country, "usd_pledged":usd_pledged, 'length':length
                   }
        
        x = mycol.insert_one(mydict)


        

