import streamlit as st
from database import get_overview_stats, get_tests, add_test, add_question, get_questions_for_test
import pandas as pd
from utils import load_questions_from_csv


def show():
    st.title('Admin Dashboard')
    # Very simple admin gating by is_admin flag
    user = st.session_state.user
    if not user or user.get('is_admin') == 0:
        st.warning('Admin access only')
        return

    stats = get_overview_stats()
    st.metric('Total Users', stats['users'])
    st.metric('Total Tests', stats['tests'])
    st.metric('Total Questions', stats['questions'])
    st.metric('Attempts', stats['attempts'])

    st.subheader('Create Test')
    title = st.text_input('Title')
    subject = st.text_input('Subject')
    time_limit = st.number_input('Time limit (minutes)', value=10)
    neg = st.number_input('Negative marking (per wrong)', value=0.0)
    if st.button('Create Test'):
        tid = add_test(title, subject, time_limit, neg)
        st.success(f'Created test {tid}')

    st.subheader('Import Questions from CSV')
    uploaded = st.file_uploader('CSV file', type=['csv'])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        tmp = 'temp_import.csv'
        df.to_csv(tmp, index=False)
        tid, cnt = load_questions_from_csv(tmp, title=title or 'Imported', subject=subject or 'General', time_limit=time_limit, negative_marking=neg)
        st.success(f'Imported {cnt} questions into test {tid}')

    st.subheader('Existing Tests')
    tests = get_tests()
    for t in tests:
        st.write(f"{t['test_id']}: {t['title']} ({t['subject']}) - {t['total_questions']} qs")
        qs = get_questions_for_test(t['test_id'])
        if qs:
            for q in qs[:5]:
                st.write('-', q['question'])

