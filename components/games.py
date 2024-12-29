import streamlit as st
from data.database import update_activity_progress, get_user_progress  # Import database functions
import random
from datetime import datetime

def get_user_stats(wallet_address):
    """Get user's gaming statistics from database"""
    puzzle_progress = get_user_progress(wallet_address, 'Puzzle NFT Game')
    minesweeper_progress = get_user_progress(wallet_address, 'Minesweeper')
    return {
        'puzzle_nfts': puzzle_progress.get('completed', 0),
        'minesweeper_wins': minesweeper_progress.get('completed', 0),
        'total_revealed': minesweeper_progress.get('current_progress', 0)
    }

def display_how_to_play(game_type):
    with st.expander("📖 How to Play"):
        if game_type == "Puzzle NFT Game":
            st.markdown("""
            ### 🧩 Puzzle NFT Game Rules
            1. **Mint Pieces**: Click 'Mint Puzzle Piece' to collect unique NFT pieces
            2. **Place Pieces**: Use the 'Place Piece' buttons to arrange pieces on the board
            3. **Complete Puzzle**: Fill the entire board with unique pieces
            4. **Win Condition**: Collect and place all 9 unique pieces to win!
            
            *Each piece has a unique rarity value that affects its properties*
            """)
        else:
            st.markdown("""
            ### 💣 Minesweeper Rules
            1. **Goal**: Clear the board without hitting any mines
            2. **Numbers**: Indicate how many mines are adjacent to that cell
            3. **Strategy**: Use numbers to deduce mine locations
            4. **Win**: Reveal all safe cells without hitting mines
            
            *Tip: Start with corners and edges for better chances!*
            """)

def display_stats(wallet_address):
    stats = get_user_stats(wallet_address)
    
    st.sidebar.markdown("### 🏆 Your Gaming Stats")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.metric("NFTs Collected", stats['puzzle_nfts'])
        st.metric("Minesweeper Wins", stats['minesweeper_wins'])
    
    with col2:
        st.metric("Cells Revealed", stats['total_revealed'])
        completion_rate = (stats['total_revealed'] / 64 * 100) if stats['total_revealed'] > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")

