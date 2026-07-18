import streamlit as st
from database import get_tests, get_results_by_user


def show():
    st.title('Dashboard')
    if not st.session_state.user:
        st.warning('Please login first')
        return
    user = st.session_state.user
    st.subheader(f"Welcome, {user['name']}")

    st.markdown('### Available Tests')
    tests = get_tests()
    for t in tests:
        st.write(f"**{t['title']}** — {t['subject']} — {t['time_limit']} mins")
        col1, col2 = st.columns([1,3])
        with col1:
            if st.button('Start', key=f'start_{t['test_id']}'):
                st.session_state.test_in_progress = int(t['test_id'])
                st.experimental_rerun()
        with col2:
            st.write('')

    st.markdown('### Your Attempts')
    results = get_results_by_user(user['id'])
    if results:
        for r in results:
            st.write(f"{r['title']} — Score: {r['score']} — Accuracy: {r['accuracy']:.2f}% — Date: {r['date']}")
    else:
        st.write('No attempts yet')
