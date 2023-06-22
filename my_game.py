"""
Simple program to show moving a sprite with the keyboard.

This program uses the Arcade library found at http://arcade.academy

Artwork from https://kenney.nl/assets/space-shooter-redux

"""
import random
import arcade

from my_sprites import Player, PlayerShot, Enemy, Explosion, Canon, Coin, Fuel, TireTracks, LifeBar



SPRITE_SCALING = 1

# Set the size of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Variables controlling the player
PLAYER_LIVES = 3
PLAYER_SPEED = 5
PLAYER_TURN_SPEED = 5
PLAYER_START_X = SCREEN_WIDTH / 2
PLAYER_START_Y = 50
PLAYER_KEY_LEFT = arcade.key.LEFT
PLAYER_KEY_RIGHT = arcade.key.RIGHT
PLAYER_KEY_FORWARD = arcade.key.UP
PLAYER_KEY_BACKWARDS = arcade.key.DOWN
PLAYER_START_ENERGY = 200
PLAYER_MAX_ENERGY = 200

#variables controlling the player_shot
PLAYER_SHOT_SPEED = 25


# variables controlling the canon
CANON_ROTATE_SPEED = 5
CANON_KEY_LEFT = arcade.key.A
CANON_KEY_RIGHT = arcade.key.D

# variables controlling the enemy
BASE_NUMBER_OF_ENEMYS = 10

# variables controlling the enemies
ENEMY_MOVE_SPEED = 16

# variables controlling the tire-
TIRETRACK_LIFETIME_SECONDS = 10

FIRE_KEY = arcade.key.SPACE

ENERGY_GUI_SIZE_MULTIPLIER = 0.5

# variables controling the coin
COIN_SPAWN_TIMER = 10
START_COINS = 0

