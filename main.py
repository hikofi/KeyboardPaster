import json
from pynput import keyboard
from pynput.keyboard import Key, Controller, Listener, KeyCode
import threading
import sys

def load_phrases(filename):
    try:
        with open(filename, 'r') as file:
            # 'reading'
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if there's an issue loading the file

def save_phrases(phrases, filename):
    with open(filename, 'w') as file:
        # 'writing'
        json.dump(phrases, file)

phrases = load_phrases('phrases.json')

def phraseList():
    for i, numberedList in enumerate(phrases, 1):
        print(f"--------------------------------------\n| {i} |  {numberedList}")
    print('--------------------------------------')

def addPhrase(newPhrase): 
    # requires newPhrase, this is what is passed into the code
    phrases.append(newPhrase)
    save_phrases(phrases, 'phrases.json')
    print(f"New phrase, '{newPhrase}', added! Use '1' to view all phrases.")

def remPhrase(index):
    print(f"The phrase, '{phrases[index]}', has been removed! Use '1' to view all phrases.")
    phrases.pop(index)
    save_phrases(phrases, 'phrases.json')
    
def editPhrase(editIndex):
    print(f"Editing, '{phrases[editIndex]}'!")
    editedPhrase = input("Enter the new phrase: ")
    phrases[editIndex] = editedPhrase
    save_phrases(phrases, 'phrases.json')

def main_menu():
    while True:
        print("[Main Menu]\n1. List Phases\n2. Edit Phrase\n3. Add Phrase\n4. Remove Phrase\nH. Help\nX. Exit\n")
        choice = input("Enter your choice: ")
        if choice == "1":
            if len(phrases) == 0:
                print("No phrases stored! Use '3' to add a phrase.")
            else:
                phraseList()
        elif choice == "2":
            print('[Edit Phrase]')
            if len(phrases) == 0:
                print("No phrases to edit! Use '3' to add a phrase.")
                continue
            while True:
                try:
                    phraseToEdit = input("Number of phrase (X to exit): ")
                    editIndex = int(phraseToEdit) - 1
                    # python uses 0th index
                    if 0 <= editIndex <= len(phrases) and phraseToEdit.lower != 'x':
                        editPhrase(editIndex)
                        break
                        # needs to return to main menu since it is still taking in the number from original input
                    else:
                        editIndex > len(phrases)
                        print('Invalid phrase!')
                except:
                    print('Returning to the main menu!')
                    break
        elif choice == "3":
            print('[Add Phrase]')
            newPhrase = input("Enter a new phrase (X to exit): ")
            try:
                if newPhrase.lower() != 'x':
                    addPhrase(newPhrase)
            except:
                print('Returning to the main menu!')
                break
        elif choice == "4":
            print('[Remove Phrase]')
            if len(phrases) == 0:
                print("No phrases stored! Use '3' to add a phrase.")
            else:
                while True:
                    try:
                        phraseToDelete = input("Number of phrase (X to exit): ")
                        index = int(phraseToDelete) - 1
                        # python uses 0th index
                        if 0 <= index <= len(phrases) and phraseToDelete.lower != 'x':
                            remPhrase(index)
                            break
                        else:
                            print('Invalid phrase!')
                    except:
                        print('Returning to main menu!!')
                        break    
        elif choice.lower() == "h":
            print("Use ['c' + (number of phrase)] to paste phrase.")       
        elif choice.lower() == "x":
            print("See ya later alligator. Please close the terminal!")
            sys.exit()
        else:
            print("I haven't added that feature yet! Please try again")

COMBINATIONS = [ {keyboard.KeyCode(char='c'), keyboard.KeyCode(char='1')},
                {keyboard.KeyCode(char='C'), keyboard.KeyCode(char='1')},
                {keyboard.KeyCode(char='c'), keyboard.KeyCode(char='2')},
                {keyboard.KeyCode(char='C'), keyboard.KeyCode(char='2')},
                {keyboard.KeyCode(char='c'), keyboard.KeyCode(char='3')},
                {keyboard.KeyCode(char='C'), keyboard.KeyCode(char='3')},
                {keyboard.KeyCode(char='c'), keyboard.KeyCode(char='4')},
                {keyboard.KeyCode(char='C'), keyboard.KeyCode(char='4')},
                {keyboard.KeyCode(char='c'), keyboard.KeyCode(char='5')},
                {keyboard.KeyCode(char='C'), keyboard.KeyCode(char='5')},
                {keyboard.KeyCode(char='c'), keyboard.KeyCode(char='6')},
                {keyboard.KeyCode(char='C'), keyboard.KeyCode(char='6')},
                {keyboard.KeyCode(char='c'), keyboard.KeyCode(char='7')},
                {keyboard.KeyCode(char='C'), keyboard.KeyCode(char='7')},
                {keyboard.KeyCode(char='c'), keyboard.KeyCode(char='8')},
                {keyboard.KeyCode(char='C'), keyboard.KeyCode(char='8')},
                {keyboard.KeyCode(char='c'), keyboard.KeyCode(char='9')},
                {keyboard.KeyCode(char='C'), keyboard.KeyCode(char='9')},   
        ]

current = set()
keyController = keyboard.Controller()
executed = False

def on_press(key):
    global executed
    if not executed: 
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            keyController.tap(Key.backspace)
            keyController.tap(Key.backspace)
            execute()
            executed = True

def on_release(key):
    global executed
    try:
        current.clear()
        executed = False
    except KeyError:
        pass

def execute():
    for COMBO in COMBINATIONS:
        if all(k in current for k in COMBO):
            for key in COMBO:
                try:
                    if key.char in ['1','2','3','4','5','6','7','8','9']:
                        index = int(key.char) - 1
                        if 0 <= index < len(phrases):
                            keyController.type(f"{phrases[index]}")
                            keyController.tap(Key.enter)
                            break
                        else:
                            keyController.type(f"No phrase for number: {key.char}")
                        return 
                except AttributeError:
                    pass

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as Listener:
        Listener.join()

if __name__ == "__main__":    
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
    main_menu()
    listener_thread.join()
