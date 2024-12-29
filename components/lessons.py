import streamlit as st
from data.database import update_activity_progress, get_user_progress

# Lesson content database
LESSONS = {
    1: {
        "title": "Introduction to Blockchain",
        "emoji": "🔗",
        "sections": [
            {
                "title": "What is Blockchain?",
                "content": """
                A blockchain is a distributed digital ledger that stores data in blocks that are linked together chronologically.
                
                Key characteristics:
                - Decentralized
                - Immutable
                - Transparent
                - Secure
                
                Think of it as a chain of digital 'blocks' containing information, where each block is connected to the ones before and after it.
                """,
                "quiz": [
                    {
                        "question": "What is the main characteristic of blockchain technology?",
                        "options": [
                            "Centralized control",
                            "Decentralized structure",
                            "Single point of failure",
                            "Editable records"
                        ],
                        "correct": 1
                    }
                ]
            },
            {
                "title": "How Blockchain Works",
                "content": """
                Blockchain operates through a network of computers (nodes) that all maintain the same record of transactions.
                
                Process:
                1. Transaction is initiated
                2. Transaction is broadcast to network
                3. Nodes validate the transaction
                4. Transaction is added to a block
                5. Block is added to the chain
                """,
                "quiz": [
                    {
                        "question": "What must happen before a transaction is added to the blockchain?",
                        "options": [
                            "It must be validated by nodes",
                            "It must be printed on paper",
                            "It must be encrypted only",
                            "It must be deleted first"
                        ],
                        "correct": 0
                    }
                ]
            },
            {
                "title": "Blockchain Applications",
                "content": """
                Blockchain technology has numerous real-world applications across various industries.
                
                Common applications:
                - Cryptocurrency
                - Supply Chain Management
                - Healthcare Records
                - Voting Systems
                - Smart Contracts
                """,
                "quiz": [
                    {
                        "question": "Which is a real-world application of blockchain?",
                        "options": [
                            "Word Processing",
                            "Video Gaming only",
                            "Cryptocurrency",
                            "Email Service"
                        ],
                        "correct": 2
                    }
                ]
            }
        ]
    },
    2: {
        "title": "Cryptography Basics",
        "emoji": "🔐",
        "sections": [
            {
                "title": "Public Key Cryptography",
                "content": """
                Public key cryptography is a fundamental concept in blockchain technology.
                
                Key Components:
                - Public Key: Shared with everyone
                - Private Key: Kept secret
                - Digital Signatures
                - Encryption/Decryption
                """,
                "quiz": [
                    {
                        "question": "Which key must be kept secret in public key cryptography?",
                        "options": [
                            "Public Key",
                            "Private Key",
                            "Master Key",
                            "Shared Key"
                        ],
                        "correct": 1
                    }
                ]
            },
            {
                "title": "Hash Functions",
                "content": """
                Hash functions are crucial for blockchain security and data integrity.
                
                Properties:
                - One-way function
                - Deterministic
                - Fast computation
                - Avalanche effect
                """,
                "quiz": [
                    {
                        "question": "What is a key property of hash functions?",
                        "options": [
                            "Reversible",
                            "Random output",
                            "Deterministic",
                            "Slow computation"
                        ],
                        "correct": 2
                    }
                ]
            },
            {
                "title": "Digital Signatures",
                "content": """
                Digital signatures provide authentication and non-repudiation in blockchain.
                
                Uses:
                - Transaction verification
                - Identity proof
                - Message authentication
                - Smart contract execution
                """,
                "quiz": [
                    {
                        "question": "What is the main purpose of digital signatures?",
                        "options": [
                            "Data encryption",
                            "Authentication",
                            "Data storage",
                            "Network speed"
                        ],
                        "correct": 1
                    }
                ]
            }
        ]
    }
}

def display_progress_bar(current_lesson, current_section, total_sections):
    progress = current_section / total_sections
    st.progress(progress)
    st.markdown(f"""
        <div style='text-align: center; color: #666;'>
            Section {current_section} of {total_sections}
        </div>
    """, unsafe_allow_html=True)

