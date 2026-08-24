# 🎵 AI Music Generator

An AI-powered music generation application that uses a Long Short-Term Memory (LSTM) neural network to learn patterns from MIDI music and generate new musical sequences.

The generated MIDI composition is converted into playable WAV audio using FluidSynth and can be listened to directly through the Streamlit web interface.

---

## ✨ Features

* 🎹 MIDI-based music generation
* 🧠 LSTM deep learning model
* 🎼 MAESTRO MIDI dataset
* 🔄 MIDI preprocessing and note/chord extraction
* 🎵 Sequence-based music generation
* 🔊 MIDI-to-WAV audio rendering using FluidSynth
* 🎧 Audio playback directly inside Streamlit
* ⬇️ Download generated MIDI files
* ⬇️ Download generated WAV files
* 🌐 Interactive Streamlit web interface
* 📊 Model and dataset information displayed in the interface

---

## 🧠 How It Works

The system follows this pipeline:

```text
MAESTRO MIDI Dataset
        ↓
MIDI Preprocessing
        ↓
Notes & Chords Extraction
        ↓
Sequence Creation
        ↓
LSTM Model Training
        ↓
Music Sequence Generation
        ↓
Generated MIDI
        ↓
FluidSynth + SoundFont
        ↓
Generated WAV Audio
        ↓
Streamlit Audio Player
```

The LSTM model learns patterns from sequences of musical notes and chords. After training, the model predicts subsequent musical events to create a new sequence.

---

## 📊 Dataset

This project uses the **MAESTRO MIDI Dataset**.

During preprocessing, MIDI files were processed and musical events were extracted.

### Processing Result

* **Dataset:** MAESTRO MIDI
* **Events processed:** 65,650 notes/chords
* **Processing library:** music21

The processed data is used to create sequences for training the LSTM model.

---

## 🧠 Model Architecture

The project uses an **LSTM-based neural network** implemented with TensorFlow/Keras.

### Training Configuration

| Parameter           |              Value |
| ------------------- | -----------------: |
| Sequence Length     |                 40 |
| Embedding Dimension |                128 |
| LSTM Units          |                256 |
| Training Epochs     |                  5 |
| Batch Size          |                 64 |
| Framework           | TensorFlow / Keras |

The model learns musical patterns from sequences of notes and chords and generates new sequences after training.

---

## 🎵 Audio Generation

The generated MIDI file is converted into playable audio using **FluidSynth**.

A SoundFont is used to provide instrument sounds during rendering.

```text
Generated MIDI
      ↓
FluidSynth
      +
MuseScore General SoundFont
      ↓
WAV Audio
```

The resulting WAV file can be played directly in the Streamlit application.

---

## 🌐 Streamlit Application

The project includes an interactive Streamlit interface.

The application provides:

### Generate Music

Users can click the **Generate Music** button to create a new musical composition.

### Audio Playback

The generated WAV file can be played directly inside the browser using the Streamlit audio player.

### Downloads

Users can download:

* Generated MIDI
* Generated WAV audio

---

## 📁 Project Structure

```text
AI_Music_Generator/
│
├── app.py
├── generate.py
├── train.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── model/
│   └── vocabulary.pkl
│
├── preprocessing/
│   └── midi_processor.py
│
├── data/
│   ├── midi/
│   └── processed/
│
├── output/
│
└── soundfont/
```

Large dataset files, trained model files, SoundFont files, generated audio, and other large files are excluded from Git using `.gitignore`.

---

## 🛠️ Technologies Used

* **Python**
* **TensorFlow / Keras**
* **music21**
* **Streamlit**
* **FluidSynth**
* **scikit-learn / Python ML ecosystem**
* **MIDI**
* **MuseScore General SoundFont**

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/HarshVardhanSingh77/AI_Music_Generator.git
```

Move into the project directory:

```bash
cd AI_Music_Generator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

Click:

```text
🎵 Generate Music
```

to generate a new composition.

---

## 🎼 Training the Model

The model can be trained using:

```bash
python train.py
```

The trained model is saved locally in the `model` directory.

Because the trained model is a large binary file, it is excluded from the GitHub repository through `.gitignore`.

---

## 🔊 FluidSynth Setup

The application uses FluidSynth to convert generated MIDI files into WAV audio.

The project also requires a compatible SoundFont, such as **MuseScore General**.

The SoundFont is intentionally excluded from GitHub because of its large file size.

---

## 📌 Project Highlights

* Processed **65,650 musical notes/chords** from MIDI data.
* Built an LSTM-based sequence generation model.
* Created an end-to-end MIDI generation pipeline.
* Integrated FluidSynth for audio rendering.
* Built a Streamlit interface for interactive music generation.
* Added browser-based audio playback and downloadable outputs.

---

## 🚀 Future Improvements

Possible improvements include:

* Longer model training for improved musical coherence
* Larger training dataset
* Multiple instrument selection
* Adjustable generation length
* Temperature/randomness controls
* Genre or mood-based generation
* Better musical evaluation metrics
* GPU-accelerated training
* Cloud deployment

---

## 👨‍💻 Author

**Harsh Vardhan Singh**

AI Music Generator project built using Python, TensorFlow/Keras, music21, FluidSynth, and Streamlit.
