import os
import random
import re
from PIL import ImageTk, Image
import ttkbootstrap as ttk
import customtkinter
from customtkinter import CTkEntry, CTkCanvas, CTkSlider, CTkTextbox, CTkButton, CTkSegmentedButton, CTkSwitch, CTkLabel
import tkinter as tk
from tkinter import Text, Entry, Label, messagebox, Button
from tkinter import OptionMenu, PhotoImage, Scale
from tkinter import Checkbutton, IntVar
from tkinter import scrolledtext
from itertools import cycle
import sys
import webbrowser
import time
import threading
#import win32com.client
import locale
import pyttsx3

locale.setlocale(locale.LC_NUMERIC, 'C') #To fix the customtkinter bugs

font_A = () 

#color code
button_color = "#1B1E27"
button_outline = "#262A36"
btn_border = "#2F333A"

orange = "#F0842D"
light_purple = "#CBA8F9"
yellow = "#F9D849"
light_blue = "#75C0F9"
green = '#AFD862'
dim_text = "#344B54"
text = "#BFBDB7"
bg = "#0C0E12"
highlight_text = "#233958"
border_color = "#1F232A"

btn_font = ('Segoe UI', 12)

button_bg_A = '#586074'
button_bg_B = '#586074'
diceword_menu_bg = '#586074'
text_panel_A = '#16181D'
text_A = '#D7D9DA'
outer_bg_A = '#16181D'
inner_bg_A = '#21242C'
panel_header_A = '#373C49'
panel_A = '#2C303A'
generate_btn_main_bg_A = '#473C8C'
generate_btn_text_A = '#B7D9E0'
symbol_A = '#D6D9E0'
faded_text_A = '#A2A9B9'
faded_text_B = '#8891A5'
color_text_C = '#A2A9B9'

#----------------------------Save format/gen section----------------------------------

current_input = ""
number_of_gens = 0
notice_of_save = ""

def remove_last_curly_bracket(file_path):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        if lines and lines[-1].strip() == '}':
            # The last line ends with a '}', remove it
            lines.pop()
            file.seek(0)
            file.truncate()
            file.writelines(lines)
            
induct_new_cuplet = False #Induction of new cuplet, turns quickly on then off
# Function to save input text if it changes
def save_input():
    global current_input
    input_text = entry.get("1.0", ttk.END)
    
    global induct_new_cuplet
    if input_text != current_input or induct_new_cuplet == True:
        induct_new_cuplet = False
        global number_of_gens
        number_of_gens -= (number_of_gens - 1)
        current_input = input_text
        global format_code
        random_number = random.randint(16384, 32767) #random
        binary_string = bin(random_number)[2:]
        format_code = int(binary_string)
        
        with open("assets\logs\logs.txt", 'a') as file:
            if input_text.strip():  # Check if input_text is not empty
                file.write("    }\n\n")
                file.write("----------- Format Code: " + str(format_code) + " -----------" + "\n\n")
                file.write(input_text)
                if not input_text.strip().endswith('\n'):
                    file.write("\n")  # Ensure input_text ends with a newline
                file.write("    {\n")
            log_text = output_text.get("1.0", ttk.END)
            if log_text.strip():  # Check if log_text is not empty
                file.write("     " + log_text)
                remove_last_curly_bracket(r"assets\logs\logs.txt")
            update_log_text()
    else:
        remove_last_curly_bracket(r"assets\logs\logs.txt")
        with open("assets\logs\logs.txt", 'a') as file:
            log_text = output_text.get("1.0", ttk.END)
            if log_text.strip():  # Check if log_text is not empty
                file.write("    |\n     " + log_text)
            file.write("    }\n")
            update_log_text()
    update_log_text()

def new_cuplet():
    global induct_new_cuplet
    induct_new_cuplet = True
    generate_new_sentence()
    
def load_word_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file]
    return words

#---------------------------------Process the text----------------------------------------
#Have a radio button "if regular expressions processing coding and processing on"
def process_text(template):
    # Convert the text to lowercase
    template = template.lower()
    
    # Remove the second article (the or a/an) if it follows another article
    template = re.sub(r'\b(a|an|the)\s+(a|an|the)\b', r'\1', template, flags=re.IGNORECASE)
    template = re.sub(r'\b(from|of)\s+(from|of)\b', r'\1', template, flags=re.IGNORECASE)
        
    # Replace "a" with "an" before vowels
    #template = re.sub(r'\ba ([AEIOUaeiou])', r'an \1', template)
    
    template = re.sub(r'\ba ([aeiou]|hour|X-|F-|herb|hones|honor|ou|ow)', r'an \1', template, flags=re.IGNORECASE)
    
    # Replace "an" with "a" before consonants
    template = re.sub(r'\ban ([qwrtypsdfgjklzxcvbnm]|ufo|ure|usu|uku|uvu|one|uto|uni|ute|use|eu)', r'a \1', template, flags=re.IGNORECASE)
        
    # (\s*) white spaces followed by a comma/period ( ,)/( .) -- replaces all instances of this pattern with just a comma/period (,)/(.)
    template = re.sub(r'\s*,', ',', template)
    
    # Remove extra spaces
    template = re.sub(r'\s{2,}', ' ', template)
    template = re.sub(r'\s{3,}', ' ', template)

    # Ensure a period at the end if it's missing
    if not template.endswith('.'):
        template = template.rstrip('\n')
        template += '.'
    
    # Remove a space before a period
    template = re.sub(r'\s+\.', '.', template)

    # Capitalize the first letter
    template = template[0].upper() + template[1:]
    
    # Capitalize (only) the first letter of the new sentence following a period
    template = re.sub(r'(?<=[.!?]\s)([a-z])', lambda x: x.group().capitalize(), template)
    
    # Capitalize 'i' when it's preceded and followed by a single space
    template = re.sub(r'(?<=\s)i(?=\s)', lambda x: x.group().capitalize(), template)

    # Remove consecutive periods
    template = re.sub(r'\.\.+', '.', template)
    template = re.sub(r'\,\.+', '.', template)
    template = re.sub(r'\.\,+', '.', template)
    template = re.sub(r'\!\.+', '!', template)
    template = re.sub(r'\?\.+', '?', template)
    
    # Replace "was" with "were" if it comes after 's'
    template = re.sub(r's was\b', 's were', template)
    
    # Replace "were" with "was" if it comes after a word not ending with 's'
    template = re.sub(r'(\w+[^s]) were\b', r'\1 was', template)
    
    #---------------------Pluralization-------------------------------------
    
    # Replace 's' with 'es' if the word ends in -s, -x, -z, -sh, or -ch and is followed by 's'
    template = re.sub(r'sss\b', r'sses', template)
    template = re.sub(r'oxs\b', r'oxes', template)
    template = re.sub(r'chs\b', r'ches', template)
    template = re.sub(r'shs\b', r'shes', template)
    template = re.sub(r'zs\b', r'zes', template)
    
    # Replace 'y' with 'ies' if the word ends with 'y' and is followed by 's'
    template = re.sub(r'(\b\w+[b-df-hj-np-tv-z])ys\b', r'\1ies', template)

    # Replace "leaf" with "leaves" if it ends in 'f' or 'fe'
    template = re.sub(r'\b(f|fe)\b', r'ves', template)
    
    return template



#-----------------------------Switches and toggle functions--------------------------------

sfw_nsfw_setting = 25
fiction_realism_setting = 50
selected_genres = ['e',]#,'sc','fa','hi','ad','my','ho','ro','co','sr','mo','te'

#Part One------------------------------Loading Bar-------------------------------------
def update_progress_bar(progress_var, value):
    # Ensure the progress value is within the 0-100 range
    value = max(0, min(100, value))
    progress_var.set(value)
    app.update_idletasks()
    
def increment_progress_bar(progress_var, placeholder_count_for_progress_bar, number_of_genres):
    amount = (100/placeholder_count_for_progress_bar)
    progress_var.set(progress_var.get() + amount)  # Increment
    update_progress_bar(progress_var, progress_var.get()) #Progress bar

def count_placeholder_words_for_progress_bar(input_sentence):
    # Define a regular expression pattern to match words enclosed in =
    pattern = r'=([^`]+)='

    # Use re.findall to find all matches in the input sentence
    matches = re.findall(pattern, input_sentence)

    # Count the number of matches
    placeholder_count_for_progress_bar = len(matches)

    return placeholder_count_for_progress_bar

progress_var = 0

#Part One------------------------------Variegated-------------------------------------

