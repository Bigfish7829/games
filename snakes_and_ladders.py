import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# Define snakes and ladders
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {2: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Setup session state
if "position" not in st.session_state:
    st.session_state.position = 1
if "message" not in st.session_state:
    st.session_state.message = ""

import time

def roll_dice(board_placeholder):
    roll = random.randint(1, 6)
    new_pos = min(st.session_state.position + roll, 100)

    st.session_state.message = f"🎲 You rolled a {roll}"
    st.session_state.position = new_pos

    # Show move after roll
    fig = draw_board()
    board_placeholder.pyplot(fig)
    time.sleep(1)

    # Snake or ladder
    if new_pos in snakes:
        st.session_state.message += f" 🐍 Oh no! You no you didn't install eaves vents with your loft insualtion, you no have condensation and your rafters are rotting! Take a Snake from {new_pos} to {snakes[new_pos]}"
        st.session_state.position = snakes[new_pos]
    elif new_pos in ladders:
        st.session_state.message += f" 🪜 Congratulations you installed dMEV and improved the indoor air quality. Take a ladder from {new_pos} to {ladders[new_pos]}"
        st.session_state.position = ladders[new_pos]

    st.write(f"Current position: {st.session_state.position}")

    # Show final move
    fig = draw_board()
    board_placeholder.pyplot(fig)



def tile_coords(n):
    row = (n - 1) // 10  # 0 (bottom) to 9 (top)
    col = (n - 1) % 10
    y = row  # bottom to top
    if row % 2 == 0:
        x = col  # left to right
    else:
        x = 9 - col  # right to left
    return x, y

# Draw board using matplotlib
def draw_board():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    # Draw colored squares
    for i in range(1, 101):
        x, y = tile_coords(i)
        color = '#f0d9b5' if (x + y) % 2 == 0 else '#b58863'  # light/dark checkerboard
        rect = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor=color, edgecolor='black')
        ax.add_patch(rect)
        ax.text(x, y, str(i), ha='center', va='center', fontsize=8, color='black')

    # Draw snakes
    for start, end in snakes.items():
        x1, y1 = tile_coords(start)
        x2, y2 = tile_coords(end)
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='red', lw=2))

    # Draw ladders
    for start, end in ladders.items():
        x1, y1 = tile_coords(start)
        x2, y2 = tile_coords(end)
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='green', lw=2))

    # Draw player
    if st.session_state.position > 0:
        x, y = tile_coords(st.session_state.position)
        ax.plot(x, y, 'o', color='blue', markersize=15)

    return fig


# Streamlit UI
st.title("🎲 Snakes and Ladders")

board_placeholder = st.empty()
fig = draw_board()
board_placeholder.pyplot(fig)

if st.button("Roll Dice"):
    roll_dice(board_placeholder)

st.info(st.session_state.message)

if st.session_state.position == 100:
    st.success("🏁 You've reached the end! Click 'Roll Dice' to restart.")
    if st.button("Restart"):
        st.session_state.position = 0
        st.session_state.message = ""
