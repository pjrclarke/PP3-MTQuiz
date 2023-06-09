import random
from time import sleep
import sys
import os
import re
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


# GLOBAL FUNCTIONS
USERNAME = ""
POINTS = 0
NUM_QUESTIONS_PER_QUIZ = 53


def clear():
    """
    Clears the screen
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def welcome_page():
    """
    The page that greets the user, promting to enter their username
    """
    global USERNAME
    print(Fore.LIGHTRED_EX)
    tprint("Musical Theatre", font="small")
    print(Fore.LIGHTBLUE_EX)
    tprint("{:>25}".format("Quiz"), font="medium")
    print(Fore.RESET)
    print("Welcome to the Musical Theater Quiz!")
    while True:
        USERNAME = input("Before we start, please enter your name:\n")
        if not re.match("^[a-zA-Z_]*$", USERNAME):
            clear()
            print(f"\n'{USERNAME}' contains special characters or numbers.\n")
            print("Your username should only contain letters / underscores.\n")
        elif len(USERNAME) < 3 or len(USERNAME) > 10:
            clear()
            print(f"\n{USERNAME} is either too small or too big.")
            print("Username must be 3 - 10 characters long.\n")
        else:
            break
    return USERNAME


def main_menu_page():
    """
    The main menu giving the user options to select.
    """
    def menu_options():
        print(f"You! Yes you, you're {USERNAME} right?!\n")
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
 {USERNAME}?\n")))
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
                \nThanks for visiting the Musical Theater Quiz, {USERNAME}!\n")
                print("Come back soon!")
                sleep(1)
                sys.exit()
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


def instructions():
    """
    Displays instructions. Includes option to return to main
    menu.
    """
    print(Fore.LIGHTBLUE_EX)
    tprint("Instructions", font="small")
    print(Fore.RESET)
    print("To play, you have to try & answer questions correctly")
    print("To select your answer, enter the corresponding letter")
    print("and then press Enter. Every correct answer is worth one point.\n")
    print(Fore.LIGHTRED_EX+"Incorrect answer? GAME OVER.\n"+Fore.RESET)
    print("Your points are recorded and uploaded to the leaderboard.")
    print("If you scored high enough, you could be in the top 10 and see your")
    print("name on the leaderboard.\n")
    print("**To quit the game during play, press the letter Q to")
    print("return to main menu**\n")
    try:
        input(f"If you're ready, press Enter to go back to main menu.")
        clear()
        main_menu_page()
    except SyntaxError:
        pass


def leaderboard():
    """
    Pulls data from a googlesheet and displays this as a leaderboard for
    users to see if they reach the top 10
    """
    print(Fore.LIGHTBLUE_EX)
    tprint("Leaderboard", font="small")
    SHEET.sheet1.sort((2, 'des'))
    row_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    page = SHEET.sheet1.get_all_values()
    page_updated = []
    index = 0
    while index < 10:
        try:
            page_updated.append(page[index])
        except IndexError:
            page_updated.append('')
        index += 1
        print(tabulate(page_updated, headers=["POSITION", "NAME", "POINTS"],
              tablefmt='double_grid', numalign="center", showindex=row_id))
    try:
        input(Fore.RESET + "Press enter to return to the main menu")
        clear()
        main_menu_page()
    except SyntaxError:
        pass


def gameover():
    """
    Function when the game ends, gives users the option to play again or
    go back to the main menu. Functions here for errors also.
    """
    while True:
        try:
            game_over_end = input(f"""Play again, {USERNAME}?\n
Type y for yes or q to quit to the menu\n""")
        except ValueError:
            sleep(0.2)
            print("You know that wasn't a correct option... Try again.")
        if game_over_end == "q":
            clear()
            main_menu_page()
        elif game_over_end == "y":
            clear()
            play()
        else:
            sleep(0.2)
            print("You know that wasn't a correct option... Try again.")


def play():
    """
    The main quiz game section.

    This houses the functions for;

    - Randomising the questions that are housed in the questions.toml file.
    - What happens when the user guesses correctly.
    - What happens when the user selects a wrong option.
    - How many points are awarded and displays this on screen.

    """
    clear()
    print(f"Let's start the quiz, {USERNAME}.\n")
    print("Answer as many questions as you can.\n")
    print("Each correct answer earns you one point.\n")
    print(f"Remember, {USERNAME}...")
    print("You only get" + Fore.LIGHTRED_EX + " ONE " + Fore.RESET + "life.\n")
    print("Type 'Q' to quit the game and return to the main menu.\n")
    print("The Quiz will start shortly. Good Luck!")
    sleep(5)
    clear()
    global POINTS
    questions = prepare_questions(
        QUESTIONS, num_questions=NUM_QUESTIONS_PER_QUIZ)
    POINTS = 0
    num_correct = 0
    for num, (question, alternatives) in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        print(f"\n{question}\n")
        correct_answer = alternatives[0]
        labeled_alternatives = dict(zip(ascii_lowercase, sorted(alternatives)))
        for label, alternative in labeled_alternatives.items():
            print(f"{label.upper()}){alternative}")
        if num_correct == 50:
            clear()
            print(f"Well done {USERNAME}!")
            print(f"You got {POINTS} points!!")
            print("You truly are a musical knowledge genius!")
            update_leaderboard()
            game_over()
            return
        while True:
            answer_label = input("\nWhat's your answer?\n").lower()
            if answer_label == "q":
                clear()
                main_menu_page()
                break
            elif answer_label in labeled_alternatives:
                answer = labeled_alternatives[answer_label]
                if answer == correct_answer:
                    POINTS += 1
                    print(Fore.LIGHTGREEN_EX + "\n Correct!\n" + Fore.RESET)
                    print(f"Good Job, {USERNAME}!")
                    print(f"You have {Fore.GREEN}{POINTS}{Fore.RESET} points.")
                    sleep(2)
                    clear()
                    break
                else:
                    print(Fore.RED + "Incorrect!" + Fore.RESET)
                    print("The correct answer was",
                          f"{Fore.GREEN}{correct_answer}!{Fore.RESET}")
                    sleep(3)
                    clear()
                    print(Fore.LIGHTRED_EX)
                    tprint("{:>15}".format("GAME OVER\n"), font="rnd-medium\n")
                    print(Fore.RESET)
                    print(f"Good effort, {USERNAME}.\n")
                    print(f"You got {POINTS} points.\n")
                    print("Your score will be added to the leaderboard.\n")
                    update_leaderboard()
                    gameover()
                    return
            else:
                print(Fore.LIGHTRED_EX)
                print("Invalid entry! Enter a valid option or 'Q' to quit.")
                print(Fore.RESET)


def prepare_questions(questions, num_questions):
    num_questions = min(num_questions, len(QUESTIONS))
    return random.sample(list(QUESTIONS.items()), k=num_questions)


def update_leaderboard():
    """
    Update the googlesheet with the username and their points.
    """
    data = USERNAME, POINTS
    print("Updating leaderboard...\n")
    leaderboard_sheet = SHEET.worksheet("leaderboard")
    leaderboard_sheet.append_row(data)
    print("Leaderboard updated successfully.\n")


def main():
    """
    Main functions that run to make the game start
    """
    welcome_page()
    clear()
    main_menu_page()


main()
