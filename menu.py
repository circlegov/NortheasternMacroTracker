# encoding: utf-8
import requests
from collections import OrderedDict
import json
from datetime import datetime
import sys
import os
import time

class MenuData:
    # needs to be optimized to pull from any school using Dine On Campus API
    # can be optimized to hold all data in one file
    # sort all files into appropriate folders

    # Location: list of locations to return foods for
    # run test to check for updated files
    def __init__(self, location, runtest=True):
        self.location = location
        if runtest:
            self.locationIds = self.checkFileEmpty('locationId.txt', self.getLocationId) # will define later to store all data needed
            self.generalMenuLinks = self.checkFileEmpty('generalMenuLink.txt', self.getGeneralMenuLink)
            self.menuTypeIds = self.checkFileEmpty('menuTypeIds.txt', self.getMenuTypeIds)
            self.allSpecificLinks = self.checkFileEmpty('allSpecificLinks.txt', self.getAllSpecificLinks)
            self.allMenuData = self.checkFileEmpty('allMenuData.txt', self.getAllMenuData)
            self.allCategories = self.checkFileEmpty('allCategories.txt', self.getAllCategories)
            self.allItems = self.checkFileEmpty('allItems.txt', self.getAllItems)
            self.allItemNutrients = self.checkFileEmpty('allItemNutrients.txt', self.getAllItemNutrients)
            if self.currentTime() != list(self.generalMenuLinks.keys())[0]: # check if todays date is date for data
                #print('generallinks')
                self.generalMenuLinks = self.getGeneralMenuLink()
            if self.currentTime() != list(self.menuTypeIds.keys())[0]:
                #print('menuids')
                self.menuTypeIds = self.getMenuTypeIds()
            if self.currentTime() != list(self.allSpecificLinks.keys())[0]:
                #print('specficilinks')
                self.allSpecificLinks = self.getAllSpecificLinks()
            if self.currentTime() != list(self.allMenuData.keys())[0]:
                #print('allmenudata')
                self.allMenuData = self.getAllMenuData()
            if self.currentTime() != list(self.allCategories.keys())[0]:
                #print('allcategories')
                self.allCategories = self.getAllCategories()
            if self.currentTime() != list(self.allItems.keys())[0]:
                #print('allitems')
                self.allItems = self.getAllItems()
            if self.currentTime() != list(self.allItemNutrients.keys())[0]:
                #print('all nutrients')
                self.allItemNutrients = self.getAllItemNutrients()

    # need basic locations
    # need food category
    # need foods
    # need macros
    # can solely use allItemNutrients by way of keys and values
    # date : location : mealType (breakfast, lunch, dinner) : food category : food : macros
    def getData(self, link, boolvar=True):

        s = requests.session()
        s.headers = OrderedDict()
        s.headers["Accept"] = "application/json, text/plain, */*"
        s.headers["Accept-Encoding"] = "gzip, deflate, br"
        s.headers["Accept-Language"] = "en-US,en;q=0.9"
        s.headers["Connection"] = "keep-alive"
        s.headers["Host"] = "api.dineoncampus.com"
        s.headers["Origin"] = "https://www.nudining.com"
        s.headers["sec-ch-ua"] = 'Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"'
        s.headers["sec-ch-ua-mobile"] = "?0"
        s.headers["sec-ch-ua-platform"] = '"Windows"'
        s.headers["Sec-Fetch-Dest"] = "empty"
        s.headers["Sec-Fetch-Mode"] = "cors"
        s.headers["Sec-Fetch-Site"] = "cross-site"
        s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"

        while boolvar:
            try:
                request_link = s.get(link, timeout=80)
                boolvar = False
            except Exception as e:
                print('Timed out', e)
                getData(link, True)

        return(request_link.text)

    # returns current date in year-month-weekday format
    def currentTime(self):
        current_date = datetime.today()
        month = current_date.month
        year = current_date.year
        weekday = current_date.day


        return(f'{year}-{month}-{weekday}')

    # checks if the file is empty
    def checkFileEmpty(self, fileName, functionName):

        try:
            if os.stat(fileName).st_size == 0:
                #print('hi1')
                variable = functionName()
                return(variable)
            else:
                #print('hi2')
                file = open(fileName, 'r')
                contents = json.loads(file.read())
                file.close()
                return(contents)
        except:
            if os.path.exists(fileName) == False:
                #print('hi3')
                variable = functionName()
                return(variable)
            else:
                #print('hi4')
                file = open(fileName, 'r')
                contents = json.loads(file.read())
                file.close()
                return(contents)

    # get location ids of all buildings and store in file locationId.txt, basically never needs updating
    def getLocationId(self):

        locationId = {}

        # get data and load it as a json for building data
        menus = json.loads(self.getData('https://api.dineoncampus.com/v1/locations/all_locations?platform=0&site_id=5751fd2b90975b60e048929a&for_menus=true&with_address=false&with_buildings=true', True))

        for x in menus['buildings']:
            for number in range(len(x['locations'])):
                locationId[x['locations'][number]['name']]= x['locations'][number]['id']
                #print(x['name'], ':\t', x['locations'][number], '\n')

        file = open('locationId.txt','w+')
        file.write(json.dumps(locationId))
        file.close()

        return(locationId)

    # date : location name: link, needs to update daily since values inside update
    def getGeneralMenuLink(self):

        date = self.currentTime()
        menuLinkDict = {}
        menuLinkDict[date] = {}
        for x in self.location:
            menuLinkDict[date][x] = {}
            menuLinkDict[date][x][self.locationIds[x]] = f'https://api.dineoncampus.com/v1/location/{self.locationIds[x]}/periods?platform=0&date={date}'

        file = open('generalMenuLink.txt','w+')
        file.write(json.dumps(menuLinkDict))
        file.close()

        return(menuLinkDict)

    # date : [location : [menutype name : id]]
    def getMenuTypeIds(self):

        date = self.currentTime()
        locationMenuTypeIds = {}
        locationMenuTypeIds[date] = {}
        for locationName in self.location:
            for locationId, link in self.generalMenuLinks[date][locationName].items():
                #print(locationName, locationId, link)
                print('Updating Menu Ids')
                try:
                    menuData = json.loads(self.getData(link))
                    menuTypes = menuData['periods']
                    menuTypeIds = {}

                    for x in menuTypes:
                        menuTypeIds[x['name']] = x['id']
                    locationMenuTypeIds[date][locationName] = {}
                    locationMenuTypeIds[date][locationName][locationId] = menuTypeIds
                except KeyError:
                    locationMenuTypeIds[date][locationName] = {}
                    locationMenuTypeIds[date][locationName][locationId] = ''
                    print('no menu available')
        file = open('menuTypeIds.txt','w+')
        file.write(json.dumps(locationMenuTypeIds))
        file.close()

        return(locationMenuTypeIds)

    # date : location : meal type : link
    def getAllSpecificLinks(self):

        date = self.currentTime()
        specificLinksDict = {}
        specificLinksDict[date] = {}

        #print(self.menuTypeIds)
        for locationName in self.menuTypeIds[date]:
            specificLinksDict[date][locationName] = {}
            for locationId in self.menuTypeIds[date][locationName]:
                for mealType in self.menuTypeIds[date][locationName][locationId]:
                    mealId = self.menuTypeIds[date][locationName][locationId][mealType]
                    specificLinksDict[date][locationName][mealType] = f'https://api.dineoncampus.com/v1/location/{locationId}/periods/{mealId}?platform=0&date={date}'
                    #print(f'https://api.dineoncampus.com/v1/location/{locationId}/periods/{mealId}?platform=0&date={date}')

                    #print(locationName, locationId, mealType, mealId)

        file = open('allSpecificLinks.txt','w+')
        file.write(json.dumps(specificLinksDict))
        file.close()

        return(specificLinksDict)

    # date : location : mealtype : data
    def getAllMenuData(self):

        date = self.currentTime()
        allMenuData = {}
        allMenuData[date] = {}
        x = 0
        for locationName in self.menuTypeIds[date]:
            allMenuData[date][locationName] = {}
            for locationId in self.menuTypeIds[date][locationName]:
                for mealType in self.menuTypeIds[date][locationName][locationId]:
                    print('Retreiving Menu Data')
                    x+=1
                    #print(self.allSpecificLinks[date][locationName][mealType])
                    allMenuData[date][locationName][mealType] = json.loads(self.getData(self.allSpecificLinks[date][locationName][mealType]))
                    time.sleep(3)
                    #print(self.allSpecificLinks[date][locationName][mealType]) # link value

        file = open('allMenuData.txt','w+')
        file.write(json.dumps(allMenuData))
        file.close()

        return(allMenuData)

    # date : location : mealtype : categories : data, FUCKED UP NEED TO FIX BC {'Trattoria': {'Rigatoni with Clam Sauce': {'calorie
    def getAllCategories(self):

        date = self.currentTime()

        allFoodCategories = {}
        allFoodCategories[date] = {}
        categories = {}

        for locationName in self.allMenuData[date]:
            allFoodCategories[date][locationName] = {}
            for mealType in self.allMenuData[date][locationName]:
                allFoodCategories[date][locationName][mealType] = {}
                if self.allMenuData[date][locationName][mealType]['menu']['periods'] == None:
                    print('refresh data set')
                else:
                    for x in range(0, len(self.allMenuData[date][locationName][mealType]['menu']['periods']['categories'])):
                        # name to data

                        name = self.allMenuData[date][locationName][mealType]['menu']['periods']['categories'][x]['name']
                        allFoodCategories[date][locationName][mealType][name] = self.allMenuData[date][locationName][mealType]['menu']['periods']['categories'][x]
                        #[self.allMenuData[date][locationName][mealType]['menu']['periods']['categories'][x]['name']] = self.allMenuData[date][locationName][mealType]['menu']['periods']['categories'][x]

        file = open('allCategories.txt','w+')
        file.write(json.dumps(allFoodCategories))
        file.close()

        return(allFoodCategories)

    # have to fix
    # date : location : mealtype : categories : item : data
    def getAllItems(self):

        date = self.currentTime()

        allItems = {}
        allItems[date] = {}
        itemData = {}

        #print(self.allCategories)
        for locationName in self.allCategories[date]:
                allItems[date][locationName] = {}
                print('Updating Menu Item Data')
                for mealType in self.allCategories[date][locationName]:
                    #print(locationName, mealType)

                    allItems[date][locationName][mealType] = {}
                    for foodCategory in self.allCategories[date][locationName][mealType]:
                        #item names
                        allItems[date][locationName][mealType][foodCategory] = {}
                        #print(mealType, ': ', foodCategory, ': ',len(self.allCategories[date][locationName][mealType][foodCategory]['items']))
                        for x in range(0, len(self.allCategories[date][locationName][mealType][foodCategory]['items'])):
                            name = self.allCategories[date][locationName][mealType][foodCategory]['items'][x]['name']
                            allItems[date][locationName][mealType][foodCategory][name] = self.allCategories[date][locationName][mealType][foodCategory]['items'][x]


        file = open('allItems.txt','w+')
        file.write(json.dumps(allItems))
        file.close()

        return(allItems)

    # date : location : mealtype : categories : item : nutrients
    def getAllItemNutrients(self):

        date = date = self.currentTime()

        allItemNutrients = {}
        allItemNutrients[date] = {}
        itemNutrients = {}

        for locationName in self.allItems[date]:
            allItemNutrients[date][locationName] = {}
            for mealType in self.allItems[date][locationName]:
                allItemNutrients[date][locationName][mealType] = {}
                for foodCategory in self.allItems[date][locationName][mealType]:
                    allItemNutrients[date][locationName][mealType][foodCategory] = {}
                    for item in self.allItems[date][locationName][mealType][foodCategory]:
                        nutrients = {'calories': self.allItems[date][locationName][mealType][foodCategory][item]['nutrients'][0]['value_numeric'],
                                    'protein': self.allItems[date][locationName][mealType][foodCategory][item]['nutrients'][1]['value_numeric'],
                                    'carbohydrates': self.allItems[date][locationName][mealType][foodCategory][item]['nutrients'][2]['value_numeric'],
                                    'fats': self.allItems[date][locationName][mealType][foodCategory][item]['nutrients'][5]['value_numeric']}

                        # value_numeric or value is value 0 is calorie, 1 is protein, 2 is carbs, 5 is fat
                        #print(self.allItems[date][locationName][mealType][foodCategory][item]['nutrients'][5])
                        allItemNutrients[date][locationName][mealType][foodCategory][item] = nutrients

        file = open('allItemNutrients.txt','w+')
        file.write(json.dumps(allItemNutrients))
        file.close()

        return(allItemNutrients)
#p = MenuData(['Levine Marketplace', 'International Village Dining', 'Food Hall at Stetson West'])
#p.getAllItemNutrients()
