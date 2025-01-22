import pyttsx3
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
import threading
from PIL import Image, ImageTk
import sys
import os

class TextToSpeechGUI:
    def __init__(self, root):
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        self.root = root
        self.root.title("Text-to-Speech Converter")

        # Load icon with error handling
        try:
            icon_path = os.path.join(base_path, "assets", "tts.ico")
            image = Image.open(icon_path)
            photo = ImageTk.PhotoImage(image)
            self.root.tk.call('wm', 'iconphoto', self.root._w, photo)
        except Exception as e:
            print(f"Error loading icon: {e}")

        # Initialize TTS engine
        self.engine = pyttsx3.init()
        self.default_rate = self.engine.getProperty("rate") or 200  # Default speech rate
        self.speed_multipliers = {"0.25x": 0.25, "0.5x": 0.5, "0.75x": 0.75, "1x": 1, "1.25x": 1.25, "1.5x": 1.5, "1.75x": 1.75, "2x": 2}
        self.current_multiplier = "1x"
        self.is_paused = False
        self.is_playing = False
        self.text_to_read = ""
        self.current_position = 0
        self.audio_index = 0

        # Get available voices
        self.voices = self.engine.getProperty("voices")
        self.current_voice = self.voices[0]  # Default voice (first in list)
        self.engine.setProperty("voice", self.current_voice.id)

        # GUI Components
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dropdown for Speed Selection
        self.speed_label = tk.Label(self.root, text="Speed:")
        self.speed_label.pack(side=tk.LEFT, padx=5)
        self.speed_menu = ttk.Combobox(self.root, values=list(self.speed_multipliers.keys()), state="readonly")
        self.speed_menu.set("1x")  # Default value
        self.speed_menu.bind("<<ComboboxSelected>>", self.set_speed)
        self.speed_menu.pack(side=tk.LEFT, padx=5)

        # Dropdown for Voice Selection
        self.voice_label = tk.Label(self.root, text="Voice:")
        self.voice_label.pack(side=tk.LEFT, padx=5)
        self.voice_menu = ttk.Combobox(self.root, values=[voice.name for voice in self.voices], state="readonly")
        self.voice_menu.set(self.current_voice.name)  # Default voice
        self.voice_menu.bind("<<ComboboxSelected>>", self.set_voice)
        self.voice_menu.pack(side=tk.LEFT, padx=5)

        # Buttons
        self.play_button = tk.Button(self.root, text="Start", command=self.play_text_thread)
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.pause_button = tk.Button(self.root, text="Stop", command=self.pause_text)
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.download_button = tk.Button(self.root, text="Download", command=self.download_audio)
        self.download_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_app)
        self.quit_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Load icons for light and dark mode with error handling
        try:
            ld_mode_icon_path = os.path.join(base_path, "assets", "ld mode.ico")
            light_mode_image = Image.open(ld_mode_icon_path).resize((20, 20), Image.LANCZOS)
            self.light_mode_icon = ImageTk.PhotoImage(light_mode_image)

            dark_mode_image = Image.open(ld_mode_icon_path).resize((20, 20), Image.LANCZOS)
            self.dark_mode_icon = ImageTk.PhotoImage(dark_mode_image)
        except Exception as e:
            print(f"Error loading mode icons: {e}")
            self.light_mode_icon = None
            self.dark_mode_icon = None

        self.is_dark_mode = False
        self.mode_button = tk.Button(self.root, image=self.light_mode_icon, command=self.toggle_mode)
        self.mode_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def toggle_mode(self):
        if self.is_dark_mode:
            self.root.config(bg="white")
            self.text_area.config(bg="white", fg="black")
            self.speed_label.config(bg="white", fg="black")
            self.voice_label.config(bg="white", fg="black")
            self.play_button.config(bg="lightgrey", fg="black")
            self.pause_button.config(bg="lightgrey", fg="black")
            self.quit_button.config(bg="lightgrey", fg="black")
            self.mode_button.config(image=self.light_mode_icon, bg="lightgrey")
            self.download_button.config(bg="lightgrey", fg="black")

        else:
            self.root.config(bg="black")
            self.text_area.config(bg="black", fg="white")
            self.speed_label.config(bg="black", fg="white")
            self.voice_label.config(bg="black", fg="white")
            self.play_button.config(bg="darkgrey", fg="white")
            self.pause_button.config(bg="darkgrey", fg="white")
            self.quit_button.config(bg="darkgrey", fg="white")
            self.mode_button.config(image=self.dark_mode_icon, bg="darkgrey")
            self.download_button.config(bg="darkgrey", fg="white")
        self.is_dark_mode = not self.is_dark_mode

    def play_text_thread(self):
        if not self.is_playing:
            tts_thread = threading.Thread(target=self.play_text)
            tts_thread.daemon = True  # Ensures thread ends when the main program exits
            tts_thread.start()

    def play_text(self):
        if self.is_paused:
            self.is_paused = False
        else:
            self.text_to_read = self.text_area.get("1.0", tk.END).strip()
            if not self.text_to_read:
                messagebox.showwarning("Warning", "Please enter some text to convert to speech.")
                return
            self.current_position = 0
            self.is_playing = True

        while self.is_playing and self.current_position < len(self.text_to_read):
            if self.is_paused:
                break
            remaining_text = self.text_to_read[self.current_position:]
            self.engine.say(remaining_text)
            self.engine.runAndWait()
            self.is_playing = False

    def pause_text(self):
        if self.is_playing:
            self.is_paused = True
            self.is_playing = False
            self.engine.stop()

    def set_speed(self, event=None):
        selected_speed = self.speed_menu.get()
        if selected_speed in self.speed_multipliers:
            multiplier = self.speed_multipliers[selected_speed]
            adjusted_rate = int(self.default_rate * multiplier)
            self.engine.setProperty("rate", adjusted_rate)

    def set_voice(self, event=None):
        selected_voice_name = self.voice_menu.get()
        for voice in self.voices:
            if voice.name == selected_voice_name:
                self.engine.setProperty("voice", voice.id)
                break

    def download_audio(self):
      self.text_to_read = self.text_area.get("1.0", tk.END).strip()
      if not self.text_to_read:
          messagebox.showwarning("Warning", "Please enter some text to convert to speech.")
          return

      # Apply selected speed and voice before generating the audio file
      selected_speed = self.speed_menu.get()
      if selected_speed in self.speed_multipliers:
          multiplier = self.speed_multipliers[selected_speed]
          adjusted_rate = int(self.default_rate * multiplier)
          self.engine.setProperty("rate", adjusted_rate)

      selected_voice_name = self.voice_menu.get()
      for voice in self.voices:
          if voice.name == selected_voice_name:
              self.engine.setProperty("voice", voice.id)
              break

      base_name = "audio_file"
      extension = ".mp3"
      file_name = base_name + extension
      counter = 1

      # Generate unique file name if file already exists
      while os.path.exists(file_name):
          file_name = f"{base_name}_{counter}{extension}"
          counter += 1

      try:
          self.engine.save_to_file(self.text_to_read, file_name)
          self.engine.runAndWait()
          messagebox.showinfo("Success", f"Audio saved as {file_name}")
      except Exception as e:
          messagebox.showerror("Error", f"Failed to save audio: {e}")


    def quit_app(self):
        self.engine.stop()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechGUI(root)
    root.mainloop()

# pyinstaller --onefile --windowed --icon=assets/speech.ico --add-data "assets:assets" Vocalize.py
