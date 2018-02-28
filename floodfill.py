# Recursive flood fill algorithm
def flood_fill(arr, coords, base_mark, mark):
    base_x, base_y = coords
    arr[base_y][base_x] = mark
    # Check above and below
    for dy in [-1, 1]:
        new_y = base_y + dy
        # If new y value is within the dungeon floor boundaries and it is equal to the base mark
        if new_y in range(0, len(arr)) and arr[new_y][base_x] == base_mark:
            flood_fill(arr, (base_x, new_y), base_mark, mark)
    # Check left and right
    for dx in [-1, 1]:
        new_x = base_x + dx
        # If new x value is within the dungeon floor boundaries and it is equal to the base mark
        if new_x in range(0, len(arr[0])) and arr[base_y][new_x] == base_mark:
            flood_fill(arr, (new_x, base_y), base_mark, mark)
