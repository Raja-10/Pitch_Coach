
# Pitch Coach - Real-Time Pitch Detection Application

## Project Description
Pitch Coach is an interactive singing trainer application designed to analyze and provide feedback on vocal pitch in real-time. The application offers features like uploading a song for pitch detection, real-time pitch capture from a microphone, and visualizations of detected pitch data. Built with Python and Pygame, Pitch Coach provides an engaging interface for vocal practice and improvement.

## Features
- **Real-Time Pitch Detection**: Capture and display pitch in real-time using your microphone.
- **Upload and Analyze Songs**: Upload .wav files for pitch analysis and playback.
- **Interactive GUI**: Modern, resizable interface with interactive buttons and feedback.
- **Visualization**: View dynamic pitch graphs and playback progress markers.

## How to Run the Project

### Clone the Repository:
```bash
git clone https://github.com/your-repository-url
cd pitch-coach
```

### Install Dependencies:
Install the required Python libraries using requirements.txt:
```bash
pip install -r requirements.txt
```

### Run the Application:
Execute the main.py script:
```bash
python main.py
```

## Dependencies
This project uses the following Python libraries:
- **pygame**: For GUI rendering and audio playback.
- **matplotlib**: For generating pitch plots.
- **aubio**: For real-time pitch detection.
- **pyaudio**: For audio stream handling.
- **tkinter**: For file dialog integration.
- **numpy**: For numerical operations.
- **librosa**: For audio analysis and pitch extraction.

Install them via requirements.txt as shown in the How to Run section.

## Usage Examples

### Main Page
- Launch the application.
- Choose between:
  - **Train**: Learn vocal techniques with feedback from Raja, your virtual trainer.
  - **Play**: Upload a song for pitch analysis.

### Train Page
- View motivational text and dynamic pitch visualizations.
- Use the Upload Song button to analyze your voice with a custom track.

### Pitch Detection Page
- Upload a .wav file.
- View the pitch detection plot.
- Use the play/pause button to control song playback.
- Observe the red marker line indicating playback progress.

## File Structure
```bash
pitch-coach/
│
├── main.py                   # Entry point for the application
├── myfunctions.py            # Utility functions (playback controls, drawing helpers, pitch detection)
├── requirements.txt          # External dependencies
├── Raja.jpeg                 # Image for vocal trainer
├── README.md                 # Project documentation
└── realtime_pitch_detect.py  #Just using aubio library for real time detection
```


