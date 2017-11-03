def flood_fill(arr, coords, base_mark, mark):
    x, y = coords
    if arr[y][x] != base_mark:
        return None
    else:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                x += dx
                y += dy
                flood_fill(arr, (x, y), base_mark, mark)
    return arr
