# encoding: utf-8
from menu import MenuData
from pprint import pprint
from prompt_toolkit.validation import Validator, ValidationError
from PyInquirer import prompt, Separator
from examples import custom_style_3
import sys
import json
import os

# taken from pyinquirer examples to use for validation
class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

class Menus:

    def __init__(self, location, menuData):
        self.location = location
        self.menuData = menuData
        self.chosenFoods = []
        self.chosenNutrients = []
        self.macros = MenuData.checkFileEmpty(self,'macros.txt', self.menuSetMacros)

    # first menu where you see all options
    def menuFirst(self):

        prompts = [
        {
            'type': 'list',
            'name': 'menuOneChoices',
            'message': 'Menu One',
            'choices': ['Macros', 'Dining Halls', 'Exit']
        }]

        answers = prompt(prompts, style=custom_style_3)

        if answers['menuOneChoices'] == 'Macros':
            self.menuMacros()
        elif answers['menuOneChoices'] == 'Dining Halls':
            self.menuHalls()
        #elif answers['menuOneChoices'] == 'Food Eaten Today':
        #    foodEatenToday()
        #elif answers['menuOneChoices'] == 'Clear Foods':
        #    clearFood()
        elif answers['menuOneChoices'] == 'Exit':
           sys.exit()
        else:
            print('jeez broke on step 1')

    # menus for food
    def menuHalls(self):


        if menuDataAccess.location[-1] != "Back":
            choiceList = menuDataAccess.location
            choiceList.append('Back')
        else:
            pass
            print('added')

        prompts = [
        {
            'type': 'list',
            'name': 'menuTwoFoodChoices',
            'message': 'Menu Two (food)',
            'choices': menuDataAccess.location
        }]

        answers = prompt(prompts, style=custom_style_3)
        for location in menuDataAccess.location:
            #print(location)
            if answers['menuTwoFoodChoices'] == location:
                self.menuMealType(location)

                break
            elif answers['menuTwoFoodChoices'] == 'Back':
                self.menuFirst()
                break
            else:
                pass
                #print(answers)
                #print('whats wrong')


    # menus for meal types such as Breakfast Lunch Dinner
    def menuMealType(self, diningLocation):

        mealTypeList = []

        for mealType in menuDataAccess.allItemNutrients[menuDataAccess.currentTime()][diningLocation]: # maybe change later
            mealTypeList.append(mealType)

        mealTypeList.append('Back')


        prompts = [
        {
            'type': 'list',
            'message': 'Menu Types',
            'name': 'menuTypes',
            'choices': mealTypeList
        }]


        answers = prompt(prompts, style=custom_style_3)
        for mealType in mealTypeList:
            print(mealType)
            if answers['menuTypes'] == mealType:
                self.menuFoodCategory(diningLocation, mealType)
                break
            elif answers['menuTypes'] == 'Back':
                self.menuHalls()
                break
            else:
                pass
                #print('whats wrong 2')

    # menu for food categories such as pizza soup
    def menuFoodCategory(self, diningLocation, mealType):

        alphabetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        foodCategoriesChoiceList = []

        foodCategories = list(menuDataAccess.allCategories[menuDataAccess.currentTime()][diningLocation][mealType].keys())
        for category in foodCategories:
            print(category)

        for number in range(0, len(foodCategories)):
            trackedNumber = number

            if trackedNumber < 9:
                foodCategoriesChoiceList.append({'key': str(trackedNumber), 'name': foodCategories[number], 'value': foodCategories[number]}) # have to add handling that if you select choice cant select others

            else:
                alphaKey = alphabetList[trackedNumber-9]
                foodCategoriesChoiceList.append({'key': str(alphaKey), 'name': foodCategories[number], 'value': foodCategories[number]})

        foodCategoriesChoiceList.append(Separator())

        menuTypes = list(menuDataAccess.allCategories[menuDataAccess.currentTime()][diningLocation].keys())
        # broken change please
        for number in range(0, len(menuTypes)):
            if trackedNumber >= 9:
                trackedNumber +=1
                alphaKey = alphabetList[trackedNumber-10]
                foodCategoriesChoiceList.append({'key': str(alphaKey), 'name': menuTypes[number], 'value': menuTypes[number]})
            else:
                trackedNumber += 1
                foodCategoriesChoiceList.append({'key': str(trackedNumber), 'name': menuTypes[number], 'value': menuTypes[number]})


        if trackedNumber > 9:
            trackedNumber += 1
            alphaKey = alphabetList[trackedNumber-10]
            foodCategoriesChoiceList.append({'key': str(alphaKey), 'name': 'Back', 'value': 'Back'})
        else:
            trackedNumber += 1
            foodCategoriesChoiceList.append({'key': str(trackedNumber), 'name': 'Back', 'value': 'Back'})


        prompts = [
            {
                'type': 'expand',
                'message': diningLocation,
                'name': 'foodCategories',
                'choices': foodCategoriesChoiceList
            }
        ]

        answers = prompt(prompts, style=custom_style_3)

        for chosenMealType in menuTypes:
            for foodCategory in foodCategories:
                if answers['foodCategories'] == foodCategory:
                    self.menuChooseFood(diningLocation, mealType, foodCategory)
                    return
                elif answers['foodCategories'] == chosenMealType:
                    self.menuFoodCategory(diningLocation, chosenMealType)
                    return
                elif answers['foodCategories'] == 'Back':
                    self.menuMealType(diningLocation)
                    return
                else:
                    pass
                    #print('whats going on')




    # shows food of the chosen category
    def menuChooseFood(self, diningLocation, mealType, foodCategory):

        alphabetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        foodChoiceList = []

        foodChoices = list(menuDataAccess.allItemNutrients[menuDataAccess.currentTime()][diningLocation][mealType][foodCategory].keys())
        nutrients = list(menuDataAccess.allItemNutrients[menuDataAccess.currentTime()][diningLocation][mealType][foodCategory].values())

        for number in range(0, len(foodChoices)):
            foodChoiceList.append({'name': foodChoices[number] + ': ' +str(nutrients[number]).replace('{','').replace('}','').replace(',','')})

        foodChoiceList.append(Separator())

        foodChoiceList.append({'name': 'Back'})



        prompts = [
        {
            'type': 'checkbox',
            'message': mealType,
            'name': 'foodChoices',
            'choices': foodChoiceList
        }]

        confirmationPrompt = [
            {
                'type': 'confirm',
                'name': 'confirmation',
                'message': 'Are you done selecting food for the day?'
            }]

        # need to add function so you cant choose back while choosing other stuff

        answers = prompt(prompts, style=custom_style_3)

        for choice in answers['foodChoices']:
            if choice == 'Back':
                self.menuFoodCategory(diningLocation, mealType)
            else:
                foodName = choice.split(':', 1)[0]
                position = foodChoices.index(foodName)
                nutrients_used = nutrients[position]
                self.chosenFoods.append(foodName)
                self.chosenNutrients.append(nutrients_used)
        confirm = prompt(confirmationPrompt, style=custom_style_3)
        if confirm['confirmation'] == False:
            self.menuFoodCategory(diningLocation, mealType)
        else:
            new_calories = 0
            new_protein = 0
            new_carbs = 0
            new_fats = 0
            # fix if someone picks an item twice/add qualifier
            foodsFileRead = open('foodsAteToday.txt', 'r')
            if os.path.exists('foodsAteToday.txt') and os.path.getsize('foodsAteToday.txt') > 0:
                foodAteToday = json.loads(foodsFileRead.read())
                foodsFileRead.close()
                if list(foodAteToday.keys())[0] == menuDataAccess.currentTime():
                    print('update current foods')
                else:
                    foodAteToday = {}
                    foodAteToday[menuDataAccess.currentTime()] = {}
            else:
                foodAteToday = {}
                foodAteToday[menuDataAccess.currentTime()] = {}
            for foodName, nutrients_used in zip(self.chosenFoods, self.chosenNutrients):

                new_calories += float(nutrients_used['calories'])
                new_protein += float(nutrients_used['protein'])
                new_carbs += float(nutrients_used['carbohydrates'])
                new_fats += float(nutrients_used['fats'])
                foodAteToday[menuDataAccess.currentTime()][foodName] = {}
                foodAteToday[menuDataAccess.currentTime()][foodName]['calories'] = nutrients_used['calories']
                foodAteToday[menuDataAccess.currentTime()][foodName]['protein'] = nutrients_used['protein']
                foodAteToday[menuDataAccess.currentTime()][foodName]['carbs'] = nutrients_used['carbohydrates']
                foodAteToday[menuDataAccess.currentTime()][foodName]['fats'] = nutrients_used['fats']
                print(foodName, ' ', nutrients_used)

            foodsFileWrite = open('foodsAteToday.txt', 'w')
            foodsFileWrite.write(json.dumps(foodAteToday))
            foodsFileWrite.close()


            macroFile = open('macros.txt', 'r')
            contents = json.loads(macroFile.read())
            macroFile.close()
            goalCalorie = contents['calories']
            goalProtein = contents['protein']
            goalCarb = contents['carb']
            goalFat = contents['fat']

            try:
                if os.path.exists('currentMacros.txt') and os.path.getsize('currentMacros.txt') > 0:
                    currentMacroFile = open('currentMacros.txt', 'r')
                    currentContents = json.loads(currentMacroFile.read())
                    currentMacroFile.close()
                    if list(currentContents.keys())[0] == menuDataAccess.currentTime():
                        currentMacroFile = open('currentMacros.txt', 'w')
                        currentCalories = currentContents[menuDataAccess.currentTime()]['calories']
                        currentProtein = currentContents[menuDataAccess.currentTime()]['protein']
                        currentCarbs = currentContents[menuDataAccess.currentTime()]['carbs']
                        currentFats = currentContents[menuDataAccess.currentTime()]['fats']
                        currentContents[menuDataAccess.currentTime()]['calories'] = currentCalories - new_calories
                        currentContents[menuDataAccess.currentTime()]['protein'] = currentProtein - new_protein
                        currentContents[menuDataAccess.currentTime()]['carbs'] = currentCarbs - new_carbs
                        currentContents[menuDataAccess.currentTime()]['fats'] = currentFats - new_fats

                        currentMacroFile.write(json.dumps(currentContents))
                        currentMacroFile.close()
                    else:
                        raise ValueError('Dates dont match up')

                else:
                    print('doesnt exist, create')
                    raise ValueError('Doesn\'t exist')
            except ValueError as e:
                print("Error is: ", e)
                currentMacroFile = open('currentMacros.txt', 'w+')
                currentContents = {}
                currentContents[menuDataAccess.currentTime()] = contents
                currentContents[menuDataAccess.currentTime()]['calories'] = goalCalorie - new_calories
                currentContents[menuDataAccess.currentTime()]['protein'] = goalProtein - new_protein
                currentContents[menuDataAccess.currentTime()]['carbs'] = goalCarb - new_carbs
                currentContents[menuDataAccess.currentTime()]['fats'] = goalFat - new_fats

                currentMacroFile.write(json.dumps(currentContents))
                currentMacroFile.close()




    # menus for macros
    def menuMacros(self):

        prompts = [
        {
        'type': 'list',
        'name': 'menuTwoMacroChoices',
        'message': 'Menu Two (Macros)',
        'choices': ['View Macros', 'Set New Macros', 'Back']
        }]

        answers = prompt(prompts, style=custom_style_3)
        if answers['menuTwoMacroChoices'] == 'View Macros':
            self.menuViewMacros()
        elif answers['menuTwoMacroChoices'] == 'Set New Macros':
            self.menuSetMacros()
        elif answers['menuTwoMacroChoices'] == 'Back':
            self.menuFirst()
        return(prompts)

    # shows current set macros
    def menuViewMacros(self):

        macroFile = open('macros.txt', 'r')
        contents = json.loads(macroFile.read())

        goalCalorie = contents['calories']
        goalProtein = contents['protein']
        goalCarb = contents['carb']
        goalFat = contents['fat']

        print(f'calories:{goalCalorie}\nprotein:{goalProtein}\ncarb:{goalCarb}\nfat:{goalFat}')

        prompts = [
        {
            'type': 'list',
            'name': 'viewMacroChoices',
            'message': 'Choose:',
            'choices': ['Set New Macros', 'Back']
        }]

        answers = prompt(prompts, style=custom_style_3)
        if answers['viewMacroChoices'] == 'Set New Macros':
            self.setNewMacros()
        elif answers['viewMacroChoices'] == 'Back':
            self.menuMacros()
        else:
            print('Unknown Error')

    # menu to set macros
    def menuSetMacros(self):

        confirmationPrompt = [
            {
                'type': 'confirm',
                'name': 'confirmation',
                'message': 'Do you want to continue?'
            }]

        macros = {'protein': '','fat': '','carb': '', 'calories':''}

        for item in ['protein','fat', 'carb', 'calories']:
            message = f'What is your goal {item} amount?'
            prompts = [
                {
                    'type': 'input',
                    'name': item,
                    'message': message,
                    'validate': NumberValidator, # need to brush up on classes and rewrite after
                    'filter': lambda val: int(val) # anonymous function filters to show only int
                }]


            answers = prompt(prompts, style=custom_style_3)
            confirmation = prompt(confirmationPrompt, style=custom_style_3)

            while confirmation['confirmation'] == False:
                answers = prompt(prompts, style=custom_style_3)
                confirmation = prompt(confirmationPrompt, style=custom_style_3)

            macros[item] = list(answers.values())[0]

        file = open('macros.txt', 'w+')
        file.write(json.dumps(macros))
        file.close()

        self.menuMacros()
    # future feature to show updated macros in the program
    def menuDailyMacros(self):
        pass
# location, foodCategories, foodNameNutrition
if __name__ == '__main__':
    mainLocations = ['Levine Marketplace', 'International Village Dining', 'Food Hall at Stetson West']
    menuDataAccess = MenuData(mainLocations)
    menu = Menus(mainLocations, menuDataAccess.allItemNutrients)
    menu.menuFirst()