def generate_sentence_variegated(template, word_lists, sfw_nsfw_setting, fiction_realism_setting, selected_genres, progress_var):
    number_of_attempts = 0
    successful_attempts = 0
    print(f"Current Level of Maturity: {int(sfw_nsfw_setting)}")
    print(f"Current Level of Fiction: {int(fiction_realism_setting)}")
    
    number_of_genres = len(selected_genres) #this part is for the progress bar
    input_sentence = template #this part is for the progress bar
    placeholder_count_for_progress_bar = count_placeholder_words_for_progress_bar(input_sentence) # for the progress bar
    
    while True:
        placeholders_replaced = False  # Track whether any placeholders were replaced in this iteration
        for placeholder, word_list in word_lists.items():
            if placeholder in template:
                random.shuffle(word_list)
                word_iterator = cycle(word_list)
                                 
                # Initialize random_word to None initially
                random_word = None

                for _ in range(len(word_list)):
                    number_of_attempts += 1
                    # Get the next word from the cycle
                    random_word = next(word_iterator)

                    # Use regular expression to find all characters between backticks
                    matches = re.findall(r'?([^=]+)', random_word)
                    print(f'Attempting to place "{random_word.split("`")[0]}" for\n {placeholder}')
                    progress_var.set(progress_var.get() + 0.2)  # Increment
                    update_progress_bar(progress_var, progress_var.get()) #Progress bar
                    
                    # Initialize default values for ratings
                    maturity_rating = 'e'
                    fiction_realism_rating = 'e'
                    selected_genre = 'e'
                    selected_genre_secondary = 'e'
                    
                    check_if_genre_list = ['sc', 'fa', 'hi', 'ad', 'my', 'ho', 'ro', 'co', 'sr', 'mo', 'te', 'nt']
                    check_if_maturity_list = ['g', 'pg', 'm', 'r', 'x', 'xx', 'xxx']
                    check_if_realism_list = ['f', 'sf', 'nf']
                    
                    if random_word == "":
                            print ("Error in text file, blank line found.\n")
                            continue
                    
                    if not matches:
                        print("Word is without parameters.")
                        matches = ['E', 'E', 'E', 'E']
                        if force_genres.get() == "off":
                            print("Therefore, passes all parameter checks.")
                            #Optional "Do 'force all parameters' option can be added"
                            break
                        else:
                            print("Force genres mode is on, word is skipped.\n")
                            continue
                    
                    if matches:
                        if matches and len(matches) > 0 and matches[0]:
                            if matches[0] in check_if_genre_list:
                                selected_genre = matches[0]
                            elif matches[0] in check_if_maturity_list:
                                maturity_rating = matches[0]
                            elif matches[0] in check_if_realism_list:
                                fiction_realism_rating = matches[0]
                                
                        if matches and len(matches) > 1 and matches[1]:
                            if matches[1] in check_if_genre_list:
                                if matches[0] in check_if_genre_list:
                                    selected_genre_secondary = matches[1]
                                else:
                                    selected_genre = matches[1]
                            elif matches[1] in check_if_maturity_list:
                                maturity_rating = matches[1]
                            elif matches[1] in check_if_realism_list:
                                fiction_realism_rating = matches[1]
                                
                        if matches and len(matches) > 2 and matches[2]:
                            if matches[2] in check_if_genre_list:
                                if matches[1] in check_if_genre_list or matches[0] in check_if_genre_list:
                                    selected_genre_secondary = matches[2]
                                else:
                                    selected_genre = matches[2]
                            elif matches[2] in check_if_maturity_list:
                                maturity_rating = matches[2]
                            elif matches[2] in check_if_realism_list:
                                fiction_realism_rating = matches[2]

                        if matches and len(matches) > 3 and matches[3]:
                            if matches[3] in check_if_genre_list:
                                if matches[2] in check_if_genre_list or matches[1] in check_if_genre_list or matches[0] in check_if_genre_list:
                                    selected_genre_secondary = matches[3]
                                else:
                                    selected_genre = matches[3]
                            elif matches[3] in check_if_maturity_list:
                                maturity_rating = matches[3]
                            elif matches[3] in check_if_realism_list:
                                fiction_realism_rating = matches[3]
                        
                        found_1 = any(item in matches for item in check_if_maturity_list)
                        
                        if not found_1:
                            print("No maturity rating")
                        else:    
                            print("Maturity Rating:", maturity_rating.upper())
                            if maturity_rating == 'e': #everything
                                minM = 0
                                maxM = 100
                            elif maturity_rating == 'g':
                                minM = 0
                                maxM = 50
                            elif maturity_rating == 'pg':
                                minM = 10
                                maxM = 70
                            elif maturity_rating == 'm':
                                minM = 45
                                maxM = 100
                            elif maturity_rating == 'r':
                                minM = 60
                                maxM = 100
                            elif maturity_rating == 'x':
                                minM = 70
                                maxM = 100
                            elif maturity_rating == 'xx':
                                minM = 80
                                maxM = 100
                            elif maturity_rating == 'xxx':
                                minM = 90
                                maxM = 100
                            if (sfw_nsfw_setting < minM or sfw_nsfw_setting > maxM):
                                print('Maturity rating disqualification\n')
                                continue
                            
                        found_2 = any(item in matches for item in check_if_realism_list)
                                
                        if not found_2:
                            print ("No fiction/realism rating.")
                        else:     
                            print("Realism Rating:", fiction_realism_rating.upper())
                            if fiction_realism_rating == 'e': #everything
                                minR = 0
                                maxR = 100
                            elif fiction_realism_rating == 'nf':
                                minR = 0
                                maxR = 55 #maybe 55
                            elif fiction_realism_rating == 'sf':
                                minR = 30
                                maxR = 95
                            elif fiction_realism_rating == 'f':
                                minR = 45 #maybe 45
                                maxR = 100
                                if (fiction_realism_setting < minR or fiction_realism_setting > maxR):
                                    print('Fiction level disqualification\n')
                                    continue  # Restart the inner loop to find another word
                                
                        found_3 = any(item in matches for item in check_if_genre_list)
                                
                        if not found_3:
                            print ("Checking genres.") #Or None would do
                        else:  
                            if selected_genre != 'e':
                                print(f"Genre: {get_full_genre_name(selected_genre)}")
                            else:
                                print("Genre: Any/All")
                                
                    
                        # Check if the word's primary genre is not in your list
                        if selected_genre not in selected_genres and selected_genre != 'e':
                            uppercase_list = [item.upper() for item in selected_genres]
                            print(f"Primary genre [{selected_genre.upper()}] -> {uppercase_list}")
                            print("Does not match genre list")
                            # Check if the word has a secondary genre and it's not 'e'
                            if selected_genre_secondary != 'e':
                                print("Checking current potential word's 2nd genre...")
                                if selected_genre_secondary in selected_genres:
                                    print(f"[{selected_genre_secondary.upper()}] -> {uppercase_list}")
                                    print("Secondary genre fits genre criteria. Word passes.\n")
                                    break
                                else:
                                    print(f"[{selected_genre_secondary.upper()}] -> {uppercase_list}")
                                    print("Does not match selected genre criteria either.\n")
                                    continue
                            else:
                                # The word has no secondary genre, and the primary genre doesn't meet the criteria
                                print("Secondary genre unlisted, word non-applicable.\n")
                                continue
                        elif selected_genre in selected_genres:
                            print("Word passes.\n")
                            break
                            
                        
                random_word = random_word.split('`')[0]  # Breaks off the backtick
                template = template.replace(placeholder, random_word, 1)
                
                placeholders_replaced = True
                successful_attempts += 1
                increment_progress_bar(progress_var, placeholder_count_for_progress_bar, number_of_genres)
                print("Success!\n")
                break
                            # Store the selected word for this placeholder
        if not placeholders_replaced:
            break  # No placeholders were replaced, so exit the loop
    print(f'Number of attempted matches = {number_of_attempts}')
    print(f'Successful parametrical pass-throughs = {successful_attempts}')
    progress_var.set(progress_var.get()-progress_var.get()) #Progress bar subtracted by total added
    update_progress_bar(progress_var, progress_var.get())
    
    template = process_text(template) #This directs all into process_text function
    return template

#---------------------Part Two ---------------------------- Mirrored Dicewords -------------------

def generate_sentence_mirrored(template, word_lists, sfw_nsfw_setting, fiction_realism_setting, selected_genres, progress_var):
    number_of_attempts = 0
    successful_attempts = 0
    print(f"Currently Selected Maturity Rating: {sfw_nsfw_setting}")
    print(f"Currently Selected Realism Rating: {fiction_realism_setting}")
    
    number_of_genres = len(selected_genres) #this part is for the progress bar
    input_sentence = template #this part is for the progress bar
    placeholder_count_for_progress_bar = count_placeholder_words_for_progress_bar(input_sentence) # for the progress bar
    
    
    for placeholder, word_list in word_lists.items():
        if placeholder in template:
            while True:
                random_word = random.choice(word_list)
                print(f'Attempting to place "{random_word.split("`")[0]}"')
                progress_var.set(progress_var.get() + 0.2)  # Increment
                update_progress_bar(progress_var, progress_var.get()) #Progress bar
                
                number_of_attempts += 1

                # Use regular expression to find all characters between backticks
                matches = re.findall(r'?([^=]+)', random_word)

                # Initialize default values for ratings
                maturity_rating = 'e'
                fiction_realism_rating = 'e'
                selected_genre = 'e'
                selected_genre_secondary = 'e'
                
                check_if_genre_list = ['sc', 'fa', 'hi', 'ad', 'my', 'ho', 'ro', 'co', 'sr', 'mo', 'te', 'nt']
                check_if_maturity_list = ['g', 'pg', 'm', 'r', 'x', 'xx', 'xxx']
                check_if_realism_list = ['f', 'sf', 'nf']
                
                if matches:
                    if matches and len(matches) > 0 and matches[0]:
                        if matches[0] in check_if_genre_list:
                            selected_genre = matches[0]
                        elif matches[0] in check_if_maturity_list:
                            maturity_rating = matches[0]
                        elif matches[0] in check_if_realism_list:
                            fiction_realism_rating = matches[0]
                            
                    if matches and len(matches) > 1 and matches[1]:
                        if matches[1] in check_if_genre_list:
                            if matches[0] in check_if_genre_list:
                                selected_genre_secondary = matches[1]
                            else:
                                selected_genre = matches[1]
                        elif matches[1] in check_if_maturity_list:
                            maturity_rating = matches[1]
                        elif matches[1] in check_if_realism_list:
                            fiction_realism_rating = matches[1]
                            
                    if matches and len(matches) > 2 and matches[2]:
                        if matches[2] in check_if_genre_list:
                            if matches[1] in check_if_genre_list or matches[0] in check_if_genre_list:
                                selected_genre_secondary = matches[2]
                            else:
                                selected_genre = matches[2]
                        elif matches[2] in check_if_maturity_list:
                            maturity_rating = matches[2]
                        elif matches[2] in check_if_realism_list:
                            fiction_realism_rating = matches[2]

                    if matches and len(matches) > 3 and matches[3]:
                        if matches[3] in check_if_genre_list:
                            if matches[2] in check_if_genre_list or matches[1] in check_if_genre_list or matches[0] in check_if_genre_list:
                                selected_genre_secondary = matches[3]
                            else:
                                selected_genre = matches[3]
                        elif matches[3] in check_if_maturity_list:
                            maturity_rating = matches[3]
                        elif matches[3] in check_if_realism_list:
                            fiction_realism_rating = matches[3]
                            
                    if random_word == "":
                        print ("Error in text file, blank line found.\n")
                        continue
                    
                    if not matches:
                        print("Word is without parameters.")
                        matches = ['E', 'E', 'E', 'E']
                        if force_genres.get() == "off":
                            print("Therefore, passes all parameter checks.")
                            #Optional "Do 'force all parameters' option can be added"
                            break
                        else:
                            print("Force genres mode is on, word is skipped.\n")
                            continue
                            
                    upper_matches = [item.upper() for item in matches]
                    print(upper_matches)
                    
                    found_1 = any(item in matches for item in check_if_maturity_list)
                        
                    if not found_1:
                        print("No maturity rating")
                    else:    
                        print("Maturity Rating:", maturity_rating.upper())
                        if maturity_rating == 'e': #everything
                            minM = 0
                            maxM = 100
                        elif maturity_rating == 'g':
                            minM = 0
                            maxM = 50
                        elif maturity_rating == 'pg':
                            minM = 10
                            maxM = 70
                        elif maturity_rating == 'm':
                            minM = 45
                            maxM = 100
                        elif maturity_rating == 'r':
                            minM = 60
                            maxM = 100
                        elif maturity_rating == 'x':
                            minM = 70
                            maxM = 100
                        elif maturity_rating == 'xx':
                            minM = 80
                            maxM = 100
                        elif maturity_rating == 'xxx':
                            minM = 90
                            maxM = 100
                        if (sfw_nsfw_setting < minM or sfw_nsfw_setting > maxM):
                            print('Maturity rating disqualification\n')
                            continue
                        
                    found_2 = any(item in matches for item in check_if_realism_list)
                            
                    if not found_2:
                        print ("No fiction/realism rating.")
                    else:     
                        print("Realism Rating:", fiction_realism_rating.upper())
                        if fiction_realism_rating == 'e': #everything
                            minR = 0
                            maxR = 100
                        elif fiction_realism_rating == 'nf':
                            minR = 0
                            maxR = 55 #maybe 55
                        elif fiction_realism_rating == 'sf':
                            minR = 30
                            maxR = 95
                        elif fiction_realism_rating == 'f':
                            minR = 45 #maybe 45
                            maxR = 100
                            if (fiction_realism_setting < minR or fiction_realism_setting > maxR):
                                print('Fiction level disqualification\n')
                                continue  # Restart the inner loop to find another word
                            
                    found_3 = any(item in matches for item in check_if_genre_list)
                            
                    if not found_3:
                        print ("Checking genres.") #Or None would do
                    else:  
                        if selected_genre != 'e':
                            print(f"Genre: {get_full_genre_name(selected_genre)}")
                        else:
                            print("Genre: Any/All")
                            
                
                    # Check if the word's primary genre is not in your list
                    if selected_genre not in selected_genres and selected_genre != 'e':
                        uppercase_list = [item.upper() for item in selected_genres]
                        print(f"Primary genre [{selected_genre.upper()}] -> {uppercase_list}")
                        print("Does not match genre list")
                        # Check if the word has a secondary genre and it's not 'e'
                        if selected_genre_secondary != 'e':
                            print("Checking current potential word's 2nd genre...")
                            if selected_genre_secondary in selected_genres:
                                print(f"[{selected_genre_secondary.upper()}] -> {uppercase_list}")
                                print("Secondary genre fits genre criteria. Word passes.\n")
                                break
                            else:
                                print(f"[{selected_genre_secondary.upper()}] -> {uppercase_list}")
                                print("Does not match selected genre criteria either.\n")
                                continue
                        else:
                            # The word has no secondary genre, and the primary genre doesn't meet the criteria
                            print("Secondary genre unlisted, word non-applicable.\n")
                            continue
                    elif selected_genre in selected_genres:
                        print("Word passes.\n")
                        break
                break
            
            else:
                # If all placeholders have been successfully replaced, exit the outer loop
                break

            # Remove bracket codes from the selected word
            increment_progress_bar(progress_var, placeholder_count_for_progress_bar, number_of_genres)
            print("Input randomization processor complete!\n")
            random_word = random_word.split('`')[0]  # Breaks off the backtick
            template = template.replace(placeholder, random_word, 100)
            
            
    print(f'Number of attempted matches = {number_of_attempts}')
    print(f'Successful parametrical pass-throughs = {successful_attempts}')
    progress_var.set(progress_var.get()-progress_var.get()) #Progress bar subtracted by total added
    update_progress_bar(progress_var, progress_var.get())
    template = process_text(template) #This directs all into process_text function
    return template

