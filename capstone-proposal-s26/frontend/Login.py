import streamlit as st
from utils.session import init_session
from login_page import show_login_page
from upload_page import show_upload_page
from pages.Closet import show_closet_page
from Outfits import show_saved_outfits_page

st.set_page_config(page_title="Smart Closet", layout="wide")
init_session()


if st.session_state.logged_in:
    choice = st.sidebar.radio("Menu", ["Closet","Saved Outfits", "Upload", "Logout"])

    if choice == "Upload":
        show_upload_page()
    elif choice == "Closet":
        show_closet_page()
    elif choice == "Saved Outfits":
        show_saved_outfits_page()
    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_id = None
        st.rerun()
else:
    show_login_page()

