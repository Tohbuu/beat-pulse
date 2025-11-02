# demo_signal.py - Generate a demo audio signal with known tempo
import numpy as np
import soundfile as sf

def create_demo_beat_signal(filename="demo_beat.wav", tempo=120, duration=10):
    """
    Create a demo audio file with a clear beat at specified tempo
    """
    sr = 22050  # Sample rate
    beat_interval = 60.0 / tempo  # Time between beats in seconds
    samples_per_beat = int(beat_interval * sr)
    
    # Create time array
    t = np.linspace(0, duration, int(sr * duration))
    
    # Create base signal (quiet background)
    signal = 0.1 * np.random.normal(0, 1, len(t))
    
    # Add kicks (low frequency) on beats
    for i in range(int(duration / beat_interval)):
        beat_start = i * samples_per_beat
        beat_end = beat_start + min(1000, samples_per_beat // 4)
        
        if beat_end < len(signal):
            # Create kick drum sound (low frequency pulse)
            kick_duration = beat_end - beat_start
            kick_t = np.linspace(0, 1, kick_duration)
            kick = np.sin(2 * np.pi * 80 * kick_t) * np.exp(-5 * kick_t)
            signal[beat_start:beat_end] += kick * 0.8
    
    # Add snares (mid frequency) on off-beats
    for i in range(int(duration / beat_interval)):
        beat_start = i * samples_per_beat + samples_per_beat // 2
        beat_end = beat_start + min(800, samples_per_beat // 4)
        
        if beat_end < len(signal):
            # Create snare drum sound (noise burst)
            snare_duration = beat_end - beat_start
            snare = np.random.normal(0, 1, snare_duration) * np.exp(-8 * np.linspace(0, 1, snare_duration))
            signal[beat_start:beat_end] += snare * 0.6
    
    # Normalize signal
    signal = signal / np.max(np.abs(signal)) * 0.8
    
    # Save as WAV file
    sf.write(filename, signal, sr)
    print(f"Created demo beat file: {filename}")
    print(f"Tempo: {tempo} BPM, Duration: {duration} seconds")
    
    return filename

if __name__ == "__main__":
    # Create demo files with different tempos
    create_demo_beat_signal("demo_120bpm.wav", tempo=120, duration=15)
    create_demo_beat_signal("demo_90bpm.wav", tempo=90, duration=15)
    create_demo_beat_signal("demo_140bpm.wav", tempo=140, duration=15)
    
    print("\nDemo files created! You can now test the beat detector:")
    print("python beat_detector.py --file demo_120bpm.wav")