def game1_puzzle_nft(wallet_address):
    st.title("🧩 Puzzle NFT Game")
    display_how_to_play("Puzzle NFT Game")
    
    if 'puzzle_board' not in st.session_state:
        st.session_state.puzzle_board = [0] * 9
        st.session_state.piece_collection = []
        st.session_state.game_started = False
    
    # Enhanced mint function with rarity colors
    def mint_puzzle_piece():
        if len(st.session_state.piece_collection) < 9:
            piece_type = random.randint(1, 9)
            rarity = random.randint(1, 100)
            
            while piece_type in [p['type'] for p in st.session_state.piece_collection]:
                piece_type = random.randint(1, 9)
            
            piece = {
                'type': piece_type,
                'rarity': rarity,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.piece_collection.append(piece)
            
            # Rarity-based success message
            if rarity > 90:
                st.success("🌟 LEGENDARY PIECE MINTED! 🌟")
            elif rarity > 70:
                st.info("✨ Rare piece minted!")
            else:
                st.success("New piece minted!")
            
            # Update database
            update_activity_progress(wallet_address, 'Puzzle NFT Game', 1, 
                                  len(st.session_state.piece_collection), 9)
        else:
            st.warning("Maximum pieces collected! Place them to complete the puzzle.")
    
    # Enhanced UI with columns and cards
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### 🎨 Mint New Pieces")
        if st.button("🎲 Mint Puzzle Piece", use_container_width=True):
            mint_puzzle_piece()
    
    with col2:
        st.markdown("### 🎯 Game Progress")
        progress = len([x for x in st.session_state.puzzle_board if x != 0]) / 9
        st.progress(progress)
        st.markdown(f"**Completed:** {progress*100:.1f}%")
    
    # Display piece collection in a grid
    st.markdown("### 🗃️ Your Collection")
    piece_cols = st.columns(3)
    for idx, piece in enumerate(st.session_state.piece_collection):
        with piece_cols[idx % 3]:
            rarity_color = "red" if piece['rarity'] > 90 else "orange" if piece['rarity'] > 70 else "blue"
            st.markdown(f"""
            <div style='padding: 10px; border: 2px solid {rarity_color}; border-radius: 5px; margin: 5px;'>
                <h4 style='color: {rarity_color};'>Piece #{piece['type']}</h4>
                Rarity: {piece['rarity']}%<br>
                Minted: {piece['timestamp']}
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced puzzle board display
    st.markdown("### 🎮 Puzzle Board")
    board_cols = st.columns(3)
    for i in range(9):
        with board_cols[i % 3]:
            piece_value = st.session_state.puzzle_board[i]
            if piece_value != 0:
                st.markdown(f"""
                <div style='padding: 20px; border-radius: 5px; text-align: center;'>
                    {piece_value}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style=' padding: 20px; border-radius: 5px; text-align: center;'>
                    -
                </div>
                """, unsafe_allow_html=True)
    
    # Place piece buttons
    st.markdown("### 🎯 Place Pieces")
    place_cols = st.columns(3)
    for idx, piece in enumerate(st.session_state.piece_collection):
        with place_cols[idx % 3]:
            if st.button(f"Place #{piece['type']}", key=f"place_{piece['type']}", 
                        use_container_width=True):
                if 0 in st.session_state.puzzle_board:
                    empty_index = st.session_state.puzzle_board.index(0)
                    st.session_state.puzzle_board[empty_index] = piece['type']
                    st.success(f"Placed Piece #{piece['type']}")
                    
                    # Check completion
                    if 0 not in st.session_state.puzzle_board:
                        st.balloons()
                        st.success("🎊 PUZZLE COMPLETED! 🎊")
                        update_activity_progress(wallet_address, 'Puzzle NFT Game', 1, 9, 9)
                else:
                    st.warning("No empty spaces left!")

def game2_minesweeper(wallet_address):
    st.title("💣 Minesweeper")
    display_how_to_play("Minesweeper")
    
    # Initialize session state
    if 'board' not in st.session_state:
        st.session_state.board = None
        st.session_state.mines = None
        st.session_state.game_over = False
        st.session_state.game_won = False
        st.session_state.revealed = None
        st.session_state.flags = None
        st.session_state.moves = 0
    
    # Enhanced board creation with difficulty settings
    def create_board(size=8, num_mines=10):
        board = [[0 for _ in range(size)] for _ in range(size)]
        mines = set()
        
        while len(mines) < num_mines:
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            if (x, y) not in mines:
                board[x][y] = -1
                mines.add((x, y))
        
        for x in range(size):
            for y in range(size):
                if board[x][y] != -1:
                    board[x][y] = count_adjacent_mines(board, x, y)
        
        return board, mines
    
    def count_adjacent_mines(board, x, y):
        mines = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board):
                    if board[nx][ny] == -1:
                        mines += 1
        return mines
    
    # Enhanced game controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("🎮 New Game", use_container_width=True):
            st.session_state.board, st.session_state.mines = create_board()
            st.session_state.revealed = [[False for _ in range(8)] for _ in range(8)]
            st.session_state.flags = [[False for _ in range(8)] for _ in range(8)]
            st.session_state.game_over = False
            st.session_state.game_won = False
            st.session_state.moves = 0
    
    with col2:
        if st.session_state.board:
            st.markdown(f"**Moves:** {st.session_state.moves}")
    
    with col3:
        if st.session_state.board:
            remaining_cells = sum(row.count(False) for row in st.session_state.revealed)
            st.markdown(f"**Remaining:** {remaining_cells}")
    
    # Enhanced board display with CSS styling
    if st.session_state.board:
        st.markdown("""
        <style>
        .minesweeper-cell {
            width: 40px;
            height: 40px;
            margin: 2px;
            border-radius: 5px;
            font-weight: bold;
        }
        .mine { background-color: #ff4444 !important; }
        .revealed { background-color: #e6f3ff; }
        .hidden { background-color: #f0f0f0; }
        </style>
        """, unsafe_allow_html=True)
        
        for x in range(8):
            cols = st.columns(8)
            for y in range(8):
                with cols[y]:
                    cell_value = st.session_state.board[x][y]
                    is_revealed = st.session_state.revealed[x][y]
                    is_flagged = st.session_state.flags[x][y]
                    
                    if st.session_state.game_over and cell_value == -1:
                        st.button('💥', key=f'{x}_{y}', disabled=True)
                    elif is_revealed:
                        display_value = str(cell_value) if cell_value > 0 else ''
                        st.button(display_value, key=f'{x}_{y}', disabled=True)
                    elif is_flagged:
                        if st.button('🚩', key=f'{x}_{y}'):
                            st.session_state.flags[x][y] = False
                    else:
                        if st.button('?', key=f'{x}_{y}'):
                            if not st.session_state.game_over and not st.session_state.game_won:
                                st.session_state.moves += 1
                                if cell_value == -1:
                                    st.session_state.game_over = True
                                    st.error("💥 BOOM! Game Over!")
                                else:
                                    st.session_state.revealed[x][y] = True
                                    revealed_cells = sum(row.count(True) for row in st.session_state.revealed)
                                    update_activity_progress(wallet_address, 'Minesweeper', 2, 
                                                          revealed_cells, 64)
                                    
                                    # Check win condition
                                    if revealed_cells == (64 - len(st.session_state.mines)):
                                        st.session_state.game_won = True
                                        st.success("🎊 Congratulations! You've won! 🎊")
                                        st.balloons()

def games(wallet_address):
    # Display stats in sidebar
    display_stats(wallet_address)
    
    # Main game selection
    st.markdown("""
    <h1 style='text-align: center;'>🎮 Blockchain Games</h1>
    """, unsafe_allow_html=True)
    
    game_choice = st.selectbox("Choose your game", 
                             ["Puzzle NFT Game", "Minesweeper"],
                             format_func=lambda x: f"🧩 {x}" if x == "Puzzle NFT Game" else f"💣 {x}")
    
    if game_choice == "Puzzle NFT Game":
        game1_puzzle_nft(wallet_address)
    elif game_choice == "Minesweeper":
        game2_minesweeper(wallet_address)
