import streamlit as st
from auth import create_user
from database import get_user_by_username


def show():
    st.title('Signup')
    name = st.text_input('Full name')
    username = st.text_input('Username')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    password2 = st.text_input('Confirm Password', type='password')

    if st.button('Create account'):
        if not all([name, username, email, password, password2]):
            st.error('Fill all fields')
            return
        if password != password2:
            st.error('Passwords do not match')
            return
        if get_user_by_username(username):
            st.error('Username already exists')
            return
        uid = create_user(name, username, email, password)
        if uid:
            st.success('Account created. Go to Login')
        else:
            st.error('Could not create account')
