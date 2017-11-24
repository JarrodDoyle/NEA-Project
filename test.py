from map_generation.cellular_automata import Dungeon_Cellular_Automata
import os

while True:
    os.system("cls")
    num_steps = int(input("Num steps: "))
    dungeon = Dungeon_Cellular_Automata(96, 64, 4, 3, 5, num_steps)
    #dungeon.initialize_dungeon()
    #for i in range(num_steps):
        #dungeon.simulate_step()
    #dungeon.connect_rooms()
    #dungeon.convert_dungeon()
    player, entity_list = dungeon.gen_dungeon()
    dungeon.display_dungeon(entity_list)
    input()
