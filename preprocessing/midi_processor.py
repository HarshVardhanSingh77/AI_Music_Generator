
from pathlib import Path
import json

from music21 import converter, instrument, note, chord


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MIDI_DIR = BASE_DIR / "data" / "midi"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "notes.json"


def extract_notes_from_midi(midi_file):
    """
    Extract notes and chords from a MIDI file.

    Notes are stored using their pitch names.
    Chords are stored by joining the pitches together.
    """

    print(f"Processing: {midi_file.name}")

    try:
        score = converter.parse(str(midi_file))

        # Remove non-musical metadata and focus on instruments/notes
        parts = instrument.partitionByInstrument(score)

        if parts:
            elements = parts.parts
        else:
            elements = [score]

        extracted_notes = []

        for part in elements:
            for element in part.flatten().notes:

                # Single note
                if isinstance(element, note.Note):
                    extracted_notes.append(element.pitch.nameWithOctave)

                # Chord
                elif isinstance(element, chord.Chord):
                    chord_notes = ".".join(
                        pitch.nameWithOctave
                        for pitch in element.pitches
                    )
                    extracted_notes.append(chord_notes)

        print(f"  Extracted: {len(extracted_notes)} notes/chords")

        return extracted_notes

    except Exception as error:
        print(f"  Error processing {midi_file.name}: {error}")
        return []


def process_dataset():
    """
    Process all MIDI files inside data/midi
    and save the extracted sequences as JSON.
    """

    if not MIDI_DIR.exists():
        print(f"MIDI directory not found: {MIDI_DIR}")
        return

    midi_files = sorted(
        list(MIDI_DIR.glob("*.mid")) +
        list(MIDI_DIR.glob("*.midi"))
    )

    if not midi_files:
        print("No MIDI files found.")
        return

    print("=" * 60)
    print("MIDI DATASET PREPROCESSING")
    print("=" * 60)
    print(f"MIDI directory : {MIDI_DIR}")
    print(f"MIDI files     : {len(midi_files)}")
    print()

    all_notes = []

    for midi_file in midi_files:
        notes = extract_notes_from_midi(midi_file)

        if notes:
            all_notes.extend(notes)

    if not all_notes:
        print("\nNo notes were extracted.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(all_notes, file, indent=2)

    print()
    print("=" * 60)
    print("PREPROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total notes/chords : {len(all_notes)}")
    print(f"Output file        : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    process_dataset()

