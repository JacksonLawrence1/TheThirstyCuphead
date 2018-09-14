""" A simple game where the player must move right or left in order
to catch the falling raindrops from the ceiling, and dodge the rocks
falling down."""

import pygame
import random

# Initialises the pygame module
pygame.init()

screen_size = (700, 500)  # Sets screen size
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("The Thirsty Cuphead")  # Title of game at the top

background_image = pygame.image.load("background.png").convert()  # Sets canvas for background image

# Constants colours needed
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (121, 127, 124)
GREEN = (0, 200, 0)
LIGHT_GREEN = (0, 255, 0)

# Sets up the font so it can be used later on
font = pygame.font.SysFont('Comic Sans MS', 20, True, False)
game_over_font = pygame.font.SysFont('Comic Sans MS', 60, True, False)


class Cuphead(pygame.sprite.Sprite):
    """
    Main sprite which is the character which the player controls
    """

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cuphead.png").convert()  # loads graphic image
        self.image.set_colorkey(BLACK)  # Set transparency color
        self.rect = self.image.get_rect()

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)  # Checks if it has collided with said sprite


class Raindrop(pygame.sprite.Sprite):
    """
    Sprite which player needs to collect
    """

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("raindrop.png")  # loads graphic image
        self.image.set_colorkey(WHITE)  # Sets transparency to white
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 5  # Moves 5 pixels each tick

        if self.rect.y > 500:
            return True  # If sprite hits ground then you die (height of screen)

    def reset_pos(self):
        """
        Once raindrop gets collected, it resets above the map to fall back down again at a random position
        """
        self.rect.x = random.randrange(50, 640)
        self.rect.y = random.randrange(-300, -80)


class Rock(pygame.sprite.Sprite):
    """
    Sprite which falls down from the top and if it hits the player, it's game over
    """

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("rock.png")  # loads graphic image
        self.image.set_colorkey(WHITE)  # sets transparency to white
        self.rect = self.image.get_rect()

    def update(self):
        """
        moves 12 pixels down each tick
        if it hits the ground, resets to the top of the map at a random position
        """
        self.rect.y += 12

        if self.rect.y > 500:
            self.rect.y = random.randrange(-1000, -60)

    def reset_pos(self):
        self.rect.y = random.randrange(-1000, -60)
        self.rect.x = random.randrange(50, 640)


amount_of_rocks = 12  # This is how many rocks will fall on the map at once

rock_list = pygame.sprite.Group()  # Creates a sprite list so that all the rocks can be called
all_sprites_list = pygame.sprite.Group()  # A list of all the sprites in the game

for i in range(amount_of_rocks):
    """
    Creates rocks at random positions above the map and adds them to the list
    """
    rock = Rock()

    rock.rect.x = random.randrange(50, 640)
    rock.rect.y = random.randrange(-1000, -60)

    rock.add(rock_list)
    rock.add(all_sprites_list)

player = Cuphead()
player.rect.x = 325
player.rect.y = 425
player.add(all_sprites_list)  # Sets the player to middle of the screen and adds to all sprites list

raindrop = Raindrop()
raindrop.rect.y = random.randrange(-300, -60)
raindrop.rect.x = random.randrange(640)
raindrop.add(all_sprites_list)  # Adds raindrop to all sprites list and gives it a random position above the map

player_speed = 0  # Initialisation of the speed of the player
score = 0  # Variable for the score of the player

repeat = True
game_over = False

clock = pygame.time.Clock()  # Creates a clock using the Pygame Library

while repeat:  # Main event loop
    clock.tick(30)  # Sets the clock to tick at 30 times a second

    mouse = pygame.mouse.get_pos()  # Variable to store position of mouse
    click = pygame.mouse.get_pressed()  # Variable that changes depending if the mouse is clicking

    if not game_over:  # Checks if the game isn't over
        screen.blit(background_image, [0, 0])  # Blits the background image loaded at beginning of code

        for event in pygame.event.get():
            """
            If player presses the x in the top right, the game will close.
            """
            if event.type == pygame.QUIT:
                repeat = False

            elif event.type == pygame.KEYDOWN:
                """
                Controls for where the player moves right or left
                """
                if event.key == pygame.K_LEFT:
                    player_speed -= 15
                elif event.key == pygame.K_RIGHT:
                    player_speed += 15

            elif event.type == pygame.KEYUP:
                """
                When the player stops pressing the button, the player's sprite will stop
                """
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_speed = 0

        if raindrop.update():
            game_over = True

        player.rect.x += player_speed  # Adds the speed to the player's coordinate

        if player.rect.x < 25:
            player.rect.x = 25
        if player.rect.x > 640:
            player.rect.x = 640

        all_sprites_list.draw(screen)  # Draws all of the sprites in the game onto the screen
        raindrop.update()
        rock_list.update()  # Updates the raindrop and rocks to be in their position

        if player.is_collided_with(raindrop):
            """
            If the player's sprite collides with the raindrop, add 1 to score and reset raindrop's position
            """
            score += 1
            raindrop.reset_pos()

        rock_collide = pygame.sprite.spritecollide(player, rock_list, True)
        # Checks if any rocks, in rock_list collide with the player's sprite

        if rock_collide:
            """
            If collides with a rock, the game is over.
            """
            game_over = True

        pygame.draw.line(screen, GRAY, [0, 0], [700, 0], 50)
        pygame.draw.line(screen, GRAY, [700, 0], [700, 500], 50)
        pygame.draw.line(screen, GRAY, [700, 500], [0, 500], 50)
        pygame.draw.line(screen, GRAY, [0, 500], [0, 0], 50)  # Border of walls for the game

        textsurface = font.render("Score: {}".format(score), True, BLACK)  # Renders the score
        screen.blit(textsurface, (290, -3))  # Blits the score to the screen

        pygame.display.flip()  # Updates game display

    else:
        for event in pygame.event.get():
            """
            If player presses the x in the top right, the game will close.
            """
            if event.type == pygame.QUIT:
                repeat = False

        screen.fill(GRAY)  # Fills the screen to be gray
        game_over_surface = game_over_font.render("Game over!", True, BLACK)  # Renders Game Over Text
        score_surface = font.render("Your Score was {}".format(score), True, BLACK)  # Renders Score
        screen.blit(game_over_surface, (190, 150))
        screen.blit(score_surface, (260, 230))  # Blits text to the screen

        play_again_surface = font.render("Play Again", True, BLACK)
        pygame.draw.rect(screen, GREEN, [250, 300, 200, 100])  # Button with text to ask if user wants to play again
        if 250 + 200 > mouse[0] > 250 and 300 + 100 > mouse[1] > 300:  # If mouse is in the region of the button
            pygame.draw.rect(screen, LIGHT_GREEN, [250, 300, 200, 100])  # Button becomes 'illuminated'
            if click[0] == 1:
                """
                Checks if the user clicks on the button, and will restart game if the user has
                """
                score = 0
                game_over = False
                player.rect.x = 325
                player.speed = 0
                raindrop.reset_pos()
                for rock in rock_list:
                    rock.reset_pos()

        screen.blit(play_again_surface, (300, 335))  #Blits the text of the play again button to the screen

        pygame.display.flip()  # Updates game display

pygame.quit()
