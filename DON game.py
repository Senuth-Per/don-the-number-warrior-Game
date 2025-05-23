import streamlit as st
import random
import datetime

# Function to determine number range based on attempt level
def number_range(attempt):
    if attempt <= 5:
        return 15, 100
    elif attempt <= 10:
        return 250, 2000
    elif attempt <= 15:
        return 3000, 10000
    else:
        return 20000, 100000

# Generate a unique filename for the game log
def get_file_name():
    current_date = datetime.datetime.now().strftime("%Y_%m_%d")
    current_time = datetime.datetime.now().strftime("%H_%M_%S")
    text_id = random.randint(0, 9999)
    return f"{current_date}_{current_time}_{text_id}.txt"

# Write game progress to a file
def write_game_log(file_name, game_data):
    with open(file_name, "w") as f:
        for line in game_data:
            f.write(line + "\n")

# Game instructions
st.title("🧠 DON: The Number Warrior")
st.markdown("""
Welcome to the **DON's Realm** – a game where you must defeat evil numbers to ascend to the next dimension.

### 🎮 How to Play
- You are the legendary **DON**, battling through **20 dimensions**.
- Each round, you'll face 5 **enemy numbers** — Minions, Warriors, Elites, and Overlords depending on the level.
- Choose one number to attack:
  - If it is **less than or equal** to your **Life Score**, you WIN and absorb its strength!
  - If it is **greater**, you are defeated and the game ends.

### 💡 Tips for Victory
- Think strategically. Sometimes the smallest enemy can be the deadliest.
- Choose enemies divisible by **13** for bonus Life Points!
- **Streak Bonus:** Win 3 rounds in a row for a power boost.
- Beware! The enemies grow stronger as you ascend.

🔥 Prove yourself and become the ultimate **DON of Numbers**!
""")

# Session state setup
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.player_name = ""
    st.session_state.life_score = random.randint(1, 50)
    st.session_state.attempt = 1
    st.session_state.log = []
    st.session_state.enemies = []
    st.session_state.last_result = ""
    st.session_state.game_over = False

# Restart button
if st.button("🔄 Restart Game"):
    st.session_state.clear()
    st.rerun()

# Player name input
if not st.session_state.game_started:
    name = st.text_input("Enter your name, brave DON:")
    if name:
        st.session_state.player_name = name
        st.session_state.game_started = True
        st.success(f"Welcome DON {name}! Your journey begins.")
        st.rerun()

# Main game logic
if st.session_state.game_started and not st.session_state.game_over:
    st.subheader(f"👑 DON {st.session_state.player_name}")
    st.markdown(f"**Life Score:** {st.session_state.life_score}")
    st.markdown(f"**Attempt:** {st.session_state.attempt} / 20")

    # Generate enemies for this attempt
    if not st.session_state.enemies:
        min_val, max_val = number_range(st.session_state.attempt)
        st.session_state.enemies = random.sample(range(min_val, max_val + 1), 5)

    st.markdown(f"### ⚔️ Enemy Numbers: {st.session_state.enemies}")

    choice = st.selectbox("Choose an enemy number to attack:", st.session_state.enemies)

    if st.button("Attack"):
        fight_number = choice
        if fight_number <= st.session_state.life_score:
            st.success(f"Bravo! You destroyed number {fight_number}.")
            bonus = 13 if fight_number % 13 == 0 else 0
            st.session_state.life_score += fight_number + bonus
            if bonus:
                st.info("✨ BONUS! You defeated a number divisible by 13!")
            result = "WON"
        else:
            st.error(f"Oh no! You were destroyed by {fight_number}.")
            result = "LOST"
            st.session_state.game_over = True

        # Log this round
        st.session_state.log.append(
            f"Attempt: {st.session_state.attempt}\n  Enemies: {st.session_state.enemies}\n  Chosen: {fight_number}\n  Status: {result}\n  Life Score: {st.session_state.life_score}"
        )

        st.session_state.last_result = result
        st.session_state.enemies = []
        if result == "WON":
            st.session_state.attempt += 1
        else:
            st.rerun()

        if st.session_state.attempt > 20:
            st.session_state.game_over = True

        st.rerun()

# Game summary
if st.session_state.game_over:
    st.header("🎯 Game Over")

    final_status = "WON" if st.session_state.attempt > 20 else "LOST"
    st.markdown(f"**DON {st.session_state.player_name}** - Final Life Score: {st.session_state.life_score}")
    st.markdown(f"**Attempts:** {st.session_state.attempt - 1}")
    st.markdown(f"**Final Result:** {final_status}")

    st.session_state.log.append(
        f"\nFinal Game Outcome: {final_status}\n  Total Attempts: {st.session_state.attempt - 1}\n  Final Life Score: {st.session_state.life_score}"
    )

    # Save log
    file_name = get_file_name()
    write_game_log(file_name, st.session_state.log)
    st.markdown(f"📝 Game log saved as: `{file_name}`")

    st.balloons()
