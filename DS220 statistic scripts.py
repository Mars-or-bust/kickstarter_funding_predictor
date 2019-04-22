import sys
sys.path.append('/anaconda3/lib/python3.6/site-packages')

import pymongo
import matplotlib
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["kickstarter"]


# queries the database based on the list and criteria specified
def query(variable_list, criteria_list):
    myquery = {}

    for item in variable_list:
        if item != None:
            myquery.update({str(item): criteria_list[variable_list.index(item)]})

    #run the query
    mydoc = mycol.find(myquery)
  
    return mydoc


# match the entries that match the match the inputs for the categories
# returns a list of all the entries that match
def filter_entries(web_input):

    variable_list = []
    criteria_list = []
    
    for item in web_input:
        if web_input.index(item) % 2 == 0:
            variable_list.append(str(item))
        else:
            criteria_list.append(str(item))
            
    return variable_list, criteria_list
        

def summary_stats(XML_list):
    '''summary statistics for the dataset'''

    # initialize are the variables
    success_count =0
    success_target =0
    success_pledged =0
    success_duration =0
    success_backers =0
    success_title_length =0

    failure_count =0
    failure_target =0
    failure_pledged =0
    failure_duration =0
    failure_backers =0
    failure_title_length =0

    labels = ['Count','avg_target','usd_pledged','length','backers','avg_donation_size','name_length']
    
    for item in range(0,len(XML_list)):
        if XML_list[item]['state'] == 'successful':
            success_count +=1
            success_target += float(XML_list[item]['goal'])
            success_pledged += float(XML_list[item]['usd_pledged'])
            success_duration += float(XML_list[item]['length'])
            success_backers += float(XML_list[item]['backers'])
            success_title_length += len(XML_list[item]['name'].split())
            

        elif XML_list[item]['state']=='failed':
            failure_count += 1
            failure_target += float(XML_list[item]['goal'])
            failure_pledged += float(XML_list[item]['usd_pledged'])
            failure_duration += float(XML_list[item]['length'])
            failure_backers += float(XML_list[item]['backers'])
            failure_title_length += len(XML_list[item]['name'].split())


    avg_success_target = success_target / success_count
    avg_success_pledged = success_pledged / success_count
    avg_success_duration = success_duration / success_count
    avg_success_backers = success_backers / success_count
    avg_success_donation_size = success_pledged / success_backers
    avg_success_title_length  = success_title_length / success_count

    avg_failure_target = failure_target / failure_count
    avg_failure_pledged = failure_pledged / failure_count
    avg_failure_duration = failure_duration / failure_count
    avg_failure_backers = failure_backers / failure_count
    avg_failure_donation_size = failure_pledged / failure_backers
    avg_failure_title_length  = failure_title_length / failure_count

    #summary data in list form
    percent_success = success_count / (success_count + failure_count)
    
    success_stats = [success_count,avg_success_target, avg_success_pledged,
                     avg_success_duration, avg_success_backers,
                     avg_success_donation_size, avg_success_title_length]
    
    for item in range(0,len(success_stats)):
        success_stats[item] = round(success_stats[item], 1)

    failure_stats = [failure_count, avg_failure_target, avg_failure_pledged,
                     avg_failure_duration, avg_failure_backers,
                     avg_failure_donation_size, avg_failure_title_length]

    for item in range(0,len(failure_stats)):
        failure_stats[item] = round(failure_stats[item], 1)

    print(percent_success)
    print(labels)
    print(success_stats)
    print(failure_stats)

def clean_lists(xml_data):
    # goal, amount pledged, length, # of backers, avg_donation size, title_length
    labels = ['goal','usd_pledged','length','backers','avg_donation','name_length']
    success_stats_list = [[],[],[],[],[],[]]
    failed_stats_list = [[],[],[],[],[],[]]
    for row in range(0,len(xml_data)):
        if (xml_data[row]['state']) == 'successful':
            success_stats_list[0].append(float(xml_data[row]['goal']))
            success_stats_list[1].append(float(xml_data[row]['usd_pledged']))
            success_stats_list[2].append(float(xml_data[row]['length']))
            success_stats_list[3].append(float(xml_data[row]['backers']))
            if float(xml_data[row]['backers']) != 0:
                success_stats_list[4].append(float(xml_data[row]['usd_pledged'])/float(xml_data[row]['backers']))
            else:
                success_stats_list[4].append(0)                 
            success_stats_list[5].append(len(xml_data[row]['name'].split()))
        elif (xml_data[row]['state']) == 'failed':
            failed_stats_list[0].append(float(xml_data[row]['goal']))
            failed_stats_list[1].append(float(xml_data[row]['usd_pledged']))
            failed_stats_list[2].append(float(xml_data[row]['length']))
            failed_stats_list[3].append(float(xml_data[row]['backers']))
            if float(xml_data[row]['backers']) != 0:
                failed_stats_list[4].append(float(xml_data[row]['usd_pledged'])/float(xml_data[row]['backers']))
            else:
                failed_stats_list[4].append(0)                 
            failed_stats_list[5].append(len(xml_data[row]['name'].split()))
        
    
    return success_stats_list, failed_stats_list
    
### needs fixed ###
def double_graph(stats_list_of_lists):
    subplot(nrows, ncols, index, **kwargs)
    subplot(pos, **kwargs)
    subplot(ax)

### needs connected to interface ###
def histogram_plot(x, bins = 25):
    n, bins, patches = plt.hist(x, bins, facecolor='green', alpha=0.5)
    plt.show()



web_input = ['category', 'Poetry', 'country', 'GB']

variable_list, criteria_list = filter_entries(web_input)

print(variable_list, criteria_list)
results = list(query(variable_list, criteria_list))

success, fail = (clean_lists(results[1:500]))

summary_stats(results)

histogram_plot(success[3])
histogram_plot(fail[3])


# create statistics to measure the results

#for item in results:
#    print()


