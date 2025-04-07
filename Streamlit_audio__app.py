import streamlit as st
from pathlib import Path
import base64

# Path to your local audio_summaries folder
AUDIO_FOLDER = Path(r"C:\Users\TO\Desktop\kuku\audio_summaries")

# Ensure audio folder exists
if not AUDIO_FOLDER.exists():
    st.error("audio_summaries folder not found.")
    st.stop()

# List all .mp3 files
audio_files = sorted([f for f in AUDIO_FOLDER.glob("*.mp3")])
if not audio_files:
    st.error("No MP3 files found in audio_summaries.")
    st.stop()

# Session state management
if "index" not in st.session_state:
    st.session_state.index = 0
if "likes" not in st.session_state:
    st.session_state.likes = [0] * len(audio_files)
if "dislikes" not in st.session_state:
    st.session_state.dislikes = [0] * len(audio_files)

# Navigation buttons
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️"):
        st.session_state.index = max(0, st.session_state.index - 1)
with col3:
    if st.button("➡️"):
        st.session_state.index = min(len(audio_files) - 1, st.session_state.index + 1)

# Get current file info
current_file = audio_files[st.session_state.index]
book_name = current_file.stem.replace("_", " ")
audio_bytes = current_file.read_bytes()
audio_base64 = base64.b64encode(audio_bytes).decode()

# Display section
st.markdown("""
    <style>
        .short-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            background: #f0f0f0;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 0 25px rgba(0,0,0,0.1);
            width: 80%;
            margin: 40px auto;
            overflow: hidden;
            word-break: break-word;
        }
        .short-title {
            color: #4A90E2;
            font-size: 28px;
            text-align: center;
            margin-bottom: 20px;
        }
        .button-row {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }
        .btn-custom {
            background-color: #eee;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            text-decoration: none;
            color: black;
        }
        .btn-custom:hover {
            transform: scale(1.05);
            background-color: #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# UI Container
with st.container():
    st.markdown(f'<div class="short-card">', unsafe_allow_html=True)

    st.markdown(f'<div class="short-title">📖 {book_name}</div>', unsafe_allow_html=True)

    st.audio(audio_bytes, format='audio/mp3')

    col_like, col_dislike, col_share, col_save = st.columns(4)
    with col_like:
        if st.button("❤️"):
            st.session_state.likes[st.session_state.index] += 1
    with col_dislike:
        if st.button("👎"):
            st.session_state.dislikes[st.session_state.index] += 1
    with col_share:
        st.button("🔗 Copy Title", on_click=lambda: st.toast(f"Copied: {book_name}"))
    with col_save:
        href = f'data:audio/mp3;base64,{audio_base64}'
        st.markdown(
            f'<a download="{book_name}.mp3" href="{href}" class="btn-custom">💾 Save</a>',
            unsafe_allow_html=True,
        )

    st.markdown(f"<p style='text-align:center; margin-top: 15px;'>❤️ {st.session_state.likes[st.session_state.index]} &nbsp;&nbsp;&nbsp; 👎 {st.session_state.dislikes[st.session_state.index]}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>File {st.session_state.index + 1} of {len(audio_files)}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
