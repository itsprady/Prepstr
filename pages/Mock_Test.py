import streamlit as st
import time
import random
from database import get_questions_for_test, get_test, save_result


def _grade_and_save(session):
    questions = session['questions']
    corrects = session['corrects']
    answers = session['answers']
    test = session['test']

    correct = 0
    wrong = 0
    total = len(questions)
    for i in range(total):
        ans = answers[i]
        if ans is None:
            continue
        if ans == corrects[i]:
            correct += 1
        else:
            wrong += 1
    score = correct - (wrong * test['negative_marking'])
    accuracy = (correct / total) * 100 if total > 0 else 0
    time_taken = int(time.time() - session['start_time'])
    # persist
    save_result(st.session_state.user['id'], test['test_id'], score, correct, wrong, accuracy, time_taken)
    return score, accuracy, correct, wrong, time_taken


def show():
    st.title('Mock Test')
    if not st.session_state.user:
        st.warning('Please login first')
        return
    if not st.session_state.get('test_in_progress'):
        st.info('No test selected. Choose a test from Dashboard to start.')
        return

    test_id = int(st.session_state.test_in_progress)
    test = get_test(test_id)
    questions_rows = get_questions_for_test(test_id)
    if not questions_rows:
        st.error('No questions found for this test')
        return

    # Initialize session for this test if not present or different test
    if 'test_session' not in st.session_state or st.session_state.test_session.get('test_id') != test_id:
        # shuffle questions
        qs = [dict(q) for q in questions_rows]
        random.shuffle(qs)
        questions = []
        options_shuffled = []
        corrects = []
        for q in qs:
            opts = [q['option1'], q['option2'], q['option3'], q['option4']]
            indexed_opts = list(enumerate(opts, start=1))  # (original_index, text)
            random.shuffle(indexed_opts)
            shuffled_texts = [t for (_, t) in indexed_opts]
            # find new correct index (0-based)
            orig_correct = q['correct_option']
            new_correct = None
            for idx, (orig_idx, _) in enumerate(indexed_opts):
                if orig_idx == orig_correct:
                    new_correct = idx
                    break
            questions.append(q)
            options_shuffled.append(shuffled_texts)
            corrects.append(new_correct)

        st.session_state.test_session = {
            'test_id': test_id,
            'test': dict(test),
            'questions': questions,
            'options': options_shuffled,
            'corrects': corrects,
            'answers': [None] * len(questions),
            'bookmarked': set(),
            'q_index': 0,
            'start_time': time.time(),
            'time_limit': int(test['time_limit']) * 60,
            'review_mode': False,
        }

    session = st.session_state.test_session
    total_q = len(session['questions'])

    # Timer
    now = time.time()
    end_time = session['start_time'] + session['time_limit']
    remaining = int(end_time - now)
    if remaining <= 0:
        # auto-submit
        score, accuracy, correct, wrong, time_taken = _grade_and_save(session)
        st.success(f'Time is up — test auto-submitted. Score: {score}. Accuracy: {accuracy:.2f}%')
        # cleanup
        st.session_state.test_in_progress = None
        del st.session_state.test_session
        return

    mins = remaining // 60
    secs = remaining % 60
    st.markdown(f"**Time left:** {mins:02d}:{secs:02d}")

    # Question palette
    st.markdown('### Question Palette')
    cols = st.columns(10)
    for i in range(total_q):
        status = ''
        if session['answers'][i] is not None:
            status = '✅'
        elif i in session['bookmarked']:
            status = '⚑'
        label = f"{i+1} {status}"
        col = cols[i % 10]
        if col.button(label, key=f'qp_{i}'):
            session['q_index'] = i
            st.experimental_rerun()

    st.write('---')
    q_index = session['q_index']
    q = session['questions'][q_index]
    opts = session['options'][q_index]

    st.markdown(f"**Q{q_index+1}. {q['question']}**")

    display_opts = ['-- Select --'] + opts
    current_answer = session['answers'][q_index]
    selected_text = None
    if current_answer is not None:
        selected_text = display_opts[current_answer + 1]
        sel_index = current_answer + 1
    else:
        sel_index = 0

    choice = st.radio('Choose', display_opts, index=sel_index, key=f'choice_{q_index}')
    if choice != '-- Select --':
        sel_idx = display_opts.index(choice) - 1
        session['answers'][q_index] = sel_idx
    else:
        session['answers'][q_index] = None

    # Bookmark / Flag
    col1, col2, col3, col4 = st.columns(4)
    if col1.button('Previous'):
        if session['q_index'] > 0:
            session['q_index'] -= 1
            st.experimental_rerun()
    if col2.button('Next'):
        if session['q_index'] < total_q - 1:
            session['q_index'] += 1
            st.experimental_rerun()
    if col3.button('Toggle Bookmark'):
        if q_index in session['bookmarked']:
            session['bookmarked'].remove(q_index)
        else:
            session['bookmarked'].add(q_index)
    if col4.button('Review'):
        session['review_mode'] = True
        st.experimental_rerun()

    st.write('---')

    # Review mode
    if session.get('review_mode'):
        st.markdown('## Review your answers')
        for i, qq in enumerate(session['questions']):
            user_ans = session['answers'][i]
            user_ans_text = session['options'][i][user_ans] if user_ans is not None else 'Not answered'
            st.write(f"Q{i+1}. {qq['question']}")
            st.write(f"Your answer: **{user_ans_text}**")
            if st.button(f'Go to Q{i+1}', key=f'goto_{i}'):
                session['q_index'] = i
                session['review_mode'] = False
                st.experimental_rerun()
            st.write('---')

        if st.button('Final Submit'):
            score, accuracy, correct, wrong, time_taken = _grade_and_save(session)
            st.success(f'Test submitted. Score: {score}. Accuracy: {accuracy:.2f}%')
            # cleanup
            st.session_state.test_in_progress = None
            del st.session_state.test_session
            st.experimental_rerun()

    # Normal view: allow manual submit
    if st.button('Submit Test'):
        # show confirmation
        confirm = st.confirm if hasattr(st, 'confirm') else None
        # grade
        score, accuracy, correct, wrong, time_taken = _grade_and_save(session)
        st.success(f'Test submitted. Score: {score}. Accuracy: {accuracy:.2f}%')
        st.session_state.test_in_progress = None
        del st.session_state.test_session
        st.experimental_rerun()
