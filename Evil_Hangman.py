##Luke McDuff
##ljm7b2@mail.umkc.edu
##CS 101/Program 6
##April/13/2014
##ALGORITHM 
##A Few Important Variables:
##		
##  -dictionary: contains contents of dictionary.txt
##		
##  -master_list: contains a list of all words that are of "N" length, variable for "N" is desired_word_length
##		
##  -guess,guessed: contain a single guess or a string with all guesses respectively
##		
##  -wordLength: is the most important; is the output "----e----", makes user think their guess is right, and also
##		is used as key to letter variation dictionary, also used in scorekeeping.
##							
##  -letter_variation_dict: dictionary with wordLength as key, potential words as values 
##			    -example: {"-e--":["meat","heat","lend"],"e--e":["effe","este"]}
##			    -for each guess, the key is returned with most word in values list
##			    -these values are then appended to an empty master_list and become the
##			    -pool of words to search through each guess, evil mode only
##-Essential logic, revised algorithm:
##
##--Get input for game parameters
##	-get total amount of guesses
##	-get info as to show words remaining or not
##	-get desired word length
##
##--Keep track of this important information
##	-calculate turns remaining
##	-letters already guessed
##	-number of words remaining to select from
##	-rebuild guess pool alphabet with letters guessed as "-" ie -> "ab-cd"
##
##--Play the game.....
##	-build initial word list from dictionary of words with length stated by user
##	-input users first letter guess
##	-build variation dictionary based off guess and build a new master list from largest value(list of words)
##	-check to see if guess is in largest letter variation dict values key
##	-print all relevant hangman info for user
##	-continue reducing size of master list until largest dict value contains 1 word
##		-if score is not 0, proceed to play real hangman
##			-if variation("---e---") contains no "-" then user has guessed word, gameover
##			-if score equals 0, gameover
##		-if score is 0, return random word from list, gameover
##ERROR HANDLING : Checks on all input is performed to ensure correct class and range.
##COMMENTS: A couple thoughts: gained a stronger grasp on the logic of using functions, worked to
##          keep functions simple which ended up helping greatly during final revisions. Started work
##          to try and adjust sort algorithm, made a little progress, but nothing worth including. Last
##          two functions are the extension functions.
##          


#####################################################################
def hangman_graphic()-> str:
    print("""
          ________   
          |	 |   
          @      |   
        _/|\_    |   
          |      |\O 
        _/ \_    | |\_
                 | | 
    _____________|/_\_
    ==================
    -----HANGMAN*-----
    ==================
    """)
    

def turns_remaining_input()->int:
    """Checks number of turns input for correct range, outputs the turns."""
    while True:
        try:
            turns_remaining = int(input("How many guesses [1+]? ->"))
            if 0<turns_remaining<=26:   #what is the point of zero turns, or more than 26?
                return turns_remaining
            else:
                print("The range of number of guesses is 1 through 26.")
                continue
        except ValueError:
            print("Please use an integer.")

def words_remaining_input()->str:
    """Checks input, and enables the printing of words remaining information."""
    while True:
        words_remaining = input("Print count of words remaining? [y/n] ->").lower()
        if words_remaining == "y" or words_remaining == "n":
            return words_remaining
        else:
            print("Please use only [y/n].")
            continue

def desired_word_length_input()->int:
    """Checks input for correct range, and outputs length of word as int."""
    while True:
        try:
            desired_word_length = int(input("How many letters in secret word? ->"))
            ##determined all length variations of words in dictionary, which are ->[2-22,24,28,29]
            if 2<=desired_word_length<=22 or desired_word_length in [24,28,29]:
                return desired_word_length
            else:
                print("There are no words in the dictionary of that length.")
                continue
        except ValueError:
            print("Please enter an integer.")
            continue

def game_parameters():
    """Collects all parameters for game setup."""
    print("{:^32}\n{:^33}\n".format("WELCOME TO HANGMAN","Lets setup the game."))
    desired_word_length = desired_word_length_input()
    words_remaining = words_remaining_input()
    turns_remaining = turns_remaining_input()
    hangman_graphic()
    wordLength = "-" *desired_word_length
    return desired_word_length, words_remaining, turns_remaining, wordLength    

def turns_remaining_calc(turns_remaining:int,wordLength:str,guess:str)->int:
    """Reduces number of turns remaining, if guess not found in word."""
    if guess not in wordLength:
        turns_remaining -= 1
    return turns_remaining
    
def alphabet_builder(guessed="")->str:
    """Builds guess alphabet to show user what letters are left to guess."""
    alph=string.ascii_lowercase
    for letter in guessed:
        alph=alph.replace(letter,"-")
    return alph.upper()

def get_guess(guessed="")->str:
    """Checks input, and outputs letter guessed by user."""
    while True:
        guess = input("---->").lower()
        if len(guess)>1 or guess not in string.ascii_lowercase:
            print("Guess a single letter.")
            continue
        if guess in guessed and guess != "":
            print("You already guessed",guess.upper()+".","Guess again.")
            continue
        else:        
            guessed += guess
            return guess, guessed

def dict_file_to_list(dictionary,desired_word_length:int)-> list:
    """Builds initial list from dictionary, based on desired word length input."""
    master_list=[word.strip() for word in dictionary if len(word.strip()) == desired_word_length]
    return master_list

def guess_in_word_or_not(guess:str,wordLength:str)->str:
    """Checks to see if guess is in word, or guess is in top word variation, -> ---ee---"""
    if guess != "":
        if guess in wordLength:
            print("\nNICE GUESS!",guess.upper(),"is present.")
        else:
            print("\nSORRY.",guess.upper(),"is not present.")

