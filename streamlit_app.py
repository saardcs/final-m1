import streamlit as st
import streamlit.components.v1 as components
from itertools import permutations
import json
import re
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_HALF_UP
import gspread
from google.oauth2.service_account import Credentials
import datetime
import os

st.set_page_config(page_title="Final Exam", layout="centered")
st.title("Final Exam")
st.header("Student Information")

# ========== Student Info ==========
class_options = ["1/11", "1/12"]
selected_class = st.selectbox("Select your class:", class_options)
nickname = st.text_input("Nickname")
student_number = st.text_input("Student Number")

answers = st.secrets["answers"]

# ========== Part I: Sudoku Puzzle (6pts) ==========
st.header("Part I: Sudoku Puzzle (6pts)")
st.write("**Instruction:** Solve the 4x4 and 6x6 Sudoku using the appropriate numbers.")

puzzle_4x4 = st.secrets["sudoku_4x4"]["puzzle"]
solution_4x4 = st.secrets["sudoku_4x4"]["solution"]
puzzle_6x6 = st.secrets["sudoku_6x6"]["puzzle"]
solution_6x6 = st.secrets["sudoku_6x6"]["solution"]

sudoku = components.declare_component("sudoku", path="sudoku_component")
sudoku2 = components.declare_component("sudoku2", path="sudoku_component2")

st.write("### 4x4 Sudoku")
board_4x4 = sudoku(default=puzzle_4x4, key="sudoku4x4")

st.write("### 6x6 Sudoku")
board_6x6 = sudoku2(default=puzzle_6x6, key="sudoku6x6")

# ========== Part II: Counting Combinations I (2pts) ==========
st.header("Part II: Counting Combinations I (2pts)")
st.write("**Instruction:** Given the colors below, make the possible combinations and answer the following questions.")
st.image("rby.png")

colors = ["", "Red", "Blue", "Yellow"]
tower_inputs = {}
cols = st.columns(6)
for i, col in enumerate(cols):
    with col:
        st.markdown(f"**Tower {i+1}**")
        tower_inputs[i] = []
        for block in range(3):
            block_color = st.selectbox(f"Select", colors, key=f"tower{i}_block{block}", label_visibility="collapsed")
            tower_inputs[i].append(block_color)

questions_4_6 = {
    4: ("How many three block towers can you make out of them?", ["a. 5", "b. 6", "c. 8", "d. 12"], answers["q4"]),
    5: ("If there is a restriction that you cannot put the yellow block at the top. How many towers can you make?", ["a. 2", "b. 4", "c. 6", "d. 8"], answers["q5"]),
    6: ("If there is a restriction that you cannot put the red block and blue block at the top. How many towers can you make?", ["a. 2", "b. 4", "c. 6", "d. 8"], answers["q6"]),
}
for qnum in questions_4_6:
    q, opts, _ = questions_4_6[qnum]
    st.radio(f"**{qnum}. {q}**", options=opts, key=f"q{qnum}")

# ========== Part III: Counting Combinations II (2pts) ==========
st.header("Part III: Counting Combinations II (2pts)")
st.write("**Instruction:** Suppose that the five-character code has the following restrictions:")
st.markdown("""
- Numbers only
- Cannot repeate characters
""")
st.image("5ch.png")

questions_7_10 = {
    7: ("What sets of characters can the code contain?", ["a. a-z (lowercase letters)", "b. 0-9 (numbers)", "c. A-Z (uppercase letters)", "d. All of the above"], answers["q7"]),
    8: ("How many possible numbers and letters are there for the first character of the code?", ["a. 52 possible letters and numbers", "b. 10 possible numbers", "c. 62 possible letters and numbers", "d. 9 possible numbers"], answers["q8"]),
    9: ("How many possible numbers and letters are there for the fifth character of the code?", ["a. 52 possible letters and numbers", "b. 10 possible numbers", "c. 62 possible letters and numbers", "d. 6 possible numbers"], answers["q9"]),
    10: ("How many different code combinations are possible given the statement above?", [
        "a. 44,261,653,680 possible combinations",
        "b. 380,204,032 possible combinations",
        "c. 100,000 possible combinations",
        "d. 30,240 possible combinations"
    ], answers["q10"]),
}

for qnum in questions_7_10:
    q, opts, _ = questions_7_10[qnum]
    st.radio(f"**{qnum}. {q}**", options=opts, key=f"q{qnum}")




# LCM



# Factor Trees
tree = components.declare_component("tree", path="tree_component")
st.write("**14 - 15. Find the Prime Factors of the following numbers.**")
tree_result = tree(key="factor_tree")


# ========== Part V: Binary Number System (5pts) ==========
st.header("Part V: Binary Number System (5pts)")

st.write("**Instruction:** Add the following binary numbers.")

# Q16
col1, col2, col3 = st.columns([1, 2, 8])

with col1:
    st.text("16.\n     +\n\n\n     =")  # Use st.text, not st.write!

with col2:
    st.text("0010\n0001\n----")
    binary_sum_16 = st.text_input("Answer", key="bin_sum_16", label_visibility="collapsed")

# Q17
col1, col2, col3 = st.columns([1, 2, 8])

with col1:
    st.text("17.\n     +\n\n\n     =")

with col2:
    st.text("0111\n0001\n----")
    binary_sum_17 = st.text_input("Answer", key="bin_sum_17", label_visibility="collapsed")

st.write("")
st.write("")








# Q18
st.write("**Instruction:** Use the Divide By 2 Method to convert the following decimal numbers into binary.")

