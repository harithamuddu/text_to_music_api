import numpy as np
from scipy.io.wavfile import write

def generate_music_from_text(prompt: str, duration: int = 20):
    sr = 44100
    samples = duration * sr

    audio = np.zeros(samples)

    def tone(freq, time, volume=1.0):
        t = np.linspace(0, time, int(sr * time), False)
        return np.sin(2 * np.pi * freq * t) * volume

    # HERO INTRO pattern
    if "hero" in prompt.lower() or "mass" in prompt.lower():
        freqs = [80, 120, 150, 180, 220, 260]  # rising hero tones
        beat_len = 0.5
        volume = 0.6
    else:
        freqs = [200, 300, 400]
        beat_len = 0.3
        volume = 0.4

    pos = 0

    # Generate hero intro rise + beats
    for f in freqs:
        tdata = tone(f, beat_len, volume)

        end_pos = pos + len(tdata)
        if end_pos > samples:
            break

        audio[pos:end_pos] += tdata
        pos += len(tdata)

    # Avoid division by zero
    max_val = np.max(np.abs(audio))
    if max_val != 0:
        audio = audio / max_val

    audio_int16 = np.int16(audio * 32767)
    output_path = "output.wav"
    write(output_path, sr, audio_int16)

    return output_path
