import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import winsound
import json
import os

# --- Window Setup ---
window = tk.Tk()
window.title("Tic Tac Toe -desktop version")
window.config(bg="#282c34")
window.geometry("640x780")  # Typical mobile screen size
window.resizable(False, False)

# --- Global variables ---
current_player = 'X'
buttons = []
player_score = 0
computer_score = 0
difficulty = 'Easy'
sound_on = True
dark_mode = True
game_mode = 'PVC'
player_names = ["Player X", "Computer O"]
game_state_file = "tic_tac_toe_state.json"
leaderboard_file = "tic_tac_toe_leaderboard.json"

# --- Sounds ---
def play_sound(filename):
    if not sound_on:
        return
    try:
        winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except:
        print(f"Error playing {filename}")

def stop_sounds():
    winsound.PlaySound(None, winsound.SND_PURGE)

def play_win_sound():
    stop_sounds()
    play_sound("win.wav")

def play_lose_sound():
    stop_sounds()
    play_sound("lose.wav")

def play_draw_sound():
    stop_sounds()
    play_sound("draw.wav")

# --- Game Logic ---

def update_score():
    score_label.config(text=f"{player_names[0]}: {player_score}   |   {player_names[1]}: {computer_score}")

def check_winner():
    combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in combos:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != " ":
            return buttons[combo[0]]["text"]
    return None

def is_draw():
    return all(button["text"] != " " for button in buttons)

