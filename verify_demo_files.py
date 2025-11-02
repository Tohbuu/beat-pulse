# verify_demo_files.py
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

def verify_demo_file(filename):
    """Verify the quality of a demo file"""
    print(f"\n🔍 VERIFYING: {filename}")
    
    # Load the audio
    audio, sr = sf.read(filename)
    
    if len(audio.shape) > 1:
        audio = audio[:, 0]  # Take first channel if stereo
    
    print(f"Duration: {len(audio)/sr:.2f}s")
    print(f"Sample rate: {sr}Hz")
    print(f"Max amplitude: {np.max(np.abs(audio)):.3f}")
    
    # Plot a short segment to see the beats
    plt.figure(figsize=(12, 4))
    
    # Show first 5 seconds
    segment = audio[:5*sr]
    time_axis = np.arange(len(segment)) / sr
    
    plt.plot(time_axis, segment)
    plt.title(f"First 5 seconds of {filename}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    
    # Mark expected beat locations
    if "120bpm" in filename:
        expected_bpm = 120
    elif "90bpm" in filename:
        expected_bpm = 90
    elif "140bpm" in filename:
        expected_bpm = 140
    else:
        expected_bpm = 120
    
    beat_interval = 60.0 / expected_bpm
    beats_in_5s = int(5 / beat_interval)
    
    for i in range(beats_in_5s):
        beat_time = i * beat_interval
        plt.axvline(x=beat_time, color='red', alpha=0.7, linestyle='--', linewidth=1)
    
    plt.tight_layout()
    plt.show()
    
    return audio, sr

if __name__ == "__main__":
    files = ["demo_90bpm.wav", "demo_120bpm.wav", "demo_140bpm.wav"]
    
    for file in files:
        try:
            verify_demo_file(file)
        except Exception as e:
            print(f"Error verifying {file}: {e}")