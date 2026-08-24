
from pathlib import Path
import subprocess
import sys

import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

GENERATED_MIDI = OUTPUT_DIR / "generated_music.mid"
GENERATED_WAV = OUTPUT_DIR / "generated_music.wav"

SOUNDFONT = BASE_DIR / "soundfont" / "MuseScore_General.sf2"

FLUIDSYNTH = Path(
    r"C:\Users\Harsh Vardhan singh\OneDrive\Desktop\Fluidsynth"
    r"\synth\fluidsynth-v2.6.0-win10-x64-cpp11"
    r"\bin\fluidsynth.exe"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Music Generator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #0e1117 0%,
            #151925 50%,
            #0e1117 100%
        );
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 2.5rem 2rem;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            rgba(108, 92, 231, 0.25),
            rgba(72, 52, 212, 0.08)
        );
        border: 1px solid rgba(255, 255, 255, 0.10);
        text-align: center;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #b8bcc8;
        max-width: 750px;
        margin: auto;
    }

    .info-card {
        padding: 1.5rem;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.09);
        min-height: 145px;
    }

    .card-icon {
        font-size: 2rem;
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }

    .card-text {
        color: #aeb4c2;
        margin-top: 0.3rem;
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 750;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    .generation-box {
        padding: 2rem;
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.09);
        text-align: center;
        margin-top: 1rem;
    }

    .audio-card {
        padding: 1.5rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.09);
        margin-top: 1rem;
    }

    .footer {
        text-align: center;
        color: #777e8c;
        padding-top: 2rem;
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎵 AI Music Generator")

    st.markdown("---")

    st.markdown("### ⚙️ Model")

    st.write("**Architecture:** LSTM")
    st.write("**Framework:** TensorFlow / Keras")
    st.write("**Sequence Length:** 40")
    st.write("**Training Epochs:** 5")

    st.markdown("---")

    st.markdown("### 🎼 Dataset")

    st.write("**Dataset:** MAESTRO MIDI")
    st.write("**Events Processed:** 65,650")
    st.write("**MIDI Processing:** music21")

    st.markdown("---")

    st.markdown("### 🔊 Audio")

    st.write("**Synthesizer:** FluidSynth")
    st.write("**SoundFont:** MuseScore General")
    st.write("**Output:** WAV + MIDI")

    st.markdown("---")

    st.caption(
        "A deep learning project that generates "
        "musical sequences from MIDI data."
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            🎵 AI Music Generator
        </div>

        <div class="hero-subtitle">
            Generate original musical sequences using
            an LSTM-based deep learning model trained
            on MIDI data.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PROJECT CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="info-card">

            <div class="card-icon">🧠</div>

            <div class="card-title">
                LSTM Deep Learning
            </div>

            <div class="card-text">
                Uses recurrent neural networks to learn
                patterns in musical sequences.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:
    st.markdown(
        """
        <div class="info-card">

            <div class="card-icon">🎹</div>

            <div class="card-title">
                MIDI Dataset
            </div>

            <div class="card-text">
                Trained using musical note and chord
                sequences extracted from MIDI files.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:
    st.markdown(
        """
        <div class="info-card">

            <div class="card-icon">✨</div>

            <div class="card-title">
                AI Generation
            </div>

            <div class="card-text">
                Generates new musical sequences and
                converts them into playable audio.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# GENERATION SECTION
# ============================================================

st.markdown(
    '<div class="section-title">🎼 Generate New Music</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="generation-box">

    <p style="color:#b8bcc8; font-size:1.05rem;">
    Click the button below to generate a new musical
    composition using the trained LSTM model.
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)


generate_clicked = st.button(
    "🎵  Generate Music",
    type="primary",
    use_container_width=True,
)


# ============================================================
# GENERATE MUSIC
# ============================================================

if generate_clicked:

    # Remove previous WAV so we don't accidentally show
    # an old audio file if the new conversion fails.
    if GENERATED_WAV.exists():
        GENERATED_WAV.unlink()

    with st.spinner(
        "🎼 Composing your music... Please wait."
    ):

        try:

            # ------------------------------------------------
            # STEP 1: Generate MIDI
            # ------------------------------------------------

            result = subprocess.run(
                [
                    sys.executable,
                    str(BASE_DIR / "generate.py"),
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:

                st.error(
                    "❌ Music generation failed."
                )

                if result.stderr:
                    with st.expander(
                        "View technical details"
                    ):
                        st.code(result.stderr)

            elif not GENERATED_MIDI.exists():

                st.error(
                    "The generation process completed, "
                    "but the MIDI file could not be found."
                )

            # ------------------------------------------------
            # STEP 2: Convert MIDI → WAV
            # ------------------------------------------------

            else:

                if not FLUIDSYNTH.exists():
                    st.error(
                        "❌ FluidSynth executable was not found."
                    )

                    st.code(str(FLUIDSYNTH))

                elif not SOUNDFONT.exists():
                    st.error(
                        "❌ SoundFont was not found."
                    )

                    st.code(str(SOUNDFONT))

                else:

                    audio_result = subprocess.run(
                        [
                            str(FLUIDSYNTH),
                            "-ni",
                            "-g",
                            "1",
                            "-F",
                            str(GENERATED_WAV),
                            str(SOUNDFONT),
                            str(GENERATED_MIDI),
                        ],
                        capture_output=True,
                        text=True,
                    )

                    if audio_result.returncode != 0:

                        st.error(
                            "❌ MIDI-to-audio conversion failed."
                        )

                        if audio_result.stderr:
                            with st.expander(
                                "View audio conversion details"
                            ):
                                st.code(
                                    audio_result.stderr
                                )

                    elif GENERATED_WAV.exists():

                        st.success(
                            "🎉 Music generated successfully!"
                        )

                    else:

                        st.error(
                            "The MIDI was generated, but "
                            "the WAV audio file could not be created."
                        )

        except Exception as error:

            st.error(
                f"An unexpected error occurred: {error}"
            )


# ============================================================
# GENERATED MUSIC
# ============================================================

if GENERATED_MIDI.exists():

    st.markdown(
        '<div class="section-title">🎧 Your Generated Music</div>',
        unsafe_allow_html=True,
    )

    if GENERATED_WAV.exists():

        st.markdown(
            """
            <div class="audio-card">

            <h3>🎵 Listen to your composition</h3>

            <p style="color:#aeb4c2;">
            Your AI-generated composition has been
            converted into playable audio.
            </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

        with GENERATED_WAV.open("rb") as audio_file:

            st.audio(
                audio_file.read(),
                format="audio/wav",
            )

        st.markdown("### ⬇️ Download")

        download_col1, download_col2 = st.columns(2)

        with download_col1:

            with GENERATED_MIDI.open("rb") as midi_file:

                st.download_button(
                    label="🎹 Download MIDI",
                    data=midi_file,
                    file_name="generated_music.mid",
                    mime="audio/midi",
                    use_container_width=True,
                )

        with download_col2:

            with GENERATED_WAV.open("rb") as wav_file:

                st.download_button(
                    label="🎧 Download WAV",
                    data=wav_file,
                    file_name="generated_music.wav",
                    mime="audio/wav",
                    use_container_width=True,
                )

    else:

        st.info(
            "Your MIDI composition is ready, but the "
            "playable WAV version has not been generated yet."
        )

        with GENERATED_MIDI.open("rb") as midi_file:

            st.download_button(
                label="🎹 Download Generated MIDI",
                data=midi_file,
                file_name="generated_music.mid",
                mime="audio/midi",
                use_container_width=True,
            )


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    '<div class="section-title">⚙️ How It Works</div>',
    unsafe_allow_html=True,
)

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown("### 1️⃣")
    st.markdown("**MIDI Data**")
    st.caption(
        "Musical data is collected from MIDI files."
    )

with step2:
    st.markdown("### 2️⃣")
    st.markdown("**Preprocessing**")
    st.caption(
        "Notes and chords are extracted and encoded."
    )

with step3:
    st.markdown("### 3️⃣")
    st.markdown("**LSTM Model**")
    st.caption(
        "The model learns patterns in musical sequences."
    )

with step4:
    st.markdown("### 4️⃣")
    st.markdown("**Audio Rendering**")
    st.caption(
        "Generated MIDI is rendered into playable WAV audio."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🎵 AI Music Generator &nbsp;•&nbsp;
    TensorFlow &nbsp;•&nbsp;
    music21 &nbsp;•&nbsp;
    FluidSynth &nbsp;•&nbsp;
    Streamlit

    </div>
    """,
    unsafe_allow_html=True,
)

