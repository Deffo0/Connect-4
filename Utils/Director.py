from Utils.Builder import *


class Director:

    def __init__(self, screen, pygame, width, height):
        self.button_builder = ButtonBuilder(screen, pygame)
        self.title_builder = TitleBuilder(screen, pygame)
        self.text_input_builder = TextInputBuilder(screen, pygame)
        self.board_builder = BoardBuilder(screen, pygame)
        self.small_font = pygame.font.Font(os.path.join("Resources", "FuzzyBubbles-Regular.ttf"), 20)
        self.tiny_font = pygame.font.Font(os.path.join("Resources", "FuzzyBubbles-Regular.ttf"), 14)
        self.medium_font = pygame.font.Font(os.path.join("Resources", "FuzzyBubbles-Regular.ttf"), 28)
        self.large_font = pygame.font.Font(os.path.join("Resources", "FuzzyBubbles-Regular.ttf"), 40)
        self.cell_font = pygame.font.Font(os.path.join("Resources", "FuzzyBubbles-Regular.ttf"), 60)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gray = (132, 136, 132)
        self.sun = (253, 169, 19)
        self.width = width
        self.height = height

    def start_menu_title(self):
        self.title_builder.specify_dimensions((self.width / 2), 50)
        self.title_builder.specify_colors(self.gray)
        self.title_builder.specify_text("Connect-4 Game", self.large_font)
        self.title_builder.build()

    def start_menu_label(self):
        self.title_builder.specify_dimensions((self.width / 2) - 80, (self.height / 2) - 100)
        self.title_builder.specify_colors(self.gray)
        self.title_builder.specify_text("Enter limited depth:", self.small_font)
        self.title_builder.build()

    def start_menu_text_input(self, user_text):
        self.text_input_builder.specify_dimensions((self.width / 2) - 175, (self.height / 2) - 75, 350, 25)
        self.text_input_builder.specify_colors(self.gray, self.white)
        self.text_input_builder.specify_text(user_text, self.tiny_font)
        self.text_input_builder.build()

    def red_player_pruning_button(self):
        self.button_builder.specify_dimensions((self.width / 4), (self.height / 2), self.width / 2, 30)
        self.button_builder.specify_colors(self.gray, self.black)
        self.button_builder.specify_text("Red player against AI with pruning", self.small_font)
        return self.button_builder.build()

    def yellow_player_pruning_button(self):
        self.button_builder.specify_dimensions((self.width / 4), (self.height / 2) + 40, self.width / 2, 30)
        self.button_builder.specify_colors(self.gray, self.black)
        self.button_builder.specify_text("Yellow player against AI with pruning", self.small_font)
        return self.button_builder.build()

    def red_player_without_pruning_button(self):
        self.button_builder.specify_dimensions((self.width / 4), (self.height / 2) + 80, self.width / 2, 30)
        self.button_builder.specify_colors(self.gray, self.black)
        self.button_builder.specify_text("Red player against AI without pruning", self.small_font)
        return self.button_builder.build()

    def yellow_player_without_pruning_button(self):
        self.button_builder.specify_dimensions((self.width / 4) , (self.height / 2) + 120, self.width / 2, 30)
        self.button_builder.specify_colors(self.gray, self.black)
        self.button_builder.specify_text("Yellow player against AI without pruning", self.small_font)
        return self.button_builder.build()

    def game_board(self, board):
        self.board_builder.specify_dimensions((self.width / 2 - (3.5 * 80), self.height / 2 - (3.5 * 80)), 80)
        self.board_builder.specify_colors(self.gray)
        self.board_builder.specify_board(board, self.cell_font)
        return self.board_builder.build()

    def gameplay_title(self, title):
        self.title_builder.specify_dimensions((self.width / 2), 30)
        self.title_builder.specify_colors(self.gray)
        self.title_builder.specify_text(title, self.large_font)
        self.title_builder.build()

    def tree_button(self):
        self.button_builder.specify_dimensions((self.width - 150), 120, 120, 30)
        self.button_builder.specify_colors(self.gray, self.black)
        self.button_builder.specify_text("Show Tree", self.small_font)
        return self.button_builder.build()

    def gameplay_restart_button(self):
        self.button_builder.specify_dimensions(self.width / 3, self.height - 65, self.width / 3, 40)
        self.button_builder.specify_colors(self.gray, self.black)
        self.button_builder.specify_text("restart", self.medium_font)
        return self.button_builder.build()


