import streamlit as st
import time
import base64
import os

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
        border-radius: 0.5rem;
    }
    h1 {
        text-align: center;
        color: #2E7D32;
        margin-bottom: 1rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        font-size: 1.1rem;
        margin: 1rem 0;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0 2rem 0;
    }
    .logo-img {
        max-width: 200px;
        height: auto;
        border-radius: 50%;
    }
    </style>
    """, unsafe_allow_html=True)

# Display logo if it exists
logo_files = ['logo.png', 'logo.jpg', 'logo.jpeg', 'logo.svg', 'leaf_blower_logo.png', 'leaf_blower_logo.jpg']
logo_path = None
for logo_file in logo_files:
    if os.path.exists(logo_file):
        logo_path = logo_file
        break

if logo_path:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo_path, use_container_width=True)
    st.markdown("---")

# Title
st.title("🍃 Leaf Blower Sound Machine")
st.markdown("---")

# Load audio file as base64
@st.cache_data
def load_audio_file(file_path):
    """Load audio file and convert to base64 data URI"""
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        # Determine MIME type based on file extension
        if file_path.endswith('.wav'):
            mime_type = 'audio/wav'
        elif file_path.endswith('.mp3'):
            mime_type = 'audio/mpeg'
        else:
            mime_type = 'audio/wav'
        return f"data:{mime_type};base64,{audio_base64}"
    return None

# Initialize session state
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'paused_time' not in st.session_state:
    st.session_state.paused_time = 0
if 'duration' not in st.session_state:
    st.session_state.duration = 60  # Default 60 seconds
if 'volume' not in st.session_state:
    st.session_state.volume = 0.7
if 'audio_data_uri' not in st.session_state:
    st.session_state.audio_data_uri = load_audio_file('leaf_blower.wav')

# Sidebar for controls
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Volume slider
    volume = st.slider(
        "Volume",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.volume,
        step=0.1,
        help="Adjust the playback volume"
    )
    # Update volume in session state
    st.session_state.volume = volume
    
    # Duration input
    duration = st.number_input(
        "Duration (seconds)",
        min_value=1,
        max_value=3600,
        value=st.session_state.duration,
        step=30,
        help="How long to play the sound (1-3600 seconds)"
    )
    st.session_state.duration = duration

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Play/Pause button
    button_label = "▶️ Play" if not st.session_state.is_playing else "⏸️ Pause"
    if st.button(button_label, key="play_pause"):
        if not st.session_state.is_playing:
            # Starting playback
            st.session_state.is_playing = True
            current_time = time.time()
            if st.session_state.start_time is None:
                st.session_state.start_time = current_time
            else:
                # Resume: adjust start_time to account for paused time
                st.session_state.start_time = current_time - st.session_state.paused_time
        else:
            # Pausing playback
            st.session_state.is_playing = False
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
                st.session_state.paused_time = elapsed
            # Pause the audio
            pause_script = """
            <script>
                (function() {
                    var audio = document.getElementById('leafBlowerAudio');
                    if (audio && !audio.paused) {
                        audio.pause();
                    }
                })();
            </script>
            """
            st.components.v1.html(pause_script, height=0)
        st.rerun()

# Status and audio player
status_placeholder = st.empty()

if st.session_state.is_playing:
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, st.session_state.duration - elapsed)
        
        if remaining > 0:
            # Create audio element and control in same HTML component
            if st.session_state.audio_data_uri:
                audio_control_html = f"""
                <audio id="leafBlowerAudio" loop style="display: none;"></audio>
                <div id="timerDisplay"></div>
                <script>
                    (function() {{
                        var audio = document.getElementById('leafBlowerAudio');
                        var timerDisplay = document.getElementById('timerDisplay');
                        var startTime = Date.now();
                        var duration = {st.session_state.duration} * 1000; // Convert to milliseconds
                        var isPlaying = false;
                        
                        // Create or get audio element
                        if (!audio) {{
                            audio = document.createElement('audio');
                            audio.id = 'leafBlowerAudio';
                            audio.loop = true;
                            audio.style.display = 'none';
                            document.body.appendChild(audio);
                        }}
                        
                        // Set source if not already set
                        if (!audio.src || !audio.src.includes('data:audio')) {{
                            audio.src = '{st.session_state.audio_data_uri}';
                        }}
                        
                        // Set volume
                        audio.volume = {volume};
                        
                        // Start playing
                        if (audio.paused) {{
                            var playPromise = audio.play();
                            if (playPromise !== undefined) {{
                                playPromise.then(function() {{
                                    console.log('Audio playing successfully');
                                    isPlaying = true;
                                    startTime = Date.now();
                                    updateTimer();
                                }}).catch(function(error) {{
                                    console.log('Audio play error:', error);
                                    // Retry after a short delay
                                    setTimeout(function() {{
                                        audio.play().then(function() {{
                                            isPlaying = true;
                                            startTime = Date.now();
                                            updateTimer();
                                        }}).catch(function(e) {{
                                            console.log('Retry failed:', e);
                                        }});
                                    }}, 200);
                                }});
                            }}
                        }} else {{
                            // Already playing, just update volume
                            audio.volume = {volume};
                            isPlaying = true;
                        }}
                        
                        // Update timer display
                        function updateTimer() {{
                            if (!isPlaying) return;
                            
                            var elapsed = Date.now() - startTime;
                            var remaining = Math.max(0, duration - elapsed);
                            
                            if (remaining > 0) {{
                                var minutes = Math.floor(remaining / 60000);
                                var seconds = Math.floor((remaining % 60000) / 1000);
                                if (timerDisplay) {{
                                    timerDisplay.textContent = '⏱️ Playing... ' + 
                                        String(minutes).padStart(2, '0') + ':' + 
                                        String(seconds).padStart(2, '0') + ' remaining';
                                }}
                                
                                // Update every second
                                setTimeout(updateTimer, 1000);
                            }} else {{
                                // Duration expired
                                if (audio && !audio.paused) {{
                                    audio.pause();
                                    audio.currentTime = 0;
                                }}
                                if (timerDisplay) {{
                                    timerDisplay.textContent = '✅ Playback completed!';
                                }}
                                isPlaying = false;
                            }}
                        }}
                        
                        // Start timer updates
                        if (isPlaying) {{
                            updateTimer();
                        }}
                        
                        // Clear any existing timeout
                        if (window.leafBlowerTimeout) {{
                            clearTimeout(window.leafBlowerTimeout);
                        }}
                        
                        // Fallback: Stop after duration (in case timer fails)
                        window.leafBlowerTimeout = setTimeout(function() {{
                            if (audio && !audio.paused) {{
                                audio.pause();
                                audio.currentTime = 0;
                            }}
                            isPlaying = false;
                        }}, duration);
                    }})();
                </script>
                """
                st.components.v1.html(audio_control_html, height=50)
            else:
                st.error("⚠️ Audio file not found! Please ensure leaf_blower.wav is in the project folder.")
            
            # Display initial remaining time (JavaScript will update it)
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            status_placeholder.info(f"⏱️ **Playing...** {minutes:02d}:{seconds:02d} remaining")
            
            # Don't rerun constantly - let JavaScript handle the timer
            # Only rerun if duration expired (checked below) or user interacts
        else:
            # Duration expired
            st.session_state.is_playing = False
            st.session_state.start_time = None
            st.session_state.paused_time = 0
            status_placeholder.success("✅ **Playback completed!**")
            
            # Stop audio
            stop_audio_html = """
            <script>
                (function() {
                    if (window.leafBlowerTimeout) {
                        clearTimeout(window.leafBlowerTimeout);
                    }
                    var audio = document.getElementById('leafBlowerAudio');
                    if (audio) {
                        audio.pause();
                        audio.currentTime = 0;
                    }
                })();
            </script>
            """
            st.components.v1.html(stop_audio_html, height=0)
    else:
        st.session_state.start_time = time.time()
        st.session_state.paused_time = 0
        st.rerun()
else:
    # Paused or stopped
    if st.session_state.start_time is not None and st.session_state.paused_time > 0:
        remaining = max(0, st.session_state.duration - st.session_state.paused_time)
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        status_placeholder.info(f"⏸️ **Paused** - {minutes:02d}:{seconds:02d} remaining")
    else:
        status_placeholder.info("⏸️ **Ready to play**")

# Instructions
st.markdown("---")
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. **Adjust Volume**: Use the slider in the sidebar to set your preferred volume level (0.0 to 1.0)
    2. **Set Duration**: Enter how long you want the sound to play (1 to 3600 seconds)
    3. **Play/Pause**: Click the button to start or pause playback
    4. **Enjoy**: The leaf blower sound will loop continuously until the duration expires
    
    The timer will automatically stop playback when the duration is reached.
    """)