#------------------------------End of *both* param checks----------------------------------

#def copy_to_clipboard():
#    generated_text = output_text.get("1.0", "end-1c")
#    app.clipboard_clear()
#    app.clipboard_append(generated_text)
#    app.update()


final_ttc = ""
def copy_to_clipboard():
    global final_ttc
    last_format_start = log_text.search(r'----------- Format Code: [01]+\s-----------\n', 'end', backwards=True, regexp=True)
    
    if last_format_start:
        # Find the first occurrence of '{' after the format code
        first_curly_brace = log_text.search(r'{', last_format_start, stopindex='end')
        
        if first_curly_brace:
            last_format_start = log_text.index(last_format_start)
            first_curly_brace = log_text.index(first_curly_brace)
            
            text_to_copy = log_text.get(first_curly_brace, 'end')
            format_code = log_text.get(last_format_start, first_curly_brace)
            format_code_match = re.search(r'Format Code: ([01]+)', format_code)
            
            print(f"From:\n {format_code_match.group(0)}\n Processing: \n   {text_to_copy}")
            if sep_type_linebreaks == False and sep_type_comma == False and sep_type_curly == True:
                edit1_ttc = text_to_copy.replace("}\n\n", "}")
                edit2_ttc = edit1_ttc.replace("\n", "")
                edit3_ttc = edit2_ttc.replace("     ","")
                edit4_ttc = edit3_ttc.replace("    ","")
                edit5_ttc = edit4_ttc.replace("|","| ")
                final_ttc = edit5_ttc.replace(".","")
            elif sep_type_linebreaks == False and sep_type_comma == True and sep_type_curly == False:
                final_ttc = text_to_copy.replace("}\n\n", "}").replace("\n", "").replace("     ","").replace("    ","").replace(".","").replace("|",", ")
            elif sep_type_linebreaks == True and sep_type_comma == False and sep_type_curly == False:
                final_ttc = text_to_copy.replace("}\n\n", "").replace("\n", "").replace("{", "").replace("     ","").replace("    ","").replace(".","").replace("|","\n")
            print(f"Result {final_ttc}")
            app.clipboard_clear()
            app.clipboard_append(final_ttc)
            app.update()  # Required to update the clipboard content

#-------------------------------REFRESH WORD LIST-----------------------------------------

def refresh_word_lists():
    global word_lists
    #word_lists = {}  # Clear the current word lists
    for file_name in os.listdir(dicewords_folder_basics):
        if file_name.endswith(".txt"):
            name = os.path.splitext(file_name)[0]
            file_path = os.path.join(dicewords_folder_basics, file_name)
            word_list = load_word_list(file_path)
            word_lists[f'={name}='] = word_list

def refresh_word_lists_2(additional_folders):
    global word_lists

    for folder in additional_folders:
        folder_path = os.path.join(dicewords_folder, folder)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".txt"):
                    name = os.path.splitext(file_name)[0]
                    file_path = os.path.join(folder_path, file_name)
                    word_list = load_word_list(file_path)
                    word_lists[f'={name}='] = word_list
                    
#-------Generate new sentence------
#----------------------------------
read_output_on_screen_tts = False
def generate_new_sentence():
    global var_radio
    global number_of_gens
    global read_output_on_screen_tts
    if number_of_gens == 0:
        refresh_word_lists()
    number_of_gens += 1
    input_sentence = entry.get("1.0", ttk.END)  # Get all the text from line 1, character 0 to the end
    check_for_input = entry.get("1.0", tk.END).strip()
    if check_for_input == "":
        print("Error: No input found to run the generate alogorithm")
    else:
        if var_radio.get() == "Locked In":
            new_sentence = generate_sentence_mirrored(input_sentence, word_lists, sfw_nsfw_setting, fiction_realism_setting, selected_genres, progress_var)
        else:
            new_sentence = generate_sentence_variegated(input_sentence, word_lists, sfw_nsfw_setting, fiction_realism_setting, selected_genres, progress_var)
        output_text.configure(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)  # Clear the current output
        output_text.insert(tk.END, new_sentence)
        output_text.configure(state=tk.DISABLED)
        save_input()
        #Make an area for this
        print(f'Generations produced for current format = {number_of_gens}\n') # Create a count
        change_color_command()  
        save_settings_to_file()
        save_template_to_file()
        if read_output_on_screen_tts == True:
            read_text(read_output_on_screen_tts)
    
thread1 = threading.Thread(target=generate_new_sentence) #this puts this task on a diff thread
thread1.start() #and causes it not to create delay (rotating cursor) in the main GUI
    
# Function to generate multiple sentences
def generate_multiple_sentences(times):
    for _ in range(times):
        generate_new_sentence()

thread2 = threading.Thread(target=generate_multiple_sentences) #this puts this task on a diff thread
thread2.start() #and causes it not to create delay (rotating cursor) in the main GUI

def open_manufacturing_plant(event=None):

    plant_window = ttk.Toplevel(app)
    plant_window.title("Manufacturing Plant")
    plant_window.configure(bg=outer_bg_A)
    plant_window.geometry('500x670')
    #------------------BG--------------------

    trigger_label = Label(plant_window, text="Multi-sided Geometric Word:")
    trigger_label.pack(pady=5)
    trigger_entry = Entry(plant_window, width=30)
    trigger_entry.pack(pady=5)

    example_label = Label(plant_window, text="Example: Weaponry")
    example_label.pack(pady=10)

    potentials_label = Label(plant_window, text="Potentials /n Example: Attack Plunger`pg`sf`ac`co (one per line):")
    potentials_label.pack(pady=10)
    potentials_text = Text(plant_window, wrap=ttk.WORD, height=10, width=58)
    potentials_text.pack(pady=10)

    def save_new_word_list():
        trigger_word = trigger_entry.get()
        potentials = potentials_text.get("1.0", "end-1c").split('\n')
        if trigger_word and potentials:
            file_name = f"{trigger_word}.txt"
            file_path = os.path.join(dicewords_folder, file_name)
            with open(file_path, 'w') as file:
                file.write('\n'.join(potentials))
            messagebox.showinfo("Success", f"New word list '{file_name}' created.")
            refresh_word_lists()
            plant_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a trigger word and at least one potential.")

    #save_button = Button(plant_window, text="Save", command=save_new_word_list)
    #save_button.pack()
    # test
    save_button_image = PhotoImage(file="assets/imgs/save1.png")  # Load the image
    save_button = ttk.Button(plant_window, image=save_button_image, command=save_new_word_list)
    save_button.photo = save_button_image  # Store a reference to the image
    save_button.pack()
    
    def fill_field_with_info():
        potentials_text.insert(ttk.END, "Instructions here.")
            
    # You can also consider adding a button to close the window
    more_info = ttk.Button(plant_window, text="Parameter Sensitivity Instructions", command=fill_field_with_info)
    more_info.pack()
    
dicewords_folder = 'dicewords'
dicewords_folder_basics = 'dicewords/basics'



# default_folder='dicewords/basics' #Change to 'dicewords' if you want super dir to be the default

#example of auto-inventory, add to this to make more word dice loaded upon opening app
color_file = os.path.join(dicewords_folder_basics, 'color.txt')
color_list = load_word_list(color_file)
word_lists = {
    '=color=': color_list,
}

def update_input_field(file_path):#tool tip
    selected_word = (file_path)
    entry.insert(ttk.INSERT, f"={selected_word}= ")
   
   
