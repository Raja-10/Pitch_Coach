# Pitch Coach - Real-Time Pitch Detection Application

## Overview
Pitch Coach is a Python-based application designed to help users improve their vocal pitch accuracy. This tool detects and visualizes pitch in real-time, providing users with feedback based on their singing or spoken pitch. The system supports uploading audio files, detecting pitch variations over time, and visualizing the pitch in an interactive graphical interface.

The application is built with `pygame` for the graphical interface and uses several libraries, including `librosa`, `aubio`, and `pygame.mixer`, for pitch detection and playback.

## Features
- **Real-time pitch detection**: Detects pitch from a live microphone input.
- **Upload and play audio**: Users can upload an audio file (WAV format) to visualize its pitch detection over time.
- **Interactive interface**: Displays dynamic pitch plots and provides controls for playback.
- **Vocal training**: Provides an engaging interface for vocal pitch training and correction.

## Libraries and Dependencies
- `pygame` - For GUI and audio playback.
- `numpy` - For numerical operations.
- `matplotlib` - For plotting the pitch data.
- `librosa` - For audio processing and pitch detection.
- `aubio` - For real-time pitch detection from microphone input.
- `tkinter` - For file dialog to upload songs.
- `pyaudio` - For microphone input streaming.
## Real-Time Pitch Detection Application

This application helps in detecting and visualizing the pitch variations in a song. It uses pitch detection algorithms to analyze both uploaded songs and real-time audio input from a microphone.

## Files Structure

- **tool2.py**: Main program to launch the application and handle the core logic.
- **myfunctions.py**: Contains utility functions for pitch detection, audio handling, and plot generation.
- **kangal.wav**: A sample song file used for pitch detection.
- **pitch_detection_report.pdf**: Report detailing the pitch detection process and system.
- **Documentation/**: Automatically generated documentation using Sphinx.
- **Raja.jpeg**: Image of Raja, the virtual vocal trainer in the app.


You can install the necessary dependencies using pip:
```bash
pip install pygame numpy matplotlib librosa aubio pyaudio


