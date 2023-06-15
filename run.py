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

"""
GLOBAL FUNCTIONS
"""
USERNAME = ""
POINTS = 0
S = "\u272a"
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
    print(Fore.LIGHTYELLOW_EX + S, S, S, S, S, S, S, S,
	    S, S, S, S, S, S, S, S, S, S, S, S, S, S, S, S + Fore.RESET)
    print(Fore.LIGHTRED_EX + Style.BRIGHT)
    tprint("Musical", font="small" +
        Fore.RESET + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT)
    tprint("Theater", font="small" +
        Fore.RESET + Style.RESET_ALL)
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT)
    tprint("Quiz", font="small" +
        Fore.RESET + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + S, S, S, S, S, S, S, S,
	    S, S, S, S, S, S, S, S, S, S, S, S, S, S, S, S + Fore.RESET)
    print(Style.RESET_ALL + Fore.RESET)
    print("Welcome to the Musical Theater Quiz!")
    while True:
        try:
            USERNAME = input("Before we start, please enter your name:\n")
        except ValueError:
            clear()
            print(f"\n{USERNAME} is invalid entry!")
            print("Username must be 3 - 10 characters\n")
        if (len(USERNAME) >= 3 and len(USERNAME) <= 10 and
                USERNAME.count("  ") <= 0):
            break
        else:
            clear()
            print(f"\n{USERNAME} is invalid entry!")
            print("Username must be 3 - 10 characters long\n")

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
                Thanks for visiting the Musical Theater Quiz, {USERNAME}!")
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

def instructions():
    """
    Displays instructions. Includes option to return to main
    menu.
    """
    print(Fore.LIGHTGREEN_EX)
    tprint("Instructions", font="small")
    print(Fore.RESET)
    print("To play the game, you have to try and answer as many questions correctly")
    print("as you can. To select your answer, enter the corresponding")
    print("letter and press enter. Every correct answer is worth one point\n")
    print(Fore.LIGHTRED_EX + "If you get a question wrong your game is over.\n" + Fore.RESET)
    print("Your points are recorded and uploaded to the leaderboard.")
    print("If you've done well enough, you could be in the top 10 and see your")
    print("name on the leaderboard.")
    print("**To quit the game during play, press the letter Q to")
    print("return to main menu**\n")
    try:
        input(f"When you're ready {USERNAME}, press Enter to go back to main menu...")
        clear()
        main_menu_page()
    except SyntaxError:
        pass

def leaderboard():
    """
    Pulls data from a googlesheet and displays this as a leaderboard for 
    users to see if they reach the top 10
    """
    print(Fore.LIGHTGREEN_EX)
    tprint("LEADERBOARD", font="small")
    SHEET.sheet1.sort((2, 'des'))
    row_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    page = SHEET.sheet1.get_all_values()
    page_updated = []
    index = 0
    while index < 10:
        try:
            page_updated.append(page[index])
        except:
            page_updated.append('')
        index +=1
    print(tabulate(page_updated, headers=["POSITION", "NAME", "POINTS"],
                tablefmt='double_grid', numalign="center", showindex = row_id))
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
            game_over_end = input(f"""Would you like to play again, {USERNAME}?\n
Type Y for yes or Q to quit to the menu\n""")
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
    global POINTS
    questions = prepare_questions (
        QUESTIONS, num_questions = NUM_QUESTIONS_PER_QUIZ)
    POINTS = 0
    num_correct = 0
    for num, (question, alternatives) in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        print(f"\n{question}\n")
        correct_answer = alternatives[0]
        labeled_alternatives = dict(zip(ascii_lowercase, sorted(alternatives)))
        for label, alternative in labeled_alternatives.items():
            print(f"{label.upper()}){alternative}")
        if num_correct >= 50:
            clear()
            print(f"Well done {USERNAME}!")
            print(f"You got {POINTS} points!!")
            print("You truly are a musical knowledge genius!")
            update_leaderboard()
            game_over()
            return
        
        while (answer_label := input("\nWhat's your answer?\n")) not in labeled_alternatives:
            print(f"Please answer one of {', '.join(labeled_alternatives)}")
            if answer_label == "q":
                clear()
                main_menu_page()
            else:
                clear()
                print(f"\nNot a valid option\n")
                print(f"Please enter {','.join(labeled_alternatives).upper()}",
                        "or Q to quit to the main menu")
        answer = labeled_alternatives[answer_label]
        if answer == correct_answer:
            POINTS += 1
            print(Fore.LIGHTGREEN_EX + "\n Correct!\n" + Fore.RESET)
            print(f"Good Job, {USERNAME}!") 
            print("You have " + Fore.GREEN + f"{POINTS}" + Fore.RESET + " points.\n\n")
            sleep(2)
            clear()      
        elif answer != correct_answer and num_correct == 0:
            clear()
            print(Fore.LIGHTRED_EX)
            tprint("{:>15}".format("GAME OVER\n\n"), font="rnd-medium\n")
            print(Fore.RESET)
            print(f"Good effort, {USERNAME}.\n\n")
            print(f"You got {POINTS} points.\n")
            print("Your score will be added to the leaderboard.\n")
            update_leaderboard()
            gameover()
        else:
            update_leaderboard()
            gameover()

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