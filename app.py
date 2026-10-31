
import streamlit as st
from quiz_generator import generate_quiz

st.set_page_config(
    page_title="AI Quiz Master",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 AI Quiz Master")
st.subheader("Test Your Knowledge with AI!")
st.write("Generate a quiz on any topic and challenge yourself.")

# Initialize session variables
if "questions" not in st.session_state:
    st.session_state.questions = []

if "current" not in st.session_state:
    st.session_state.current = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

if "finished" not in st.session_state:
    st.session_state.finished = False

# Quiz settings
st.sidebar.header("⚙️ Quiz Settings")

topic = st.sidebar.text_input(
    "Enter Quiz Topic",
    placeholder="e.g. Python, AI, Science"
)

difficulty = st.sidebar.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

number = st.sidebar.number_input(
    "Number of Questions",
    min_value=3,
    max_value=10,
    value=5
)

# Generate quiz
if st.sidebar.button("✨ Generate Quiz", use_container_width=True):

    if not topic.strip():
        st.sidebar.warning("Please enter a topic.")

    else:
        with st.spinner("AI is preparing your quiz..."):
            try:
                questions = generate_quiz(
                    topic, difficulty, number
                )

                st.session_state.questions = questions
                st.session_state.current = 0
                st.session_state.score = 0
                st.session_state.submitted = False
                st.session_state.selected_answer = None
                st.session_state.finished = False

                st.rerun()

            except Exception as e:
                st.error(f"Quiz generation failed: {e}")

# Display quiz
questions = st.session_state.questions

if questions and not st.session_state.finished:

    current = st.session_state.current
    question = questions[current]

    st.divider()

    st.write(
        f"**Question {current + 1} of {len(questions)}**"
    )

    st.progress((current + 1) / len(questions))

    st.subheader(question["question"])

    selected = st.radio(
        "Choose your answer:",
        question["options"],
        index=None,
        key=f"option_{current}",
        disabled=st.session_state.submitted
    )

    # Submit answer
    if not st.session_state.submitted:

        if st.button("Submit Answer", type="primary"):

            if selected is None:
                st.warning("Please select an answer.")

            else:
                st.session_state.selected_answer = selected

                if selected == question["answer"]:
                    st.session_state.score += 1

                st.session_state.submitted = True
                st.rerun()

    # Show answer and explanation
    if st.session_state.submitted:

        if st.session_state.selected_answer == question["answer"]:
            st.success("Correct Answer! 🎉")
        else:
            st.error(
                f"Incorrect! Correct answer: {question['answer']}"
            )

        st.info(f"Explanation: {question['explanation']}")

        if current + 1 < len(questions):
            if st.button("Next Question ➡️", type="primary"):
                st.session_state.current += 1
                st.session_state.submitted = False
                st.session_state.selected_answer = None
                st.rerun()

        else:
            if st.button("Finish Quiz 🏆", type="primary"):
                st.session_state.finished = True
                st.rerun()

# Final result
if st.session_state.finished:

    total = len(st.session_state.questions)
    score = st.session_state.score

    st.balloons()
    st.divider()
    st.title("🏆 Quiz Completed!")

    st.metric("Your Score", f"{score} / {total}")

    percentage = (score / total) * 100

    st.progress(percentage / 100)

    st.write(f"**Accuracy:** {percentage:.1f}%")

    if percentage >= 80:
        st.success("Excellent work! 🌟")
    elif percentage >= 50:
        st.info("Good job! Keep practising.")
    else:
        st.warning("Keep learning. You can do better!")

    if st.button("🔄 Play Again"):
        st.session_state.questions = []
        st.session_state.current = 0
        st.session_state.score = 0
        st.session_state.submitted = False
        st.session_state.selected_answer = None
        st.session_state.finished = False
        st.rerun()

else:
    if not questions:
        st.info(
            "👈 Enter a topic, select difficulty "
            "and click Generate Quiz to begin!"
        )