def refresh_word_lists_on_load(dicewords_folder): #loads all dicewords on open app
    global word_lists

    for folder_path, _, file_names in os.walk(dicewords_folder):
        for file_name in file_names:
            if file_name.endswith(".txt"):
                name = os.path.splitext(file_name)[0]
                file_path = os.path.join(folder_path, file_name)
                word_list = load_word_list(file_path)
                word_lists[f'={name}='] = word_list
                
refresh_word_lists_on_load(dicewords_folder)
#-----------------------------------------UI--------------------------------------
#-----------------------------------------UI--------------------------------------
# Create the main application window

title_font = ("SimSun", 24, "bold")  # Replace with your preferred font, size, and style

app = tk.Tk()

app.title("DiceWords")

#cosmo flatly litera minty lumen sandstone yeti pulse united morph journal darkly superhero solar cyborg vapor cerculean simplex
# Create a new style
style = ttk.Style()
# Set the focus highlight borderwidth to 0 to remove it for all TButton widgets ('1252x800')
style.map("TButton", background=[("active", "!disabled", light_blue)], borderwidth=[("active", -3), ("focus", -1)], bordercolor='black')
style.configure("TButton", background=button_color, foreground=text, bordercolor=button_color, border_width=-2)
app.geometry("1195x800")
app.config(bg=bg)

# Create a canvas with a black background
canvas = ttk.Canvas(app, bg=outer_bg_A, width=1000, height=825)

def load_bg_img():
    img = Image.open("assets/imgs/bg2.png")
    photoImg = ImageTk.PhotoImage(img)
    image_width = photoImg.width()
    image_height = photoImg.height()
    canv_x = (1250 - image_width) // 2
    canv_y = (825 - image_height) // 2
    canvas.create_image(canv_x, canv_y, anchor=ttk.NW, image=photoImg)
    canvas.create_image(0, 0, anchor=ttk.NW, image=photoImg)
    canvas.place(x=0, y=-9)

#load_bg_img()

titleImg = PhotoImage(file='assets/imgs/title5.png')
titleLabel = ttk.Label(text=None, image=titleImg, background=bg)
titleLabel.place(y=5, x=280) #x=390 for old title

parameters_canvas = PhotoImage(file='assets/imgs/gray4.png')
parameters_Label = ttk.Label(text=None, image=parameters_canvas, background='black')
parameters_Label.place(y=25, x=750+35) #x=390 for old title

input_canvas = PhotoImage(file='assets/imgs/input_area3.png')
input_canvas_label = ttk.Label(text=None, image=input_canvas, background='black')
input_canvas_label.place(y=115, x=258) #x=390 for old title


def open_discord(event):
    webbrowser.open("https://discord.gg/v73CFMVnV4")

discordImg = PhotoImage(file='assets/imgs/discord4.png')
discordLabel = ttk.Label(text=None, image=discordImg, background='black', cursor="hand2")
discordLabel.place(y=35, x=1145)

# Bind a click event to open the link when clicked
discordLabel.bind("<Button-1>", lambda event: open_discord(event))



#----------------------TEST--------THEME---------------------------------


#Standardized for easy movement of whole app 
xx = 0
yy = 0
x5 = 115
y5 = 7

# Create a label for the title with the custom font
#title_label = ttk.Label(app, font=title_font, foreground=text_A, background=text_panel_A, text="Geolinguistics: Electro-mechanical Diceword Manufacturing")
#title_label.place(relx=0.18, rely=0.01)
# Create a tooltip-like window
coordinate_label = tk.Label(app, text="", font=("Arial", 10), foreground='white', background="white", relief="solid")
coordinate_label.place(x=0, y=0)

def update_coordinates(event):
    x, y = event.x_root, event.y_root
    label_text = f'X: {x}, Y: {y-23}'  # Adjust for the top bar
    coordinate_label.config(text=label_text)

app.bind("<Enter>", update_coordinates)
app.bind("<Motion>", update_coordinates)

#entry_label.place(x=xx+250, y=yy+112) entry1
#input text
entry = CTkTextbox(app, 
                   corner_radius=3, 
                   #placeholder_text="?adjective= ?noun-thing=", 
                   #placeholder_text_color="gray", 
                   #font=None
                   fg_color="#0C0E12",
                   text_color=("#BFBDB7"), bg_color="#0C0E12",
                   width=454, height=158,                           #CTkTextbox this and above
                   wrap="word",
                   #width=55, height=9,
                   #width=45, height =7,
                   font=('Times New Roman', 18)
                   )
#entry.place(x=165+25, y=138-30)                                     #CtkTextbox
entry.place(x=xx+x5+165, y=yy+y5+122)





#--------------------------------------------------------------------------------
#1) figure out how to use the same placeholder more than once
#2) redesign so these sentence work everytime, start small and build



A1_parts=[]#These lists are in the below file.
# Load the template from the file (*)<---
with open("assets/logs/template_pieces_randomization.txt", "r") as template_file:
    template_code = template_file.read()
    exec(template_code, globals(), locals())
    

# Function to add a randomly constructed sentence to the entry field
gen_template_setting = 5
def add_random_sentence():
    gen_template_setting
    random_sentence = ""  # Initialize random_sentence
    use_all = False
    if use_all == True:
        gen_choice = random.randint(0, 20)
        #gen_choice = random.choice([0, 1, 2, 3]) #Obsoleted, range become 0-20
    else:
        gen_choice = gen_template_setting
        
    if 0 <= gen_choice <= 3:
        gen_choice_deeper = random.choice([0, 0, 0, 1])
    elif 3 < gen_choice <= 7:
        gen_choice_deeper = random.choice([0, 1])
    elif 7 < gen_choice <= 12:
        gen_choice_deeper = random.choice([1, 2])
    elif 12 < gen_choice <= 17:
        gen_choice_deeper = random.choice([2, 3])
    elif 17 < gen_choice <= 20:
        gen_choice_deeper = random.choice([2, 3, 3, 3])
    
    if gen_choice_deeper == 0:
        A1 = random.choice(A1_parts) #A1_parts is loaded from file  * (Don't worry about squiggly underlines)
        random_sentence = f"{A1}"
    elif gen_choice_deeper == 1:
        B1 = random.choice(B1_parts) #B1_parts is loaded from file  |
        B2 = random.choice(B2_parts) #B2_parts is loaded from file  |
        random_sentence = f"{B1} {B2}"
    elif gen_choice_deeper == 2:
        C1 = random.choice(C1_parts) #C1_parts is loaded from file  |
        C2 = random.choice(C2_parts) #C2_parts is loaded from file  |
        C3 = random.choice(C3_parts) #C3_parts is loaded from file  *
        random_sentence = f"{C1} {C2} {C3}"
    elif gen_choice_deeper == 3:
        D1 = random.choice(D1_parts) #C1_parts is loaded from file  |
        D2 = random.choice(D2_parts) #C2_parts is loaded from file  |
        D3 = random.choice(D3_parts) #C3_parts is loaded from file  *
        D4 = random.choice(D4_parts) #C3_parts is loaded from file  *
        random_sentence = f"{D1} {D2} {D3} {D4}"
    entry.delete("1.0", "end")
    entry.insert(ttk.END, random_sentence)
    change_color_command()
#--------------------------------------Text Color Change-----------------------------------


    
#-----------------------------Output assets/logs/logs.txt onto screen------------------------------

y2=360
x2=-577
x7=120
y7=0
# Create a scrolled text widget for displaying the log1 logs1
log_text = scrolledtext.ScrolledText(app, wrap=ttk.WORD, font=('Consolas', 11), 
                                     width=52, height=11)
log_text.place(x=xx+x2+x7+740, y=yy+y2+y7+120) #x=xx+730+48

# Configure the background color
log_text.configure(bg=bg, fg=light_purple, insertbackground=highlight_text)


    
def update_log_text():
    line_count = 50  # Initial line count
    found_pattern = False
    try:
        while line_count <= 200:  # Adjust the upper limit as needed
            with open("assets/logs/logs.txt", 'r') as file:
                lines = file.readlines()[-line_count:]
                line_count += 5
            # Check for the presence of the pattern
            pattern = re.compile(r'format\s+code', re.IGNORECASE)
            if any(pattern.search(line) for line in lines):
                found_pattern = True
                break

        if found_pattern:
                log_text.delete(1.0, ttk.END)
                log_text.insert(ttk.END, ''.join(lines))
                log_text.see(ttk.END)
    except FileNotFoundError:
        pass  # Handle the case when the file doesn't exist

# Call the update_log_text function initially to populate the text field
update_log_text()

#-----------------------------------------------------------------------------------------------
y3=-5
x3=-112
#generate_img = PhotoImage(file="assets/imgs/btn27a.png")
# A button to send input to output
generate_button = CTkButton(app, font=btn_font, corner_radius=0, bg_color=button_color, border_width=1, 
                            border_color=btn_border, hover_color=highlight_text, 
                            fg_color=button_color, text_color=text, width=298, text="Send to Output", 
                            command=generate_new_sentence)
generate_button.place(y=y3+y5+283, x=x3+x5+430)
# Entry field for specifying the number of sentences to generate
num_sentences_entry = tk.Text(app, width=2, height=1, font=('Arial', 8)) #width=28, corner_radius=1, border_width=1, border_color=light_blue
num_sentences_entry.insert('1.0', "03")
num_sentences_entry.place(y=y3+y5+283, x=x3+x5+281)
#command=generate_new_sentence, border_width=3, border_color=text, bg_color=bg, fg_color=bg, text_color=text, hover_color=green)
multiple_button = CTkButton(app, font=btn_font, corner_radius=0, bg_color=button_color, border_width=1, 
                            border_color=btn_border, hover_color=highlight_text, 
                            fg_color=button_color, text_color=text, width=120, text="Multiples", 
                            command=lambda: generate_multiple_sentences(int(num_sentences_entry.get('1.0', 'end-1c'))))
multiple_button.place(y=y3+y5+283, x=x3+x5+309) #x=572 for perfect alignment with other button in cur location


text_edited = False
def save_cached_template_to_file():
    global text_edited
    text_to_cache = ""
    if text_edited == True:
        text_to_cache = entry.get("1.0", tk.END)
        print("Last edited text in the input field was saved")
    with open('assets/logs/template_cache.txt', 'w') as cache:  # Truncate the file
        cache.write(text_to_cache)
        text_edited = False
        
current_line = 1

def text_is_edited(event=None):
    if event:
        global text_edited
        text_edited = True
        line_number_label.config(text=f"Edit")

app.bind('<KeyRelease>', text_is_edited)

