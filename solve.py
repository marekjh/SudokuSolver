from copy import copy, deepcopy
import sys

N = 9  # Should be a square number
M = int(N**0.5)

def main():
    if len(sys.argv) < 2:
        print("Supply path to grid")
        return
    
    puzzle = read_file(sys.argv[1])
    sol = solve(set_puzzle(puzzle))
    for row in sol:
        print(row)

def solve(puzzle):
    remaining = set()
    for i in range(N):
        remaining = remaining.union({(i, j) for j in range(N)})
    return solve_helper(puzzle, remaining)

def solve_helper(puzzle, remaining):
    grid = split_grid()
    while True:
        for move in (naked_single, hidden_single):
            deduction = move(puzzle, remaining, grid)
            if len(remaining) == 0:
                return puzzle
            if deduction:
                break
        else:
            for space in remaining:
                i, j = space
                candidates = puzzle[i][j]
                for n in candidates:
                    puzzle[i][j] = {n}
                    try:
                        sol = solve_helper(deepcopy(puzzle), copy(remaining))
                    except NoSolution:
                        sol = None
                    if sol is not None:
                        return sol
            return None     # Puzzle has no solution

def update_candidates(puzzle, remove, i, j):
    removed = puzzle[i][j].intersection(remove)
    puzzle[i][j] -= remove
    if len(puzzle[i][j]) == 0:
        raise NoSolution
    return len(removed) > 0

def naked_single(puzzle, spaces, grid):
    remove = set()
    updated = False
    for i, j in spaces:
        if len(puzzle[i][j]) == 1:
            remove.add((i, j))
            for chunk in (grid["rows"][i] - {(i, j)}, grid["cols"][j] - {(i, j)}, grid["blocks"][i//M][j//M] - {(i, j)}):
                for x, y in chunk:
                    check = update_candidates(puzzle, puzzle[i][j], x, y) 
                    if not updated:
                        updated = check
    spaces -= remove
    return updated

def hidden_single(puzzle, spaces, grid):
    updated = False
    for i, j in spaces:
        for chunk in (grid["rows"][i] - {(i, j)}, grid["cols"][j] - {(i, j)}, grid["blocks"][i//M][j//M] - {(i, j)}):
            candidates = set()
            for x, y in chunk:
                candidates = candidates.union(puzzle[x][y])
            candidate = puzzle[i][j] - candidates
            if len(candidate) == 1:
                puzzle[i][j] = candidate
                updated = True
                break
    return updated

def set_puzzle(puzzle):
    for i, row in enumerate(puzzle):
        for j, e in enumerate(row):
            if e:
                puzzle[i][j] = {e}
            else:
                puzzle[i][j] = {x for x in range(1, N+1)}
    return puzzle

def split_grid():
    rows = [{(i, j) for j in range(N)} for i in range(N)]
    cols = [{(i, j) for i in range(N)} for j in range(N)]
    blocks = [] 
    for i in range(M):
        row = []
        for j in range(M):
            spaces = set()
            for k in range(M):
                spaces = spaces.union({(i*M + k, j*M + l) for l in range(M)})
            row.append(spaces)
        blocks.append(row)
    return {"rows": rows, "cols": cols, "blocks": blocks}

def read_file(file):
    with open(file, "r") as f:
        lines = [x.strip() for x in f.readlines()]
    return [[10 + ord(x) - ord("a") if x.isalpha() else int(x) for x in list(y)] for y in lines]
 
class NoSolution(Exception):
    pass

if __name__ == "__main__":  
    main()
