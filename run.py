import json
from collections import defaultdict

def check_capacity(max_capacity: int, guests: list) -> bool:
    resulting_capacity_table = _get_resulting_capacity_table(guests)
    resulting_capacity_table_items_sorted = sorted(resulting_capacity_table.items())
    current_capacity = 0
    for _, result_capacity in resulting_capacity_table_items_sorted:
        current_capacity += result_capacity
        if current_capacity > max_capacity:
            return False
    return True

def _get_resulting_capacity_table(guests: list) -> defaultdict[str, int]:
    resulting_capacity_table: defaultdict[str, int] = defaultdict(int)
    for guest in guests:
        check_in = guest['check-in']
        check_out = guest['check-out']
        resulting_capacity_table[check_in] += 1
        resulting_capacity_table[check_out] -= 1
    return resulting_capacity_table


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)


    result = check_capacity(max_capacity, guests)
    print(result)