
import sys
import heapq
import collections


# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]
INF = 10 ** 9

def _get_input() -> list[list[str]]:
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]

def _get_neighbours(i, j, data):
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    for d in directions:
        newI, newJ = i + d[0], j + d[1]
        if newI < 0 or newI >= len(data) or newJ < 0 or newJ >= len(data[0]):
            continue
        if data[newI][newJ] != '#':
            yield newI, newJ

def _bfs(data: list[list[str]], start_position: tuple[int, int]) \
    -> list[tuple[int, int, int, int]]:
    result = list()
    i, j = start_position
    deque = collections.deque()
    deque.append((i, j, 0, 0))
    visited = set()
    while deque:
        i, j, dist, mask_door = deque.pop()
        visited.add((i, j))
        if data[i][j] in keys_char and (i, j) != start_position:
            result.append((i, j, dist, mask_door))
        for neighbour in _get_neighbours(i, j, data):
            if neighbour not in visited:
                next_i, next_j = neighbour
                if data[next_i][next_j] in doors_char:
                    mask_door |= (1 << doors_char.index(data[next_i][next_j]))
                deque.append((next_i, next_j, dist + 1, mask_door))
    return result


def _get_graph(data: list[list[str]], positions: list[tuple[int, int]]) \
    -> dict[tuple[int, int], list[tuple[int, int, int, int]]]:
    graph = dict()
    for pos in positions:
        graph[pos] = _bfs(data, pos)
    return graph

def _has_key_for_door(mask_keys: int, mask_door: int) -> bool:
    return mask_keys == (mask_keys | mask_door)


def _get_positions(data):
    height, width = len(data), len(data[0])
    robot_positions, key_positions = list(), list()
    robot_index = 0
    for i in range(height):
        for j in range(width):
            c = data[i][j]
            if c == '@':
                robot_positions.append((i, j))
                data[i][j] = f'r{robot_index}'
                robot_index += 1
            elif c in keys_char:
                key_positions.append((i, j))
    return robot_positions,key_positions

def _get_mask(key: str) -> int:
    return 1 << keys_char.index(key)

def solve(data: list[list[str]]) -> int:
    robot_positions, key_positions = _get_positions(data)
    positions = robot_positions + key_positions
    graph = _get_graph(data, positions)

    start_positions = tuple(robot_positions)
    mask_all_key = (1 << len(key_positions)) - 1
    key_index = _build_key_index(data, key_positions)
    heap_state = [(0, start_positions, 0)]
    best_dist = {(start_positions, 0): 0}
    
    while heap_state:
        current_distation, current_positions, mask_key = heapq.heappop(heap_state)
        if best_dist[(current_positions, mask_key)] < current_distation:
            continue
        if mask_key == mask_all_key:
            return current_distation
        for robot_index, robot_pos in enumerate(current_positions):
            for nextI, nextJ, nextDist, mask_door in graph[robot_pos]:
                if (nextI, nextJ) not in key_index:
                    continue
                if mask_key & key_index[(nextI, nextJ)]:
                    continue
                if not _has_key_for_door(mask_key, mask_door):
                    continue
                
                new_positions = _change_robot_positions(current_positions, robot_index, nextI, nextJ)
                new_mask = mask_key | key_index[(nextI, nextJ)]
                new_dist = current_distation + nextDist
                new_state = (new_positions, new_mask)
                if new_dist < best_dist.get(new_state, INF):
                    best_dist[new_state] = new_dist
                    heapq.heappush(heap_state, (new_dist, new_positions, new_mask))
    return -1

def _change_robot_positions(current_positions, robot_index, nextI, nextJ):
    new_positions = list(current_positions)
    new_positions[robot_index] = (nextI, nextJ)
    new_positions = tuple(new_positions)
    return new_positions

def _build_key_index(data, key_positions):
    key_index = dict()
    for pos in key_positions:
        key_index[pos] = _get_mask(data[pos[0]][pos[1]])
    return key_index

                            
def main():
    data = _get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()