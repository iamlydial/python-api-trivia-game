# imported packages to make the game work
import requests  # library for making HTTP requests to fetch data from web APIs.
import pprint  # module for pretty-printing data structures,
import time  # module providing time-related functions
import random  # module for generating random numbers and shuffling sequences, useful for randomizing answer choices.

# connection to the API
trivia_categories_url = "https://opentdb.com/api_category.php"
response = requests.get(trivia_categories_url).json()
# console log to verify the response
# pprint.pprint(response)


# Mapping dictionaries for categories, difficulties, and question types
# This code creates dictionaries that map IDs to their respective names or labels
# for trivia categories, question difficulty level.

category_mapping = {}
for category in response['trivia_categories']:
    category_mapping[str(category['id'])] = category['name']

difficulty_mapping = {
    '1': 'easy',
    '2': 'medium',
    '3': 'hard'
}

game_data = {
    "score": 0,
    "correct_answers": []
}

# Defining the filename for storing the trivia game results
filename = "trivia_results.txt"

# game logic starts
welcome_message = input(">>>WELCOME TO THE TRIVIA GAME<<<\nAre you ready for a quick 10-minute Trivia Challenge? Y/N")
if welcome_message.lower() == 'y':
    # Print the category IDs and names
    for category in response['trivia_categories']:
        print(f"ID: {category['id']}, Name: {category['name']}")
    while True:
        category_selection = input("Type the category ID: ")
        selected_question = ''

        # convert the user's input from string to integer, as category IDs are usually integers
        try:
            category_selection = int(category_selection)
        except ValueError:
            print("Invalid choice! Please type a valid category ID.")
            continue

        # Check if the selected category ID exists in the list of available categories
        if any(category['id'] == category_selection for category in response['trivia_categories']):
            selected_question = category_selection
            break
        else:
            print("Invalid choice! Please type the ID of an existing category.")

    # creates an infinite loop that keep running if the input is not '1', '2', or '3'
    while True:
        # user get to select the difficulty of the questions
        difficulty_selection = input("Select Difficulty: 1 - easy; 2 - medium; 3 - hard: ")
        if difficulty_selection in ('1', '2', '3'):
            selected_difficulty = difficulty_mapping[difficulty_selection]
            break  # exit the loop if the input is valid
        else:
            print("Invalid choice! Please select 1, 2, or 3.")

    # auxiliary message for the user with selected category ID and difficulty level
    print(
        f"Selected category name: >>>{category_mapping.get(category_selection, 'Unknown')}<<<.\nSelected difficulty: >>>{selected_difficulty}<<<")

    # construct the URL for fetching trivia questions based on user's category and difficulty selections
    trivia_url = (
        f"https://opentdb.com/api.php?"
        f"amount=5&category={category_selection}"
        f"&difficulty={selected_difficulty}"
    )

    # console logs the new url to check if the trigger is correct
    # print(trivia_url)

    # second api fetch with newly constructed link
    response_1 = requests.get(trivia_url).json()
    # console log to see response
    # pprint.pprint(response_1)

    # user countdown and message for the game to start
    for i in range(3, 0, -1):
        print(f">>>{i}")
        time.sleep(1)
    print("~~~Let's go!~~~")

    # initialization of variable to store question count, score, results and answers
    question_count = 0
    score = 0
    results = response_1['results']
    user_answer = ""

    # initialize open file with write property to log the game responses
    with open(filename, "w") as file:
        # Iterate through the retrieved trivia questions while there are more questions to ask (up to 5 questions or available questions)
        while question_count < 5 and question_count < len(response_1['results']):
            current_question = response_1['results'][question_count]

            # in order to showcase the user true / false and multiple answers Qs I distinguish each case for the answer display and logic.
            if current_question['type'] == 'boolean':
                print(current_question['question'])
                print("Type 'True' or 'False' to answer:")
                user_answer = input().strip().lower()  # Convert the user's input to lowercase for case-insensitive matching

                # Check if the user's answer is correct
                if user_answer == current_question['correct_answer'].lower():
                    score += 1
                    print(f"Correct!\nYour Score: {score}")
                else:
                    print(f"Incorrect!\nYour Score: {score}")

            if current_question['type'] == 'multiple':
                print(current_question['question'])
                choices = current_question['incorrect_answers'] + [current_question['correct_answer']]
                choices = [choice.strip() for choice in choices]  # Remove leading/trailing whitespace

                # shuffles the answer choices randomly to mix up the order for user interaction
                random.shuffle(choices)

                # Display the shuffled choices
                for i, choice in enumerate(choices):
                    print(f"{i + 1}. {choice}")

                # Prompt the user to input the number corresponding to their answer choice,
                print("Type the number corresponding to your answer:")
                user_choice = input()

                try:
                    # then attempt to convert the input to an integer (subtracting 1 to adjust for zero-based indexing).
                    user_choice_index = int(user_choice) - 1
                    # Finally, assign the selected answer choice to the variable 'user_answer.'
                    user_answer = choices[user_choice_index]

                    # Check if the user's answer is correct
                    if user_answer == current_question['correct_answer']:
                        score += 1
                        print(f"Correct!\nYour Score: {score}")
                    else:
                        print(f"Incorrect!\nYour Score: {score}")

                except (ValueError, IndexError):
                    print("Invalid choice! Please select a number from the given choices.\n")

            # Write the current question, correct answer, and user's answer to the file,
            # followed by a newline to separate each question's information.
            file.write(f"Question: {current_question['question']}\n")
            file.write(f"Correct Answer: {current_question['correct_answer']}\n")
            file.write(f"User Answer: {user_answer}\n\n")

            question_count += 1

    # Write the final score for the user on a separate file that I declared at the beginning
    with open(filename, "a") as file:
        file.write(f"Correct answers: {score} / 5")

    print(f"Correct answers: {score} / 5")
    print(f'Your final score is {score}. Find the report of your game in the file: {filename}')
else:
    print(f'>>>Ok, Bye!<<<')
