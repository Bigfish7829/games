import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# Define snakes and ladders
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Setup session state
if "position" not in st.session_state:
    st.session_state.position = 0
if "message" not in st.session_state:
    st.session_state.message = ""

def roll_dice():
    roll = random.randint(1, 6)
    pos = st.session_state.position + roll
    st.session_state.message = f"🎲 You rolled a {roll}"

    if pos in snakes:
        st.session_state.message += f" 🐍 Oh no! Snake from {pos} to {snakes[pos]}"
        pos = snakes[pos]
    elif pos in ladders:
        st.session_state.message += f" 🪜 Nice! Ladder from {pos} to {ladders[pos]}"
        pos = ladders[pos]

    st.session_state.position = min(pos, 100)

# Function to convert tile number to (x, y) on a 10x10 grid
def tile_coords(n):
    row = (n - 1) // 10
    col = (n - 1) % 10
    if row % 2 == 0:
        x = col
    else:
        x = 9 - col
    y = 9 - row
    return x, y

# Draw board using matplotlib
def draw_board():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    # Draw grid numbers
    for i in range(1, 101):
        x, y = tile_coords(i)
        ax.text(x, y, str(i), ha='center', va='center', fontsize=8)

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

st.pyplot(draw_board())

st.write(f"Current position: {st.session_state.position}")
if st.button("Roll Dice"):
    roll_dice()

st.info(st.session_state.message)

if st.session_state.position == 100:
    st.success("🏁 You've reached the end! Click 'Roll Dice' to restart.")
    if st.button("Restart"):
        st.session_state.position = 0
        st.session_state.message = ""
