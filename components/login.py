import streamlit as st
from wallet_connect import wallet_connect
from data import database
import sqlite3
from datetime import datetime

def connect():
    """Handles wallet connection and ensures data is saved in the database."""
    wc = wallet_connect(label="wallet", key="wallet")
    if wc:
        if wc == True:
            wallet_address = wc.get_address()  # Retrieve the wallet address
            st.sidebar.success(f"Connected: {wallet_address}")

            # Check if user already exists in the database
            if not database.check_user_exists(wallet_address):
                # Auto-generate password and register the user
                password = ''.join([wallet_address[-6], wallet_address[-5], wallet_address[-2], wallet_address[-1]])
                activity = "Auto Signup"
                database.add_user(wallet_address, password, activity, name="Auto Registered")

                st.sidebar.success(f"🆕 Auto-registered with password: {password}")
            else:
                # Update the activity for existing user
                conn = sqlite3.connect(database.DB_NAME)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE log_book SET 
                    datetime = ?, 
                    activity = ? 
                    WHERE metamask_account = ?
                """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Wallet Reconnected", wallet_address))
                conn.commit()
                conn.close()
                st.sidebar.success("Welcome back! Wallet reconnected.")

            # Save user data in session state
            st.session_state.wallet_address = wallet_address
            st.session_state.logged_in = True
            st.session_state.user_name = wallet_address  # Optional: Replace with actual name if available
        else:
            st.sidebar.warning("Please connect your wallet.")

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
