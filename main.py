import mido
from pynput.keyboard import Controller, Key
import time
import sys

keyboard = Controller()


# Replace the notes depending on your in game keyboard layout
midi_note_to_bard_key = {
    # Lower octave (C3 to B3)
    48: 'y',  # C3
    49: 'w',  # C#3/Db3
    50: 'u',  # D3
    51: 'x',  # D#3/Eb3
    52: 'i',  # E3
    53: 'o',  # F3
    54: 'c',  # F#3/Gb3
    55: 'p',  # G3
    56: 'v',  # G#3/Ab3
    57: '!',  # A3
    58: 'b',  # A#3/Bb3
    59: '$',  # B3
    # Upper octave (C4 to B4)
    60: 'à',  # C4
    61: 'h',  # C#4/Db4
    62: ')',  # D4
    63: 'j',  # D#4/Eb4
    64: 'a',  # E4
    65: 'z',  # F4
    66: 'k',  # F#4/Gb4
    67: 'e',  # G4
    68: 'l',  # G#4/Ab4
    69: 'r',  # A4
    70: 'm',  # A#4/Bb4
    71: 't',  # B4
    # Starting note of the next octave (C5)
    72: '&',  # C5
    73: 'q',  # C#5/Db5
    74: 'é',  # D5
    75: 's',  # D#5/Eb5
    76: '"',  # E5
    77: "'",  # F5
    78: 'd',  # F#5/Gb5
    79: '(',  # G5
    80: 'f',  # G#5/Ab5
    81: '-',  # A5
    82: 'g',  # A#5/Bb5
    83: 'è',  # B5
}

def ticks_to_seconds(ticks, tempo, ticks_per_beat):
    return mido.tick2second(ticks, ticks_per_beat, tempo)

def get_tempo(midi_file_path):
    midi_file = mido.MidiFile(midi_file_path)
    for i, track in enumerate(midi_file.tracks):
        for msg in track:
            if msg.type == 'set_tempo':
                return msg.tempo
    return 500000

def adjust_octave(note):
    octave_shift = 0
    while note < 48:
        note += 12
        octave_shift -= 1
    while note > 72:
        note -= 12
        octave_shift += 1
    return note, octave_shift

def press_octave_shift(octave_shift):
    if octave_shift > 0:
        keyboard.press(Key.shift)
    elif octave_shift < 0:
        keyboard.press(Key.ctrl)

def release_octave_shift(octave_shift):
    if octave_shift > 0:
        keyboard.release(Key.shift)
    elif octave_shift < 0:
        keyboard.release(Key.ctrl)

def play_note(shifted_note, octave_shift):
    press_octave_shift(octave_shift)

    key_to_press = midi_note_to_bard_key.get(shifted_note)
    if key_to_press:
        keyboard.press(key_to_press)
        keyboard.release(key_to_press)

    release_octave_shift(octave_shift)

def play_bard(midi_file_path):
    midi_file = mido.MidiFile(midi_file_path)
    tempo = get_tempo(midi_file_path)

    time.sleep(3)

    for i, track in enumerate(midi_file.tracks):
        for msg in track:
            if not msg.is_meta:
                # seconds_to_wait = ticks_to_seconds(msg.time, tempo, ticks_per_beat)
                # time.sleep(seconds_to_wait)
                if msg.type == 'note_on' or msg.type == 'note_off':
                    key_to_press = midi_note_to_bard_key.get(msg.note)
                    if key_to_press:
                        keyboard.press(key_to_press)
                        time.sleep(0.1)
                        keyboard.release(key_to_press)
                    # note, octave_shift = adjust_octave(msg.note)

                    # if msg.velocity > 0:
                    #     play_note(note, octave_shift)

if len(sys.argv) > 1:
    midi_path = sys.argv[1]
    play_bard(midi_path)
else:
    print("Please provide the path to the MIDI file as an argument.")
