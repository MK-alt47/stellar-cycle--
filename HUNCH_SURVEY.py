total_questions = 10
storage = []

survey_questions = [
    {
        "id": 1,
        "question": "Enter your email",
        "type": "open_ended",
        "options": []
    },
    {
        "id": 2,
        "question": "Enter your password",
        "type": "open_ended",
        "options": []
    },
    {
        "id": 3,
        "question": "Enter your height (EX: 5.4 = 5 feet 4 inches)",
        "type": "int_open_ended",
        "options": []
    },
    {
        "id": 4,
        "question": "Would you like to enter your weight in lbs (Y/N)?",
        "type": "weight_open_ended",
        "options": []
    },
    {
        "id": 5,
        "question": "Enter your home timzeone (-11 to +12)",
        "type": "int_open_ended",
        "options": []
    },
    {
        "id": 6,
        "question": "Enter time you usually go to bed at (In Military time 0-23)",
        "type": "open_ended",
        "options": []
    },
    {
        "id": 7,
        "question": "Enter how well you usually sleep every night (1 = Terribly 10 = Amazing)",
        "type": "multiple_choice",
        "options": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", ]
    },
    {
        "id": 8,
        "question": "How much do your travel (outside of state/country)",
        "type": "multiple_choice",
        "options": ["1 - Never Travel", "2 - Travel Once Every Few Years", "3 - Travel Once or Twice a Year", "4 - Traveling Almost Every Month", "5 - Travel Everyday"]
    },
    {
        "id": 9,
        "question": "Enter how many cups of coffee/cans of energy drinks you usually drink in a day",
        "type": "int_open_ended",
        "options": []
    },
    {
        "id": 10,
        "question": "Enter how many meals you usually eat daily",
        "type": "int_open_ended",
        "options": []
    }
]

responses = {}

print(f"Welcome to the Survey! \n In this survey we will ask you {total_questions} and you will answer them all so we can get a perfect schedule set up for you.")

for q in survey_questions:
    print(f"\nQuestion {q['id']}: {q['question']}")
    
    # Render options if multiple choice
    if q['type'] == "multiple_choice":
        for idx, option in enumerate(q['options'], 1):
            print(f"  {idx}. {option}")
        
        # Validate choice input
        while True:
            try:
                choice = int(input("Please select an option (number): "))
                if 1 <= choice <= len(q['options']):
                    responses[q['id']] = q['options'][choice - 1]
                    storage.append(choice)
                    break
                print("Invalid choice. Please select from the listed options.")
            except ValueError:
                print("Please enter a valid number.")
                
    # Handle open-ended questions
    elif q['type'] == "open_ended":
        question = input("Your answer: ").strip()
        responses[q['id']] = question
        storage.append(question)

    elif q['type'] == "weight_open_ended":
        while True:
            question = input("Your answer: ").strip()
            if question == "y" or question == "Y":
                try:
                    weight = input("Enter your weight (In lbs, don't include lbs): ")
                    number = weight * int(0.453592)
                    responses[q['id']] = question
                    storage.append(number)
                    break
                except ValueError:
                    print("Invalid answer, try again.")

                break
            
            elif question == "n" or question == "N":
                try:
                    weight = input("Enter your weight (In kg, don't include kg): ")
                    number = float(weight)
                    responses[q['id']] = question
                    storage.append(number)
                    break
                except ValueError:
                    print("Invalid answer, try again.")

                break

            else:
                print("Invalid answer, please try again.")

    elif q['type'] == "int_open_ended":
            while True:
                question = input("Your answer: ").strip()
                try:
                    number = float(question)
                    break
                except ValueError:
                    print("Invalid answer, try again.")

            responses[q['id']] = question
            storage.append(question)

# Display or save results
print("\n--- Survey Complete! We will get you on your way shortly! ---")
print(storage)
