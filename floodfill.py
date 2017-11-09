def flood_fill(arr, coords, base_mark, mark):
    base_x, base_y = coords
    arr[base_y][base_x] = mark
    for dy in [-1, 1]:
        new_y = base_y + dy
        if new_y in range(0, len(arr)) and arr[new_y][base_x] == base_mark:
            flood_fill(arr, (base_x, new_y), base_mark, mark)
    for dx in [-1, 1]:
        new_x = base_x + dx
        if new_x in range(0, len(arr[0])) and arr[base_y][new_x] == base_mark:
            flood_fill(arr, (new_x, base_y), base_mark, mark)
            
