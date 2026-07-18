import streamlit as st
from database import get_user_by_username, init_db
from auth import check_password, ensure_admin, create_user


def show():
    st.title('Login')
    init_db()
    ensure_admin()

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        user = get_user_by_username(username)
        if user and check_password(password, user['password_hash']):
            st.session_state.user = dict(user)
            st.success('Logged in as ' + username)
        else:
            st.error('Invalid credentials')

    st.info("Don't have an account? Go to Signup")
