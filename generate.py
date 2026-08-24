
from pathlib import Path
import pickle

import numpy as np
import tensorflow as tf
from music21 import stream, note, chord


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_FILE = BASE_DIR / "model" / "music_model.keras"
VOCAB_FILE = BASE_DIR / "model" / "vocabulary.pkl"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "generated_music.mid"


# --------------------------------------------------
# Generation settings
# --------------------------------------------------

GENERATE_LENGTH = 100
TEMPERATURE = 1.0


# --------------------------------------------------
# Load model and vocabulary
# --------------------------------------------------

def load_model_and_vocabulary():

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_FILE}"
        )

    if not VOCAB_FILE.exists():
        raise FileNotFoundError(
            f"Vocabulary not found: {VOCAB_FILE}"
        )

    model = tf.keras.models.load_model(MODEL_FILE)

    with VOCAB_FILE.open("rb") as file:
        vocabulary = pickle.load(file)

    return model, vocabulary


# --------------------------------------------------
# Predict next note
# --------------------------------------------------

def predict_next_note(model, pattern, vocabulary, temperature=1.0):

    note_to_int = vocabulary["note_to_int"]
    int_to_note = vocabulary["int_to_note"]

    sequence_length = vocabulary["sequence_length"]

    encoded_pattern = [
        note_to_int[note_name]
        for note_name in pattern
        if note_name in note_to_int
    ]

    # Make sure the sequence has the required length
    if len(encoded_pattern) < sequence_length:
        encoded_pattern = (
            [0] * (sequence_length - len(encoded_pattern))
            + encoded_pattern
        )
    else:
        encoded_pattern = encoded_pattern[-sequence_length:]

    input_sequence = np.array(
        [encoded_pattern],
        dtype=np.int32,
    )

    predictions = model.predict(
        input_sequence,
        verbose=0,
    )[0]

    # Temperature controls randomness
    predictions = np.log(
        np.maximum(predictions, 1e-8)
    ) / temperature

    probabilities = np.exp(predictions)

    probabilities = probabilities / np.sum(
        probabilities
    )

    index = np.random.choice(
        len(probabilities),
        p=probabilities,
    )

    return int_to_note[index]


# --------------------------------------------------
# Convert prediction into music21 object
# --------------------------------------------------

def create_music_element(note_name):

    # Chord
    if "." in note_name:

        pitches = note_name.split(".")

        chord_notes = [
            note.Note(pitch_name)
            for pitch_name in pitches
        ]

        return chord.Chord(chord_notes)

    # Single note
    return note.Note(note_name)


# --------------------------------------------------
# Generate MIDI
# --------------------------------------------------

def generate_music():

    print("=" * 60)
    print("AI MUSIC GENERATOR")
    print("=" * 60)

    model, vocabulary = load_model_and_vocabulary()

    note_to_int = vocabulary["note_to_int"]

    all_notes = list(note_to_int.keys())

    # Choose a random starting sequence
    pattern = list(
        np.random.choice(
            all_notes,
            size=vocabulary["sequence_length"],
            replace=True,
        )
    )

    generated_elements = []

    print()
    print(f"Generating {GENERATE_LENGTH} musical events...")

    for step in range(GENERATE_LENGTH):

        next_note = predict_next_note(
            model,
            pattern,
            vocabulary,
            TEMPERATURE,
        )

        generated_elements.append(
            create_music_element(next_note)
        )

        pattern.append(next_note)

        if len(pattern) > vocabulary["sequence_length"]:
            pattern = pattern[
                -vocabulary["sequence_length"]:
            ]

        if (step + 1) % 10 == 0:
            print(
                f"Generated: {step + 1}/{GENERATE_LENGTH}"
            )

    # Create MIDI stream
    music_stream = stream.Stream()

    for element in generated_elements:
        music_stream.append(element)

    # Create output directory
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save MIDI
    music_stream.write(
        "midi",
        fp=str(OUTPUT_FILE),
    )

    print()
    print("=" * 60)
    print("MUSIC GENERATION COMPLETE")
    print("=" * 60)
    print(f"Generated MIDI : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    generate_music()

