#!/usr/bin/env python
import curses

import entities
import interface
import levels
import misc
from misc import debug


directions = {"h": (0, -1),
              "v": (1, -1),
              "j": (1, 0),
              "n": (1, 1),
              "l": (0, 1),
              "u": (-1, 1),
              "k": (-1, 0),
              "y": (-1, -1)}

# Wymyslic mape 
# Niech interfejs rysuje wszystko 
class Game:
    def __init__(self):
        self.player = entities.Player(0, 0)
        self.interface = None

    def prepare_game(self, stdscr):
        self.current_level = levels.Level(level_num=1, player=self.player)
        self.interface = interface.Interface(stdscr)
        self.player.move(*self.current_level.entrance)
        self.current_level.draw(self.interface)
    
    def main_loop(self, stdscr):
        self.prepare_game(stdscr)

        while True:
            self.world_tick()
            self.check_world_status()
            self.handle_player_action()
            self.draw()

    @property
    def status(self):
        level_num = self.current_level.level_num
        return "HP: 10/10\tMP: 10/10\tLevel: {}".format(level_num)

    def draw(self):
        self.current_level.draw(self.interface)
        self.interface.set_player_status(self.status)
        self.interface.refresh_and_center(self.player.y, self.player.x)

    def handle_player_action(self):
        user_input = self.interface.get_user_input()
        self.interpret_input(user_input)

    def interpret_input(self, user_input):
        if user_input in directions.keys():
            direction = directions[user_input]
            new_pos = (self.player.y + direction[0],
                       self.player.x + direction[1]) 
            tile_type = self.current_level.get_tile_type(new_pos)

            if tile_type == "WALL":
                # debug_print("Player has walken into the wall, ignorning")
                pass
            elif tile_type == "WALKABLE":
                self.interface.msg("We're walking!")
                self.player.move_relative(*direction)

            elif tile_type == "MONSTER":
                raise NotImplementedError("Fight hasn't been implemented yet :(")

            else:
                raise NotImplementedError("What")

        else:
            self.interface.msg("I don't understand what you want me to do")

    def check_world_status(self):
        pass

    def world_tick(self):
        self.current_level.tick()
        for creature in self.current_level.creatures:
            debug("Creature;", creature.y, creature.x)
            if isinstance(creature, entities.Player):
                continue
            room = self.current_level.grid[creature.y][creature.x]
            visible_entities = [entity for entity
                                in self.current_level.creatures  
                                if entity in room]
            debug(self.current_level.creatures)
            new_y, new_x = creature.decide_move(visible_entities)
            if not self.current_level.in_bounds(new_y, new_x):
                continue
            try:
                if self.current_level.grid[new_y][new_x].walkable:
                    creature.y = new_y
                    creature.x = new_x
            except IndexError:
                continue

if __name__ == "__main__":
    game = Game()
    curses.wrapper(game.main_loop)