def print_hangman_info(turns_remaining,wordLength, master_list,words_remaining="y", guess="", guessed="")->str:
    """Main printing hub for game information."""
    print()
    guess_in_word_or_not(guess,wordLength)
    if turns_remaining == 1:
        print("You have {} guess left.".format(turns_remaining))
    else:               #punctuation correction for guess vs guesses
        print("You have {} guesses left.".format(turns_remaining))
    print("Letters chosen: {}\nWord: {}".format(guessed.upper(), wordLength.upper()))
    if words_remaining == "y":
        if len(master_list) == 1:
            print(len(master_list),"word remaining.")
        else:           #punctuation correction for words vs word
            print(len(master_list),"words remaining.")
    print("Choose one of the following: {}".format(alphabet_builder(guessed)))

def letter_variation_builder(master_list:list, guessed:str, real_evil_h=True)->dict:
    """Takes each letter guessed and finds all combinations in master word list for each guess.
       Each variation is sent to dictionary building function."""
    letter_var_dict = {}
    if real_evil_h == False:
        global wordLength
    for word in master_list:
        if real_evil_h == True:#resets if in evilhangman
            wordLength = "-"*desired_word_length
        for letter in guessed:
            for char in range(len(word)):   #build variation, ie "----e----"
                if letter in word[char]:
                    wordLength = wordLength[:char]+word[char]+wordLength[char+1::]                   
        letter_var_dict = letter_var_dict_builder(letter_var_dict,wordLength,word)
    return letter_var_dict, wordLength

def letter_var_dict_builder(letter_var_dict:dict,wordLength:str,word:str)->dict:
    """Builds letter variation dictionary."""
    if wordLength in letter_var_dict:   #build dict {"----e---":["cat","mouse"]}
        letter_var_dict[wordLength].append(word)
    else:
        letter_var_dict[wordLength] = [word]    
    return letter_var_dict

def reduce_master_list(master_list:list,guess:str,guessed:str,turns_remaining:int):
    """With each guess, creates new master list from largest value(word list) in
       letter variation dictionary. It only reduces until largest value in dictionary
       is a single word. Then it finds the key with the least amount of letters already guessed,
       this is then outputed to play hangman function. If player runs out of guesses before hangman
       stage is reached, an int is outputted instead which triggers the end of game."""
    while True:
        letter_var_dict,x = letter_variation_builder(master_list, guessed)
        largest_word_lst=sorted([(len(v),k) for k,v in letter_var_dict.items()],reverse=True)#[(9,"--e--")]
        #if difficulty == 1:
            #largest_word_lst = higher_difficulty_sort(largest_word_lst)

        if largest_word_lst[0][0] == 1: #finds variation with least amount of guesses
            best_word_choice = sorted([(i[-1].count("-"),i) for i in largest_word_lst],reverse=True)
            wordLength= best_word_choice[0][-1][1]
            master_list=letter_var_dict[wordLength]
            return wordLength, master_list,best_word_choice,guessed,turns_remaining,guess

        master_list, wordLength = letter_var_dict[largest_word_lst[0][-1]], largest_word_lst[0][-1]
        turns_remaining = turns_remaining_calc(turns_remaining,wordLength,guess)
        if turns_remaining == 0:
            print("\nYou are out of guesses. GAME OVER.\nThe word was: ",random.choice(master_list).upper())
            return 1,2,3,4,5,6 #outputs an int if turns left equal 0, triggers end of game
        print_hangman_info(turns_remaining,wordLength, master_list,words_remaining, guess, guessed)
        guess, guessed = get_guess(guessed)

def play_real_hangman(master_list:list, guess:str, guessed:str, turns_remaining:int):
    """Takes final word and matching variation->("----e-e---") and applies normal hangman logic."""
    for i in master_list: 
        final_word=i     
    while True:
        n, wordLength = letter_variation_builder(master_list, guessed,real_evil_h=False)
        turns_remaining = turns_remaining_calc(turns_remaining,wordLength,guess)
        if wordLength.count("-")==0:           
            print("\nYou won! You correctly guessed:", final_word.upper()+".","With", turns_remaining,\
                  "guesses left!")
            break
        if turns_remaining == 0:
            print("\nYou are out of guesses. GAME OVER.\nThe word was: ",final_word.upper())
            break
        print_hangman_info(turns_remaining,wordLength, master_list,words_remaining, guess, guessed)
        guess, guessed = get_guess(guessed)

def higher_difficulty_sort(largest_word_lst): #rough start to an extension of sorting
    """Experimented with the idea of changing method of sort."""
    largest=[]
    for i in largest_word_lst:
        
        largest.append((i[-1].count("-"),i[0],i[-1]))
    
    #print(sorted(largest))
    largest_word_lst = sorted(largest)
    return largest_word_lst

def difficulty_input()->int:
    while True:
        try:
            difficulty = int(input("\nWould you like to try the optional sorting method? 1=yes,2=no "))
            if difficulty not in [1,2]:
                print("Enter 1 for yes, 2 for no.")
                continue
            return difficulty
        except ValueError:
            print("Please, an integer; eiter 1 or 2.")
            continue


#PROGRAM#
import random
import string
dictionary = open("dictionary.txt","r")

##setup##
desired_word_length, words_remaining, turns_remaining, wordLength = game_parameters()

#difficulty = difficulty_input() 

master_list = dict_file_to_list(dictionary,desired_word_length)
dictionary.close()
print_hangman_info(turns_remaining,wordLength, master_list,words_remaining)
guess, guessed = get_guess()

##gameplay##
wordLength, master_list,best_word_choice,guessed,turns_remaining,\
            guess=reduce_master_list(master_list,guess,guessed,turns_remaining)

if wordLength != 1:    
    play_real_hangman(master_list, guess, guessed, turns_remaining)

