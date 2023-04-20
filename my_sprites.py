""""
This file includes alle the Sprites used in the game.
"""

import random

import arcade


class Player(arcade.Sprite):
    """
    The player
    """

    def __init__(self, center_x, center_y, max_x, max_y, scale=1 ):
        """
        Setup new Player object
        """
        
        self.max_x = max_x
        self.max_y = max_y

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

        # Don't let the player move off screen
        # FIXME: What about the y axis?
        if self.left < 0:
            self.left = 0
        elif self.right > self.max_x - 1:
            self.right = self.max_x - 1

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

class Coins(arcade.Sprite):

    def __init__(self):


        super().__init__(
            center_y=random.randint(1,600),
            center_x=random.randint(1,800),
            filename="images/sprites/tankSand_barrel3_outline.png"
        )

class Enemy(arcade.Sprite):

    def __init__(self, max_x, max_y, speed, scale=1):

        super().__init__(
            filename="images/sprites/barrelBlack_top.png",
            scale=scale,
            flipped_diagonally=False,
            flipped_horizontally=True,
            flipped_vertically=False
        )

        self.center_x = random.randint(0, max_x)
        self.center_y = random.randint(0, max_y)

        self.angle = random.randint(0, 360)
        self.forward(speed)

    def update(self):
        """
        Move the sprite
        """

        # Update the position
        self.center_x += self.change_x
        self.center_y += self.change_y


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
        #if self.bottom > SCREEN_HEIGHT:
        #    self.kill()
