import streamlit as st
import base64
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="Leaf Blower Sound Machine",
    page_icon="🍃",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .play-button {
        background-color: #4CAF50;
        color: white;
    }
    .pause-button {
        background-color: #f44336;
        color: white;
    }
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    h1 {
        text-align: center;
        color: #2c3e50;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def get_audio_base64(file_path):
    """Convert audio file to base64 for embedding"""
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    return base64.b64encode(audio_bytes).decode()

def create_audio_player(audio_file, volume, autoplay=False, loop=True):
    """Create an HTML audio player with controls"""
    audio_base64 = get_audio_base64(audio_file)
    autoplay_attr = "autoplay" if autoplay else ""
    loop_attr = "loop" if loop else ""
    
    audio_html = f"""
        <audio id="audioPlayer" {autoplay_attr} {loop_attr} style="width: 100%;">
            <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
        <script>
            var audio = document.getElementById('audioPlayer');
            audio.volume = {volume};
        </script>
    """
    return audio_html

# Initialize session state
if 'playing' not in st.session_state:
    st.session_state.playing = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0

# Header with logo
logo_path = Path("leaf_blower_logo.png")
if logo_path.exists():
    st.image(str(logo_path), width=200)

st.title("🍃 Leaf Blower Sound Machine")
st.markdown("---")

# Description
st.markdown("""
<div class="info-box">
    <p>Relax with the soothing sounds of a leaf blower. Perfect for concentration, meditation, or drowning out unwanted noise!</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for controls
col1, col2 = st.columns(2)

with col1:
    # Volume control
    volume = st.slider(
        "🔊 Volume",
        min_value=0,
        max_value=100,
        value=50,
        help="Adjust the playback volume"
    )
    volume_normalized = volume / 100.0

with col2:
    # Duration control
    duration_minutes = st.number_input(
        "⏱️ Duration (minutes)",
        min_value=1,
        max_value=480,
        value=30,
        step=5,
        help="Set how long to play the sound"
    )

# Play/Pause button
st.markdown("---")

button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:
    if not st.session_state.playing:
        if st.button("▶️ Play", use_container_width=True, type="primary"):
            st.session_state.playing = True
            st.session_state.start_time = time.time()
            st.rerun()
    else:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.playing = False
            if st.session_state.start_time:
                st.session_state.elapsed_time += time.time() - st.session_state.start_time
                st.session_state.start_time = None
            st.rerun()

# Audio player
audio_file = "leaf_blower.wav"

if st.session_state.playing:
    # Calculate elapsed time
    current_elapsed = st.session_state.elapsed_time
    if st.session_state.start_time:
        current_elapsed += time.time() - st.session_state.start_time
    
    # Check if duration has been reached
    if current_elapsed >= duration_minutes * 60:
        st.session_state.playing = False
        st.session_state.elapsed_time = 0
        st.session_state.start_time = None
        st.success("✅ Playback completed!")
        st.rerun()
    else:
        # Display audio player
        st.markdown("---")
        st.markdown("### 🎵 Now Playing")
        audio_html = create_audio_player(audio_file, volume_normalized, autoplay=True, loop=True)
        st.markdown(audio_html, unsafe_allow_html=True)
        
        # Progress information
        remaining_seconds = (duration_minutes * 60) - current_elapsed
        remaining_minutes = int(remaining_seconds // 60)
        remaining_secs = int(remaining_seconds % 60)
        
        st.info(f"⏳ Time remaining: {remaining_minutes}m {remaining_secs}s")
        
        # Auto-refresh to update timer
        time.sleep(1)
        st.rerun()

# Status indicator
st.markdown("---")
status_col1, status_col2 = st.columns(2)
with status_col1:
    st.metric("Status", "🟢 Playing" if st.session_state.playing else "🔴 Stopped")
with status_col2:
    elapsed_minutes = int(st.session_state.elapsed_time // 60)
    elapsed_secs = int(st.session_state.elapsed_time % 60)
    if st.session_state.start_time:
        current_time = time.time() - st.session_state.start_time
        elapsed_minutes = int((st.session_state.elapsed_time + current_time) // 60)
        elapsed_secs = int((st.session_state.elapsed_time + current_time) % 60)
    st.metric("Elapsed", f"{elapsed_minutes}m {elapsed_secs}s")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
    <p>💨 Embrace the power of ambient leaf blowing 💨</p>
</div>
""", unsafe_allow_html=True)

