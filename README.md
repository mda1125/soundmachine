# 🍃 Leaf Blower Sound Machine

A Streamlit web application that plays a looping leaf blower sound for background noise.

## Features

- **Play/Pause Control**: Start and stop playback with a single button
- **Volume Slider**: Adjust volume from 0.0 to 1.0
- **Duration Setting**: Set playback duration from 1 to 3600 seconds
- **Looping Audio**: Continuous looping until duration expires
- **Timer Display**: Shows remaining playback time

## Requirements

- Python 3.7+
- Streamlit

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd soundmachine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your audio file:
   - Place a `leaf_blower.wav` file in the project folder
   - Or modify `app.py` to use a different filename

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Or with Python 3:
```bash
python3 -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

1. **Adjust Volume**: Use the slider in the sidebar to set your preferred volume level (0.0 to 1.0)
2. **Set Duration**: Enter how long you want the sound to play (1 to 3600 seconds)
3. **Play/Pause**: Click the button to start or pause playback
4. **Enjoy**: The leaf blower sound will loop continuously until the duration expires

## Project Structure

```
soundmachine/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── leaf_blower.wav     # Audio file (add your own)
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## License

This project is open source and available for personal use.

