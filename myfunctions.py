# pitch_detection.py
import librosa
import pygame
import sys
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import pygame
import tkinter as tk
from tkinter import filedialog
import sys
import os
import pyaudio
import aubio 
from collections import deque
from io import BytesIO


def detect_pitch(song_path):
    """
    Detects the pitch of an audio file over time.

    Parameters:
    - song_path (str): Path to the audio file (MP3, WAV, etc.)

    Returns:
    - time_data (numpy array): Time in seconds for each pitch estimate.
    - pitch_data (numpy array): Detected pitch in Hz corresponding to each time.
    """
    try:
        # Load the audio file using librosa
        y, sr = librosa.load(song_path)

        # Use librosa's pitch detection function
        pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

        # Get the index of the peak pitch at each frame
        pitch_data = []
        time_data = librosa.times_like(pitches)

        for t in range(len(time_data)):
            # Get the pitch with the maximum magnitude at the current time
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:  # Only consider valid pitches (non-zero)
                pitch_data.append(pitch)

        # Convert the time and pitch data to numpy arrays
        time_data = np.array(time_data[:len(pitch_data)])
        pitch_data = np.array(pitch_data)

        return time_data, pitch_data

    except Exception as e:
        print(f"Error in pitch detection: {e}")
        return None, None
    

def create_random_plot():
    """
    Creates a matplotlib plot of a noisy pitch signal.

    Returns:
        pygame.Surface: A surface with the rendered plot image.
    """

    fig, ax = plt.subplots(figsize=(9, 4), dpi=100)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    x = np.linspace(0, 10, 100)
    y = np.sin(x) + np.random.normal(0, 0.2, x.shape)

    ax.plot(x, y, label="Noisy Pitch Signal", color="cyan", linewidth=2)
    ax.set_title("Pitch vs. Time", fontsize=14, fontweight="bold", color="white")
    ax.set_xlabel("Time (s)", fontsize=12, color="white")
    ax.set_ylabel("Pitch (Hz)", fontsize=12, color="white")
    
    ax.grid(True, linestyle="--", linewidth=0.5, color="gray", alpha=0.7)
    ax.legend(loc="upper right", fontsize=10, facecolor='black', edgecolor='white')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    raw_data = canvas.get_renderer().tostring_rgb()
    size = canvas.get_width_height()
    
    plt.close(fig)

    return pygame.image.fromstring(raw_data, size, "RGB")


def create_pause_button(size,text_color):
    """
    Creates a pause button surface.

    Args:
        size (int): Size of the button.
        text_color (array): Colour of the text text_color (array): Colour of the text 
    
    Returns:
        pygame.Surface: A surface containing the pause button.
    """
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    # Draw pause bars
    bar_width = size//4
    pygame.draw.rect(surface, text_color, (size//4, size//4, bar_width, size//2))
    pygame.draw.rect(surface, text_color, (size//2, size//4, bar_width, size//2))
    return surface

def get_song_length(song_path):
    """
    Gets the length of a song in seconds.

    Args:
        song_path (str): Path to the song file.

    Returns:
        float: Length of the song in seconds.
    """
    sound = pygame.mixer.Sound(song_path)
    return sound.get_length()

def create_play_button(size,text_color):
    """
    Creates a play button surface.

    Args:
        size (int): Size of the button.
        text_color (array): Colour of the text 

    Returns:
        pygame.Surface: A surface containing the play button.
    """
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    # Draw play triangle
    points = [(size//4, size//4), (size//4, size*3//4), (size*3//4, size//2)]
    pygame.draw.polygon(surface, text_color, points)
    return surface


def get_realtime_pitch():
    """
    Captures real-time pitch data from the microphone.

    Returns:
        float: Detected pitch in Hz, or None if no pitch detected.
    """

    # Aubio settings for pitch detection
    samplerate = 44100
    buffer_size = 1024
    p = pyaudio.PyAudio()
    pitch_detector = aubio.pitch("default", buffer_size, buffer_size//2, samplerate)
    pitch_detector.set_unit("Hz")
    audio_buffer = deque(maxlen=int(samplerate / buffer_size))  # Store ~1 second of audio

    # Set up audio stream
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=samplerate, input=True, frames_per_buffer=buffer_size)


    audio_data = np.frombuffer(stream.read(buffer_size), dtype=np.float32)[:buffer_size // 2]  # Slice to 512 samples
    pitch = pitch_detector(audio_data)[0]
    if pitch > 0:  # Filter out zero values
        return pitch
    return None

def pitch_plot(song_path):
    """
    Generates a pitch detection plot for a song.

    Args:
        song_path (str): Path to the song file.

    Returns:
        pygame.Surface: A surface containing the plot image.
    """
    time_data, pitch_data = detect_pitch(song_path)
    if time_data is None or pitch_data is None:
        return None

    fig, ax = plt.subplots(figsize=(9, 4), dpi=100, facecolor='black')
    ax.plot(time_data, pitch_data, label="Detected Pitch", color='cyan', linewidth=2)
    ax.set_xlabel("Time (s)", color='white')
    ax.set_ylabel("Pitch (Hz)", color='white')
    ax.set_title("Pitch Detection Over Time", color='white')
    ax.grid(True, color='white')
    ax.legend()
    ax.set_facecolor('black')
    ax.tick_params(axis='both', which='both', labelcolor='white', color='white')

    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data = img_buffer.read()
    img_surface = pygame.image.load(BytesIO(img_data))

    plt.close(fig)
    return img_surface