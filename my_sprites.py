""""
This file includes alle the Sprites used in the game.
"""

import random

import arcade


class Player(arcade.Sprite):
    """
    The player
    """

    def __init__(self, energy, center_x, center_y, max_x, max_y, max_energy, scale=1, fuel=150):

        """
        Setup new Player object
        """

        self.fuel = fuel
        self.coins = 0
        self.max_x = max_x
        self.max_y = max_y
        self.energy = energy
        self.max_energy = max_energy

        # Call init() on the class we inherited from
        super().__init__(
            center_x=center_x,
            center_y=center_y,
            filename="images/sprites/tankBody_sand.png",
            flipped_diagonally=True,
            flipped_horizontally=True,
            flipped_vertically=False,
            scale=scale
        )

    def update(self):
        """
        Move the sprite
        """

        # Update center_x
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Stop moving. Someone else will start me again.
        self.change_x = 0
        self.change_y = 0

        # makes sure energy doesn't go over max
        self.energy = min(self.energy, self.max_energy)
        # makes sure energy doesn't go under zero
        self.energy = max(self.energy, 0)

        # Don't let the player move off screen
        # FIXME: What about the y axis?
        if self.left < 0:
            self.left = 0
        elif self.right > self.max_x - 1:
            self.right = self.max_x - 1

class TireTracks(arcade.Sprite):
    """
    The player
    """

    def __init__(self, target_sprite, scale=1, lifetime_seconds=10):
        """
        Setup new TireTrack object
        """
        self.lifetime_seconds = lifetime_seconds
        self.fade_timer = self.lifetime_seconds

        # Call init() on the class we inherited from
        super().__init__(
            center_x=target_sprite.center_x,
            center_y=target_sprite.center_y,
            angle=target_sprite.angle,
            filename="images/sprites/tracksSmall.png",
            flipped_diagonally=True,
            flipped_horizontally=True,
            flipped_vertically=False,
            scale=scale
        )

    def on_update(self, delta_time):

        # Starts to fade when only half of the lifetime is left
        if self.fade_timer <= self.lifetime_seconds / 2:
            # Makes sure fade_timer doesn't go under 0
            self.fade_timer = max(0, self.fade_timer)
            # Multiplies alpha by time left to make it fade away
            self.alpha *= (self.fade_timer / (self.lifetime_seconds / 2))
        self.fade_timer -= delta_time

        # deletes track if invisible
        if self.alpha <= 0:
            self.kill()


class Canon(arcade.Sprite):

    def __init__(self, target_sprite, rotate_speed, scale=1):

        # canon always locks to a chosen sprite
        self.target_sprite = target_sprite
        self.image = "images/sprites/tankDark_barrel1.png"

        self.canon_rotate_speed = rotate_speed
        # angle relative to target sprite
        self.relative_angle = 0


        super().__init__(
            filename=self.image,
            scale=scale,
            flipped_diagonally=True,
            flipped_horizontally=True,
            flipped_vertically=False
        )

    def on_update(self, delta_time):

        self.position = self.target_sprite.position
        self.angle = self.relative_angle + self.target_sprite.angle

class Coin(arcade.Sprite):

    def __init__(self, max_x, max_y):

        super().__init__(
            center_x=random.randint(1, max_x),
            center_y=random.randint(1, max_y),
            filename="images/sprites/tankSand_barrel3_outline.png"
        )

class Fuel(arcade.Sprite):

    def __init__(self, max_x, max_y):


        super().__init__(
            center_y=random.randint(1,max_x),
            center_x=random.randint(1,max_y),
            filename="images/sprites/barrelRed_side.png"
        )

