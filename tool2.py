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
from myfunctions import *
from io import BytesIO
import pyaudio
import aubio 
from collections import deque



# Initialize pygame
pygame.init()

# Initialize the mixer for playing sound
pygame.mixer.init()

# Set up the display with resizable option
window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Pitch Coach")

# Define colors
grad_colour1 = (100, 0, 100)
grad_colour2 = (0, 100, 100)
title_color = (255, 255, 255)
shadow_color = (0, 0, 0)
button_color = (100, 0, 200)
button_hover_color = (70, 70, 230)
text_color = (255, 255, 255)
border_color = (255, 255, 255)

# Load fonts
title_font_size = 40
button_font_size = 30
title_font = pygame.font.SysFont("verdana", title_font_size, bold=True)
button_font = pygame.font.SysFont("verdana", button_font_size, bold=True)

# Button dimensions
button_width, button_height = 200, 50
control_button_size = 50  # Size for play/pause buttons

# Load and scale photo
# Get the directory where the current script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "Raja.jpeg")
photo = pygame.image.load(file_path)
photo = pygame.transform.scale(photo, (150, 150))  # Resize image to fit



# Playback control state
is_playing = False

# Variable to store the uploaded song
uploaded_song = None


# Create button surfaces after defining the control_button_size
play_button_surface = create_play_button(control_button_size,text_color)
pause_button_surface = create_pause_button(control_button_size,text_color)


def draw_gradient(window, color_top, color_bottom):
    """
    Draws a vertical gradient on the window.

    Args:
        window (pygame.Surface): The pygame window to draw on.
        color_top (tuple): RGB color for the top gradient.
        color_bottom (tuple): RGB color for the bottom gradient.
    """
    width, height = window.get_size()
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        pygame.draw.line(window, (r, g, b), (0, y), (width, y))


def draw_title(window, text, font, color, shadow_color, position):
    """
    Draws a title with shadow on the window.

    Args:
        window (pygame.Surface): The pygame window to draw on.
        text (str): The title text.
        font (pygame.font.Font): The font to use.
        color (tuple): RGB color for the text.
        shadow_color (tuple): RGB color for the shadow.
        position (tuple): Position to center the title.
    """
    shadow = font.render(text, True, shadow_color)
    shadow_rect = shadow.get_rect(center=position)
    window.blit(shadow, (shadow_rect.x + 4, shadow_rect.y + 4))
    title = font.render(text, True, color)
    title_rect = title.get_rect(center=position)
    window.blit(title, title_rect)


def draw_button(window, rect, text, font, color, hover_color, text_color):
    """
    Draws a clickable button on the window.

    Args:
        window (pygame.Surface): The pygame window to draw on.
        rect (pygame.Rect): The rectangle defining the button.
        text (str): The text displayed on the button.
        font (pygame.font.Font): The font to use for the text.
        color (tuple): RGB color of the button.
        hover_color (tuple): RGB color when hovered.
        text_color (tuple): RGB color of the text.
    """
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(window, hover_color, rect)
    else:
        pygame.draw.rect(window, color, rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)

def upload_song():
    """
    Opens a file dialog to upload a song and switches to pitch detection page.

    Globals:
        uploaded_song (str): The path of the uploaded song.
        current_page (str): The current page of the application.
    """
    global uploaded_song, current_page
    root = tk.Tk()
    root.withdraw()
    
    song_path = filedialog.askopenfilename(initialdir=script_dir, filetypes=[("wav files", "*.wav")])
    if song_path:
        uploaded_song = song_path
        current_page = "pitch_detection"



