import sys


def build_units(n, box):
    """Return the list of units (rows, columns, boxes) and each cell's peers."""
    units = []
    for r in range(n):
        units.append([r * n + c for c in range(n)])
    for c in range(n):
        units.append([r * n + c for r in range(n)])
    for br in range(0, n, box):
        for bc in range(0, n, box):
            units.append([(br + r) * n + (bc + c)
                          for r in range(box) for c in range(box)])

    cell_units = [[] for _ in range(n * n)]
    for u in units:
        for cell in u:
            cell_units[cell].append(u)

    peers = []
    for cell in range(n * n):
        p = set()
        for u in cell_units[cell]:
            p.update(u)
        p.discard(cell)
        peers.append(list(p))
    return units, peers


def popcount(x):
    return bin(x).count("1")


def assign(domains, cell, bit, peers):
    """Assign a value (as a bit) to a cell and remove it from all peers.
    Returns False if a contradiction is found."""
    domains[cell] = bit
    for p in peers[cell]:
        if domains[p] & bit:
            domains[p] &= ~bit
            if domains[p] == 0:
                return False
    return True


def propagate(domains, assigned, units, peers, n):
    """Repeatedly apply naked singles and hidden singles until nothing changes."""
    changed = True
    while changed:
        changed = False

        # Naked singles: a cell with only one possible value
        for cell in range(n * n):
            if not assigned[cell] and popcount(domains[cell]) == 1:
                assigned[cell] = True
                if not assign(domains, cell, domains[cell], peers):
                    return False
                changed = True

        # Hidden singles: a value that fits in only one cell of a unit
        for u in units:
            for v in range(n):
                bit = 1 << v
                spots = [c for c in u if domains[c] & bit]
                if not spots:
                    return False
                if len(spots) == 1:
                    c = spots[0]
                    if not assigned[c]:
                        assigned[c] = True
                        if not assign(domains, c, bit, peers):
                            return False
                        changed = True
    return True


def backtrack(domains, assigned, units, peers, n):
    """Backtracking search with MRV and constraint propagation."""
    if not propagate(domains, assigned, units, peers, n):
        return None

    # MRV: choose the unassigned cell with the fewest possible values
    best, best_count = -1, n + 1
    for cell in range(n * n):
        if not assigned[cell]:
            cnt = popcount(domains[cell])
            if cnt < best_count:
                best, best_count = cell, cnt
                if cnt == 2:
                    break
    if best == -1:
        return domains  # every cell assigned -> solved

    d = domains[best]
    while d:
        bit = d & -d
        d &= d - 1
        new_domains = domains[:]
        new_assigned = assigned[:]
        new_assigned[best] = True
        if assign(new_domains, best, bit, peers):
            result = backtrack(new_domains, new_assigned, units, peers, n)
            if result is not None:
                return result
    return None


def solve(values, n):
    box = int(round(n ** 0.5))
    units, peers = build_units(n, box)
    full = (1 << n) - 1
    domains = [full] * (n * n)
    assigned = [False] * (n * n)

    for cell, v in enumerate(values):
        if v != 0:
            bit = 1 << (v - 1)
            if not domains[cell] & bit:
                return None
            assigned[cell] = True
            if not assign(domains, cell, bit, peers):
                return None

    result = backtrack(domains, assigned, units, peers, n)
    if result is None:
        return None
    return [d.bit_length() for d in result]


def read_values(count):
    """Read numbers until we have `count` of them (allows one or many lines)."""
    values = []
    while len(values) < count:
        line = input()
        values.extend(int(tok) for tok in line.split())
    return values[:count]


def main():
    print("Welcome to the Sudoku Solver!")
    sizes = {"4x4": 4, "9x9": 9, "16x16": 16}

    print("Enter a size (4x4, 9x9, 16x16):")
    size_text = input().strip().lower().replace(" ", "")
    while size_text not in sizes:
        print("Invalid size. Enter a size (4x4, 9x9, 16x16):")
        size_text = input().strip().lower().replace(" ", "")
    n = sizes[size_text]

    print("Enter the values (a blank is represented by a 0):")
    values = read_values(n * n)

    solution = solve(values, n)
    if solution is None:
        print("No solution exists.")
        return

    print("The solution is")
    for r in range(n):
        print(" ".join(str(solution[r * n + c]) for c in range(n)))


if __name__ == "__main__":
    main()