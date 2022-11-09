import sys
import time

import pygame

import Agent as ai
from Utils.Director import Director

pygame.init()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)

begin = False
user = None
pruning = None
board = None
tree = None
ai_turn = False
limited_depth = ""
director = Director(screen, pygame, width, height)


def start_menu():
    global screen, board, begin, limited_depth, user, pruning
    # Draw title and label
    director.start_menu_title()
    director.start_menu_label()
    # Draw start buttons
    red_w_pruning = director.red_player_pruning_button()
    red_without_pruning = director.red_player_without_pruning_button()
    yellow_w_pruning = director.yellow_player_pruning_button()
    yellow_without_pruning = director.yellow_player_without_pruning_button()
    for start_menu_event in pygame.event.get():
        if start_menu_event.type == pygame.KEYDOWN:
            if start_menu_event.key == pygame.K_BACKSPACE:
                limited_depth = limited_depth[:-1]
                time.sleep(0.1)

            else:
                limited_depth += start_menu_event.unicode
                time.sleep(0.1)

    director.start_menu_text_input(limited_depth)

    # Check if algorithm buttons is clicked
    start_click, _, _ = pygame.mouse.get_pressed()
    if start_click == 1 and limited_depth != "":
        start_mouse = pygame.mouse.get_pos()
        if red_w_pruning.collidepoint(start_mouse):
            user = ai.red
            pruning = True
            board = ai.initial_state()
            time.sleep(0.2)
            begin = True

        elif red_without_pruning.collidepoint(start_mouse):
            user = ai.red
            pruning = False
            board = ai.initial_state()
            time.sleep(0.2)
            begin = True

        elif yellow_w_pruning.collidepoint(start_mouse):
            user = ai.yellow
            pruning = True
            board = ai.initial_state()
            time.sleep(0.2)
            begin = True

        elif yellow_without_pruning.collidepoint(start_mouse):
            user = ai.yellow
            pruning = False
            board = ai.initial_state()
            time.sleep(0.2)
            begin = True


def gameplay():
    global board, begin, ai_turn, tree
    the_end = False
    tiles = director.game_board(board)
    tree_button = director.tree_button()
    player = ai.player(board)
    if player is None:
        the_end = True

    if the_end:
        score = ai.get_score(board)
        title = f"Game Over: Score is {score[0]} red : {score[1]} yellow"
    elif user == player:
        title = f"Play as {user}"
    else:
        title = f"Computer thinking..."
    director.gameplay_title(title)

    if user != player and not the_end:
        if ai_turn:
            time.sleep(0.5)
            move, tree = ai.minimax(board, pruning, int(limited_depth))
            board = ai.result(board, move)
            ai_turn = False
        else:
            ai_turn = True

    gameplay_click, _, _ = pygame.mouse.get_pressed()
    if gameplay_click == 1:
        gameplay_mouse = pygame.mouse.get_pos()
        if tree_button.collidepoint(gameplay_mouse):
            tree = ai.get_tree()
        elif user == player and not the_end:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ai.EMPTY and tiles[i][j].collidepoint(gameplay_mouse):
                        print("lol")
                        board = ai.result(board, j)
                        print(board)
                        time.sleep(0.2)

    if the_end:
        again_button = director.gameplay_restart_button()
        end_click, _, _ = pygame.mouse.get_pressed()
        if end_click == 1:
            end_mouse = pygame.mouse.get_pos()
            if again_button.collidepoint(end_mouse):
                time.sleep(0.2)
                begin = False


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 0, 0))

    if begin is False:
        start_menu()

    else:
        gameplay()

    pygame.display.flip()