def load_from_template_cache():
    try:
        with open('assets/logs/template_cache.txt', "r") as cache:
            lines = cache.readlines()
            # Remove leading/trailing white spaces and empty lines
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            last_edited_text = "\n".join(cleaned_lines)
            entry.delete("1.0", tk.END)
            entry.insert("1.0", last_edited_text)
            return last_edited_text
    except FileNotFoundError:
        return ""

def load_left_line():
    global text_edited
    if text_edited:
        save_cached_template_to_file()
    text_edited = False
    global current_line
    if current_line > 1:
        current_line -= 1
    update_text_field()
    save_settings_to_file()

def load_right_line():
    global text_edited
    if text_edited:
        save_cached_template_to_file()
    text_edited = False
    global current_line
    if current_line < len(template_lines):
        current_line += 1
    update_text_field()
    save_settings_to_file()

def update_text_field():
    entry.delete(1.0, tk.END)  # Clear the text field
    entry.insert(tk.END, template_lines[current_line - 1])  # Load the current line
    line_number_label.config(text=f"{current_line} of {len(template_lines)}")
                    #config = tk. configure = CTk
def save_template_to_browse():
    global current_line
    text_to_save = entry.get("1.0", tk.END)
    cleaned_text = text_to_save.strip()
    with open('assets/logs/add_templates.txt', 'a') as browse_templates_file:
        browse_templates_file.write('\n')
        browse_templates_file.write(cleaned_text)
    print(f"Current template written into add_templates.txt") #my templates? or {name}_templates?
    current_line = len(template_lines) + 1
    read_and_update_template_browser()
    update_text_field()
        
def read_and_update_template_browser():
    global template_lines
    with open('assets/logs/add_templates.txt', 'r') as browse_templates_file: # Update template_lines list
        template_lines = browse_templates_file.read().split('\n')
    line_number_label.config(text=f"{current_line} of {len(template_lines)}") # Update the label
                    #config = tk. configure = CTk
with open('assets/logs/add_templates.txt', 'r') as browse_templates_file:
    template_lines = browse_templates_file.read().split('\n')

def delete_current_template():
    global current_line
    with open('assets/logs/add_templates.txt', 'r') as browse_templates_file:
        lines = browse_templates_file.readlines()

    if 0 < current_line <= len(lines):
        del lines[current_line - 1]
        current_line = min(current_line, len(lines))

        with open('assets/logs/add_templates.txt', 'w') as browse_templates_file:
            # Remove empty lines
            lines = [line.strip() for line in lines if line.strip()]
            browse_templates_file.write('\n'.join(lines))

    read_and_update_template_browser()
    update_text_field()



y10=-250
    
line_number_label = ttk.Label(app, foreground=text, background=button_color, text=f"{current_line}/{len(template_lines)}")
line_number_label.place(x=x3+x5+840, y=y3+y5+345+y10) #, text_color=text

left_img = PhotoImage(file="assets/imgs/right4.png")
browse_left_button = tk.Button(app, command=load_left_line, highlightthickness= 0,
                               image=left_img, text=None)
browse_left_button.place(x=x3+x5+795, y=y3+y5+340+y10)


right_img = PhotoImage(file="assets/imgs/left4.png")
browse_right_button = tk.Button(app, command=load_right_line, highlightthickness= 0,
                                image=right_img, text=None)
browse_right_button.place(x=x3+x5+905, y=y3+y5+340+y10)

open_last_edited_button = CTkButton(app, font=btn_font, corner_radius=0, bg_color=button_color, border_width=1, 
                            border_color=btn_border, hover_color=highlight_text, 
                            fg_color=button_color, text_color=text, width=148,
                            text='Retrieve Last Edited', command=load_from_template_cache, image=None)
open_last_edited_button.place(x=x3+x5+795, y=y3+y5+285+y10)

save_template_button = CTkButton(app, font=btn_font, corner_radius=0, bg_color=button_color, border_width=1, 
                            border_color=btn_border, hover_color=highlight_text, 
                            fg_color=button_color, text_color=text, width=74,
                            text='Save', command=save_template_to_browse)
save_template_button.place(x=x3+x5+790, y=y3+y5+315+y10)

delete_template_button = CTkButton(app, font=btn_font, corner_radius=0, bg_color=button_color, border_width=1,
                                  border_color=btn_border, hover_color=highlight_text,
                                  fg_color=button_color, text_color=text, width=74,
                                  text='Delete', command=delete_current_template)
delete_template_button.place(x=x3+x5+875, y=y3+y5+315+y10)



progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(app, variable=progress_var)
progress_bar.place(x=0, y=yy+770, relwidth=1)
#progress_bar.pack(fill="x") 

#progress_bar.pack(side="bottom", fill="x")

#------------------------------------------------------------------------------------------
# A button to add a randomly constructed sentence
rand_template_img = PhotoImage(file="assets/imgs/btn2A.png")
add_sentence_button = tk.Button(app, image=rand_template_img, text="Randomize Template", height= 70, width=70,
                                 command=add_random_sentence)
add_sentence_button.place(x=xx+x5+715+35, y=yy+y5+237)

x4=160 #500
y4=362
# Create output text widget, output1
output_text = CTkTextbox(app, font=('Segoe UI Variable Small Semibold', 20),
                   #height=5, width=32,
                   corner_radius=0,
                   fg_color=bg,
                   text_color=light_blue, bg_color=text,
                   width=454, height=118,
                   wrap="word")
output_text.place(x=xx+x4+x7, y=yy+y4+y7)

# Create a (centered try) output label
label_font = ('Helvetica', 12)
output_field_label = CTkLabel(app, text="Output", height=12, font=label_font, text_color=text_A, bg_color=text_panel_A)
output_field_label.place(x=x4+128, y=y4-15+y7)

#Center a label above the output text field
#diceword_menu_label = ttk.Label(app, text="Dicewords:")
#diceword_menu_label.place(x=60, y=125)


#-----------Mirrored Matching Dicewords/Variegated Matching Dicewords----------------------------- 


#When the same exact ?placeholder= or Geolinguistic DiceWord appears more than once, the processor will:
#Roll for each #Roll once, apply broadly
#Possibly change varigated/mirrored to that^^^^ Label + Segmented Button vary1

var_radio = ttk.StringVar(value="Variegated")

def print_new_value(switch_to):
    print(f"Switching to: {switch_to}")

def on_off_radio(value, *args):
    var_radio.set(value)
    global switch_to
    if value == "Variegated":
        switch_to = "Variegated"
        print_new_value(switch_to)
        print("Repeated placeholds will each have an equal roll and will (more than likely) be different from those prior, that share the same name.")
    if value == "Locked In":
        switch_to = "Locked In"
        print_new_value(switch_to)
        print("Repeated placeholders will hold the same outcome as the ones prior to them. If you'd like to use this feature while also using another placeholder of the same type that differentiates, consider copying the file and adding a marker to the .txt file that delineates it from the original.")

segemented_button_var = customtkinter.StringVar(value="Variegated")
segemented_button = customtkinter.CTkSegmentedButton(app, values=
                                                     ["Variegated", "Locked In"],
                                                     command=on_off_radio, variable=var_radio,
                                                     unselected_color = text_panel_A,
                                                     fg_color= bg,
                                                     text_color= 'black',
                                                     unselected_hover_color = yellow,
                                                     selected_hover_color= green,
                                                     selected_color= dim_text,
                                                     bg_color= bg
                                                     )

segemented_button.place(x=x3+x5+584, y=y3+y5+312)

sep_type_comma, sep_type_linebreaks, sep_type_curly = False, False, True
def copy_processor_callback(value):
    global sep_type_comma, sep_type_linebreaks, sep_type_curly
    if value == "     Commas     ":
        sep_type_comma = True
        sep_type_linebreaks = False
        sep_type_curly = False
        print("Setting Change: Processing alterations set to individuate generations by commas.")
    elif value == "    Line Breaks    ":
        sep_type_comma = False
        sep_type_linebreaks = True
        sep_type_curly = False
        print("Setting Change: Processing alterations set to individuate generations by line breaks.")
    elif value == "     Pipe Bars     ":
        sep_type_comma = False
        sep_type_linebreaks = False
        sep_type_curly = True
        print("Setting Change: Processing alterations set to individuate generations by pipe bars.")
#sep_type1
sep_by_button_var = customtkinter.StringVar(value="    Pipe Bars    ")
sep_by_button = customtkinter.CTkSegmentedButton(app, values=["     Pipe Bars     ", "     Commas     ", "    Line Breaks    "],
                                                     command=copy_processor_callback,
                                                     variable=sep_by_button_var,
                                                     unselected_color = text_panel_A,
                                                     fg_color= bg,
                                                     text_color= 'black',
                                                     unselected_hover_color = yellow,
                                                     selected_hover_color= green,
                                                     selected_color= '#325D88',
                                                     bg_color= bg,
                                                     width=200
                                                                                )

sep_by_button.place(x=x5+317, y=y5+y7+714)
#----------------------------------------Sliders--------------------------------------------
#editing
#maturity_slider = ttk.Scale(app, from_=0, to=100, orient="vertical", length=200, value=50)
#maturity_slider.place(x=900, y=225)

#editing
#realism_slider = ttk.Scale(app, from_=0, to=100, orient="vertical", length=200, value=50)
#realism_slider.place(x=970, y=225) slider1

rand_genre_slider = CTkSlider(app, from_=0, to=10, 
                            orientation="horizontal", width=75, height=23,
                            fg_color = 'black',
                            progress_color='#141820', #'#080818',
                            bg_color=button_color,
                            button_color=diceword_menu_bg,
                            button_hover_color=faded_text_B)
rand_genre_slider.place(x=x5+712+35, y=y5+205)
rand_genre_slider.set(3)


gen_template_slider = CTkSlider(app, from_=0, to=20, 
                            orientation="horizontal", width=75, height=23,
                            fg_color = 'black',
                            progress_color='#141820',
                            bg_color=button_color,
                            button_color=diceword_menu_bg,
                            button_hover_color=faded_text_B)
gen_template_slider.place(x=x5+712+35, y=y5+311)
gen_template_slider.set(5)

r_s_x=682+x5+35
m_s_x=652+x5+35
s_y=145+y5

realism_slider = CTkSlider(app, from_=0, to=100, 
                            orientation="vertical", width=28, height=185,
                            fg_color = 'black',
                            progress_color='#141820',
                            bg_color=button_color,
                            button_color=diceword_menu_bg,
                            button_hover_color=faded_text_B)
realism_slider.place(x=r_s_x, y=s_y)
realism_slider.set(50)

maturity_slider = CTkSlider(app, from_=0, to=100, 
                            orientation="vertical", width=28, height=185,
                            fg_color = 'black',
                            progress_color='#141820',
                            bg_color=button_color,
                            button_color=diceword_menu_bg,
                            button_hover_color=faded_text_B)
