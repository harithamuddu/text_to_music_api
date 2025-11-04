import numpy as np
from scipy.io.wavfile import write

def generate_music_from_text(prompt: str, duration: int = 15):
    sr = 44100
    samples = duration * sr
    audio = np.zeros(samples)

    # ----------- Wave generators -----------
    def sine(freq, t, volume=1.0):
        x = np.linspace(0, t, int(sr*t), False)
        return np.sin(2*np.pi*freq*x) * volume

    def square(freq, t, volume=1.0):
        x = np.linspace(0, t, int(sr*t), False)
        return np.sign(np.sin(2*np.pi*freq*x)) * volume

    def saw(freq, t, volume=1.0):
        x = np.linspace(0, t, int(sr*t), False)
        return 2*(x*freq - np.floor(0.5 + x*freq)) * volume

    def impact():
        # Short punchy cinematic hit
        hit = saw(80, 0.15, 1.0) * np.exp(-np.linspace(0, 5, int(sr*0.15)))
        return hit

    # ---------------------------------------    
    #            HERO INTRO STYLE           
    # ---------------------------------------
    prompt = prompt.lower()

    if "hero" in prompt or "mass" in prompt or "intro" in prompt:
        rise_freqs = [80, 120, 150, 180, 220, 260, 300]  # rising tone
        beat_time = 0.4
    else:
        rise_freqs = [200, 300, 400]
        beat_time = 0.3

    pos = 0

    # ----------- Generate Hero Intro Rise -----------
    for f in rise_freqs:
        if pos >= samples:
            break

        # Layer 1: strong square wave (main hero energy)
        layer1 = square(f, beat_time, 0.6)

        # Layer 2: saw wave (cinematic rise)
        layer2 = saw(f, beat_time, 0.4)

        # Layer 3: soft sine (smoothness)
        layer3 = sine(f, beat_time, 0.2)

        combined = layer1 + layer2 + layer3

        end = pos + len(combined)
        if end > samples:
            end = samples

        audio[pos:end] += combined[:end-pos]
        pos += len(combined)

        # add cinematic hit after each rise
        hit = impact()
        end2 = pos + len(hit)
        if end2 < samples:
            audio[pos:end2] += hit
            pos += len(hit)

    # ----------- Normalize Audio Safely -----------
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    audio_int16 = np.int16(audio * 32767)
    output_path = "output.wav"
    write(output_path, sr, audio_int16)

    return output_path
