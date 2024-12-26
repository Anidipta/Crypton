import streamlit as st
from components import dashboard, games, lessons

st.title("Crypton: Learn Blockchain Through Games")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Lessons", "Games"])

if page == "Dashboard":
    dashboard.display()
elif page == "Lessons":
    lessons.display()
elif page == "Games":
    games.display()