# variables controling the fuel
FUEL_SPAWN_TIMER = 10
START_FUEL = 200
FUEL_INCREMENT = 25
FUEL_SPEED_FACTOR = 0.01

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
        self.player_shot_list = None

        # Set up the player info
        self.player_sprite = None
        self.player_score = None
        self.player_lives = None

        # A list of connected joysticks for player control
        self.player_joysticks = []

        self.wave_number = 0

        # Track the current state of what key is pressed
        self.player_left_pressed = False
        self.player_right_pressed = False
        self.player_forward_pressed = False
        self.player_backwards_pressed = False

        self.canon_left_pressed = False
        self.canon_right_pressed = False

        # LifeBar Variables
        self.life_bar_list = None

        # the time for the coin spawn
        self.coin_timer = COIN_SPAWN_TIMER
        self.fuel_timer = FUEL_SPAWN_TIMER

        # Get list of joysticks
        joysticks = arcade.get_joysticks()

        if joysticks:
            print("Found {} joystick(s)".format(len(joysticks)))

            if len(joysticks) >= 1:
              self.player_joysticks.append(joysticks[0])

            if len(joysticks) >= 2:
              self.player_joysticks.append(joysticks[1])

            # Setup joysticks
            for j in self.player_joysticks:
                # Open communication
                j.open()
                # Map joystick functions. on_joynutton_XX
                j.push_handlers(self)

        else:
            print("No joysticks found")


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
        self.enemy_sprite_list = arcade.SpriteList()
        self.explosion_sprite_list = arcade.SpriteList()
        self.coin_sprite_list = arcade.SpriteList()
        self.fuel_sprite_list = arcade.SpriteList()
        self.tire_track_list = arcade.SpriteList()
        self.life_bar_list = arcade.SpriteList()

        # Create a Player object
        self.player_sprite = Player(
            energy=PLAYER_START_ENERGY,
            center_x=PLAYER_START_X,
            center_y=PLAYER_START_Y,
            max_x=SCREEN_WIDTH,
            max_y=SCREEN_HEIGHT,
            max_energy=PLAYER_MAX_ENERGY,

            scale=SPRITE_SCALING,
            fuel=START_FUEL
        )

        self.canon_sprite = Canon(
            target_sprite=self.player_sprite,
            rotate_speed=CANON_ROTATE_SPEED,
            scale=SPRITE_SCALING
            )

        # start wave_number
        self.wave_number = self.start_new_wave(0)

        # Create a LifeBar for the player and append it to the spritelist
        l = LifeBar(
            target_sprite=self.player_sprite,
            max_energy=PLAYER_MAX_ENERGY
        )

        self.life_bar_list.append(l)


    def start_new_wave(self, wave_no):
        """
        creates new enemies on the screan
        """
        for i in range(BASE_NUMBER_OF_ENEMYS + wave_no):
            e = Enemy(
                max_x=SCREEN_WIDTH,
                max_y=SCREEN_HEIGHT,
                speed=ENEMY_MOVE_SPEED,
                scale=SPRITE_SCALING,
                target_sprite=self.player_sprite
            )
            self.enemy_sprite_list.append(e)

        return wave_no + 1

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the Tire Tracks
        self.tire_track_list.draw()

        # Draw the player shot
        self.player_shot_list.draw()
        self.explosion_sprite_list.draw()

        # Draw the player sprite
        self.player_sprite.draw()

        # Draw the canon
        self.canon_sprite.draw()

        # Draw coins
        self.coin_sprite_list.draw()

        # Draw fuel
        self.fuel_sprite_list.draw()

        # Draw the enemy
        self.enemy_sprite_list.draw()

        # Draw players score on screen
        arcade.draw_text(
            "SCORE: {}".format(self.player_score),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 20,  # Y position
            arcade.color.WHITE   # Color of text
        )

        # Draw players fuel on screen
        arcade.draw_text(
            "fuel: {}".format(int(self.player_sprite.fuel)),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 40,  # Y position
            arcade.color.WHITE   # Color of text
        )

        # Draw players coins on screen
        arcade.draw_text(
            "COINS: {}".format(self.player_sprite.coins),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 60,  # Y position
            arcade.color.WHITE   # Color of text
        )
        for lifebar in self.life_bar_list:
            lifebar.draw()



        # Draw players fuel on screen
        arcade.draw_text(
            "fuel: {}".format(int(self.player_sprite.fuel)),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 40,  # Y position
            arcade.color.WHITE   # Color of text
        )

        # Draw players coins on screen
        arcade.draw_text(
            "COINS: {}".format(self.player_sprite.coins),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 60,  # Y position
            arcade.color.WHITE   # Color of text
        )



    def on_update(self, delta_time):
        """
        Movement and game logic
        """

        # Timer for coin spawn
        if self.coin_timer <= 0:
            self.coin_sprite_list.append(Coin(SCREEN_WIDTH, SCREEN_HEIGHT))
            self.coin_timer = COIN_SPAWN_TIMER
        self.coin_timer -= delta_time

        # Timer for fuel spawn
        if self.fuel_timer <= 0:
            self.fuel_sprite_list.append(Fuel(SCREEN_WIDTH, SCREEN_HEIGHT))
            self.fuel_timer = FUEL_SPAWN_TIMER
        self.fuel_timer -= delta_time

        # fuel loss
        if self.player_forward_pressed or self.player_backwards_pressed:
            # looses fuel the more fuel you have
            self.player_sprite.fuel -= delta_time * self.player_sprite.fuel / 100

        # insure fuel is between 0 and 20
        self.player_sprite.fuel = max(40, self.player_sprite.fuel)
        self.player_sprite.fuel = min(100, self.player_sprite.fuel)

        # Append new tire tracks randomly
        if self.player_forward_pressed or self.player_backwards_pressed:
            if random.randint(1, 5) == 1:
                self.tire_track_list.append(TireTracks(target_sprite=self.player_sprite, lifetime_seconds=TIRETRACK_LIFETIME_SECONDS))

        # Calculate player speed based on the keys pressed
        self.player_sprite.change_x = 0

        # Move player with keyboard
        if self.player_left_pressed and not self.player_right_pressed:
            self.player_sprite.angle += PLAYER_TURN_SPEED
        if self.player_right_pressed and not self.player_left_pressed:
            self.player_sprite.angle += -PLAYER_TURN_SPEED
        if self.player_forward_pressed and not self.player_backwards_pressed:
            self.player_sprite.forward(PLAYER_SPEED * (FUEL_SPEED_FACTOR * self.player_sprite.fuel))
        if self.player_backwards_pressed and not self.player_forward_pressed:
            self.player_sprite.forward(-PLAYER_SPEED * (FUEL_SPEED_FACTOR * self.player_sprite.fuel))

        # Move player with joystick if present
        # FIXME: Add players to a list and use i below
        for i in range(len(self.player_joysticks)):
            if round(self.player_joysticks[i].x) == -1:
                self.player_sprite.angle += PLAYER_TURN_SPEED
            if round(self.player_joysticks[i].x) == 1:
                self.player_sprite.angle -= PLAYER_TURN_SPEED

        # Update the sprites
        self.player_sprite.update()
        self.tire_track_list.on_update(delta_time)
        self.player_shot_list.update()
        self.explosion_sprite_list.on_update(delta_time)
        self.enemy_sprite_list.on_update(delta_time)
        self.canon_sprite.on_update(delta_time)

        if self.canon_left_pressed:
            self.canon_sprite.relative_angle += 5
        elif self.canon_right_pressed:
            self.canon_sprite.relative_angle -= 5

        # checks for collisions between the player_shot and enemy sprite
        for e in self.enemy_sprite_list:
            for s in self.player_shot_list:
                if arcade.check_for_collision(e, s):
                    e.kill()
                    s.kill()
                    self.explosion_sprite_list.append(
                        Explosion(position=e.position,scale=SPRITE_SCALING)
                        )
                    self.player_sprite.coins += 1

        # checks for collisions between the player_sprite and coins
        for c in self.coin_sprite_list:
            if arcade.check_for_collision(c, self.player_sprite):
                c.kill()
                self.player_sprite.coins += 10

        # checks for collisions between the player_sprite and fuel
        for f in self.fuel_sprite_list:
            if arcade.check_for_collision(f, self.player_sprite):
                f.kill()
                self.player_sprite.fuel += FUEL_INCREMENT

        # loses life if you touch enemy
        for e in self.enemy_sprite_list:
            if arcade.check_for_collision(e, self.canon_sprite):
                self.player_sprite.energy -= 1

        # checks if the level has ended
        if len(self.enemy_sprite_list) <= 0:
            self.wave_number = self.start_new_wave(self.wave_number)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        # Track state of arrow keys for the player
        if key == PLAYER_KEY_FORWARD:
            self.player_forward_pressed = True
        elif key == PLAYER_KEY_BACKWARDS:
            self.player_backwards_pressed = True
        elif key == PLAYER_KEY_LEFT:
            self.player_left_pressed = True
        elif key == PLAYER_KEY_RIGHT:
            self.player_right_pressed = True

        if key == FIRE_KEY:
            new_shot = PlayerShot(
                position=self.player_sprite.position,
                angle=self.canon_sprite.angle,
                speed=PLAYER_SPEED,
                scale=SPRITE_SCALING
            )

            self.player_shot_list.append(new_shot)

        # Track state of arrow keys for the canon
        if key == CANON_KEY_LEFT:
            self.canon_left_pressed = True
        elif key == CANON_KEY_RIGHT:
            self.canon_right_pressed = True

    def on_key_release(self, key, modifiers):
        """
        Called whenever a key is released.
        """

        # player
        if key == arcade.key.UP:
            self.player_forward_pressed = False
        elif key == arcade.key.DOWN:
            self.player_backwards_pressed = False
        elif key == arcade.key.LEFT:
            self.player_left_pressed = False
        elif key == arcade.key.RIGHT:
            self.player_right_pressed = False

        # canon
        if key == CANON_KEY_LEFT:
            self.canon_left_pressed = False
        elif key == CANON_KEY_RIGHT:
            self.canon_right_pressed = False


    def on_joybutton_press(self, joystick, button_no):
        print("Button pressed:", button_no, joystick)
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
