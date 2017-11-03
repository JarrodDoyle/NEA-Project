from map_generation.cellular_automata import Dungeon_Cellular_Automata
import os

while True:
    os.system("cls")
    num_steps = int(input("Num steps: "))
    dungeon = Dungeon_Cellular_Automata(10, 10, 4, 3, 45)
    dungeon.initialize_dungeon()
    for i in range(num_steps):
        dungeon.simulate_step()
    print()
    dungeon.display_dungeon()
    dungeon.check_connectivity()
    dungeon.display_dungeon()
    input()