def minimax(board, is_maximizing):
    winner = check_winner_minimax(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def is_board_full(board):
    return all(cell != " " for cell in board)

def check_winner_minimax(board):
    combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return board[combo[0]]
    return None

def computer_move():
    global current_player, computer_score
    empty = [i for i, b in enumerate(buttons) if b["text"] == " "]

    if not empty:
        return

    best = None

    if difficulty == 'Hard':
        board = [b["text"] for b in buttons]
        best_score = -float('inf')
        for i in empty:
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best = i
    else:
        best = random.choice(empty)

    buttons[best].config(bg="#f9d71c")
    window.update()
    buttons[best]["text"] = current_player
    window.after(100, lambda idx=best: buttons[idx].config(bg="#61afef"))

    winner = check_winner()
    if winner:
        if winner == 'O':
            computer_score += 1
            update_score()
            play_lose_sound()
            messagebox.showinfo("Game Over", f"😞 {player_names[1]} wins!")
            update_leaderboard(player_names[1])
            restart_game()
    elif is_draw():
        play_draw_sound()
        messagebox.showinfo("Game Over", "🤝 It's a draw!")
        restart_game()
    else:
        current_player = "X"

def button_click(i):
    global current_player, player_score, computer_score
    if buttons[i]["text"] == " ":
        buttons[i].config(bg="#f9d71c")
        window.update()
        buttons[i]["text"] = current_player
        window.after(100, lambda idx=i: buttons[idx].config(bg="#61afef"))

        winner = check_winner()
        if winner:
            if winner == 'X':
                player_score += 1
                update_score()
                play_win_sound()
                messagebox.showinfo("Game Over", f"🎉 {player_names[0]} wins!")
                update_leaderboard(player_names[0])
            else:
                computer_score += 1
                update_score()
                play_lose_sound()
                messagebox.showinfo("Game Over", f"😞 {player_names[1]} wins!")
                update_leaderboard(player_names[1])
            restart_game()
        elif is_draw():
            play_draw_sound()
            messagebox.showinfo("Game Over", "🤝 It's a draw!")
            restart_game()
        else:
            if game_mode == 'PVC':
                current_player = "O"
                window.after(300, computer_move)
            else:
                current_player = 'O' if current_player == 'X' else 'X'

def restart_game():
    global current_player
    current_player = "X"
    stop_sounds()
    for btn in buttons:
        btn["text"] = " "
        btn.config(bg="#61afef")
    save_game_state()

def reset_scores():
    global player_score, computer_score
    player_score = 0
    computer_score = 0
    update_score()
    save_game_state()

def set_difficulty(level):
    global difficulty
    difficulty = level
    restart_game()

def toggle_sound():
    global sound_on
    sound_on = not sound_on
    sound_btn.config(text="🔈 On" if sound_on else "🔇 Off")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    if dark_mode:
        bg = "#282c34"
        fg = "white"
        btn_bg = "#61afef"
        active_bg = "#528bff"
    else:
        bg = "white"
        fg = "black"
        btn_bg = "#a0c4ff"
        active_bg = "#4895ef"

    window.config(bg=bg)
    frame.config(bg=bg)
    btn_frame.config(bg=bg)
    for btn in buttons:
        btn.config(bg=btn_bg, fg=fg, activebackground=active_bg)
    score_label.config(bg=bg, fg=fg)
    restart_btn.config(bg="#98c379" if dark_mode else "#6a994e", fg=fg)
    easy_btn.config(bg="#d19a66" if dark_mode else "#f4a261", fg=fg)
    medium_btn.config(bg="#d19a66" if dark_mode else "#f4a261", fg=fg)
    hard_btn.config(bg="#e06c75" if dark_mode else "#e76f51", fg=fg)
    sound_btn.config(bg="#61afef" if dark_mode else "#4895ef", fg=fg)
    theme_btn.config(bg="#61afef" if dark_mode else "#4895ef", fg=fg)
    mode_btn.config(bg="#61afef" if dark_mode else "#4895ef", fg=fg)
    reset_btn.config(bg="#e06c75" if dark_mode else "#e76f51", fg=fg)
    names_btn.config(bg="#56b6c2" if dark_mode else "#2a9d8f", fg=fg)
    leaderboard_btn.config(bg="#56b6c2" if dark_mode else "#2a9d8f", fg=fg)

def toggle_mode():
    global game_mode
    if game_mode == 'PVC':
        game_mode = 'PVP'
        mode_btn.config(text="Mode: Player vs Player")
        player_names[1] = "Player O"
    else:
        game_mode = 'PVC'
        mode_btn.config(text="Mode: Player vs Computer")
        player_names[1] = "Computer O"
    reset_scores()
    restart_game()

def set_player_names():
    p1 = simpledialog.askstring("Player 1 Name", "Enter Player X's name:", parent=window)
    if p1:
        player_names[0] = p1
    if game_mode == 'PVP':
        p2 = simpledialog.askstring("Player 2 Name", "Enter Player O's name:", parent=window)
        if p2:
            player_names[1] = p2
    update_score()
    save_game_state()

def update_leaderboard(winner):
    leaderboard = load_leaderboard()
    leaderboard[winner] = leaderboard.get(winner, 0) + 1
    with open(leaderboard_file, "w") as f:
        json.dump(leaderboard, f)

def show_leaderboard():
    leaderboard = load_leaderboard()
    sorted_board = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    text = "🏆 Leaderboard 🏆\n\n"
    if sorted_board:
        for i, (name, score) in enumerate(sorted_board, start=1):
            text += f"{i}. {name}: {score}\n"
    else:
        text += "No games played yet."
    messagebox.showinfo("Leaderboard", text)

def load_leaderboard():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "r") as f:
            return json.load(f)
    return {}

def save_game_state():
    state = {
        "player_score": player_score,
        "computer_score": computer_score,
        "difficulty": difficulty,
        "sound_on": sound_on,
        "dark_mode": dark_mode,
        "game_mode": game_mode,
        "player_names": player_names,
        "board": [b["text"] for b in buttons]
    }
    with open(game_state_file, "w") as f:
        json.dump(state, f)

def load_game_state():
    if os.path.exists(game_state_file):
        with open(game_state_file, "r") as f:
            state = json.load(f)
            return state
    return None

