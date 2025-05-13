import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# --- Game data ---
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {2: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# --- Session state setup ---
if "position" not in st.session_state:
    st.session_state.position = 1
if "message" not in st.session_state:
    st.session_state.message = ""
if "event" not in st.session_state:
    st.session_state.event = None
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False
if "popup_text" not in st.session_state:
    st.session_state.popup_text = ""


# --- Tile coordinate helper ---
def tile_coords(n):
    row = (n - 1) // 10
    col = (n - 1) % 10
    y = row
    x = col if row % 2 == 0 else 9 - col
    return x, y

# --- Draw the board with snakes, ladders, and player ---
@st.cache_resource
def generate_base_board():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    for i in range(1, 101):
        x, y = tile_coords(i)
        color = '#f0d9b5' if (x + y) % 2 == 0 else '#b58863'
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor=color, edgecolor='black'))
        ax.text(x, y, str(i), ha='center', va='center', fontsize=8)

    for start, end in snakes.items():
        x1, y1 = tile_coords(start)
        x2, y2 = tile_coords(end)
        segments = 100
        x = np.linspace(x1, x2, segments)
        y = np.linspace(y1, y2, segments)
        wiggle = np.sin(np.linspace(0, 4 * np.pi, segments)) * 0.15
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
        num_rungs = int(((y2 - y1)**2 + (x2 - x1)**2)**0.5 / 0.2)
        for i in range(1, num_rungs):
            t = i / num_rungs
            rung_x = (1 - t) * x1 + t * x2
            rung_y = (1 - t) * y1 + t * y2
            ax.plot([rung_x - dx, rung_x + dx], [rung_y, rung_y], color='green', linewidth=1)

    return fig

# --- Overlay player on cached board ---
def draw_board_with_player():
    fig = generate_base_board()
    ax = fig.axes[0]
    x, y = tile_coords(st.session_state.position)
    ax.plot(x, y, 'o', color='blue', markersize=15)
    return fig

# --- Game logic ---
def roll_dice(board_placeholder):
    roll = random.randint(1, 6)
    new_pos = min(st.session_state.position + roll, 100)

    st.session_state.message = f"🎲 You rolled a {roll}"
    st.session_state.event = None
    st.session_state.position = new_pos
    board_placeholder.pyplot(draw_board_with_player())

    if new_pos in snakes:
        end = snakes[new_pos]
        st.session_state.position = end
        st.session_state.popup_text = f"🐍 **Banana Skin!** You slipped from {new_pos} to {end}."
        st.session_state.show_popup = True
    elif new_pos in ladders:
        end = ladders[new_pos]
        st.session_state.position = end
        st.session_state.popup_text = f"🪜 **Retrofit Win!** You climbed from {new_pos} to {end}."
        st.session_state.show_popup = True


    board_placeholder.pyplot(draw_board_with_player())

# --- UI ---

st.title("🎲 Retrofit Wins and Banana Skins")

board_placeholder = st.empty()
board_placeholder.pyplot(draw_board_with_player())

# Simulated popup
if st.session_state.show_popup:
    st.warning(st.session_state.popup_text)
    if st.button("Close"):
        st.session_state.show_popup = False
else:
    if st.button("Roll Dice"):
        roll_dice(board_placeholder)

    st.info(st.session_state.message)

    if st.session_state.position == 100:
        st.success("🏁 You've reached Net Zero! Click 'Roll Dice' to restart.")
        if st.button("Restart"):
            st.session_state.position = 1
            st.session_state.message = ""
            st.session_state.show_popup = False
            st.session_state.popup_text = ""
