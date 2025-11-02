# demo_signal.py - Generate CLEAR demo audio signals
import numpy as np
import soundfile as sf

def create_demo_beat_signal(filename="demo_beat.wav", tempo=120, duration=10):
    """
    Create a demo audio file with VERY clear, distinct beats
    """
    sr = 22050  # Sample rate
    beat_interval = 60.0 / tempo  # Time between beats in seconds
    total_beats = int(duration / beat_interval)
    
    # Create time array
    t_total = np.linspace(0, duration, int(sr * duration))
    signal = np.zeros_like(t_total)
    
    print(f"Creating {filename}: {tempo} BPM, {total_beats} total beats")
    
    # Create very strong, distinct beats
    for i in range(total_beats):
        beat_time = i * beat_interval
        beat_start_idx = int(beat_time * sr)
        beat_duration = int(0.15 * sr)  # 150ms beats (longer for clarity)
        
        # Ensure we don't go out of bounds
        if beat_start_idx + beat_duration < len(signal):
            # Create time array for this beat
            t_beat = np.linspace(0, 0.15, beat_duration)
            
            # STRONG kick drum on EVERY beat (no skipping!)
            # Low frequency for clear beats (60Hz)
            kick_freq = 60 + np.random.uniform(-5, 5)  # Slight variation
            kick = np.sin(2 * np.pi * kick_freq * t_beat) 
            kick *= np.exp(-12 * t_beat)  # Sharp decay
            signal[beat_start_idx:beat_start_idx+beat_duration] += kick * 1.0
            
            # Add high-frequency click at the very beginning for sharp attack
            click_duration = int(0.01 * sr)  # 10ms click
            if beat_start_idx + click_duration < len(signal):
                click = np.random.normal(0, 1, click_duration) * np.exp(-50 * np.linspace(0, 0.01, click_duration))
                signal[beat_start_idx:beat_start_idx+click_duration] += click * 0.3
    
    # Add very subtle background (almost silent)
    background = 0.005 * np.random.normal(0, 1, len(signal))
    signal += background
    
    # Normalize carefully
    max_val = np.max(np.abs(signal))
    if max_val > 0:
        signal = signal / max_val * 0.8
    
    # Save as WAV file
    sf.write(filename, signal, sr)
    print(f"✓ Created: {filename} - {tempo} BPM, {duration}s")
    
    return filename

if __name__ == "__main__":
    print("Creating CLEAR demo beat files...")
    # Create demo files with different tempos
    create_demo_beat_signal("demo_120bpm.wav", tempo=120, duration=15)
    create_demo_beat_signal("demo_90bpm.wav", tempo=90, duration=15) 
    create_demo_beat_signal("demo_140bpm.wav", tempo=140, duration=15)
    
    print("\n🎵 Demo files created! Test with:")
    print("python beat_detector.py --file demo_90bpm.wav")