import random
import os

MAXRANDOMVALUE = 3
MAXPREV = 500

arr = [[0 for _ in range(4)] for _ in range(4)]
score = 0
highscore = 0
count = 0
prev_states = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(MAXPREV + 1)]

def find_len(n):
    return len(str(n)) if n else 0

def print_board():
    global highscore
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\t\t\t\t\t===============2048==============\n")
    print(f"\t\t\t\t\tYOUR SCORE={score}\n\t\t\t\t\t", end="")
    if score < highscore:
        print(f"HIGH SCORE={highscore}\t\t\t\t\t\n")
    else:
        highscore = score
        print(f"HIGH SCORE={highscore}\t\t\t\t\t\n")
    print("\t\t\t\t\t---------------------------------\n")

    for i in range(4):
        for j in range(4):
            print("\t\t\t\t\t|", end="") if j == 0 else None
            if arr[i][j] != 0:
                length = find_len(arr[i][j])
                print(" " * (4 - length) + str(arr[i][j]) + " " * (4 - length) + " " * (length - 1) + "|", end="")
            else:
                print(" " * 7 + "|", end="")
        print() if i != 3 else None
        print("\t\t\t\t\t-------------------------------------\n") if i != 3 else None

    print("\n\t\t\t\t\t---------------------------------\n")
    print("\t\t\t\t\tPREV-> P\t\t\t\t\t\n")
    print("\t\t\t\t\tRESTART-> R\t\t\t\t\t\n")
    print("\t\t\t\t\tEXIT-> U\t\t\t\t\t\n")
    print("\t\t\t\t\tENTER YOUR CHOISE -> W,S,A,D\n\t\t\t\t\t", end="")


def move_value(c):
    new_c = [0] * 4
    idx = 0
    for x in c:
        if x != 0:
            new_c[idx] = x
            idx += 1
    return new_c

def add_random_no():
    empty_cells = [(i, j) for i in range(4) for j in range(4) if arr[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        arr[i][j] = 2 if random.random() < 0.9 else 4  # 90% chance for 2, 10% for 4


def update_row(c):
    global score
    c = move_value(c)
    for i in range(3):
        if c[i] == c[i+1] and c[i] != 0:
            c[i] *= 2
            score += c[i]
            c[i+1] = 0
    return move_value(c)



def create_prev():
    global count
    with open("hstr.txt", "a") as f:
        f.write(str(score) + " ")
    if count == MAXPREV:
        prev_states[:-1] = prev_states[1:]  # Shift states down
        count -=1
    prev_states[count] = [row[:] for row in arr]
    count += 1



def update_arr_to_prev():
    global score, count
    if count == 0:
        print("\n******FURTHER MORE PREV NOT POSSIBLE********")
        return

    with open("hstr.txt", "r") as f:
        scores = [int(s) for s in f.read().split()]
        score = scores[count-1]

    arr[:] = prev_states[count - 1][:]
    count -= 1


def reset_game():
    global arr, score, count
    arr = [[0 for _ in range(4)] for _ in range(4)]
    score = 0
    count = 0
    add_random_no()


def main():
    global highscore, count

    print("===============2048==============\n")
    print("WELCOME TO PUZZLE 2048\n")
    print("> CONTROLS\n")
    print("  FOR MOVES:- 'W','S','A','D'\n")
    print("  GO BACKWARD:- 'P'\n")
    print("  RESTAT THE GAME:- 'R'\n")
    print("  EXIT:-'U'\n")
    input("\nPRESS ANY KEY TO START THE GAME....")
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\n===============2048==============\n")
    print("\nLOADING...\n")
    print("-" * 35)
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        with open("highscore.txt", "r") as f:
            highscore = int(f.read())
    except FileNotFoundError:
        highscore = 0

    try:
        with open("hstr.txt", "w") as f:
            pass
    except Exception as e:
        print(f"Error handling file hstr.txt: {e}")

    add_random_no()
    print_board()

    while True:
        if score > highscore:
            with open("highscore.txt", "w") as f:
                f.write(str(score))

        choice = input().upper()

        if choice in ('D', 'A', 'S', 'W'):
            create_prev()
            original_board = [row[:] for row in arr] #Check if the board changed
            for i in range(4):
                if choice == 'D':
                    arr[i] = update_row(arr[i])
                elif choice == 'A':
                    arr[i] = update_row(arr[i][::-1])[::-1]
                elif choice == 'S':
                    col = [arr[j][i] for j in range(4)]
                    updated_col = update_row(col)
                    for j in range(4):
                        arr[j][i] = updated_col[j]
                elif choice == 'W':
                    col = [arr[j][i] for j in range(4)]
                    updated_col = update_row(col[::-1])[::-1]
                    for j in range(4):
                        arr[j][i] = updated_col[j]

            if arr != original_board: #Only add random number if the board changed
                add_random_no()
                print_board()

        elif choice == 'P':
            update_arr_to_prev()
            print_board()
        elif choice == 'R':
            reset_game()
            print_board()
        elif choice == 'U':
            exit(0)
        else:
            print("\n============INVALID KEY==========\n")
            

        #Check for Game Over:
        if all(any(arr[i][j] == arr[i][j+1] or arr[j][i] == arr[j+1][i] or arr[i][j]==0 for j in range(3)) for i in range(4)):
            continue
        else:
            print("\n=============GAME OVER============\n")
            while True:
                reschk = input("WANT TO PLAY MORE?? Y/N??\n").upper()
                if reschk in ('Y', 'N'):
                    break
                print("Invalid input. Please enter Y or N.")

            if reschk == 'Y':
                reset_game()
                print_board()
            else:
                exit(0)



if __name__ == "__main__":
    main()
