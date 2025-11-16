import pygame
import random
import time

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("t.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

correct_sound = pygame.mixer.Sound("correct.mp3")
wrong_sound = pygame.mixer.Sound("wrong.mp3")

game_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Hangman Game")

window_width, window_height = pygame.display.get_surface().get_size()

font = pygame.font.SysFont('timesnewroman', int(window_height // 16))
small_font = pygame.font.SysFont('timesnewroman', int(window_height // 20))

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (173, 216, 230)

background_image = pygame.image.load("c.jpg")
background_image = pygame.transform.scale(background_image, (window_width, window_height))

HANGMANPICS = [
    '''  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========''',
    '''  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========''',
    '''  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========''',
    '''  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========''',
    '''  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========''',
    '''  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========''',
    '''  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n========='''
]

word_categories = {
    "Easy": {
        "Chocolates": ["kitkat", "munch"],
        "Cars": ["bmw", "audi"],
        "Countries": ["india", "brazil"],
        "Fruits": ["kiwi", "pear"],
        "Animals": ["cat", "bat", "owl"],
        "Planets": ["mars", "earth"],
        "Sports": ["golf", "tennis"],
        "Cities": ["paris", "london"],
        "Movies": ["it", "jaws"],
        "Instruments": ["drum", "flute"],
        "Flowers": ["rose", "lily"],
        "Books": ["it", "1984"],
        "Colors": ["red", "blue"],
        "Occupations": ["chef", "clerk"],
        "Mountains": ["k2", "fuji"],
        "Birds": ["owl", "crow"],
        "Rivers": ["nile", "seine"]
    },
    "Medium": {
        "Chocolates": ["milkybar", "snickers"],
        "Cars": ["benz", "porsche"],
        "Countries": ["canada", "france"],
        "Fruits": ["mango", "banana"],
        "Animals": ["dog", "fish"],
        "Planets": ["venus", "jupiter"],
        "Sports": ["cricket", "soccer"],
        "Cities": ["tokyo", "berlin"],
        "Movies": ["hero", "dune"],
        "Instruments": ["piano", "guitar"],
        "Flowers": ["daisy", "tulip"],
        "Books": ["dune", "hamlet"],
        "Colors": ["pink", "gray"],
        "Occupations": ["pilot", "nurse"],
        "Mountains": ["denali", "blanc"],
        "Birds": ["finch", "sparrow"],
        "Rivers": ["amazon", "ganges"]
    },
    "Hard": {
        "Chocolates": ["dairymilk"],
        "Cars": ["ferrari", "lamborghini"],
        "Countries": ["germany"],
        "Fruits": ["apple"],
        "Animals": ["eagle"],
        "Planets": ["neptune"],
        "Sports": ["hockey"],
        "Cities": ["sydney"],
        "Movies": ["titanic"],
        "Instruments": ["sax"],
        "Flowers": ["carnation"],
        "Books": ["frankenstein"],
        "Colors": ["black"],
        "Occupations": ["doctor"],
        "Mountains": ["everest"],
        "Birds": ["eagle"],
        "Rivers": ["yangtze"]
    }
}

chosen_word = []
blank_list = []
wrong_guesses = []
max_tries = 6
update_display = 0
difficulty_chosen = False
category = ""
hint_count = 0
max_hints = 3
score = 0
running = True

def display_text(text, font, color, x_ratio, y_ratio):
    rendered_text = font.render(text, True, color)
    x = int(window_width * x_ratio)
    y = int(window_height * y_ratio)
    game_window.blit(rendered_text, (x, y))

def give_hint():
    global hint_count
    if hint_count < max_hints:
        hint_letter = random.choice([letter for letter in chosen_word if letter not in blank_list])
        hint_count += 1
        for idx, letter in enumerate(chosen_word):
            if letter == hint_letter:
                blank_list[idx] = hint_letter
        return hint_letter
    return None

def display_hangman(state_index):
    hangman_pic_lines = HANGMANPICS[state_index].split("\n")
    y_offset = int(window_height * 0.1)
    for line in hangman_pic_lines:
        display_text(line, small_font, black, 0.05, y_offset / window_height)
        y_offset += int(window_height * 0.03)

def update_screen():
    game_window.blit(background_image, (0, 0))
    display_hangman(update_display)
    display_text(' '.join(blank_list), font, black, 0.05, 0.75)
    display_text(f"Wrong guesses: {', '.join(wrong_guesses)}", small_font, red, 0.1, 0.85)
    display_text(f"Hints used: {hint_count}/{max_hints}", small_font, black, 0.1, 0.9)
    display_text(f"Score: {score}", small_font, black, 0.7, 0.9)
    display_text(f"Category: {category}", small_font, black, 0.6, 0.05)
    display_text("Rules:", small_font, black, 0.6, 0.12)
    display_text("[ESC] Exit", small_font, black, 0.6, 0.18)
    display_text("Press '1' for hint", small_font, black, 0.6, 0.24)
    pygame.display.update()

def start_new_game():
    global chosen_word, blank_list, wrong_guesses, update_display, category, hint_count
    difficulty = "Easy" if max_tries == 8 else "Medium" if max_tries == 6 else "Hard"
    category = random.choice(list(word_categories[difficulty].keys()))
    chosen_word = list(random.choice(word_categories[difficulty][category]))
    blank_list = ["_"] * len(chosen_word)
    wrong_guesses = []
    update_display = 0
    hint_count = 0
    display_text(f"Category: {category}", small_font, black, 0.5, 0.5)
    pygame.display.update()
    time.sleep(2)

def choose_difficulty(event):
    global max_tries, difficulty_chosen
    if event.key == pygame.K_e:
        max_tries = 8
    elif event.key == pygame.K_m:
        max_tries = 6
    elif event.key == pygame.K_h:
        max_tries = 4
    else:
        return
    difficulty_chosen = True
    start_new_game()

def display_text_centered(text, font, color, y_ratio):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(window_width // 2, int(window_height * y_ratio)))
    game_window.blit(rendered_text, text_rect)

def display_front_page():
    while True:
        game_window.blit(background_image, (0, 0))
        display_text_centered("HANGMAN GAME!", font, black, 0.3)
        display_text_centered("Press [SPACE] to Start", small_font, green, 0.5)
        display_text_centered("[ESC] to Exit", small_font, red, 0.6)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

display_front_page()

while running:
    game_window.blit(background_image, (0, 0))
    display_text("Choose difficulty:", font, black, 0.1, 0.4)
    game_window.blit(background_image, (0, 0))
    display_text("Choose Difficulty", font, black, 0.4, 0.3)
    display_text("[E] Easy", small_font, red, 0.35, 0.45)
    display_text("[M] Medium", small_font, red, 0.35, 0.55)
    display_text("[H] Hard", small_font, red, 0.35, 0.65)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            choose_difficulty(event)
    if difficulty_chosen:
        break

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                give_hint()
                update_screen()
            elif pygame.K_a <= event.key <= pygame.K_z:
                guess = chr(event.key)
                correct_guess = False
                if guess in blank_list or guess in wrong_guesses:
                    continue
                for idx, letter in enumerate(chosen_word):
                    if guess == letter:
                        blank_list[idx] = guess
                        correct_guess = True
                if correct_guess:
                    correct_sound.play()
                else:
                    wrong_guesses.append(guess)
                    update_display += 1
                    wrong_sound.play()
                if update_display >= len(HANGMANPICS) - 1:
                    display_text(f"You lost! The word was '{''.join(chosen_word)}'", font, red, 0.1, 0.4)
                    pygame.display.update()
                    time.sleep(3)
                    score -= 1
                    start_new_game()
                if blank_list == chosen_word:
                    display_text("Congratulations! You won!", font, green, 0.1, 0.4)
                    pygame.display.update()
                    time.sleep(3)
                    score += 1
                    start_new_game()
    update_screen()

pygame.quit()
