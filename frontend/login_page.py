import streamlit as st
from services.api import login_user, register_user

def show_login_page():
    st.subheader("Login / Sign Up")

    with st.form("auth_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            login_btn = st.form_submit_button("Login", use_container_width=True)

        with col2:
            signup_btn = st.form_submit_button("Sign Up", use_container_width=True)

    if login_btn:
        response = login_user(email, password)
        if response.status_code == 200:
            user_data = response.json()
            st.session_state.logged_in = True
            st.session_state.username = user_data["name"]
            st.session_state.user_id = user_data["user_id"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid email or password")

    if signup_btn:
        response = register_user(name, email, password)
        if response.status_code == 200:
            st.success("Account created successfully")
        else:
            st.error(response.json().get("detail", "Sign up failed"))