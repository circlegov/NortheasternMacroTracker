# NortheasternMacroTracker

NortheasternMacroTracker is a Python tool for tracking your macros at Northeastern University.

## Installation

Install cli.py and menu.py in a new directory.

or

Install the executable from releases.

## Usage

```bash
python cli.py
```

or

```bash
python3 cli.py
```
or

```bash
Open the executable
```

Start by setting your macros.  
Then continue by choosing the foods you consumed for the day.  
To view your remaining daily macros, open currentMacros.txt.  
The amount remaining will reset to the daily macro goals once the program is reopened.

On the food menu with circles, press space to choose foods.
Do not choose the Back button while foods are chosen, the program will break. Known Bug.
## Known Bugs

If macros are not set before choosing foods, the program breaks.  
If the back button is chosen while a food is chosen, the program breaks.

## Next Steps

~~Package the program into an executable.~~  
~~Bug Fixes.~~  
~~Allow the user to update their macros throughout the day rather than all at once.~~ 
~~Allowing macros to be set automatically based on weight, age, and gender.~~
Condensing the various text files containing menu information into one file.
Rewrite the MenuData class to operate solely as a menu and not update menu information.   
Allow a user to choose their school from a list of the schools available on the Dine On Campus API.  
Add other API support such as Nutrislice API.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
