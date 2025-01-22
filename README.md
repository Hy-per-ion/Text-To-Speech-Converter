# 🎤 Vocalize: A Text-to-Speech Converter Application 🎤

Vocalize is a user-friendly Text-to-Speech (TTS) application that allows users to convert text into speech effortlessly. With customizable speed and voice options, it provides a seamless experience for creating and playing audio files. 🎉🎧✨

---

## 🛠 Features 🛠

- 📝 **Convert Text to Speech**: Paste or type text into the text box to listen to it.  
- 🎵 **Adjust Speed**: Choose from Slow, Normal, or Fast playback speeds.  
- 🎤 **Select Voice**: Pick from available system voices for personalized audio output.  
- 💾 **Save Audio**: Export text as an `.mp3` audio file for offline use.  
- ❌ **Exit Application**: Quit the app easily with a single click.

---

## 🚀 How to Run 🚀

1. 🖥 **Prerequisites**:  
   - Install Python (3.x)  
   - Install dependencies using `pip install pyttsx3` and `tkinter` (comes pre-installed with Python).  

2. ⚙ **Run the Application**:  
   ```bash
   python Vocalize.py

---

## 🖱 Executable Version

Use the pre-built `.exe` file for Windows (created using `pyinstaller`).
```bash
   pyinstaller --onefile --windowed --icon=assets/speech.ico --add-data "assets:assets" Vocalize.py
```
---

## 🌟 Usage 🌟

1. Enter Text ✏: Type or paste your text into the input box.
2. Set Speed ⏩: Use the dropdown menu to choose playback speed.
3. Select Voice 🗣️: Pick a system voice from the dropdown list.
4. Play Audio ▶: Click the Play button to hear the audio.
5. Save Audio 💾: Click the Save button to save the audio as an .mp3 file.

---

## 📋 Notes 📋

- 🎨 The application is powered by the pyttsx3 library for offline text-to-speech conversion.
- 💡 Ensure you have the correct Python environment if running from the script.
- 🗑️ After creating the .exe, you can safely delete the build folder and .spec file.

---

## 🎯 Future Enhancements 🎯

- Add support for additional languages. 🌍
- Introduce pitch modulation options. 🎚️
- Create a web-based version for cross-platform usage. 🌐



