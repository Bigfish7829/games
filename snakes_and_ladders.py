import streamlit as st
import random

# Session state for player positions
if "position" not in st.session_state:
    st.session_state.position = 0

snakes = {16: 6, 47: 26, 49: 11}
ladders = {1: 38, 4: 14, 9: 31}

def roll_dice():
    roll = random.randint(1, 6)
    pos = st.session_state.position + roll
    pos = snakes.get(pos, pos)
    pos = ladders.get(pos, pos)
    st.session_state.position = min(pos, 100)
    return roll

st.title("🎲 Snakes and Ladders")
st.write(f"You are on square {st.session_state.position}")

if st.button("Roll Dice"):
    result = roll_dice()
    st.write(f"You rolled a {result}")
    st.write(f"New position: {st.session_state.position}")
    if st.session_state.position == 100:
        st.success("You've won!")

# Optionally render a 10x10 grid using st.pyplot or st.markdown with emojis
