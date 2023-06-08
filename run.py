import random
from time import sleep
import sys
import os
from art import *
from colorama import Fore, Back, Style

username = ""
POINTS = 0
s = "\u272a"

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
    print(Back.RED + Style.BRIGHT)
    tprint("{:>20}".format("Musical"), font="rnd-medium\n")
    print(Back.BLUE + Style.BRIGHT)
    tprint("{:>20}".format("Theater"), font="rnd-medium\n")
    print(Back.MAGENTA + Style.BRIGHT)
    tprint("{:>20}".format("quiz"), font="rnd-medium\n")
    print(Back.RESET + Style.RESET_ALL + Fore.RESET + "\n")
    print("Welcome to the Musical Theater Quiz!\n")
    while True:
        try:
            username = input("Before we start, please enter your name:\n")
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
        
        print(f"Welcome {username}!\n")
        print(
            f"Please select 1, 2, 3 or 4 from the Main Menu below.\n "
            )
        print(f"1) Play the Quiz.")
        print(f"2) Instructions.")
        print(f"3) High Scores.")
        print(f"4) Exit Game.\n")

    menu_options()
    while True:
        user_option = 0
        try:
            user_option = (int(input(f"What would you like to do,\
 {username}?\n")))
            if user_option == 1:
                clear()
                print("1 selected")
            elif user_option == 2:
                clear()
                instructions()
            elif user_option == 3:
                clear()
                print("3 selected")
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
         
def instructions():
    """
    Displays game instructions. Includes option to return to main
    menu by pressing enter key.
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

def main():
   
    welcome_page()
    clear()
    main_menu_page()

main()