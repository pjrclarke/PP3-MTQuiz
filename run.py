import random
from time import sleep
import os
from art import *
from colorama import Fore, Back, Style

username = ""
POINTS = 0


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def welcome_page():
 
    global username
    print(Back.RED + Style.BRIGHT + "\n")
    tprint("Musical", font="rnd-medium\n")
    print(Back.BLUE + Style.BRIGHT)
    tprint("Theater", font="rnd-medium\n")
    print(Back.MAGENTA + Style.BRIGHT)
    tprint("quiz", font="rnd-medium\n")
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
            
def main():
   
    welcome_page()
    clear()
    main_menu_page()

main()