def draw_pitch_detection_page(window):
    """
    Draws the pitch detection page on the provided Pygame window. This includes
    displaying the uploaded song's name, a pitch detection plot, and a control 
    button for play/pause functionality.

    If pitch detection fails, an error message is displayed instead of the plot.

    Args:
        window (pygame.Surface): The Pygame window surface where the elements are drawn.

    Returns:
        pygame.Rect or None: Returns the control button's rectangle if the pitch plot is
        successfully drawn, otherwise returns None.
        
    Elements:
        - Gradient Background: Draws a gradient background on the entire window.
        - Song Name: Displays the name of the uploaded song.
        - Pitch Plot: Displays the pitch detection plot if available.
        - Play/Pause Control Button: Allows toggling playback of the uploaded song.
        - Time Marker Line: Displays a red line representing the current playback time.
        - Error Message: If pitch detection fails, an error message is displayed.
    """
    # Draw the gradient background
    draw_gradient(window, grad_colour1, grad_colour2)
    window_width, window_height = window.get_size()
    font = pygame.font.SysFont("verdana", 25)

    # Display the uploaded song's name
    song_text = f"Uploaded Song: {uploaded_song.split('/')[-1]}"
    song_text_surface = font.render(song_text, True, text_color)
    song_text_rect = song_text_surface.get_rect(center=(window_width // 2, 100))
    window.blit(song_text_surface, song_text_rect)
    
    # Generate the pitch detection plot surface
    plot_surface = pitch_plot(uploaded_song)
    if plot_surface:
        plot_rect = plot_surface.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(plot_surface, plot_rect)

        # Draw the play/pause control button
        control_button_rect = pygame.Rect(
            window_width // 2 - control_button_size // 2,
            plot_rect.bottom + 20,
            control_button_size,
            control_button_size
        )
        pygame.draw.rect(window, button_color, control_button_rect, border_radius=10)
        
        if is_playing:
            window.blit(pause_button_surface, control_button_rect)
        else:
            window.blit(play_button_surface, control_button_rect)

        # Display the playback time marker
        if is_playing:
            song_length = get_song_length(uploaded_song)
            current_time = pygame.mixer.music.get_pos() / 1000.0
            
            # Calculate margins and line position
            margin = plot_rect.width * 0.13
            usable_width = plot_rect.width - (2 * margin)
            relative_position = current_time / song_length
            line_x = plot_rect.left + margin + (relative_position * usable_width) + 25
            
            # Adjust line height for reduced dimensions
            height_reduction = plot_rect.height * 0.15
            line_start_y = plot_rect.top + height_reduction
            line_end_y = plot_rect.bottom - height_reduction
            
            # Draw the time marker line
            pygame.draw.line(window, (255, 0, 0), 
                             (line_x, line_start_y), 
                             (line_x, line_end_y), 
                             3)
            
        return control_button_rect
    else:
        # Display an error message if pitch detection fails
        error_text = "Pitch detection failed."
        error_text_surface = font.render(error_text, True, text_color)
        error_text_rect = error_text_surface.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(error_text_surface, error_text_rect)
        return None


def toggle_playback():
    """
    Toggles between playing and pausing the uploaded song.

    Globals:
        is_playing (bool): The playback state.
    """
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
    else:
        if pygame.mixer.music.get_pos() == -1:
            pygame.mixer.music.load(uploaded_song)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()
    is_playing = not is_playing

def draw_train_page(window):
    """
    Draws the training page with a photo, introductory text, and an upload button.

    Args:
        window (pygame.Surface): The pygame window to draw on.
    """
    draw_gradient(window, grad_colour1, grad_colour2)

    window_width, window_height = window.get_size()
    photo_rect = pygame.Rect(50, 100, 150, 150)
    pygame.draw.rect(window, border_color, photo_rect, 3)
    window.blit(photo, photo_rect)

    text = "Hello there! I'm Raja, your vocal Trainer."
    font = pygame.font.SysFont("verdana", 25)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(left=photo_rect.right + 20, centery=photo_rect.centery)
    window.blit(text_surface, text_rect)

    plot_surface = create_random_plot()
    plot_rect = plot_surface.get_rect(center=(window_width // 2, 500))
    window.blit(plot_surface, plot_rect)

    upload_button_text = "Upload Song"
    upload_button_rect = pygame.Rect(window_width // 2 - button_width // 2, 
                                   plot_rect.bottom + 20, button_width, button_height)
    draw_button(window, upload_button_rect, upload_button_text, button_font, 
                button_color, button_hover_color, text_color)

    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if upload_button_rect.collidepoint(mouse_pos):
            upload_song()





# Main loop
running = True
current_page = "main"
clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_page == "main":
                window_width, window_height = window.get_size()
                train_button_rect = pygame.Rect(window_width // 2 - button_width - 10, 
                                              window_height // 2, button_width, button_height)
                if train_button_rect.collidepoint(event.pos):
                    current_page = "train"
            elif current_page == "pitch_detection":
                control_button_rect = draw_pitch_detection_page(window)
                if control_button_rect and control_button_rect.collidepoint(event.pos):
                    toggle_playback()

    window_width, window_height = window.get_size()

    if current_page == "main":
        title_position = (window_width // 2, window_height // 4)
        train_button_rect = pygame.Rect(window_width // 2 - button_width - 10, 
                                      window_height // 2, button_width, button_height)
        play_button_rect = pygame.Rect(window_width // 2 + 10, window_height // 2, 
                                     button_width, button_height)

        draw_gradient(window, grad_colour1, grad_colour2)
        draw_title(window, "Pitch Coach", title_font, title_color, shadow_color, title_position)
        draw_button(window, train_button_rect, "Train", button_font, button_color, 
                   button_hover_color, text_color)
        draw_button(window, play_button_rect, "Play", button_font, button_color, 
                   button_hover_color, text_color)

    elif current_page == "train":
        draw_train_page(window)

    elif current_page == "pitch_detection":
        draw_pitch_detection_page(window)
                # Capture and display real-time pitch
        pitch = get_realtime_pitch()
        if pitch:
            # Update the display or plot with the new pitch
            font = pygame.font.SysFont("verdana", 25)
            pitch_text = font.render(f"Detected Pitch: {pitch:.2f} Hz", True, text_color)
            window.blit(pitch_text, (50, 50))



    pygame.display.flip()
    clock.tick(60)


pygame.quit()