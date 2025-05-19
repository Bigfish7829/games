import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# Define default snakes, ladders, and chance tiles
default_snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {2: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
chance_tiles = [i for i in range(6, 101, 6)]

# Session state
for key, default in {
    "position": 1,
    "message": "",
    "rolls": 0,
    "awaiting_chance_answer": False,
    "chance_roll_pending": False,
    "snakes": default_snakes.copy(),
    "free_roll_next": False,
    "chance_answer_submitted": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Convert tile number to coordinates
def tile_coords(n):
    row = (n - 1) // 10
    col = (n - 1) % 10
    y = row
    x = col if row % 2 == 0 else 9 - col
    return x, y

# Base board (checkerboard, snakes, ladders, numbers)
def get_base_board():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    for i in range(1, 101):
        x, y = tile_coords(i)
        color = '#f0d9b5' if (x + y) % 2 == 0 else '#b58863'
        rect = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor=color, edgecolor='black')
        ax.add_patch(rect)
        ax.text(x, y, str(i), ha='center', va='center', fontsize=8)

    for i in chance_tiles:
        x, y = tile_coords(i)
        ax.text(x, y, "?", ha='center', va='center', fontsize=14, color='red', weight='bold')

    for start, end in st.session_state.snakes.items():
        x1, y1 = tile_coords(start)
        x2, y2 = tile_coords(end)
        x = np.linspace(x1, x2, 100)
        y = np.linspace(y1, y2, 100)
        wiggle = np.sin(np.linspace(0, 4 * np.pi, 100)) * 0.15
        dx, dy = x2 - x1, y2 - y1
        length = np.hypot(dx, dy)
        ux, uy = -dy / length, dx / length
        ax.plot(x + wiggle * ux, y + wiggle * uy, color='yellow', linewidth=3)

    for start, end in ladders.items():
        x1, y1 = tile_coords(start)
        x2, y2 = tile_coords(end)
        dx = 0.15
        ax.plot([x1 - dx, x2 - dx], [y1, y2], color='green', linewidth=2)
        ax.plot([x1 + dx, x2 + dx], [y1, y2], color='green', linewidth=2)
        rungs = int(np.hypot(x2 - x1, y2 - y1) / 0.2)
        for i in range(1, rungs):
            t = i / rungs
            xr = (1 - t) * x1 + t * x2
            yr = (1 - t) * y1 + t * y2
            ax.plot([xr - dx, xr + dx], [yr, yr], color='green', linewidth=1)

    return fig

def draw_board_with_player():
    fig = get_base_board()
    ax = fig.axes[0]
    if st.session_state.position > 0:
        x, y = tile_coords(st.session_state.position)
        ax.plot(x, y, 'o', color='blue', markersize=15)
    return fig

# Dice logic
def roll_dice(board_placeholder, free_roll):
    roll = random.randint(1, 6)
    new_pos = min(st.session_state.position + roll, 100)
    st.session_state.message = f"🎲 You rolled a {roll}"

    if not free_roll:
        st.session_state.rolls += 1

    st.session_state.position = new_pos
    board_placeholder.pyplot(draw_board_with_player())
    time.sleep(1)

    if new_pos in st.session_state.snakes:
        st.session_state.message += (
            f" 🐍 Oh no! You didn’t install eaves vents with your loft insulation, "
            f"you now have condensation and your rafters are rotting! "
            f"Slip from {new_pos} to {st.session_state.snakes[new_pos]}"
        )
        st.session_state.position = st.session_state.snakes[new_pos]
    elif new_pos in ladders:
        st.session_state.message += (
            f" 🪜 Congratulations! You installed dMEV and improved indoor air quality. "
            f"Climb from {new_pos} to {ladders[new_pos]}"
        )
        st.session_state.position = ladders[new_pos]


    board_placeholder.pyplot(draw_board_with_player())

    # Chance
    if st.session_state.position in chance_tiles:
        st.session_state.awaiting_chance_answer = True
        st.session_state.chance_answer_submitted = False

st.title("🎲 Retrofit Wins and Banana Skins")
board_placeholder = st.empty()
board_placeholder.pyplot(draw_board_with_player())

# Dice button
if not st.session_state.awaiting_chance_answer:
    if st.button("Roll Dice"):
        roll_dice(board_placeholder, st.session_state.free_roll_next)
        st.session_state.free_roll_next = False


# Chance question
if st.session_state.awaiting_chance_answer:
    with st.form(key="chance_form", clear_on_submit=True):
        st.subheader("❓ Chance Question")
        st.write("Which retrofit measure typically has the biggest impact on reducing carbon emmissions?")
        answer = st.radio("Choose one:", ["Loft insulation", "Solar panels", "Air source heat pumps"], index=None)
        submitted = st.form_submit_button("Submit Answer")

        if submitted and answer:
            if answer == "Air source heat pumps":
                st.session_state.chance_answer_result = "correct"
                st.success("Correct! You get a free roll.")
                st.session_state.free_roll_next = True

                if st.session_state.snakes:
                    highest_snake = max(st.session_state.snakes)
                    del st.session_state.snakes[highest_snake]
                    st.info(f"🎉 You are on the way to a no regrets retrofit! The banana skin from tile {highest_snake} has been removed!")
            else:
                st.session_state.chance_answer_result = "incorrect"
                st.warning("Incorrect. Better luck next time.")

            st.session_state.awaiting_chance_answer = False
            if st.button("OK"):
                st.rerun()




st.info(st.session_state.message)
st.write(f"🎯 Total Rolls: {st.session_state.rolls}")

# End game
if st.session_state.position == 100:
    st.success(f"🏁 You've reached Net Zero in {st.session_state.rolls} rolls!")
    if st.button("Restart"):
        for key in ["position", "message", "rolls", "awaiting_chance_answer", "chance_roll_pending", "snakes", "free_roll_next", "chance_answer_submitted"]:
            del st.session_state[key]
        st.experimental_rerun()
