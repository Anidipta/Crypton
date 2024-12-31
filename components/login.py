import streamlit as st
from wallet_connect import wallet_connect
from data import database
import sqlite3
from datetime import datetime

def connect():
    """Handles wallet connection and ensures data is saved in the database."""
    wc = wallet_connect(label="wallet", key="wallet")
    
    if wc and hasattr(wc, 'get_address'):
        wallet_address = wc.get_address()
        if wallet_address:
            st.sidebar.success(f"Connected: {wallet_address}")
            
            # Check if user exists and handle registration
            if not database.check_user_exists(wallet_address):
                password = ''.join([str(wallet_address[-6]), str(wallet_address[-5]), 
                                  str(wallet_address[-2]), str(wallet_address[-1])])
                database.add_user(wallet_address, password, "Auto Signup", name="Auto Registered")
                st.sidebar.success(f"🆕 Auto-registered with password: {password}")
            
            # Update activity log
            conn = sqlite3.connect(database.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO log_book (metamask_account, datetime, activity)
                VALUES (?, ?, ?)
            """, (wallet_address, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                  "Auto Login" if database.check_user_exists(wallet_address) else "Auto Signup"))
            conn.commit()
            conn.close()
            
            # Set session state
            st.session_state.wallet_address = wallet_address
            st.session_state.logged_in = True
            st.session_state.user_name = wallet_address
            st.session_state.page = "Dashboard"
            
            return True
    
    st.sidebar.warning("Please connect your wallet.")
    return False

def login():
    """Renders the login form."""
    st.sidebar.markdown("### Login")
    login_address = st.sidebar.text_input("Metamask Address")
    login_password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if database.validate_user(login_address, login_password):
            st.session_state.wallet_address = login_address
            st.session_state.logged_in = True
            st.session_state.user_name = login_address
            st.sidebar.success("Logged in successfully!")

            # Log the activity as 'Login' in the database
            conn = sqlite3.connect(database.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE log_book SET 
                datetime = ?, 
                activity = ? 
                WHERE metamask_account = ?
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Login", login_address))
            conn.commit()
            conn.close()

        else:
            st.sidebar.error("Invalid credentials. Please try again.")

def signup():
    """Renders the signup form."""
    st.sidebar.markdown("### Sign Up")
    signup_name = st.sidebar.text_input("Name")
    signup_address = st.sidebar.text_input("Metamask Address")
    signup_password = st.sidebar.text_input("Password (4 digits)", type="password")

    if st.sidebar.button("Sign Up"):
        if database.check_user_exists(signup_address):
            st.sidebar.error("Account exists. Please login.")
        elif len(signup_password) != 4 or not signup_password.isdigit():
            st.sidebar.error("Password must be exactly 4 digits.")
        else:
            database.add_user(signup_address, signup_password, "Manual Signup", signup_name)
            st.sidebar.success("Account created successfully! Please login.")
