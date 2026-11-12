names = ['example123']
password = ['1234567890']
height = ['5.10']
weight = [59.87]
timezone = ['-4']
sleeptime = ['23']
sleepwellness = [7]
travel = [2]
coffee = ['0']
meals = ['3']

question = input("Enter section you'd like to update: ")
if question == "username" or question == "Username":
    update = input("Enter new Username: ")
    names[0] = update
    print(f"New username: {names}")
elif question == "password" or question == "Password":
    update = input("Enter new Passowrd: ")
    password[0] = update
    print(f"New password: {password}")
elif question == "height" or question == "Height":
    update = input("Enter height: ")
    height[0] = update
    print(f"New height: {height}")
elif question == "weight" or question == "Weight":
    update = input("Enter weight: ")
    weight[0] = update
    print(f"New weight: {weight}")
elif question == "timezone" or question == "Timezone":
    update = input("Enter Timezone: ")
    timezone[0] = update
    print(f"New timezone: {timezone}")
elif question == "sleeptime" or question == "Sleeptime":
    update = input("Enter time you usually go to sleep: ")
    sleeptime[0] = update
    print(f"New time you usually go to sleep: {sleeptime}")
elif question == "sleep wellness" or question == "Sleep wellness":
    update = input("Enter how well you sleep on a scale of 1-10: ")
    sleepwellness[0] = update
    print(f"New sleep welness: {sleepwellness}")
elif question == "travel" or question == "Travel":
    update = input("Enter how much you travel: ")
    travel[0] = update
    print(f"New travel amount: {travel}")
elif question == "caffine" or question == "Caffine":
    update = input("Enter how many cups of coffee/cans of energy drinks you drink daily: ")
    coffee[0] = update
    print(f"New amount of caffine: {coffee}")
elif question == "meals" or question == "Meals":
    update = input("Enter the number of meals you eat daily: ")
    meals[0] = update
    print(f"New number of meals: {meals}")