maturity_slider.place(x=m_s_x, y=s_y)
maturity_slider.set(25)

slider_font = ("Helvetica", 7)
# Create labels for the slider text
realism_slider_label = ttk.Label(app, background= text_panel_A, foreground= faded_text_A, text="Realism", font=slider_font) 
realism_slider_label2 = ttk.Label(app, background= text_panel_A, foreground= faded_text_A, text="Fiction",font=slider_font)  # Label for Fictional
maturity_slider_label = ttk.Label(app, background= text_panel_A, foreground= faded_text_A, text="Mature",font=slider_font)    
maturity_slider_label2 = ttk.Label(app, background= text_panel_A, foreground= faded_text_A, text="SFW",font=slider_font)    # Label for "SFW"

# Position the labels as desired (label1 on top, label2 on the bottom)
realism_slider_label.place(x=r_s_x-4, y=s_y-15)  
realism_slider_label2.place(x=r_s_x, y=s_y+180)  # Place for Fictional
maturity_slider_label.place(x=m_s_x-4, y=s_y-16)
maturity_slider_label2.place(x=m_s_x, y=s_y+180)  # Place for "SFW"

# Function to update the settings variables when the sliders change
def update_settings(slider_type):
    global fiction_realism_setting
    global sfw_nsfw_setting
    global gen_template_setting
    global rand_genre_setting
    fiction_realism_setting = int(realism_slider.get())
    sfw_nsfw_setting = int(maturity_slider.get())
    gen_template_setting = int(gen_template_slider.get())
    rand_genre_setting = int(rand_genre_slider.get())
    if slider_type == "r_slide":
        print(f"Fictional/Realism Slider = {fiction_realism_setting}")
    elif slider_type == "m_slide":
        print(f"SFW/Mature Slider = {sfw_nsfw_setting}")
    elif slider_type == "t_slide":
        print(f"Generate Randomized Template Slider = {gen_template_setting}")
    elif slider_type == "g_slide":
        print(f"Randomize Genre(s) Slider = {rand_genre_setting}")

# Bind the slider changes to the update_settings function
realism_slider.bind("<ButtonRelease-1>", lambda event: update_settings("r_slide"))
maturity_slider.bind("<ButtonRelease-1>", lambda event: update_settings("m_slide"))
gen_template_slider.bind("<ButtonRelease-1>", lambda event: update_settings("t_slide"))
rand_genre_slider.bind("<ButtonRelease-1>", lambda event: update_settings("g_slide"))


#-------------------------------Dicewords, Hand Picked----------------------------------------------

y8= 32
x8= 0


def update_diceword_listbox(event):
    global dynamic_height_scroll
    max_display_items_small = 9  # Maximum number of items to display when there are fewer items
    max_display_items_large = 27  # Maximum number of items to display when there are more items
    switch_to_large_list_limit = 15

    # Get the selected directory from Listbox B
    selected_directory = os.path.join(dicewords_dir, more_directories_listbox.get(more_directories_listbox.curselection()))

    # Clear Listbox A
    diceword_listbox.delete(0, tk.END)

    # List all .txt files in the selected directory
    txt_files = [f for f in os.listdir(selected_directory) if f.endswith(".txt")]

    # Populate Listbox A with all items
    for txt_file in txt_files:
        filename_without_extension = os.path.splitext(txt_file)[0]
        diceword_listbox.insert(tk.END, filename_without_extension)

    # Set the height of Listbox A based on the number of items
    num_items = len(txt_files)
    if num_items < switch_to_large_list_limit:
        diceword_listbox.config(height=max_display_items_small)
        listbox_scrollbar.place(height=167)
    else:
        diceword_listbox.config(height=max_display_items_large)
        listbox_scrollbar.place(height=400+(18.18*5))

    # Calculate the scrollbar height
    num_items_displayed = max_display_items_small if num_items < switch_to_large_list_limit else max_display_items_large
    item_height = 18.18  # Approximate height of each item in pixels
    scrollbar_height = num_items_displayed * item_height
    dynamic_height_scroll = scrollbar_height
    #listbox_scrollbar.place(height=dynamic_height_scroll)

    
lstbx_font = ('Nirmala UI', 10)

# Listbox_A widget
diceword_listbox = tk.Listbox(app, selectmode=tk.SINGLE, height=22, width=16, font=lstbx_font)
diceword_listbox.place(x=xx+x8+100, y=yy+y8+45) #110 @ orig | x=71, y=140 |<--closer to scroll

# Create a Scrollbar widget
dynamic_height_scroll = 300
listbox_scrollbar = tk.Scrollbar(app, orient="vertical", command=diceword_listbox.yview)
listbox_scrollbar.place(x=x8+71, y=y8+45, height=dynamic_height_scroll)

# Configure the Listbox_A widget to work with the Scrollbar
diceword_listbox.config(yscrollcommand=listbox_scrollbar.set)
listbox_scrollbar.config(command=diceword_listbox.yview)

# Listbox_B widget, populate it with directories
more_directories_listbox = tk.Listbox(app, selectmode=tk.SINGLE, height=7, width=17, font=lstbx_font)
more_directories_listbox.place(x=xx+100, y=yy+627)

# Because 'dicewords' is the main subdirectory in the project, we use it for B
dicewords_dir = os.path.join(os.getcwd(), dicewords_folder) #dicewords_folder
directories = [d for d in os.listdir(dicewords_dir) if os.path.isdir(os.path.join(dicewords_dir, d))]

# Create a Scrollbar widget for listbox_B
static_height_scroll = 132
listbox_scrollbar_B = tk.Scrollbar(app, orient="vertical", command=more_directories_listbox.yview)
listbox_scrollbar_B.place(x=71, y=627, height=static_height_scroll)
more_directories_listbox.config(yscrollcommand=listbox_scrollbar_B.set)
listbox_scrollbar_B.config(command=more_directories_listbox.yview)


for directory in directories:
    directory_name = os.path.basename(directory)
    directory_name = directory_name.capitalize()  # Capitalize the first letter
    more_directories_listbox.insert(tk.END, directory_name)

def on_listbox_select(event):
    selected_index = diceword_listbox.curselection()
    if selected_index:
        selected_item = diceword_listbox.get(selected_index[0])
        selected_diceword.set(selected_item)
        update_input_field(selected_item)
        change_color_command()

diceword_listbox.bind('<<ListboxSelect>>', on_listbox_select) 
# Bind Listbox B to update Listbox A when a directory is selected

# (Highlighted) directory by default, within "dicewords" folder
more_directories_listbox.selection_set(directories.index('basics'))
update_diceword_listbox(None)

b_dicewords = [filename.split('.')[0] for filename in os.listdir(dicewords_folder_basics) if filename.endswith('.txt')]
selected_diceword = tk.StringVar()

#------------------------down menu to select dicewords----------------------------------------



#--------------------------------ComboBox for Directories---------------------------------------------
# Create a list to store directory names
directory_names = []

# Populate the list with directory names (similar to Listbox B)
for directory in directories:
    directory_name = os.path.basename(directory)
    directory_name = directory_name.capitalize()  # Capitalize the first letter
    directory_names.append(directory_name)

# Create the Combobox widget and set its values
directory_combobox = ttk.Combobox(app, values=directory_names, state="readonly")
directory_combobox.place(x=xx + x8 + 71, y=yy + y8 + -5)

# Bind an event handler to update Listbox A when a selection is made in the Combobox
def update_listbox_from_combobox(event):
    selected_directory = directory_combobox.get()
    selected_index = directory_names.index(selected_directory)
    more_directories_listbox.select_clear(0, tk.END)  # Deselect any existing selection in Listbox B
    more_directories_listbox.select_set(selected_index)  # Select the corresponding directory in Listbox B
    update_diceword_listbox(None)  # Call the function to update Listbox A

directory_combobox.bind('<<ComboboxSelected>>', update_listbox_from_combobox)

# Set the default selection
directory_combobox.set("Basics")


#Obsoleted, now brings in basic dicewords (b_dicewords) twice if on
# Populate the Listbox with dicewords
#for b_diceword in b_dicewords:
#    diceword_listbox.insert(tk.END, b_diceword)

#-----------------------------------------change text color-----------------------------
def change_color_command(event=None):
    if event:
    # Clear previous tags
        entry.tag_delete('placeholder')
        
        # Find all matches of text enclosed in double backticks
        start = '1.0'
        
        while True:
            start = entry.search('?', start, 'end', regexp=True)
            if not start:
                break
            end = entry.search('=', f"{start}+2c", 'end', regexp=True)
            if not end:
                break
            entry.tag_config('placeholder', background=None, foreground="#B4D862")
            entry.tag_add('placeholder', start, f"{end}+2c")
            start = f"{end}+2c"
    
def change_color(event=None):
    if event.widget == entry:
        # Clear previous tags
        event.widget.tag_delete('placeholder')

        # Find all matches of text enclosed in double backticks
        start = '1.0'

        while True:
            start = event.widget.search('{=}', start, 'end', regexp=True)
            if not start:
                break
            end = event.widget.search('=', f"{start}+2c", 'end', regexp=True)
            if not end:
                break
            event.widget.tag_config('placeholder', foreground='#3E3F3A')
            event.widget.tag_add('placeholder', start, f"{end}+2c") #^was nothing, but became b3d4f5
            start = f"{end}+2c"

# Bind the change_color function to the entry widget
app.bind("<ButtonRelease-1>", change_color_command)
diceword_listbox.bind("<ButtonRelease-1>", change_color)
entry.bind('<KeyRelease>', change_color_command)
#-----------------------------Additional Folders Listbox-------------------------------
additional_folders = []
def on_folder_selection(event):
    global word_lists
    selected_indices = more_directories_listbox.curselection()
    if selected_indices:  # Check if there is a selection
        selected_folder = more_directories_listbox.get(selected_indices[0])  # Get the first selected item
        additional_folders.append(selected_folder)
        update_diceword_listbox(None)
        refresh_word_lists_2(additional_folders)
       # print('Example of diceword polyhedrons/faces in this index:')
       # counter = 0                                 #error checking mechanism, optional
       # for key, value in word_lists.items():
       #     print(f'{key}: {value}')
       #     counter += 1
       #     if counter >= 3:
       #         break                                #end of error checking mechanism

#def show_potentials_in_file():

more_directories_listbox.bind("<<ListboxSelect>>", on_folder_selection)



#--------------------------------Copy, Induct, Refresh, Clear Input-----------------------------------

# COPY AND PROCESS #Search key: copy1