def display_completion_certificate(lesson_number, wallet_address):
    st.markdown(f"""
        <div style='background-color: rgba(30, 30, 30, 0.9); padding: 20px; border-radius: 10px; text-align: center;
             border: 2px solid; border-image: linear-gradient(45deg, #ff6b6b, #4ecdc4) 1;'>
            <h2 style='color: #4ecdc4;'>🎉 Congratulations!</h2>
            <p style='color: #fff;'>You've completed Lesson {lesson_number}: {LESSONS[lesson_number]['title']}</p>
            <p style='color: #888;'>Wallet Address: {wallet_address[:6]}...{wallet_address[-4:]}</p>
            <div style='background-color: rgba(40, 40, 40, 0.9); padding: 10px; border-radius: 5px; margin-top: 10px;'>
                <p style='color: #4ecdc4;'>✅ Achievement Unlocked: {LESSONS[lesson_number]['emoji']} {LESSONS[lesson_number]['title']} Master</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def handle_navigation():
    # Get current state
    current_lesson = st.session_state.current_lesson
    current_section = st.session_state.current_section
    total_sections = len(LESSONS[current_lesson]['sections'])
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_section > 0:
            if st.button("← Previous", key=f"prev_{current_lesson}_{current_section}", use_container_width=True):
                st.session_state.current_section -= 1
                st.rerun()
    
    with col3:
        if current_section < total_sections - 1:
            if st.button("Next →", key=f"next_{current_lesson}_{current_section}", use_container_width=True):
                st.session_state.current_section += 1
                st.rerun()

def render_quiz(quiz, lesson_number, section_idx, wallet_address):
    st.markdown("### 📝 Knowledge Check")
    
    for idx, question in enumerate(quiz):
        st.markdown(f"""
            <div style='background-color: rgba(40, 40, 40, 0.9); padding: 15px; border-radius: 5px; margin: 10px 0;
                 border: 1px solid; border-image: linear-gradient(45deg, #ff6b6b, #4ecdc4) 1;'>
                <p style='color: #fff; font-weight: bold;'>{question['question']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        answer = st.radio(
            "Select your answer:",
            question['options'],
            key=f"quiz_{lesson_number}_{section_idx}_{idx}"
        )
        
        if st.button("Check Answer", key=f"check_{lesson_number}_{section_idx}_{idx}"):
            if answer == question['options'][question['correct']]:
                st.success("✅ Correct! Well done!")
                progress_percentage = ((section_idx + 1) * 100) // len(LESSONS[lesson_number]['sections'])
                update_activity_progress(
                    wallet_address=wallet_address,
                    activity_type="lesson",
                    sl_no=lesson_number,
                    completion=progress_percentage,
                    points=10
                )
            else:
                st.error("❌ Try again!")

def lessons(wallet_address):
    # Custom styling
    st.markdown("""
        <style>
            .stApp {
                color: #ffffff;
            }
            .lesson-card {
                background-color: rgba(30, 30, 30, 0.9);
                padding: 20px;
                border-radius: 10px;
                border: 2px solid;
                border-image: linear-gradient(45deg, #ff6b6b, #4ecdc4) 1;
                margin: 10px 0;
                transition: transform 0.2s;
            }
            .lesson-card:hover {
                transform: translateY(-2px);
            }
            .section-content {
                background-color: rgba(40, 40, 40, 0.9);
                padding: 20px;
                border-radius: 8px;
                margin: 10px 0;
                border: 1px solid;
                border-image: linear-gradient(45deg, #ff6b6b, #4ecdc4) 1;
                color: #ffffff;
            }
            .stButton button {
                color: white;
                border: none;
            }
            .stProgress > div > div {
                background-color: #4ecdc4;
            }
        </style>
    """, unsafe_allow_html=True)

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("📚 Blockchain Learning Path")
        st.markdown("### Your Journey to Blockchain Mastery")

        # Get user progress
        progress = get_user_progress(wallet_address, "lesson")
        
        # Initialize session state for lesson navigation
        if 'current_lesson' not in st.session_state:
            st.session_state.current_lesson = 1
            st.session_state.current_section = 0

        # Lesson selection
        col1, col2 = st.columns([3, 1])
        with col1:
            lesson_choice = st.selectbox(
                "Select a Lesson",
                range(1, len(LESSONS) + 1),
                format_func=lambda x: f"{LESSONS[x]['emoji']} Lesson {x}: {LESSONS[x]['title']}"
            )
            st.session_state.current_lesson = lesson_choice
        
        with col2:
            current_progress = progress.get('current_progress', 0)
            st.markdown(f"""
                <div style='padding: 20px; text-align: center; background-color: rgba(30, 30, 30, 0.9); 
                     border-radius: 10px; border: 2px solid; border-image: linear-gradient(45deg, #ff6b6b, #4ecdc4) 1;'>
                    <h4 style='color: #4ecdc4;'>Progress</h4>
                    <h2 style='color: #ffffff;'>{current_progress}%</h2>
                </div>
            """, unsafe_allow_html=True)

        # Display lesson content
        current_lesson = LESSONS[lesson_choice]
        st.markdown(f"""
            <div class='lesson-card'>
                <h2 style='color: #4ecdc4;'>{current_lesson['emoji']} {current_lesson['title']}</h2>
                <p style='color: #ffffff;'>Number of sections: {len(current_lesson['sections'])}</p>
                <p style='color: #ffffff;'>Points available: {len(current_lesson['sections']) * 10}</p>
            </div>
        """, unsafe_allow_html=True)

        # Reset section when changing lessons
        if 'prev_lesson' not in st.session_state or st.session_state.prev_lesson != lesson_choice:
            st.session_state.current_section = 0
            st.session_state.prev_lesson = lesson_choice

        current_section = current_lesson['sections'][st.session_state.current_section]
        
        # Display progress bar
        display_progress_bar(
            lesson_choice,
            st.session_state.current_section + 1,
            len(current_lesson['sections'])
        )

        # Display section content
        st.markdown(f"""
            <div class='section-content'>
                <h3 style='color: #4ecdc4;'>{current_section['title']}</h3>
                {current_section['content']}
            </div>
        """, unsafe_allow_html=True)

        # Display quiz
        if 'quiz' in current_section:
            render_quiz(
                current_section['quiz'],
                lesson_choice,
                st.session_state.current_section,
                wallet_address
            )

        # Navigation buttons
        handle_navigation()

        # Check if lesson is completed
        if current_progress == 100:
            display_completion_certificate(lesson_choice, wallet_address)

    else:
        st.warning("🔒 Please connect your wallet to access the lessons.")
        st.markdown("""
            <div style='text-align: center; padding: 20px; background-color: rgba(30, 30, 30, 0.9); 
                 border-radius: 10px; border: 2px solid; border-image: linear-gradient(45deg, #ff6b6b, #4ecdc4) 1;'>
                <h3 style='color: #4ecdc4;'>Why Learn with Us?</h3>
                <ul style='list-style-type: none; color: #ffffff;'>
                    <li>🎮 Interactive Learning</li>
                    <li>🏆 Earn While You Learn</li>
                    <li>📊 Track Your Progress</li>
                    <li>🎓 Expert-Curated Content</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
