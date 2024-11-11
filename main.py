import pygame
import random
import time

pygame.init()

# Increase window size
width, height = 1200, 900  # Increased dimensions
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Memory Recall Experiment")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 74)
instruction_font = pygame.font.Font(None, 40)  # Smaller font for instructions
typing_font = pygame.font.Font(None, 36)  # Smaller font for typing input

AWL_WORDS = [
    "abstruse", "cohort", "disparate", "elicit", "juxtapose",
    "nascent", "obfuscate", "quintessential", "sycophant", "ubiquitous"
]

def get_random_words(num_words=10):
    return random.sample(AWL_WORDS, num_words)

def display_choice_screen():
    window.fill(WHITE)
    prompt = font.render("Choose display mode:", True, BLACK)
    black_option = font.render("Press B for Black", True, BLACK)
    color_option = font.render("Press C for Color", True, BLACK)

    window.blit(prompt, (width // 2 - prompt.get_width() // 2, height // 2 - 100))
    window.blit(black_option, (width // 2 - black_option.get_width() // 2, height // 2))
    window.blit(color_option, (width // 2 - color_option.get_width() // 2, height // 2 + 100))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return "Black", BLACK
                elif event.key == pygame.K_c:
                    return "Color", None
            elif event.type == pygame.QUIT:
                pygame.quit()
                return None, None

def display_color_choice():
    window.fill(WHITE)
    prompt = font.render("Choose word color:", True, BLACK)
    red_option = font.render("Press R for Red", True, BLACK)
    blue_option = font.render("Press B for Blue", True, BLACK)

    window.blit(prompt, (width // 2 - prompt.get_width() // 2, height // 2 - 100))
    window.blit(red_option, (width // 2 - red_option.get_width() // 2, height // 2))
    window.blit(blue_option, (width // 2 - blue_option.get_width() // 2, height // 2 + 100))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "Red", RED
                elif event.key == pygame.K_b:
                    return "Blue", BLUE
            elif event.type == pygame.QUIT:
                pygame.quit()
                return None, None

def display_countdown(seconds=5):
    for i in range(seconds, 0, -1):
        window.fill(WHITE)
        countdown_text = font.render(f"{i}", True, BLACK)
        instruction_text = instruction_font.render("Get ready to recall the words!", True, BLACK)

        window.blit(countdown_text, (width // 2 - countdown_text.get_width() // 2, height // 2))
        window.blit(instruction_text, (width // 2 - instruction_text.get_width() // 2, height // 2 + 100))
        pygame.display.flip()
        time.sleep(1)

def display_words(word_list, display_time=5):
    start_time = time.time()
    while time.time() - start_time < display_time:
        window.fill(WHITE)
        y_offset = 50
        for word, color in word_list:
            text = font.render(word, True, color)
            text_rect = text.get_rect(center=(width // 2, y_offset))
            window.blit(text, text_rect)
            y_offset += 50
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
    return True

def get_recall_input():
    input_text = ""
    window.fill(WHITE)
    prompt = font.render("Type words you recall:", True, BLACK)
    window.blit(prompt, (50, 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text.split()  # Split by spaces for individual words
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character
                else:
                    input_text += event.unicode  # Append character
                window.fill(WHITE)
                window.blit(prompt, (50, 50))
                recall_text = typing_font.render(input_text, True, BLACK)  # Use smaller font for input
                window.blit(recall_text, (50, 150))  # Display typed input
                pygame.display.flip()
            elif event.type == pygame.QUIT:
                pygame.quit()
                return None

def display_restart_screen(correct_recall, total_words):
    window.fill(WHITE)
    result_text = f"Words correctly recalled: {correct_recall}/{total_words}"
    result_display = font.render(result_text, True, BLACK)
    restart_prompt = font.render("Press R to Restart or Q to Quit", True, BLACK)
    withdraw_prompt = font.render("Press W to Withdraw from study", True, BLACK)

    window.blit(result_display, (50, 300))
    window.blit(restart_prompt, (50, 400))
    window.blit(withdraw_prompt, (50, 500))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True, True  # Restart and continue
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False, True  # Quit and continue
                elif event.key == pygame.K_w:
                    print("Participant chose to withdraw from the study.")
                    print("Results not recorded.")
                    return True, False  # Restart the experiment without recording
            elif event.type == pygame.QUIT:
                pygame.quit()
                return False, False  # Quit

def display_debrief():
    window.fill(WHITE)
    debrief_text_1 = font.render("Debriefing:", True, BLACK)
    debrief_text_2 = font.render("The purpose of this study was to investigate", True, BLACK)
    debrief_text_3 = font.render("if color has an effect on recalling words.", True, BLACK)
    debrief_text_4 = font.render("Thank you for your participation!", True, BLACK)

    window.blit(debrief_text_1, (50, 100))
    window.blit(debrief_text_2, (50, 200))
    window.blit(debrief_text_3, (50, 300))
    window.blit(debrief_text_4, (50, 400))
    pygame.display.flip()

    # Wait for a few seconds before exiting
    time.sleep(15)

def run_experiment():
    while True:  # Loop for multiple runs
        participant_number = input("Enter participant number: ")
        mode, selected_color = display_choice_screen()
        if mode is None:
            return

        if mode == "Color":
            color_choice, selected_color = display_color_choice()
            if selected_color is None:
                return
            mode_description = f"Color ({color_choice})"
        else:
            mode_description = "Black"

        word_list = [(word, selected_color) for word in get_random_words(10)]
        display_countdown(5)

        if not display_words(word_list):
            return

        window.fill(WHITE)
        pygame.display.flip()
        time.sleep(1)

        recalled_words = get_recall_input()
        if recalled_words is None:
            return

        original_words = [word for word, color in word_list]
        correct_recall = sum(1 for word in recalled_words if word in original_words)

        print(f"Participant {participant_number}: Mode = {mode_description}, Words correctly recalled = {correct_recall}/{len(original_words)}")

        restart, recorded = display_restart_screen(correct_recall, len(original_words))
        if not recorded:
            continue  # Restart the experiment if user chooses to withdraw

        if not restart:
            break  # Exit the loop if user chooses to quit

    # Display debriefing at the end of the experiment
    display_debrief()

# Start the experiment
run_experiment()
