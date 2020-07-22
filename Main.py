import tkinter as tk
import requests
import time
from tkinter import scrolledtext
from tkinter import messagebox
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary

"""
    File Name: Main.py
    Author: Ryan Bell
    Date Created: 7/20/2020
    Date Last Modified: 7/22/2020
    Python Version: 3.8.5
"""

DICTIONARY_URL = "https://www.dictionary.com/browse/"
MERRIAM_URL = "https://www.merriam-webster.com/dictionary/"


def init_gui(window):
    """Initializes the Graphical User Interface that are static"""

    #Dictionary.com button
    dictionary_com = tk.Button(window, text="Dictionary.com", bd=3, bg="#4e89bf", fg="#000000", activebackground="#2b5072", command= lambda: handle_button("Dictionary.com"))
    dictionary_com.grid(row=1, column=0, padx=3)

    #Merriam-webster button
    merriam_webster = tk.Button(window, text="Merriam-Webster", bd=3, bg="#4e89bf", fg="#000000", activebackground="#2b5072", command= lambda: handle_button("Merriam-Webster"))
    merriam_webster.grid(row=1, column=1, padx=3)

    #PyDictionary button
    py_dictionary = tk.Button(window, text="PyDictionary", bd=3, bg="#4e89bf", fg="#000000", activebackground="#2b5072", command= lambda: handle_button("PyDictionary"))
    py_dictionary.grid(row=1, column=2, padx=3)

    #Title above the word entry box
    word_title = tk.Label(window, text="Find definition for the word:", bg="#272626", fg="#ffffff", font=("Arial", 11))
    word_title.grid(row=2, columnspan=3, sticky="w e")
    
    #Search button you click after inputting a word to search for
    search_button = tk.Button(window, text="Search for Definition", bd=3, bg="#4e89bf", fg="#000000", activebackground="#2b5072", width=20, command= lambda: search_word(word_entry.get()))
    search_button.grid(row=4, columnspan=3, sticky="e")

    #Clear button to clear various texts on the gui
    clear_button = tk.Button(window, text="Clear", bd=3, bg="#4e89bf", fg="#000000", activebackground="#2b5072", width=20, command=clear)
    clear_button.grid(row=4, columnspan=3, sticky="w")


def clear():
    """Clears the definition title, definition, and word entry input"""
    word_entry.delete(0, 'end')
    definition_title.configure(text="Definition for :")
    definition_display.delete(1.0, 'end')


def handle_button(dictionary):
    """Handles the buttons clicked for changing the currently used Dictionary"""
    global dictionary_selected
    dictionary_selected = dictionary

    #Update the label showing which Dictionary is in use
    title.configure(text="Dictionary Selected: " + dictionary_selected)


def search_word(word):
    """Searches for the definition of the word specified and updates gui"""
    try:
        adverb = ""
        definition = ""

        #Sets the base_url based on which Dictionary is currently selected
        if dictionary_selected == "Dictionary.com":
            base_url = DICTIONARY_URL
        elif dictionary_selected == "Merriam-Webster":
            base_url = MERRIAM_URL
        elif dictionary_selected == "PyDictionary":
            base_url = ""
        else:
            messagebox.showerror("Dictionary Error", "Something went wrong with the dictionary")
        
        #We don't need to connect to a url if using PyDictionary
        if dictionary_selected != "PyDictionary":
            url = base_url + word
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            #Handle webscraping for Dictionary.com
            if dictionary_selected == "Dictionary.com":
                adverb = soup.find(class_="css-1gxch3 e1hk9ate2")
                adverb = adverb.get_text()
                definition = soup.find(class_="one-click-content css-1p89gle e1q3nk1v4") #All Definitions - class_="css-1o58fj8 e1hk9ate4"
                definition = definition.get_text()
            #Handle webscraping for Merriam-Webster
            elif dictionary_selected == "Merriam-Webster":
                adverb = soup.find(class_="important-blue-link")
                adverb = adverb.get_text()
                definition = soup.find(class_="dtText")
                definition = definition.get_text().replace(":", "")
        else:
            #Handle getting the definiton and adverb from PyDictionary
            word_meaning = py_dictionary.meaning(word)
            adverb = list(word_meaning)[0]
            word_meaning_values = word_meaning.values()
            definition = list(word_meaning_values)[0][0]

        #Clears the whole scrollbox where the definition is displayed
        definition_display.delete(1.0, "end")

        #Update the current wording being searched label
        definition_title.configure(text="Definition for " + word + ":")

        #Display the adverb and definition to the current word searched on the scrollbox
        definition_display.insert(1.0, adverb + "\n- " + definition)
    except:
        #Clears the whole scrollbox where the definition is displayed
        definition_display.delete(1.0, 'end')

        #Update the current wording being searched label
        definition_title.configure(text="Definition for :")

        #Show an error box because word can't be found
        messagebox.showerror("Error!", "Word not found!\nPlease check your spelling.")


if __name__ == '__main__':
    py_dictionary = PyDictionary()

    base_url = "https://www.dictionary.com/browse/"

    dictionary_selected = "Dictionary.com"
    word_searching = ""

    #Initialize the tkinter gui
    window = tk.Tk()
    window.title("Search for a Definition")
    window.configure(bg="#272626")

    #Displays the current dictionary you are using
    title = tk.Label(window, text="Dictionary Selected: " + dictionary_selected, bg="#272626", fg="#ffffff", font=("Arial", 12))
    title.grid(row=0, columnspan=3)

    #Title above the definition box to show which word you're searching for
    definition_title = tk.Label(window, text="Definition for :", bg="#272626", fg="#ffffff", font=("Arial", 12))
    definition_title.grid(row=5, columnspan=3, pady=3)

    #Display the definition in a scrollbox in case of overflow
    definition_display = scrolledtext.ScrolledText(window, bg="#272626", fg="#ffffff", bd=1, width=34, height=10)
    definition_display.grid(row=6, columnspan=3)

    #The word entry in which the user would like to search
    word_entry = tk.Entry(window, textvariable=word_searching, bd=1, bg="#272626", fg="#ffffff", selectforeground="#ffffff", justify="center")
    word_entry.grid(row=3, columnspan=3, pady=3, sticky="w e")
    word_entry.focus()

    #Initialize the static gui
    init_gui(window)

    #Loop for the gui
    window.mainloop()