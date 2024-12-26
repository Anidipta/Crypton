import streamlit as st

def dashboard(wallet_address):
    st.title("📊 Dashboard")
    
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # Get user activities and display them in a Pinterest-like layout
        st.write(f"Welcome back, {st.session_state.user_name}!")
        
        # Example of showing activities with text boxes, graphs, etc.
        st.markdown("### Your Previous Activities:")
        
        # Example grid layout (Pinterest-like)
        activity_data = [
            {"title": "Activity 1", "description": "Description of activity 1", "date": "2024-12-01"},
            {"title": "Activity 2", "description": "Description of activity 2", "date": "2024-12-05"},
            {"title": "Activity 3", "description": "Description of activity 3", "date": "2024-12-10"},
        ]
        
        # Using columns to create a Pinterest-like layout
        for activity in activity_data:
            with st.container():
                st.markdown(f"### {activity['title']}")
                st.markdown(f"**Date:** {activity['date']}")
                st.write(activity["description"])
                st.markdown("---")
        
    else:
        # Title and Subtitle
        st.title("🪙 Crypton: Learn Blockchain Through Games")
        st.subheader("Explore Blockchain concepts through interactive lessons and fun games!")

        st.write("Please log in to view your dashboard.")