class Enemy(arcade.Sprite):
    def __init__(self, target_sprite, scale, max_x, max_y, speed):
        self.image = "images/sprites/barrelBlack_top.png"

        self.max_x = max_x
        self.max_y = max_y
        self.speed = speed


        super().__init__(
            filename=self.image,
            scale=scale,
            flipped_diagonally=False,
            flipped_horizontally=True,
            flipped_vertically=False
        )
        self.target_sprite = target_sprite

        self.center_x = random.randint(0, max_x)
        self.center_y = random.randint(0, max_y)

        self.angle = random.randint(0, 360)

    def on_update(self, delta_time):
        """
        Move the sprite
        """
        # makes the enemy follow the player
        self.angle = arcade.get_angle_degrees(
            self.center_x,
            self.center_y,
            self.target_sprite.center_x,
            self.target_sprite.center_y
        )
        # resets change_x and y because .forward() only adjusts change_x and y
        self.stop()
        self.forward(self.speed)
        # get_angle_degrees doesn't give the output we expected but if you swap change_x and change_y it does
        self.change_x, self.change_y = self.change_y, self.change_x

        # Update the position
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        if self.right > self.max_x:
            self.kill()
        elif self.left < 0:
            self.kill()

        if self.bottom > self.max_y:
            self.kill()
        elif self.top < 0:
            self.kill()

class Explosion(arcade.Sprite):
    """
    An animated explosion.
    """

    def __init__(self, position, scale, lifetime=1.0, start_size=0.01):
        type = random.randint(1, 5)

        super().__init__(
            filename=f"images/sprites/explosion{type}.png",
            scale=scale,
        )

        self.position = position
        self.lifetime = lifetime
        self.start_size = start_size

    def on_update(self, delta_time: float = 1 / 60):
        self.scale = self.lifetime/delta_time * self.start_size

        self.lifetime -= delta_time

        if self.lifetime <= 0:
            self.kill()

        self.position = position
        self.lifetime = lifetime
        self.start_size = start_size

    def on_update(self, delta_time: float = 1 / 60):
        self.scale = self.lifetime/delta_time * self.start_size

        self.lifetime -= delta_time

        if self.lifetime <= 0:
            self.kill()
        
class PlayerShot(arcade.Sprite):
    """
    A shot fired by the Player
    """

    def __init__(self, position, angle, speed, scale=1):
        """
        Setup new PlayerShot object
        """

        # Set the graphics to use for the sprite
        # We need to flip it so it matches the mathematical angle/direction
        super().__init__(
            filename="images/sprites/bulletSand1.png",
            scale=scale,
            flipped_diagonally=True,
            flipped_horizontally=True,
            flipped_vertically=False
        )

        # Shoot points in this direction
        self.angle = angle

        # Shoot spawns/starts here
        self.position = position

        # Shot moves forward
        self.forward(speed)


    def update(self):
        """
        Move the sprite
        """

        # Update the position
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Remove shot when over top of screen
        # if self.bottom > SCREEN_HEIGHT:
        #    self.kill()


class LifeBar(arcade.Sprite):
    """

    """

    def __init__(self, target_sprite, max_energy, size_multiplier=1, height=20, y_offset=30):
        self.target_sprite = target_sprite
        self.max_energy = max_energy
        self.size_multiplier = size_multiplier
        self.bar_height = height
        self.y_offset = y_offset

        super().__init__(
            scale=0,
            flipped_diagonally=True,
            flipped_horizontally=True,
            flipped_vertically=False
        )

    def draw(self):

        x = self.target_sprite.center_x
        y = self.target_sprite.center_y + self.y_offset
        h = self.bar_height * self.size_multiplier

        # draws a red rectangle behind the dynamic green rectangle
        arcade.draw_rectangle_filled(
            center_x=x,
            center_y=y,
            width=self.max_energy * self.size_multiplier,
            height=h,
            color=arcade.color.RED
        )

        # draws a rectangle that scales its width with the amount of energy
        arcade.draw_rectangle_filled(
            center_x=x + (self.target_sprite.energy / 2 - (self.max_energy / 2)) * self.size_multiplier,
            center_y=y,
            width=self.target_sprite.energy * self.size_multiplier,
            height=h,
            color=arcade.color.GREEN
        )

