from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
current_path = []
opposites = {"n": "s", "e": "w", "s": "n", "w": "e"}
visited_rooms = set()

s = Stack()

s.push(player.current_room)

while s.size() > 0:
    current_room = s.pop()
    target_room = None
    last_moved_direction = None

    # mark the current room visited
    visited_rooms.add(current_room.id)

    # loop through the exits of the current room
    for exit in current_room.get_exits():
        # check if the room each exit leads to has been visited
        room_in_direction = current_room.get_room_in_direction(exit)

        if room_in_direction.id not in visited_rooms:
            last_moved_direction = exit
            target_room = room_in_direction

    if last_moved_direction is not None:
        current_path.append(last_moved_direction)
        traversal_path.append(last_moved_direction)

    prev_room = current_room
    while target_room is None and len(current_path) > 0:
        last_direction = current_path.pop()
        backtrack_direction = opposites[last_direction]

        prev_room = prev_room.get_room_in_direction(backtrack_direction)
        traversal_path.append(backtrack_direction)

        for exit in prev_room.get_exits():
            room_in_direction = prev_room.get_room_in_direction(exit)

            if room_in_direction.id not in visited_rooms:
                target_room = prev_room

    if target_room is not None:
        s.push(target_room)
    else:
        print("no more unexplored paths down this road.")

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
