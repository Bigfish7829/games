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
if "position" not in st.session_state:
    st.session_state.position = 1
if "message" not in st.session_state:
    st.session_state.message = ""
if "rolls" not in st.session_state:
    st.session_state.rolls = 0
if "awaiting_chance_answer" not in st.session_state:
    st.session_state.awaiting_chance_answer = False
if "chance_roll_pending" not in st.session_state:
    st.session_state.chance_roll_pending = False
if "snakes" not in st.session_state:
    st.session_state.snakes = default_snakes.copy()
if "event_message" not in st.session_state:
    st.session_state.event_message = ""

# Convert tile number to coordinates
def tile_coords(n):
    row = (n - 1) // 10
    col = (n - 1) % 10
    y = row
    x = col if row % 2 == 0 else 9 - col
    return x, y

# Base board
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
        ax.text(x, y, str(i), ha='center', va='center', fontsize=8, color='black')

    for i in chance_tiles:
        x, y = tile_coords(i)
        ax.text(x, y, "?", ha='center', va='center', fontsize=14, color='red', weight='bold')

    for start, end in st.session_state.snakes.items():
        x1, y1 = tile_coords(start)
        x2, y2 = tile_coords(end)
        segments = 100
        x = np.linspace(x1, x2, segments)
        y = np.linspace(y1, y2, segments)
        wiggle = np.sin(np.linspace(0, 4 * np.pi, segments)) * 0.15
        dx, dy = x2 - x1, y2 - y1
        length = np.hypot(dx, dy)
        ux, uy = -dy / length, dx / length
        x_snake = x + wiggle * ux
        y_snake = y + wiggle * uy
        ax.plot(x_snake, y_snake, color='yellow', linewidth=3)

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

def draw_board_with_player():
    fig = get_base_board()
    ax = fig.axes[0]
    if st.session_state.position > 0:
        x, y = tile_coords(st.session_state.position)
        ax.plot(x, y, 'o', color='blue', markersize=15)
    return fig

free_roll_index = False

def roll_dice(board_placeholder, free_roll):
    roll = random.randint(1, 6)
    new_pos = min(st.session_state.position + roll, 100)

    if not free_roll:
        st.session_state.rolls += 1

    st.session_state.message = f"🎲 You rolled a {roll}"
    st.session_state.position = new_pos
    board_placeholder.pyplot(draw_board_with_player())
    time.sleep(1)

    if new_pos in st.session_state.snakes:
        st.session_state.event_message = f"🐍 Oh no! You didn’t install eaves vents with your loft insulation, you now have condensation and your rafters are rotting! Slip from {new_pos} to {st.session_state.snakes[new_pos]}"
        st.session_state.position = st.session_state.snakes[new_pos]
    elif new_pos in ladders:
        st.session_state.event_message = f"🪜 Congratulations! You installed dMEV and improved indoor air quality. Climb from {new_pos} to {ladders[new_pos]}"
        st.session_state.position = ladders[new_pos]

    board_placeholder.pyplot(draw_board_with_player())

    if st.session_state.position in chance_tiles:
        st.session_state.awaiting_chance_answer = True
        st.session_state.chance_roll_pending = True
        st.session_state.event_message = "❓ Chance Question: How much does a typical solar panel array save the resident in a year?"

# Streamlit UI
st.title("🎲 Retrofit Wins and Banana Skins")

# Overlay Event Message
if st.session_state.event_message:
    st.markdown(
        f"""
        <div style='position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000;'>
            <div style='background: white; padding: 40px; border-radius: 10px; max-width: 600px; text-align: center; box-shadow: 0 0 10px rgba(0,0,0,0.5);'>
                <h3>Event</h3>
                <p style='font-size: 18px'>{st.session_state.event_message}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Continue"):
        st.session_state.event_message = ""

board_placeholder = st.empty()
board_placeholder.pyplot(draw_board_with_player())

if st.button("Roll Dice") and not st.session_state.awaiting_chance_answer:
    roll_dice(board_placeholder, free_roll_index)

st.info(st.session_state.message)
st.write(f"🎯 Total Rolls: {st.session_state.rolls}")

if st.session_state.position == 100:
    st.success(f"🏁 You've reached Net Zero in {st.session_state.rolls} rolls!")
    if st.button("Restart"):
        st.session_state.position = 1
        st.session_state.message = ""
        st.session_state.rolls = 0
        st.session_state.awaiting_chance_answer = False
        st.session_state.chance_roll_pending = False
        st.session_state.snakes = default_snakes.copy()
        st.session_state.event_message = ""
