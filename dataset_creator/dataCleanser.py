
import os
import json
import re
from termcolor import colored

DataSet = {}
totalReviews = 0
reviewsAdded = 0
reviewsRemoved = 0

def getJsonData(path) -> []:
    '''
    Read in JSON data
    '''
    with open("./dataSets/" + path) as f:
        return json.load(f)

def isReviewVaid(review):
    '''
    Ensures that review length is greater than 3 words and that the review is in English
    '''
    if (len(review['text'].split()) > 3 and review['language'] == 'en' ):
        return True
    
    return False

def parsePlace(place):
    '''
    Method processes places
    Ensures places is not yet in dataset.  If the place is already in the dataset, unqiue reviews are compiled
    '''
    global reviewsAdded, reviewsRemoved, totalReviews
    placeID = place['place_id']

    # is place already in dataset
    if placeID in DataSet:
        print(colored('{0} already in DataSet'.format(place['name']), 'yellow'))
        for review in place['reviews']:

            # does existing dataset have this review
            if (not isReviewVaid(review)) or any( x['author_name'] == review['author_name'] and x['time'] == review['time'] for x in DataSet[placeID]['reviews']):
                continue
            else:
                print(colored("Adding review to {0}".format(place['name']), 'green'))
                totalReviews += 1
                reviewsAdded += 1
                DataSet[placeID]['reviews'].append(review)
    else:
        toRemove = []
        for i, review in enumerate(place['reviews']):
            # is review valid
            if not isReviewVaid(review):
                toRemove.append(i - len(toRemove))
            else:
                totalReviews += 1

        #remove invalid reviews
        for i in toRemove:
            reviewsRemoved += 1
            print(colored("Removed review from {0} By: {1}".format(place['name'], place['reviews'][i]['author_name']), 'red'))
            r = place['reviews'].pop(i)

        # does place have any valid reviews
        if len(place['reviews']) < 1:
            print(colored('No Reviews: {0}'.format(place['name']), 'red'))
            return
        
        print("Adding {0} to DataSet".format(place['name']))
        DataSet[placeID] = place

def writeDataSetFile():
    '''
    Writes JSON file
    '''
    y = json.dumps(list(DataSet.values()), ensure_ascii=False).encode('utf8')
    print('Places: ' + str(len(DataSet)))
    print('Total Reviews: ' + str(totalReviews))
    print('Reviews Added: ' + str(reviewsAdded))
    print('Reviews Removed: ' + str(reviewsRemoved))
    with open('dataset.json', 'w') as json_file:
        json_file.write(y.decode())

if __name__ == "__main__":
    arr = os.listdir("./dataSets/")

    # avoid hidden files
    regex = re.compile('^[^.]')
    paths = [ s for s in arr if regex.match(s) ]

    for path in paths:
        print('\n\n\nopening ' + path)
        places = getJsonData(path)
        for place in places:
            parsePlace(place)
    
    writeDataSetFile()

