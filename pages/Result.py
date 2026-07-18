import streamlit as st
from database import get_results_by_user


def show():
    st.title('Results')
    if not st.session_state.user:
        st.warning('Please login first')
        return
    results = get_results_by_user(st.session_state.user['id'])
    if not results:
        st.info('No results yet')
        return
    for r in results:
        st.write(f"Test: {r['title']} | Score: {r['score']} | Accuracy: {r['accuracy']:.2f}% | Date: {r['date']}")
