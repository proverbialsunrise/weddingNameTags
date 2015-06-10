#!/usr/local/bin/python

import json
import pdb
from pprint import pprint
from string import Template
import re

def loadGuestsFromFile(fileName):
    guests = []
    with file(fileName) as data_file: 
        for guestLine in data_file:
            try:
                guestData = json.loads(guestLine)
                if guestData["attendance"] == "yes":
                    guests.append(guestData)
            except ValueError:
                #print "Couldn't load one of the lines...shoot."
                pass

    return guests


def replaceText(replacements, string):
    reps = dict((re.escape(k), v) for k, v in replacements.iteritems())
    pattern = re.compile("|".join(reps.keys()))
    replacedString = pattern.sub(lambda m: reps[re.escape(m.group(0))], string)
    return replacedString



def createPage(svgTemplateFilename, replacements, pageNumber):
    #load the SVG file and insert the guest information.
    with file(svgTemplateFilename) as svgTemplate:
        svgString = svgTemplate.read()
        svgString = replaceText(replacements, svgString)
        #Save to file in processed folder
        #Create the filename by stripping whitespace from the name
        saveFilename = 'processed/' + "{:0>2d}".format(pageNumber) + '.svg'
        with open(saveFilename, 'w') as saveFile:
            saveFile.write(svgString)

        return saveFilename


def replacementsDictionaryForGuest(guestNumber, guest):
    colourTemplate = Template('#COLOUR${guestNum}#')
    colourToReplace = colourTemplate.substitute(guestNum=guestNumber)
    nameTemplate = Template('#NAME${guestNum}#')
    nameToReplace = nameTemplate.substitute(guestNum=guestNumber)
    numberTemplate = Template('#NUM${guestNum}#')
    numberToReplace = numberTemplate.substitute(guestNum=guestNumber)
    colour = '#7E54A2'
    if guest['mealSelection'] == 'vegan':
        colour = '#C16873' #Coral colour
        ##68c198 Alternate?
    elif guest['mealSelection'] == 'lamb':
        colour = '#9868c1'#Purple colour
        ##7e54a2 Alternate?
    else: #turkey
        colour = '#60C08B' #Green colour

    try:
        tableNumber = guest['table']
    except KeyError:
        print "Table not assigned for guest: " + guest['name']
        tableNumber = "?"

    replacements = {nameToReplace: guest['name'].upper(),
                    numberToReplace: tableNumber.upper(),
                    colourToReplace: colour}
    return replacements

def replacementDictionaryForGuests(guests):
    i = 1
    replacements = {}
    for guest in guests:
        reps = replacementsDictionaryForGuest(i, guest)
        replacements.update(reps)
        i+=1
    return replacements


#Things that need to happen
#1. Open the database and load the guests
#2. Get the guests in chunks of 6
#3. For each chunk of 6, make the necessary replacements
#     - Build the replacements dictionary for each guest
#     - append the replacements dictionaries together
#4. Make the svg document for those 6 guests and save



guests = loadGuestsFromFile("attendingGuestDB.json")
#Sort the guests into alphabetical order.
guests.sort(key=lambda guest: guest['name'])
numberOfGuests=len(guests)
numberOfPages=numberOfGuests / 6 + 1
for i in range(1,numberOfPages+1):
    startIndex = (i*6)-6
    endIndex = min(i*6,numberOfGuests)
    pageOfGuests = guests[startIndex:endIndex]
    replacements = replacementDictionaryForGuests(pageOfGuests)
    savedFileName = createPage("6NameTagsTemplate.svg",replacements, i)
    print "Saved page: " + savedFileName

print "Saved {} guests on {} pages".format(numberOfGuests, numberOfPages)