def restore_game():
    state = load_game_state()
    if state:
        global player_score, computer_score, difficulty, sound_on, dark_mode, game_mode, player_names, current_player
        player_score = state.get("player_score", 0)
        computer_score = state.get("computer_score", 0)
        difficulty = state.get("difficulty", "Easy")
        sound_on = state.get("sound_on", True)
        dark_mode = state.get("dark_mode", True)
        game_mode = state.get("game_mode", "PVC")
        player_names = state.get("player_names", ["Player X", "Computer O"])
        board = state.get("board", [" "] * 9)
        current_player = "X"
        for i in range(9):
            buttons[i]["text"] = board[i]
        update_score()
        apply_theme()
        # Update difficulty buttons style
        easy_btn.config(relief=tk.SUNKEN if difficulty == "Easy" else tk.RAISED)
        medium_btn.config(relief=tk.SUNKEN if difficulty == "Medium" else tk.RAISED)
        hard_btn.config(relief=tk.SUNKEN if difficulty == "Hard" else tk.RAISED)
        # Update mode button text
        if game_mode == "PVC":
            mode_btn.config(text="Mode: Player vs Computer")
        else:
            mode_btn.config(text="Mode: Player vs Player")
    else:
        restart_game()
        apply_theme()
        update_score()

# --- UI Setup ---

frame = tk.Frame(window, bg="#282c34")
frame.pack(pady=10)

score_label = tk.Label(frame, text="", font=("Arial", 18, "bold"), fg="white", bg="#282c34")
score_label.pack()

btn_frame = tk.Frame(window, bg="#282c34")
btn_frame.pack(pady=20)

button_font = ("Arial", 28, "bold")
button_size = 6

for i in range(9):
    btn = tk.Button(btn_frame, text=" ", font=button_font, width=button_size, height=2, bg="#61afef", fg="white",
                    command=lambda i=i: button_click(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

controls_frame = tk.Frame(window, bg="#282c34")
controls_frame.pack(pady=10)

restart_btn = tk.Button(controls_frame, text="Restart", font=("Arial", 14), bg="#98c379", fg="white", width=10, command=restart_game)
restart_btn.grid(row=0, column=0, padx=5, pady=5)

reset_btn = tk.Button(controls_frame, text="Reset Scores", font=("Arial", 14), bg="#e06c75", fg="white", width=10, command=reset_scores)
reset_btn.grid(row=0, column=1, padx=5, pady=5)

names_btn = tk.Button(controls_frame, text="Set Names", font=("Arial", 14), bg="#56b6c2", fg="white", width=10, command=set_player_names)
names_btn.grid(row=0, column=2, padx=5, pady=5)

difficulty_frame = tk.Frame(window, bg="#282c34")
difficulty_frame.pack(pady=10)

easy_btn = tk.Button(difficulty_frame, text="Easy", font=("Arial", 14), bg="#d19a66", fg="white", width=8, command=lambda: set_difficulty("Easy"))
easy_btn.grid(row=0, column=0, padx=5)

medium_btn = tk.Button(difficulty_frame, text="Medium", font=("Arial", 14), bg="#d19a66", fg="white", width=8, command=lambda: set_difficulty("Medium"))
medium_btn.grid(row=0, column=1, padx=5)

hard_btn = tk.Button(difficulty_frame, text="Hard", font=("Arial", 14), bg="#e06c75", fg="white", width=8, command=lambda: set_difficulty("Hard"))
hard_btn.grid(row=0, column=2, padx=5)

options_frame = tk.Frame(window, bg="#282c34")
options_frame.pack(pady=10)

sound_btn = tk.Button(options_frame, text="🔈 On", font=("Arial", 14), bg="#61afef", fg="white", width=10, command=toggle_sound)
sound_btn.grid(row=0, column=0, padx=5, pady=5)

theme_btn = tk.Button(options_frame, text="Theme", font=("Arial", 14), bg="#61afef", fg="white", width=10, command=toggle_theme)
theme_btn.grid(row=0, column=1, padx=5, pady=5)

mode_btn = tk.Button(options_frame, text="Mode: Player vs Computer", font=("Arial", 14), bg="#61afef", fg="white", width=20, command=toggle_mode)
mode_btn.grid(row=0, column=2, padx=5, pady=5)

leaderboard_btn = tk.Button(window, text="Leaderboard", font=("Arial", 14), bg="#56b6c2", fg="white", width=20, command=show_leaderboard)
leaderboard_btn.pack(pady=10)

# --- Initialize ---

restore_game()

window.protocol("WM_DELETE_WINDOW", lambda: (save_game_state(), window.destroy()))

window.mainloop()
