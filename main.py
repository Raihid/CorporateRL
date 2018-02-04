#!/usr/bin/env python
"""This module implements the CorporateRL game. Have fun!"""
import curses

import entities
import interface
import levels
from misc import debug


DIRECTIONS = {"KEY_DOWN": (1, 0),
              "KEY_UP": (-1, 0),
              "KEY_RIGHT": (0, 1),
              "KEY_LEFT": (0, -1),

              "h": (0, -1),
              "v": (1, -1),
              "j": (1, 0),
              "n": (1, 1),
              "l": (0, 1),
              "u": (-1, 1),
              "k": (-1, 0),
              "y": (-1, -1)}


class Game:
    """Class representing the game object, the main part of the program"""

    def __init__(self):
        """Prepares for the first launch"""
        self.interface = None
        self.level_num = 0
        self.current_level = None
        self.player = entities.Player(0, 0)

    def prepare_game(self, stdscr):
        """Sets up the interface and the first level."""
        self.interface = interface.Interface(stdscr)
        self.descend()

    def main_loop(self, stdscr):
        """The main loop of the game - taktakes player input and calculates the
        world's response."""
        self.prepare_game(stdscr)

        while self.player.hp > 0:
            self.world_tick()
            self.check_world_status()
            self.draw()
            self.handle_player_action()

    def descend(self):
        """Handles descending - creates new level and resets player's character
        statistics"""

        self.level_num += 1
        self.current_level = levels.Level(self.level_num, self.player)
        entrance = self.current_level.entrance
        self.player.move(entrance.y, entrance.x)
        self.player.reset()

    def farewell(self):
        """Prints a goodbye message after game over."""
        print("Sorry, you died. Better luck next time!")

    @property
    def status(self):
        """Creates status message for the status bar

        Returns:
            String containing the status.
        """
        level_num = self.current_level.level_num
        return "HP: {}/{}\tBombs: {}\tLevel: {}".format(
            self.player.hp, self.player.max_hp,
            self.player.bombs_n, level_num)

    def draw(self):
        """Draws the whole game screen."""
        self.current_level.draw(self.interface)
        self.interface.set_player_status(self.status)
        self.interface.refresh_and_center(self.player.y, self.player.x)

    def handle_player_action(self):
        """Gets user input from the interface module and tries to interpret it.
        In case of failure it waits for another input."""
        handled = False
        while not handled:
            user_input = self.interface.get_user_input()
            handled = self.interpret_input(user_input)

    def interpret_input(self, user_input):
        """Reacts to user input.

        Args:
            user_input: string containing the user input (representing one
            press).
        Returns:
            Boolean representing if the interpretation was succesful.
        """

        interpreted = True
        if user_input in DIRECTIONS.keys():
            direction = DIRECTIONS[user_input]
            new_pos = (self.player.y + direction[0],
                       self.player.x + direction[1])
            tile = self.current_level.get_tile(new_pos)

            if tile is None:
                return True

            if isinstance(tile, entities.Entity):
                # Fight implementation
                monster = tile
                monster.hp -= self.player.damage()

            if tile.walkable:
                self.interface.msg("We're walking!")
                self.player.move_relative(*direction)

        elif user_input is " ":
            if self.player.bombs_n > 0:
                self.current_level.put_bomb(self.player.y, self.player.x)
                self.player.bombs_n -= 1
            else:
                self.interface.msg("You don't have anymore bombs!")

        elif user_input is ">":
            tile = self.current_level.grid[self.player.y][self.player.x]
            if isinstance(tile, levels.Stairs) and tile.axis == 1:
                self.descend()
            else:
                self.interface.msg("You can't descend here!")
        else:
            interpreted = False
            self.interface.msg("I don't understand what you want me to do")

        return interpreted

    def check_world_status(self):
        """Looks for bombs and dead creatures and handles them accordingly."""
        bombs = [entity for entity in self.current_level.creatures
                 if isinstance(entity, entities.Bomb)]

        for bomb in bombs:
            if bomb.time_till_blow <= 0:
                self.current_level.explosion(bomb)

        for idx, creature in enumerate(self.current_level.creatures):
            if creature.hp <= 0:
                del self.current_level.creatures[idx]

    def world_tick(self):
        """Simulates the world reaction - mainly NPCs behavior."""
        self.current_level.tick()

        for creature in self.current_level.creatures:
            if isinstance(creature, entities.Player):
                continue
            room = self.current_level.grid[creature.y][creature.x]
            visible_entities = [entity for entity
                                in self.current_level.creatures
                                if entity in room]
            new_y, new_x = creature.make_action(visible_entities)

            tile = self.current_level.get_tile((new_y, new_x))

            if tile is None:
                continue

            elif isinstance(tile, entities.Player):
                self.player.hp -= creature.damage()

            elif tile.walkable:
                creature.y = new_y
                creature.x = new_x


if __name__ == "__main__":
    game = Game()
    curses.wrapper(game.main_loop)
    game.farewell()
