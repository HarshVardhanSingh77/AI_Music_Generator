
from pathlib import Path
import json
import pickle

import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "processed" / "notes.json"
MODEL_DIR = BASE_DIR / "model"

MODEL_FILE = MODEL_DIR / "music_model.keras"
VOCAB_FILE = MODEL_DIR / "vocabulary.pkl"


# --------------------------------------------------
# Training settings
# --------------------------------------------------

SEQUENCE_LENGTH = 40
EMBEDDING_DIM = 128
LSTM_UNITS = 128
EPOCHS = 5
BATCH_SIZE = 128

# --------------------------------------------------
# Load processed notes
# --------------------------------------------------

def load_notes():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_FILE}"
        )

    with DATA_FILE.open("r", encoding="utf-8") as file:
        notes = json.load(file)

    if len(notes) <= SEQUENCE_LENGTH:
        raise ValueError(
            "Not enough notes to create training sequences."
        )

    return notes


# --------------------------------------------------
# Create vocabulary
# --------------------------------------------------

def create_vocabulary(notes):
    unique_notes = sorted(set(notes))

    note_to_int = {
        note_name: index
        for index, note_name in enumerate(unique_notes)
    }

    int_to_note = {
        index: note_name
        for note_name, index in note_to_int.items()
    }

    return note_to_int, int_to_note


# --------------------------------------------------
# Create training sequences
# --------------------------------------------------

def create_sequences(notes, note_to_int):
    inputs = []
    targets = []

    encoded_notes = [
        note_to_int[note_name]
        for note_name in notes
    ]

    for start in range(
        len(encoded_notes) - SEQUENCE_LENGTH
    ):
        sequence = encoded_notes[
            start:start + SEQUENCE_LENGTH
        ]

        target = encoded_notes[
            start + SEQUENCE_LENGTH
        ]

        inputs.append(sequence)
        targets.append(target)

    return (
        np.array(inputs, dtype=np.int32),
        np.array(targets, dtype=np.int32),
    )


# --------------------------------------------------
# Build LSTM model
# --------------------------------------------------

def build_model(vocabulary_size):
    model = Sequential([
        Embedding(
            input_dim=vocabulary_size,
            output_dim=EMBEDDING_DIM,
        ),

        LSTM(
            LSTM_UNITS,
            return_sequences=True,
        ),

        LSTM(
            LSTM_UNITS,
        ),

        Dense(
            vocabulary_size,
            activation="softmax",
        ),
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


# --------------------------------------------------
# Main training function
# --------------------------------------------------

def train_model():

    print("=" * 60)
    print("AI MUSIC GENERATOR - LSTM TRAINING")
    print("=" * 60)

    # Load notes
    notes = load_notes()

    print(f"Total notes/chords : {len(notes)}")

    # Vocabulary
    note_to_int, int_to_note = create_vocabulary(notes)

    vocabulary_size = len(note_to_int)

    print(f"Unique notes/chords : {vocabulary_size}")

    # Training sequences
    X, y = create_sequences(
        notes,
        note_to_int,
    )

    print(f"Input sequences     : {len(X)}")
    print(f"Sequence length     : {SEQUENCE_LENGTH}")

    # Create model
    model = build_model(vocabulary_size)

    model.summary()

    # Create model directory
    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("=" * 60)
    print("STARTING TRAINING")
    print("=" * 60)

    # Train
    model.fit(
        X,
        y,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_split=0.1,
        shuffle=True,
    )

    # Save model
    model.save(MODEL_FILE)

    # Save vocabulary
    with VOCAB_FILE.open("wb") as file:
        pickle.dump(
            {
                "note_to_int": note_to_int,
                "int_to_note": int_to_note,
                "sequence_length": SEQUENCE_LENGTH,
            },
            file,
        )

    print()
    print("=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"Model saved      : {MODEL_FILE}")
    print(f"Vocabulary saved : {VOCAB_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    train_model()

