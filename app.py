
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Social Networks MCQ Quiz", layout="centered")

@st.cache_data
def load_questions():
    df = pd.read_csv("SN_clean.csv")
    return df

questions_df = load_questions()

quiz_size = 50
quiz_questions = questions_df.sample(n=quiz_size, random_state=random.randint(0, 9999)).reset_index(drop=True)

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "user_answers" not in st.session_state:
    st.session_state.user_answers = ["" for _ in range(quiz_size)]

st.title("🧠 Social Networks Quiz – NPTEL Practice")
st.markdown("Answer all 50 questions. You’ll get your score and correct answers at the end.")
st.markdown("---")

for i, row in quiz_questions.iterrows():
    st.subheader(f"Q{i+1}. {row['Question']}")
    options = [row['A'], row['B'], row['C'], row['D']]
    random.shuffle(options)
    answer = st.radio("", options, key=f"q{i}", index=-1, label_visibility="collapsed")
    st.session_state.user_answers[i] = answer

st.markdown("---")

if st.button("📤 Submit Quiz"):
    st.session_state.submitted = True

if st.session_state.submitted:
    score = 0
    st.subheader("📝 Quiz Results")
    for i, row in quiz_questions.iterrows():
        correct = row['Answer'].strip()
        user = st.session_state.user_answers[i]
        is_correct = user == correct
        if is_correct:
            score += int(row['Marks']) if 'Marks' in row else 1

        st.markdown(f"**Q{i+1}: {row['Question']}**")
        st.markdown(f"- Your Answer: {'✅ ' if is_correct else '❌ '}{user}")
        st.markdown(f"- Correct Answer: {correct}\n")

    st.success(f"🎉 You scored {score} out of 75")
    st.balloons()
