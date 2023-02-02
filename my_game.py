"""
Simple program to show moving a sprite with the keyboard.

This program uses the Arcade library found at http://arcade.academy

Artwork from https://kenney.nl/assets/space-shooter-redux

"""

import arcade

SPRITE_SCALING = 0.5

# Set the size of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Variables controlling the player
PLAYER_LIVES = 3
PLAYER_SPEED = 5
PLAYER_START_X = SCREEN_WIDTH / 2
PLAYER_START_Y = 50
PLAYER_SHOT_SPEED = 4

FIRE_KEY = arcade.key.SPACE


class Player(arcade.Sprite):
    """
    The player
    """

    def __init__(self, **kwargs):
        """
        Setup new Player object
        """

        # Graphics to use for Player
        self.speed = None
        kwargs['filename'] = "images/playerShip1_red.png"

        # How much to scale the graphics
        kwargs['scale'] = SPRITE_SCALING
        kwargs['flipped_diagonally'] = True
        kwargs['flipped_horizontally'] = True
        kwargs['flipped_vertically'] = False

        # Pass arguments to class arcade.Sprite
        super().__init__(**kwargs)

        self.angle = 90

    def update(self):
        """
        Move the sprite
        """

        # Update center_x
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.change_x = 0
        self.change_y = 0

        # Don't let the player move off screen
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class PlayerShot(arcade.Sprite):
    """
    A shot fired by the Player
    """

    def __init__(self, start_position, start_angle=90):
        """
        Setup new PlayerShot object
        """

        # Set the graphics to use for the sprite
        # We need to flip it so it matches the mathematical angle/direction
        super().__init__(
            filename="images/Lasers/laserBlue01.png",
            scale=SPRITE_SCALING,
            flipped_diagonally=True,
            flipped_horizontally=True,
            flipped_vertically=False
        )

        # Shoot points in this direction
        self.angle = start_angle

        # Shoot spawns/starts here
        self.position = start_position

        # Shot moves forward
        self.forward(PLAYER_SHOT_SPEED)

    def update(self):
        """
        Move the sprite
        """

        # Update the position
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Remove shot when over top of screen
        if self.bottom > SCREEN_HEIGHT:
            self.kill()


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height)

        # Variable that will hold a list of shots fired by the player
        self.tank_right_pressed = None
        self.tank_left_pressed = None
        self.tank_backward_pressed = None
        self.tank_forward_pressed = None
        self.player_shot_list = None

        # Set up the player info
        self.player_sprite = None
        self.player_score = None
        self.player_lives = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Get list of joysticks
        joysticks = arcade.get_joysticks()

        if joysticks:
            print("Found {} joystick(s)".format(len(joysticks)))

            # Use 1st joystick found
            self.joystick = joysticks[0]

            # Communicate with joystick
            self.joystick.open()

            # Map joysticks functions to local functions
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
            self.joystick.on_joyaxis_motion = self.on_joyaxis_motion
            self.joystick.on_joyhat_motion = self.on_joyhat_motion

        else:
            print("No joysticks found")
            self.joystick = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # No points when the game starts
        self.player_score = 0

        # No of lives
        self.player_lives = PLAYER_LIVES

        # Sprite lists
        self.player_shot_list = arcade.SpriteList()

        # Create a Player object
        self.player_sprite = Player(
            center_x=PLAYER_START_X,
            center_y=PLAYER_START_Y
        )

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the player shot
        self.player_shot_list.draw()

        # Draw the player sprite
        self.player_sprite.draw()

        # Draw players score on screen
        arcade.draw_text(
            "SCORE: {}".format(self.player_score),  # Text to show
            10,  # X position
            SCREEN_HEIGHT - 20,  # Y positon
            arcade.color.WHITE  # Color of text
        )

    def on_update(self, delta_time):
        """
        Movement and game logic
        """

        # Calculate player speed based on the keys pressed
        self.player_sprite.change_x = 0

        # Move player with keyboard
        '''
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_SPEED_X
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_SPEED_X
        '''

        if self.tank_left_pressed and not self.tank_right_pressed:
            self.player_sprite.angle += 3
        if self.tank_right_pressed and not self.tank_left_pressed:
            self.player_sprite.angle -= 3
        if self.tank_forward_pressed and not self.tank_backward_pressed:
            self.player_sprite.forward(PLAYER_SPEED)
        if self.tank_backward_pressed and not self.tank_forward_pressed:
            self.player_sprite.forward(-PLAYER_SPEED)

        # Move player with joystick if present
        if self.joystick:
            self.player_sprite.change_x = round(self.joystick.x) * PLAYER_SPEED

        # Update player sprite
        self.player_sprite.update()

        # Update the player shots
        self.player_shot_list.update()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        # Track state of arrow keys
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

        if key == arcade.key.W:
            self.tank_forward_pressed = True
        if key == arcade.key.S:
            self.tank_backward_pressed = True
        if key == arcade.key.A:
            self.tank_left_pressed = True
        if key == arcade.key.D:
            self.tank_right_pressed = True

        if key == FIRE_KEY:
            new_shot = PlayerShot(
                self.player_sprite.position
            )

            self.player_shot_list.append(new_shot)

    def on_key_release(self, key, modifiers):
        """
        Called whenever a key is released.
        """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

        if key == arcade.key.W:
            self.tank_forward_pressed = False
        if key == arcade.key.S:
            self.tank_backward_pressed = False
        if key == arcade.key.A:
            self.tank_left_pressed = False
        if key == arcade.key.D:
            self.tank_right_pressed = False

    def on_joybutton_press(self, joystick, button_no):
        print("Button pressed:", button_no)
        # Press the fire key
        self.on_key_press(FIRE_KEY, [])

    def on_joybutton_release(self, joystick, button_no):
        print("Button released:", button_no)

    def on_joyaxis_motion(self, joystick, axis, value):
        print("Joystick axis {}, value {}".format(axis, value))

    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        print("Joystick hat ({}, {})".format(hat_x, hat_y))


def main():
    """
    Main method
    """

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
