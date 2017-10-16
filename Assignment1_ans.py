#   Author SMIT N DOSHI
#   Tried to make using MVC (Model View Controller) DESIGN PATTERN


# FUNCTIONS FOR DISPLAYING VALUES

def displaytMainMenu():
    print("----------------------------------------------------")
    print("Select category:")
    print("1. Drink")
    print("2. Snacks")
    print("3. Exit")

def displayDrinkMenu():
    print("----------------------------------------------------")
    print("Water <$1>")
    print("Juice <$3>")
    print("Soda <$1.5>")

def displaySnacksMenu():
    print("----------------------------------------------------")
    print("Chips <$1.25>")
    print("Peanuts <0.75>")
    print("Cookies <$1.5>")




def userIntValidation(usrInt):
    while True:
        try:
            userInput = int(input(usrInt))
        except ValueError:
            print("\nInvalid Input \n")
            continue

        if userInput <= 0:
            print("please Number greater than zero")
            continue
        else:
            return userInput
            break

def userStrValidation(userStr):
    while True:
        userInput = input(userStr)
        if userInput not in ["Water","water","WATER","JUICE","juice","Juice","Soda","soda","SODA","Chips",
                            "chips","CHIPS","COOKIES","cookies","Cookies","Peanuts","PEANUTS","peanuts","X","x"]:
            print("Invalid Selection")
        else:

# I am Happy with the user's Input

            return userInput
            break

# Above Function is Tested and Working Fine

def mainLogic():
# use of global variable

    global infiniteLoop1
    infiniteLoop1 = 1
    displayonce = 1

# initial Amount paid by user = 0, total purchase amount = 0 and changeAmount = noOfDollar

    amountuserpaid       =  0
    totalpurchaseamount  =  0
    changeamount         =  0

# STORE THE VALUE OF WATER, JUICE and SODA for Quater Calculation

    water = 1
    juice = 3
    soda = 1.5

# STORE THE VALUE OF Chips, Peanuts and Cookies for Quater Calculation

    chips = 1.25
    cookies = 1.5
    peanuts = 0.75

    print("***** Welcome to the UB Vending Machine *****")

# Input directly sent to the function(passing parameters to the Function) and validated

    numberOFQuater  = userIntValidation("Enter the number of Quaters you wish to insert:")

    numberofdollars = numberOFQuater * 0.25

# converted amount

    amountuserpaid = numberofdollars
    changeamount   = numberofdollars

# Below is an While in Infinite Loop

    while infiniteLoop1 == 1:

        if numberofdollars < 1:

            print("Please Enter more Quaters inorder to buy")

        else:
# After Checking No of Dolars display main menu

# To display below print statement once. I have used an if condition


            if displayonce == 1:

                print("You entered", changeamount,"dollars")

# Disabling the above print statement
                displayonce = displayonce - 1

                displaytMainMenu()
            else:
                displaytMainMenu()

# Now again check the user input selection is int or not and are they within the range
            userOption = userIntValidation("Select an Option:")



# Now check if the usersOption is from 1 to 3 or not using if
            if userOption == 1:
#                print("Printing Drink Menu")
                displayDrinkMenu()

# variable  userDrinkInput to accept user input and validate through function

                userdrinksinput = userStrValidation("Enter your drink selection <x to exit>:")

#                print("Users Drink Input Taken and will check")
# if for checking user can purchase or not

                if changeamount >= 0.75:

#                    print("Printing users change amount", changeamount)

                    if (userdrinksinput == "water" or userdrinksinput == "Water" or userdrinksinput == "WATER")and (changeamount >= water):
                        changeamount = changeamount - water
                        print("Vending: Water, you have",changeamount,"left")

                    elif (userdrinksinput == "juice" or userdrinksinput == "Juice" or userdrinksinput == "JUICE")and (changeamount >= juice):
                        changeamount = changeamount - juice
                        print("Vending: Juice, you have",changeamount,"left")

                    elif (userdrinksinput == "soda" or userdrinksinput == "Soda" or userdrinksinput == "SODA") and (changeamount >= soda):
                        changeamount = changeamount - soda
                        print("Vending: Soda, you have",changeamount,"left")

                    elif userdrinksinput == "x" or userdrinksinput == "X":

#                        print("User selected X so printing main menu")

                        displaytMainMenu()

# Else part acting as Default print if the userinput is not from the range
                    else:
                        print("Sorry you can't purchase")

# Else part for checking changeamount that user has
                else:
                    print("Please Add More Quaters")


# END of DRINK MENU SELECTION

# START OF SNACKS MENU SELECTION

            elif userOption == 2:

#                print("Printing Snacks Menu")

                displaySnacksMenu()

# variable  usersnackinput to accept user input and validate through function

                usersnackinput = userStrValidation("Enter your Snacks selection <x to exit>:")

#                print("Users Snacks Input Taken and will check")

# if for checking user can purchase or not

                if changeamount >= 1:

#                    print("Printing users change amount", changeamount)

                    if (usersnackinput == "chips" or usersnackinput == "Chips" or usersnackinput == "CHIPS") and (changeamount >= chips):
                        changeamount = changeamount - chips
                        print("Vending: Chips, you have",changeamount,"left")

                    elif (usersnackinput == "cookies" or usersnackinput == "Cookies" or usersnackinput == "COOKIES")and (changeamount >= cookies):
                        changeamount = changeamount - cookies
                        print("Vending: Cookies, you have",changeamount,"left")

                    elif (usersnackinput == "peanuts" or usersnackinput == "Peanuts" or usersnackinput == "PEANUTS")and (changeamount >= peanuts):
                        changeamount = changeamount - peanuts
                        print("Vending: Peanut, you have",changeamount,"left")

                    elif usersnackinput == "x" or usersnackinput == "X":

#                        print("User selected X so printing main menu")

                        displaytMainMenu()

# Else part acting as Default print if the userinput is not from the range
                    else:
                        print("Please Check the input")

# Else part for checking ChangeAmount that user has
                else:
                    print("Sorry you can't purchase")

# END OF SNACKS SELECTION MENU

# START OF EXIT OPTION

            elif userOption == 3:

# CALCULATE

                totalpurchaseamount = numberofdollars - changeamount
                print("Paid Amount: {}, Total Purchase: {}, Change: {}".format(amountuserpaid,totalpurchaseamount,changeamount))
                infiniteLoop1 = 0

# END OF EXIT OPTION

# Below is an Else Part for the mainMenu, userOption selection
            else:
                print("Please Enter the Number from the Options")

# End of While InfiniteLoop part

# THIS MY FUNCTION CALLING BLOCK or call to MAIN LOGIC
mainLogic()