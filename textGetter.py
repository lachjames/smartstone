from urllib import request
import html
import time
import threading
import pickle

threadCount = 0
completedCount = 0
units = []

def main():
	if not load_units():
		update_units()
			
	tool()

def searchAll(text, finding, endString):
	#startIndex = 0
	endIndex = 0
	#findingIndex = text.find(finding)
	#print("Text:", text)
	#print(findingIndex)
	
	foundList = []
	for findingIndex in findAllLocations(text, finding):
	    #if finding == r"<tr><td class=\'center\'>": print(findingIndex) #DEBUG
	    #time.sleep(0.1) #DEBUG
	    #print(text[findingIndex:findingIndex + len(finding)])
	    for i in range(findingIndex + len(finding), len(text)):
	        #print(i)
	        if text[i:(i + len(endString))] == endString:
	            endIndex = i
	            #print(text[(findingIndex + len(finding)):endIndex]) #DEBUG
	            foundList.append(text[(findingIndex + len(finding)):endIndex])
	            break
	#print(foundList)
	return foundList
	
def search(text, finding, endString):
    #startIndex = 0
    endIndex = 0
    findingIndex = text.find(finding)
    #print("Text:", text)
    #print(findingIndex)
    if findingIndex == -1:
        return -1
    else:
        for i in range(findingIndex + len(finding), len(text)):
            if text[i:(i + len(endString))] == endString:
                endIndex = i
                #print(text[(findingIndex + len(finding)):endIndex]) #DEBUG
                return text[(findingIndex + len(finding)):endIndex]
    return -1

def findAllLocations(text, finding):
    locationList = []
    for i in range(0, len(text) - len(finding)):
        if text[i:i + len(finding)] == finding:
            #print(text[i:i + len(finding)]) #DEBUG
            locationList.append(i)
    return locationList
	
if __name__ == "__main__": main()