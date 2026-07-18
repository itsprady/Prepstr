import streamlit as st
import time
from database import get_questions_for_test, get_test
from database import save_result


def show():
    st.title('Mock Test')
    if not st.session_state.user:
        st.warning('Please login first')
        return
    if not st.session_state.test_in_progress:
        st.info('No test selected. Choose a test from Dashboard to start.')
        return
    test_id = st.session_state.test_in_progress
    test = get_test(test_id)
    questions = get_questions_for_test(test_id)
    if not questions:
        st.error('No questions found for this test')
        return

    if 'q_index' not in st.session_state:
        st.session_state.q_index = 0
        st.session_state.answers = {i: None for i in range(len(questions))}
        st.session_state.start_time = time.time()

    st.header(test['title'])
    st.write(f"Time: {test['time_limit']} minutes | Negative marking: {test['negative_marking']}")

    q = questions[st.session_state.q_index]
    st.markdown(f"**Q{st.session_state.q_index+1}. {q['question']}**")
    opts = [q['option1'], q['option2'], q['option3'], q['option4']]
    choice = st.radio('Choose', options=opts, index=st.session_state.answers[st.session_state.q_index]-1 if st.session_state.answers[st.session_state.q_index] else 0)
    # Map back to index
    sel_index = opts.index(choice) + 1
    st.session_state.answers[st.session_state.q_index] = sel_index

    col1, col2, col3 = st.columns(3)
    if col1.button('Previous'):
        if st.session_state.q_index > 0:
            st.session_state.q_index -= 1
    if col2.button('Next'):
        if st.session_state.q_index < len(questions) - 1:
            st.session_state.q_index += 1
    if col3.button('Flag/Bookmark'):
        st.info('Flagged (UI only)')

    if st.button('Submit Test'):
        # grading
        correct = 0
        wrong = 0
        for i, qq in enumerate(questions):
            ans = st.session_state.answers.get(i)
            if ans is None:
                continue
            if ans == qq['correct_option']:
                correct += 1
            else:
                wrong += 1
        total = len(questions)
        score = correct - (wrong * test['negative_marking'])
        accuracy = (correct / total) * 100 if total > 0 else 0
        time_taken = int(time.time() - st.session_state.start_time)
        save_result(st.session_state.user['id'], test_id, score, correct, wrong, accuracy, time_taken)
        st.success(f'Test submitted. Score: {score}. Accuracy: {accuracy:.2f}%')
        st.session_state.test_in_progress = None
        # Reset indices
        del st.session_state.q_index
        del st.session_state.answers
        del st.session_state.start_time
        st.experimental_rerun()