st.write("18. Convert the decimal number 9 into binary.")


# Initialize session state
if "steps" not in st.session_state:
    st.session_state.steps = []
if "input_error" not in st.session_state:
    st.session_state.input_error = ""

# --- Add Step Handler ---
def add_step():
    raw = st.session_state.div_input.strip()
    try:
        num, den = map(int, raw.split("/"))
        if den == 0:
            st.session_state.input_error = "❌ Division by zero is not allowed."
            return
        st.session_state.steps.append({
            "numerator": num,
            "denominator": den,
            "quotient": num // den,
            "remainder": num % den,
        })
        st.session_state.div_input = ""
        st.session_state.input_error = ""  # Clear error on success
    except:
        st.session_state.input_error = "❌ Invalid format. Use e.g., 9/2"

# --- Remove Last Step Handler ---
def remove_last_step():
    if st.session_state.steps:
        st.session_state.steps.pop()

# --- Show existing steps ---
for step in st.session_state.steps:
    st.text(f"{step['numerator']} ÷ {step['denominator']} = {step['quotient']} R {step['remainder']}")

# --- Input and Buttons ---
st.text_input("Type a division (e.g., 9/2)", key="div_input")
if st.session_state.input_error:
    st.warning(st.session_state.input_error)

cols = st.columns([1.5, 6])
with cols[0]:
    st.button("Add division step", on_click=add_step, key="add_step")
with cols[1]:
    st.button("Remove last step", on_click=remove_last_step, key="rem_step")


cols = st.columns([1.1, 7])
with cols[0]:
    binary_18 = st.text_input("Answer", key="bin_18")
st.write("")
st.write("")






# Q19
st.write("19. Convert the decimal number 21 into binary.")

# Initialize session state
if "steps2" not in st.session_state:
    st.session_state.steps2 = []
if "input_error" not in st.session_state:
    st.session_state.input_error = ""

# --- Add Step Handler ---
def add_step():
    raw = st.session_state.div_input.strip()
    try:
        num, den = map(int, raw.split("/"))
        if den == 0:
            st.session_state.input_error = "❌ Division by zero is not allowed."
            return
        st.session_state.steps2.append({
            "numerator": num,
            "denominator": den,
            "quotient": num // den,
            "remainder": num % den,
        })
        st.session_state.div_input = ""
        st.session_state.input_error = ""  # Clear error on success
    except:
        st.session_state.input_error = "❌ Invalid format. Use e.g., 9/2"

# --- Remove Last Step Handler ---
def remove_last_step():
    if st.session_state.steps2:
        st.session_state.steps2.pop()

# --- Show existing steps ---
for step in st.session_state.steps2:
    st.text(f"{step['numerator']} ÷ {step['denominator']} = {step['quotient']} R {step['remainder']}")

# --- Input and Buttons ---
st.text_input("Type a division (e.g., 9/2)", key="div_input2")
if st.session_state.input_error:
    st.warning(st.session_state.input_error)

cols = st.columns([1.5, 6])
with cols[0]:
    st.button("Add division step", on_click=add_step, key="add_step2")
with cols[1]:
    st.button("Remove last step", on_click=remove_last_step, key="rem_step2")


cols = st.columns([1.1, 7])
with cols[0]:
    binary_19 = st.text_input("Answer", key="bin_19")

st.write("")
st.write("")


# Q20
st.write("20. Convert each decimal number into a 7-bit binary number to complete the image.")

# Decimals with partial conversions provided (first 3 rows fixed)
decimal_values = [14, 28, 56, 127, 14, 28, 56, 112]
provided_binaries = [
    format(14, '07b'),
    format(28, '07b'),
    format(56, '07b'),
    "", "", "", "", ""
]

# Inputs for last 5 binaries (Q20) — keys q20_4 to q20_8 for last five rows (indices 3 to 7)
binary_inputs_q20 = []

col1, col2 = st.columns([1.1, 7])

with col1:
    # Display provided binary values for the first 3 rows (disable the inputs)
    for i, decimal_value in enumerate(decimal_values[:3]):
        # Use disabled text inputs to keep height alignment
        st.text_input(f"{decimal_value}", value=provided_binaries[i], disabled=True)#, label_visibility="collapsed")
    
    # Input fields for the last 5 rows (user can fill in the binary values)
    binary_inputs_q20 = []
    for idx in range(3, 8):
        # Ensure that the key is unique by including both the decimal value and its index
        unique_key = f"q20_{decimal_values[idx]}_{idx}"  # Add the index to make the key unique
        binary_input = st.text_input(f"{decimal_values[idx]}", key=unique_key)
        binary_inputs_q20.append(binary_input)

def decode_binary_to_image(bin_list):
    """Convert list of 8 binary strings (8-bit each) into a 8x8 numpy array (pixels)"""
    pixels = np.zeros((8, 7))
    for i, b in enumerate(bin_list):
        if len(b) == 7 and all(c in '01' for c in b):
            pixels[i] = np.array([int(bit) for bit in b])
        else:
            pixels[i] = np.zeros(7)  # Empty row for incomplete binary data
    return pixels

# Combine the provided and user inputs (use user inputs for rows 4 to 8)
full_binary_list = provided_binaries[:3] + binary_inputs_q20
img_pixels = decode_binary_to_image(full_binary_list)

with col2:
    fig, ax = plt.subplots(figsize=(4, 6))
    ax.imshow(img_pixels, cmap="gray_r", vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)

