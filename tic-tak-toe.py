import streamlit as st

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮", layout="centered")
st.markdown("<h1 style='text-align: center;'>🎮 Tic Tac Toe</h1>", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "turn" not in st.session_state:
    st.session_state.turn = "X"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "winning_cells" not in st.session_state:
    st.session_state.winning_cells = []
if "score" not in st.session_state:
    st.session_state.score = {"X": 0, "O": 0, "Draw": 0}

# ---------------- GAME LOGIC ---------------- #
WINNING_COMBOS = [
    (0,1,2), (3,4,5), (6,7,8),  # rows
    (0,3,6), (1,4,7), (2,5,8),  # cols
    (0,4,8), (2,4,6)            # diagonals
]

def check_winner():
    board = st.session_state.board
    for combo in WINNING_COMBOS:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != "":
            st.session_state.winner = board[a]
            st.session_state.winning_cells = [a, b, c]
            st.session_state.score[board[a]] += 1
            return
    if "" not in board:
        st.session_state.winner = "Draw"
        st.session_state.score["Draw"] += 1

def play_move(i):
    if st.session_state.board[i] == "" and st.session_state.winner is None:
        st.session_state.board[i] = st.session_state.turn
        st.session_state.turn = "O" if st.session_state.turn == "X" else "X"
        check_winner()

def restart():
    st.session_state.board = [""] * 9
    st.session_state.turn = "X"
    st.session_state.winner = None
    st.session_state.winning_cells = []

def reset_score():
    st.session_state.score = {"X": 0, "O": 0, "Draw": 0}
    restart()

# ---------------- DISPLAY BOARD ---------------- #
st.write("")

cols = st.columns(3, gap="small")
for i in range(9):
    style = "font-size:40px; height:80px; border-radius:12px;"
    if i in st.session_state.winning_cells:
        style += "background-color:#90EE90; font-weight:bold;"  # highlight winner
    elif st.session_state.board[i] == "X":
        style += "color:#FF4B4B; font-weight:bold;"
    elif st.session_state.board[i] == "O":
        style += "color:#1E90FF; font-weight:bold;"

    with cols[i % 3]:
        st.button(
            st.session_state.board[i] if st.session_state.board[i] != "" else " ",
            key=f"cell-{i}",
            on_click=play_move,
            args=(i,),
            use_container_width=True,
            help=f"Cell {i+1}",
        )
        st.markdown(f"""
        <style>
        div[data-testid="stButton"][key="cell-{i}"] button {{
            {style}
        }}
        </style>
        """, unsafe_allow_html=True)

    if i % 3 == 2 and i != 8:
        cols = st.columns(3, gap="small")

# ---------------- STATUS ---------------- #
st.write("")
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.success("🤝 It's a Draw!")
    else:
        st.success(f"🏆 Player {st.session_state.winner} wins!")
else:
    st.info(f"👉 Next Turn: Player **{st.session_state.turn}**")

# ---------------- SCOREBOARD ---------------- #
st.write("### 📊 Scoreboard")
st.table(st.session_state.score)

# ---------------- CONTROLS ---------------- #
col1, col2 = st.columns(2)
with col1:
    st.button("🔄 Restart Game", on_click=restart, use_container_width=True)
with col2:
    st.button("🗑️ Reset Scoreboard", on_click=reset_score, use_container_width=True)
