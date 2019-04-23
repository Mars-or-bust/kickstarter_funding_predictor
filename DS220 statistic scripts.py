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



def query(variable_list, criteria_list):

    '''
    This function takes in a list of categories and the criteria to be
    searched for in those categories. It then uses those lists to
    construct a query and returns any matching results from the database.
    '''
    
    myquery = {}

    for item in variable_list:
        if item != None:
            myquery.update({str(item): criteria_list[variable_list.index(item)]})

    #run the query
    mydoc = mycol.find(myquery)
  
    return mydoc



def filter_entries(web_input):
    '''
    match the entries that match the match the inputs for the categories
    returns a list of all the entries that match
    '''

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

    # Labels for each of the columns
    labels = ['Count','avg_target','usd_pledged','length','backers','avg_donation_size','name_length']

    # calculate summary statistics for failed and successful campaigns
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

    # if there were no successful campaigns return none
    if success_count == 0:
        return None

    # calculate averages for each campaign
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
    percent_success = round(success_count / (success_count + failure_count),2) * 100

    
    success_stats = [success_count,avg_success_target, avg_success_pledged,
                     avg_success_duration, avg_success_backers,
                     avg_success_donation_size, avg_success_title_length]

    # round the stats
    for item in range(0,len(success_stats)):
        success_stats[item] = round(success_stats[item], 1)

    # do the same for failed campaign stats
    failure_stats = [failure_count, avg_failure_target, avg_failure_pledged,
                     avg_failure_duration, avg_failure_backers,
                     avg_failure_donation_size, avg_failure_title_length]

    for item in range(0,len(failure_stats)):
        failure_stats[item] = round(failure_stats[item], 1)

    # return the overall success rate, along with all the stats
    return(percent_success, labels, success_stats, failure_stats)


def clean_lists(xml_data):
    '''
    seperates the list from the database into successful and failed lists
    while getting rid of cancalled results
    '''
    # goal, amount pledged, length, # of backers, avg_donation size, title_length
    labels = ['Funding Goal','USD Pledged','Campaign Length','Number of Backers','AVG Donation','Title Length']
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
        
    
    return success_stats_list, failed_stats_list, labels
    

### needs connected to interface ###
def histogram_plot(successful, failed, label,bins = 50):
    '''
    prints histograms of the data
    '''
    ax1 = plt.subplot(2, 1, 1)
    n, bins, patches = plt.hist(successful, bins, facecolor='green', alpha=0.5)
    plt.title(str(label) + ' Histogram - Successful')
    plt.xlabel(str(label))
    plt.ylabel('Count')

    plt.subplot(2, 1, 2, sharex=ax1)
    n, bins, patches = plt.hist(failed, bins, facecolor='green', alpha=0.5)
    plt.title(str(label) + ' Histogram - Failed')
    plt.xlabel(str(label))
    plt.ylabel('Count')

    plt.tight_layout()
    plt.show()

def success_chance(results, goal):
    # calculates the chances of a campaign succeeding based on a price point
    total = len(results)
    success = 0

    for item in results:
        if float(item['goal']) >= float(goal) and item['state'] == 'successful':
            success += 1
            
    return round((success / total),3)


def main():
    web_input = ['category', 'Poetry', 'country', 'GB']

    main_category = input("Enter the campaign category (Ex: Music): ")
    sub_category = input("Enter the sub_category (Ex: Indie Rock): ")
    country = input("Enter the country (Ex: US): ")
    goal = input("Enter your target goal: ")
    print('\n')
    
    web_input = ['category',sub_category,'main_category',main_category, 'country',country]

    variable_list, criteria_list = filter_entries(web_input)

    # break results into two smaller lists
    results = list(query(variable_list, criteria_list))

    success, fail, labels = (clean_lists(results[1:500]))


    # check to see if there were any7 successful campaigns
    if summary_stats(results) == None:
        print('No successful campaigns match that query')
        return None
    else:
        # calculate the chance of success based on the goal
        percent_achieved_goal = success_chance(results,goal)
        print(str(percent_achieved_goal*100) + '% of campaigns whose goal was $'
              + str(goal) + ' or more were successful. \n\n')

        # print the summary statistics
        percent_success, labels, success_stats, fail_stats = summary_stats(results)
        print("Summary Statistics for selected category and location")
        print("-----------------------------------------------------\n")
        print('Percent of campaigns that reach funding goal: ', round(percent_success,3), '%\n')
        for i in range(0,len(success_stats)):
            print(labels[i] + '\nSucessful Campaigns: ' + str(success_stats[i]) +
                  '\nFailed Campaigns: ' + str(fail_stats[i]) + '\n')

    
    success, fail, labels = (clean_lists(results[1:500]))

    # plot histograms of all the variables
    for i in range(0,len(success)):
        histogram_plot(success[i],fail[i],labels[i])



main()