copy_button = CTkButton(app, font=btn_font, corner_radius=0, bg_color=button_color, border_width=1, border_color=btn_border, hover_color=highlight_text, fg_color=button_color, text_color=text, 
                        text="Process & Copy to Clipboard", width=297, command=copy_to_clipboard)
copy_button.place(x=xx+x2+x7+891, y=yy+y2+y7+333) #(x=xx+858, y=yy+725)

# CUPLET

new_grouping_button = CTkButton(app, font=btn_font, corner_radius=0, bg_color=button_color, border_width=1, border_color=btn_border, hover_color=highlight_text, fg_color=button_color, text_color=text, 
                                text="Induct New Cuplet", width=150, command=new_cuplet)
new_grouping_button.place(x =xx+x2+x7+740, y =yy+y2+y7+333) #628 orig


# REFRESH BUTTON

refresh_button = CTkButton(app, font=btn_font, corner_radius=0, bg_color=button_color, border_width=1, border_color=btn_border, hover_color=highlight_text, fg_color=button_color, text_color=text,
                           text="Refresh .txt Files", width= 150, command=refresh_word_lists)
refresh_button.place(x=x8+70, y=y8+554)


# Create a button to open the Manufacturing Plant man1 manufacture1
conveyor_img = PhotoImage(file="assets\imgs\manufacture.png")
smaller_image = conveyor_img #.subsample(2) <--- cuts image into half its size, (or a third, etc.)
conveyor_button = tk.Button(app,
                          text=("Open \n Manufacturing Plant"), image=smaller_image, command=open_manufacturing_plant)
conveyor_button.place(x=1000, y=1500)


#----------------------------------------------------Genre check boxes----------------------------------
#if 9 needed add "Custom" genre

# Function to get the full genre name based on the short name
def get_full_genre_name(short_name):
    # Define a dictionary to map short names to full names
    genre_names = {
        'sc': 'Sci Fi/Futuristic',
        'fa': 'Fantasy/Tolkein',
        'hi': 'Historical',
        'ad': 'Action/Adventure',
        'my': 'Mystery',
        'ho': 'Dark/Horror',
        'ro': 'Bright/Romance',
        'co': 'Comedy',
        'sr': 'Surreal',
        'mo': 'Modern',
        'te': 'Tech/Material',
        'nt': 'Nature'
    }
    return genre_names.get(short_name, 'e')  # Default to 'Unknown' if not found

# Define the labels and their respective IntVar variables
genres1 = [
    ("sc", ttk.IntVar()),
    ("fa", ttk.IntVar()),
    ("mo", ttk.IntVar())
]
genres2 = [
    ("hi", ttk.IntVar()),
    ("ad", ttk.IntVar()),
    ("co", ttk.IntVar())
]
genres3 = [
    ("ro", ttk.IntVar()),
    ("ho", ttk.IntVar()),
    ("sr", ttk.IntVar())
]
genres4 = [
    ("te", ttk.IntVar()),
    ("nt", ttk.IntVar()),
    ("my", ttk.IntVar())
]

sc_on = ttk.IntVar()
fa_on = ttk.IntVar()
hi_on = ttk.IntVar()
ad_on = ttk.IntVar()
my_on = ttk.IntVar()
ho_on = ttk.IntVar()
ro_on = ttk.IntVar()
co_on = ttk.IntVar()
sr_on = ttk.IntVar()
mo_on = ttk.IntVar()
te_on = ttk.IntVar()
nt_on = ttk.IntVar()

genre_vars = {
    'sc': sc_on,
    'fa': fa_on,
    'hi': hi_on,
    'ad': ad_on,
    'my': my_on,
    'ho': ho_on,
    'ro': ro_on,
    'co': co_on,
    'sr': sr_on,
    'mo': co_on,
    'te': te_on,
    'nt': nt_on
}

# Function to toggle the state of the IntVar variable
force_genres = 'off'
temp_switch = False
click_count = 0

def toggle_genre_state(var_name):
    global temp_switch
    global force_genres
    global click_count
    var = genre_vars[var_name]
    var.set(not var.get())
    if var_name not in selected_genres:
        selected_genres.append(var_name)
        print(f"Genre List:\n {selected_genres}")
    else:
        selected_genres.remove(var_name)
        print(f"Genre List:\n {selected_genres}")
    if len(selected_genres) <= 1: #if last genre is turned off
        
        if force_genres.get == 1: #and the force genres switch is on
            temp_switch = True
            click_count = 1  # Reset the click count when temp_switch is set to True
        elif force_genres.get == 0:
            temp_switch = False
            click_count = 0
        
        force_genres.set('off')
        force_genres_switch.deselect
        force_genres_switch.configure(state="disabled")
        
    elif len(selected_genres) >= 2:
        force_genres_switch.configure(state="normal")
        if temp_switch == True:
            force_genres.set('on')
            force_genres_switch.select()
            temp_switch = False

label_fg_color = "gray"
y90=y5+370
x_c=x5+650+34

genre_vars_index=[]
on_color = '#001749'

for i, (short_name, var) in enumerate(genres1):
    y_coord = y90 + i * 27
    label_text = get_full_genre_name(short_name)
    checkbutton = CTkSwitch(app, bg_color=button_color,
                            button_color=diceword_menu_bg, fg_color='black',
                            progress_color=diceword_menu_bg,
                            button_hover_color=faded_text_B,
                            variable=var, command=lambda name=short_name: toggle_genre_state(name))
    checkbutton.place(x=x_c, y=y_coord, anchor="w")
    
    genre_vars_index.append(var)
    
    # Create a label widget for the name
    label = CTkLabel(app, text=label_text, fg_color=button_color, bg_color=bg, text_color=text)
    label.place(x=x_c+40, y=y_coord, anchor="w")  # Adjust the padx value for spacing
    
for i, (short_name, var) in enumerate(genres2):
    y_coord = y90 + i * 27  # Adjust the y-coordinate to space the widgets vertically
    label_text = get_full_genre_name(short_name)  # Define a function to get the full genre name
    checkbutton = CTkSwitch(app, bg_color=button_color,
                            button_color=diceword_menu_bg, fg_color='black',
                            progress_color=diceword_menu_bg,
                            button_hover_color=faded_text_B,
                            text=label_text, variable=var, command=lambda name=short_name: toggle_genre_state(name))
    checkbutton.place(x=x_c, y=y_coord+81, anchor="w")
    
    genre_vars_index.append(var)
    
    label = CTkLabel(app, text=label_text, fg_color=button_color, bg_color=bg, text_color=text)
    label.place(x=x_c+40, y=y_coord+81, anchor="w") 

for i, (short_name, var) in enumerate(genres3):
    y_coord = y90 + i * 27  
    label_text = get_full_genre_name(short_name)  
    checkbutton = CTkSwitch(app, bg_color=button_color,
                            button_color=diceword_menu_bg, fg_color='black',
                            progress_color=diceword_menu_bg,
                            button_hover_color=faded_text_B,
                            text=label_text, variable=var, command=lambda name=short_name: toggle_genre_state(name))
    checkbutton.place(x=x_c, y=y_coord+162, anchor="w")
    
    genre_vars_index.append(var)

    label = CTkLabel(app, text=label_text, fg_color=button_color, bg_color=bg, text_color=text)
    label.place(x=x_c+40, y=y_coord+162, anchor="w")  
    
for i, (short_name, var) in enumerate(genres4):
    y_coord = y90 + i * 27  
    label_text = get_full_genre_name(short_name)  
    checkbutton = CTkSwitch(app, bg_color=button_color,
                            button_color=diceword_menu_bg, fg_color='black',
                            progress_color=diceword_menu_bg,
                            button_hover_color=faded_text_B,
                            text=label_text, variable=var, command=lambda name=short_name: toggle_genre_state(name))
    checkbutton.place(x=x_c, y=y_coord+243, anchor="w")
    
    genre_vars_index.append(var)

    label = CTkLabel(app, text=label_text, fg_color=button_color, bg_color=bg, text_color=text)
    label.place(x=x_c+40, y=y_coord+243, anchor="w")
    
    
    
    
def toggle_force_genres():
    print("Switch toggled, current value:", force_genres.get())
    #if selected_genres >= 1:
    
force_genres = customtkinter.StringVar(value="on")


force_genres_switch = CTkSwitch(app, text="Force Genres        ", text_color=text, bg_color=button_color,
                            button_color=diceword_menu_bg, fg_color='black',
                            progress_color=diceword_menu_bg,
                            button_hover_color=faded_text_B,
                            variable=force_genres, command=toggle_force_genres, onvalue="on", offvalue="off")
force_genres_switch.place(x=x_c, y=y_coord+301, anchor="w")



#--------------------------------------------------------------------------------------------------
#print(genre_vars)

rand_genre_setting = 3
def randomize_genres():
    global rand_genre_setting
    rand_genre = rand_genre_setting
    binary_sequence = ''
    # Set the state of the variable (0 for off, 1 for on)
    for genre_var_indice in genre_vars_index:
        if rand_genre == 0:
            one_percent = [0] * 99
            one_percent.append(1)
            random_state = random.choice(one_percent) #1%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        elif rand_genre == 1:
            random_state = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])#10%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        elif rand_genre == 2:
            random_state = random.choice([0, 0, 0, 0, 0, 0, 1])#14%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        elif rand_genre == 3:
            random_state = random.choice([0, 0, 0, 0, 1]) #20%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        elif rand_genre == 4:
            random_state = random.choice([0, 0, 1])#33%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        elif rand_genre == 5:
            random_state = random.choice([0, 0, 0, 1]) #40%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        elif rand_genre == 6:
            random_state = random.choice([0, 1]) #50%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        elif rand_genre == 7:
            random_state = random.choice([0, 1, 1]) #67%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        elif rand_genre == 8:
            random_state = random.choice([0, 1, 1, 1]) #75%
            genre_var_indice.set(random_state)
        elif rand_genre == 9:
            random_state = random.choice([0, 1, 1, 1, 1, 1, 1, 1, 1, 1]) #90%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        elif rand_genre == 10:
            nearly_hundred = [1] * 99
            nearly_hundred.append(0)
            random_state = random.choice(nearly_hundred) #99%
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
        else:
            random_state = random.choice([0 ,1])
            print("Out of range, resorting to: 0, 1")
            genre_var_indice.set(random_state)
            binary_sequence += str(random_state)
    print(binary_sequence)
    selected_genres.clear()  # Clear the list to update it with the new state
    selected_genres.append('e')
    if genre_vars_index[0].get() == 1:
        selected_genres.append('sc')
    if genre_vars_index[1].get() == 1:
        selected_genres.append('fa')
    if genre_vars_index[2].get() == 1:
        selected_genres.append('mo')
    if genre_vars_index[3].get() == 1:
        selected_genres.append('hi')
    if genre_vars_index[4].get() == 1:
        selected_genres.append('ad')
    if genre_vars_index[5].get() == 1:
        selected_genres.append('co')
    if genre_vars_index[6].get() == 1:
        selected_genres.append('ro')
    if genre_vars_index[7].get() == 1:
        selected_genres.append('ho')
    if genre_vars_index[8].get() == 1:
        selected_genres.append('sr')
    if genre_vars_index[9].get() == 1:
        selected_genres.append('te')
    if genre_vars_index[10].get() == 1:
        selected_genres.append('nt')
    if genre_vars_index[11].get() == 1:
        selected_genres.append('my')
    print(selected_genres)

