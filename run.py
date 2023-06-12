import random
from time import sleep
import sys
import os
import gspread 
from tabulate import tabulate
from google.oauth2.service_account import Credentials
from art import *
from colorama import Fore, Back, Style
import pathlib
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from string import ascii_lowercase

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("musical_quiz")

QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions.toml"
QUESTIONS = tomllib.loads(QUESTIONS_PATH.read_text())
username = ""
POINTS = 0
s = "\u272a"
NUM_QUESTIONS_PER_QUIZ = 15

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def welcome_page():
    global username
    print(Fore.LIGHTYELLOW_EX + s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s + Fore.RESET)
    print(Fore.LIGHTRED_EX + Style.BRIGHT)
    tprint("{:>10}".format("Musical"), font="rnd-medium\n" +
        Fore.RESET + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s + Fore.RESET)
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT)
    tprint("{:>15}".format("Theater"), font="rnd-medium\n" +
        Fore.RESET + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s + Fore.RESET)
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT)
    tprint("{:>20}".format("quiz"), font="rnd-medium\n" +
        Fore.RESET + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s + Fore.RESET)
    print(Style.RESET_ALL + Fore.RESET + "\n")
    print("Welcome to the Musical Theater Quiz!\n")
    while True:
        try:
            username = input("Before we start, please enter your name:\n\n")
        except ValueError:
            clear()
            print(f"\n{username} is invalid entry!")
            print("Username must be 3 - 10 characters\n")
        if (len(username) >= 3 and len(username) <= 10 and
                username.count("  ") <= 0):
            break
        else:
            clear()
            print(f"\n{username} is invalid entry!")
            print("Username must be 3 - 10 characters long\n")

def main_menu_page():

    def menu_options():
        print(f"You! Yes you, you're {username} right?!\n")
        print(
            f"Please select 1, 2, 3 or 4 from the Main Menu below.\n "
            )
        print(f"1) Play the Quiz.")
        print(f"2) Instructions.")
        print(f"3) Leaderboard.")
        print(f"4) Exit Game.\n")

    menu_options()
    while True:
        user_option = 0
        try:
            user_option = (int(input(f"What would you like to do,\
 {username}?\n")))
            if user_option == 1:
                clear()
                play()
            elif user_option == 2:
                clear()
                instructions()
            elif user_option == 3:
                clear()
                leaderboard()
            elif user_option == 4: 
                clear()
                print(f"\
                Thanks for visiting the Musical Theater Quiz {username}!")
                sleep(1)
                exit()
            else:
                clear()
                menu_options()
                sleep(0.2)
                print(f"Not a valid entry!")
                print(f"Please enter 1, 2, 3 or 4!\n")
        except ValueError:
            clear()
            menu_options()
            sleep(0.2)
            print(f"Not a valid entry!")
            print(f"Please enter 1, 2, 3 or 4!\n")

def prepare_questions(questions, num_questions):
    num_questions = min(num_questions, len(questions))
    return random.sample(list(questions.items()), k=num_questions)

def get_answer(question, alternatives):
    print(f"\n{question}?\n")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    for label, alternative in labeled_alternatives.items():
        print(f"  {label}) {alternative}")

    while (answer_label := input("\nWhat's your answer?\n")) not in labeled_alternatives:
        print(f"Please answer one of {', '.join(labeled_alternatives)}")

    return labeled_alternatives[answer_label]

def ask_question(question, alternatives):
    correct_answer = alternatives[0]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answer = get_answer(question, ordered_alternatives)
    if answer == correct_answer:
        print(Fore.LIGHTGREEN_EX + "\n\n Correct! Great Job!\n\n" + Fore.RESET)
        sleep(2)
        clear()
        return 1
    else:
        print(Fore.LIGHTRED_EX + f"\n\nNope! You really thought that {answer!r}",
            "was the answer?" + Fore.RESET)
        sleep(2)
        clear()
        return 0

def play():
    questions = prepare_questions(
        QUESTIONS, num_questions=NUM_QUESTIONS_PER_QUIZ
    )

    num_correct = 0
    for num, (question, alternatives) in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        num_correct += ask_question(question, alternatives)

    print(f"\nYou got {num_correct} correct out of {num} questions\n")
    print("Your total will be added onto the leaderboard, did you make,"
        "the top 10?\n")
    print(f"Didn't do well, {username}? Try again!\n")
    update_leaderboard()
    main_menu_page()

def instructions():
    """
    Displays instructions. Includes option to return to main
    menu.
    """
    print(Fore.LIGHTGREEN_EX)
    tprint("{:>20}".format("Instructions"), font="rnd-medium\n")
    print(Fore.RESET)
    print("To play the game, all you have to do is answer all")
    print("30 questions correctly.\n")
    print("To select your answer, enter corresponding number and press enter.")
    print("Every correct answer is worth 1 point.\n\n")
    print(Fore.LIGHTRED_EX + "If you get a question wrong your game is over.\n\n" + Fore.RESET)
    print("Your points are recorded and uploaded to the leaderboard.\n")
    print("If you've done well enough, you could be in the top 10 and see your")
    print("name on the leaderboard.\n")
    print("To quit the game during play, press the letter Q to")
    print("return to main menu\n")
    try:
        input("Press Enter to go back to main menu...\n")
        clear()
        main_menu_page()
    except SyntaxError:
        pass

def leaderboard():
    print(Fore.LIGHTGREEN_EX)
    tprint("LEADERBOARD", font="rnd-medium\n")
    print(Fore.RESET)
    SHEET.sheet1.sort((2, 'des'))
    row_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    page = SHEET.sheet1.get_all_values()
    print(tabulate(page[0:10], headers=["POSITION", "NAME", "POINTS"],
                   tablefmt='fancy_grid', numalign="center", showindex=row_id))
    try:
        input("Press enter to return to the main menu")
        clear()
        main_menu_page()
    except SyntaxError:
        pass

def update_leaderboard():
    """
    Update the worksheet with the user name and their final points.
    """
    data = USER_NAME, POINTS
    print("Updating leaderboard...\n")
    leaderboard_sheet = SHEET.worksheet("main")
    leaderboard_sheet.append_row(data)
    print("Leaderboard updated successfully.\n")

def main():
    welcome_page()
    clear()
    main_menu_page()

main()