rand_genres_img = PhotoImage(file="assets/imgs/btn1A.png")
randomize_genres_btn = tk.Button(app, height=70, width=70, image=rand_genres_img, text="Randomize Genres", command=randomize_genres)
randomize_genres_btn.place(x=xx+x5+715+35, y=yy+y5+132)
# randomize_genres_btn.place(x=xx+390, y=yy+320)

#my_switch = CTkSwitch(app, text="Toggle Switch")

# Place the switch in your window
#my_switch.place(x=30, y=50)

#---------------------------------SAVE SETTINGS CACHE------------------------------------
#----------------------------------------CACHE-------------------------------------------
SETTINGS_CACHE_FILE = "assets/logs/settings_cache.txt"

# Load settings from cache
def load_settings_cache():
    try:
        with open(SETTINGS_CACHE_FILE, "r") as settings_cache:
            lines = settings_cache.readlines()
            return lines[-1].strip() if lines else ""
    except FileNotFoundError:
        return ""

def save_settings_to_file():
    with open(SETTINGS_CACHE_FILE, "w") as file:
        # Save genre settings
        settings_string = ''.join(str(var.get()) for var in genre_vars_index)
        file.write(f"genre_settings={settings_string}\n")

        # Save other settings
        file.write(f"sep_type_comma={sep_type_comma}\n")
        file.write(f"sep_type_linebreaks={sep_type_linebreaks}\n")
        file.write(f"sep_type_curly={sep_type_curly}\n")
        # Add more settings here
        file.write(f"current_line={current_line}")

# New combined function to load all settings
def load_settings_from_file():
    global sep_type_comma, sep_type_linebreaks, sep_type_curly, current_line
    try:
        with open(SETTINGS_CACHE_FILE, "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                if key == "genre_settings":
                    load_genre_settings(value)
                elif key == "sep_type_comma":
                    sep_type_comma = value == "True"
                elif key == "sep_type_linebreaks":
                    sep_type_linebreaks = value == "True"
                elif key == "sep_type_curly":
                    sep_type_curly = value == "True"
                if key == "current_line":
                    current_line = int(value)
                    line_number_label.config(text=f"{current_line} of {len(template_lines)}")
                # Add more settings here

    except FileNotFoundError:
        pass
    
def load_genre_settings(settings_string):
    for i, var in enumerate(genre_vars_index):
        var.set(int(settings_string[i]))
    if genre_vars_index[0].get() == 1:
            selected_genres.append('sc')
    if genre_vars_index[1].get() == 1:
        selected_genres.append('fa')
    if genre_vars_index[2].get() == 1:
        selected_genres.append('mo')
    if genre_vars_index[3].get() == 1:
        selected_genres.append('hi')
    if genre_vars_index[4].get() == 1:
        selected_genres.append('ad')
    if genre_vars_index[5].get() == 1:
        selected_genres.append('co')
    if genre_vars_index[6].get() == 1:
        selected_genres.append('ro')
    if genre_vars_index[7].get() == 1:
        selected_genres.append('ho')
    if genre_vars_index[8].get() == 1:
        selected_genres.append('sr')
    if genre_vars_index[9].get() == 1:
        selected_genres.append('te')
    if genre_vars_index[10].get() == 1:
        selected_genres.append('nt')
    if genre_vars_index[11].get() == 1:
        selected_genres.append('my')
        
        
        
load_settings_from_file()
#("Curly Braces")("Commas")("Line Breaks")
#sep_type2
if sep_type_curly:
    sep_by_button_var.set("     Pipe Bars     ")
elif sep_type_comma:
    sep_by_button_var.set("     Commas     ")
elif sep_type_linebreaks:
    sep_by_button_var.set("    Line Breaks    ")
    
#------------------------------Text to speech------------------------------------------
#-------------------List Potential Voices In User's System-----------------------------

# Initialize the TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')


with open("assets/logs/voice_choice.txt", "r") as voice_file:
    voice_code = voice_file.read()
    exec(voice_code, globals(), locals())

#-------------------------------Make button, TTS engine----------------------------

def tts_callback(value):
    global read_output_on_screen_tts
    if value == 'TTS On':
        print(value)
        read_output_on_screen_tts = True
    elif value == 'TTS Off':
        print(value)
        read_output_on_screen_tts = False

tts_button = customtkinter.CTkSegmentedButton(app, values=["TTS On", "TTS Off"],
                                                     unselected_color = text_panel_A,
                                                     fg_color= bg,
                                                     text_color= 'black',
                                                     unselected_hover_color = yellow,
                                                     selected_hover_color= green,
                                                     selected_color= dim_text,
                                                     bg_color= bg,
                                                     command=tts_callback)

tts_button.set("TTS Off")
tts_button.place(x=x5+317,y=y5+307)

engine = pyttsx3.init()

def read_text(read_output_on_screen_tts):
    if read_output_on_screen_tts == True:
        text_to_read = output_text.get("1.0", "end-1c")
        engine.say(text_to_read)
        engine.runAndWait()
    else:
        None
    
    
#---------------------------------SAVE TEMPLATE CACHE------------------------------------
ALL_INPUT_TEMPLATES = "assets/logs/all_input_templates.txt"



def load_from_all_input_templates():
    global ALL_INPUT_TEMPLATES
    try:
        with open(ALL_INPUT_TEMPLATES, "r") as input_templates:
            lines = input_templates.readlines()
            return lines[-1] if lines else ""
    except FileNotFoundError:
        return ""

def save_template_to_file():
    text_to_save = entry.get("1.0", tk.END)
    cached_text = load_from_all_input_templates()
    # Check if the current text is the same as the last saved entry
    if text_to_save.strip() != cached_text.strip():
        write_to_all_input_templates(text_to_save)
        
def write_to_all_input_templates(text_to_save):
    with open(ALL_INPUT_TEMPLATES, "r") as input_templates:
        lines = input_templates.readlines()

    # Remove duplicate lines from the list
    lines = list(set(lines))

    # Open the file in write mode and write the non-duplicate lines
    with open(ALL_INPUT_TEMPLATES, "w") as input_templates:
        input_templates.writelines(lines)
    
    # Append the new text
    with open(ALL_INPUT_TEMPLATES, "a") as input_templates:
        input_templates.write(text_to_save)
  
# Load the cached text when the app starts #Possibly have on/off switch for this
cached_text = load_from_all_input_templates()
entry.insert(ttk.END, cached_text)
    
#-------------------------------------------------------------------------------------

#----------------------------Output cmd1 on screen------------------------------------
                                                                            #25        #18
out_text_cmd = ttk.ScrolledText(app, state=tk.DISABLED, wrap=tk.WORD, width=25, height=40, font=("Courier", 8))
out_text_cmd.place(x=xx+990, y=yy+125) #(x=xx+934+48, y=yy+45) <-- closer to margin


# Function to update the output
def update_output_cmd(message):
    out_text_cmd.config(state=tk.NORMAL)
    out_text_cmd.insert(tk.END, message + '\n')
    out_text_cmd.config(state=tk.DISABLED)
    out_text_cmd.see(tk.END)  # Scroll to the end

# Redirect stdout and stderr to a custom function
class OutputRedirector:
    def __init__(self, text_widget, redirect_to=None):
        self.text_widget = text_widget
        self.redirect_to = redirect_to

    def write(self, text):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, text)
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)  # Scroll to the end
        if self.redirect_to:
            self.redirect_to.write(text)

# Redirect stdout and stderr
output_redirector = OutputRedirector(out_text_cmd, sys.stdout)
sys.stdout = output_redirector
sys.stderr = output_redirector



#---------------------------------paste prompt directly to webpage-------------------------------------

#End of App

#--------------------------------Credits----------------------------------------
#Created by Nicholas McDaniel or MackNcD
#EDIT: Additional credits to:
#Discord: @Note, @Gille, @JeffIsNotHere
#Throw me a dollar please, I worked hard on this
#Contact: nickmcdozxtra@gmail.com

def open_link(event):
    webbrowser.open("https://www.buymeacoffee.com/dicewords")
link_label = ttk.Label(app, text="www.buymeacoffee.com/dicewords", background='black', foreground=dim_text, cursor="hand2")
link_label.place(x=995, y=720)

# Bind a click event to open the link when clicked
link_label.bind("<Button-1>", open_link)

app.mainloop()

#----------------------------------------------------------------------------------------










#-------------Boolean save switches-----------


# Initialize BooleanVar to track the switch state
save_input_state = ttk.BooleanVar()
save_output_state = ttk.BooleanVar()

# Function to toggle save input switch state
def toggle_save_input():
    save_input_state.set(not save_input_state.get())

# Function to toggle save output switch state
def toggle_save_output():
    save_output_state.set(not save_output_state.get())


# Create input switch
input_switch_label = Label(app, text="Save Formats")
input_switch_label.place(relx=0.937, rely=0.88)

input_switch = ttk.Radiobutton(app, background=panel_A, variable=save_input_state, command=toggle_save_input)
input_switch.place(relx=0.914, rely=0.88)

# Create output switch
output_switch_label = Label(app, text="Save Gens")
output_switch_label.place(relx=0.937, rely=0.92)

output_switch = ttk.Radiobutton(app, background=panel_A, variable=save_output_state, command=toggle_save_output)
output_switch.place(relx=0.914, rely=0.92)




































#--------------------------------Credits----------------------------------------
#Created by Nicholas McDaniel AKA or Nick_McD or NCK-MCD or MackNcD
#Contact for colab work nickmcdozxtra@gmail.com
#If you don't like it no worries, if you do, please reward my efforts:

#https://www.buymeacoffee.com/dicewords


#def open_link(event):
#    webbrowser.open("https://www.buymeacoffee.com/dicewords")
#link_label = ttk.Label(app, text="https://www.buymeacoffee.com/dicewords", cursor="hand2")
#link_label.place(x=55, y=1000)

# Bind a click event to open the link when clicked
#link_label.bind("<Button-1>", open_link)