# enhanced_realtime.py
import numpy as np
import sounddevice as sd
import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class EnhancedRealTimeDetector:
    def __init__(self, sample_rate=22050, block_size=1024):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.energy_history = deque(maxlen=100)
        self.beat_times = deque(maxlen=50)
        self.tempo_history = deque(maxlen=20)
        self.is_running = False
        self.beat_count = 0
        self.start_time = time.time()
        self.last_beat_time = 0
        
        # Setup for dynamic thresholding
        self.energy_buffer = deque(maxlen=30)
        self.current_threshold = 0.01
        
    def calculate_dynamic_threshold(self):
        """Calculate dynamic threshold based on recent energy"""
        if len(self.energy_buffer) < 10:
            return 0.01
        
        energies = list(self.energy_buffer)
        mean_energy = np.mean(energies)
        std_energy = np.std(energies)
        
        return mean_energy + (std_energy * 1.5)
    
    def estimate_current_tempo(self):
        """Estimate current tempo from recent beats"""
        if len(self.beat_times) < 3:
            return 0
        
        recent_times = list(self.beat_times)
        if len(recent_times) >= 3:
            intervals = np.diff(recent_times[-5:])  # Last 5 intervals
            avg_interval = np.mean(intervals)
            return 60.0 / avg_interval if avg_interval > 0 else 0
        return 0
    
    def audio_callback(self, indata, frames, time_info, status):
        """Enhanced audio callback with dynamic thresholding"""
        if status:
            print(f"Audio status: {status}")
        
        if self.is_running:
            audio = indata[:, 0]
            energy = np.sum(audio ** 2)
            current_time = time.time() - self.start_time
            
            # Update energy buffer and threshold
            self.energy_buffer.append(energy)
            self.current_threshold = self.calculate_dynamic_threshold()
            
            # Dynamic beat detection
            time_since_last_beat = current_time - self.last_beat_time if self.last_beat_time > 0 else float('inf')
            min_beat_interval = 0.2  # Maximum 300 BPM
            
            if (energy > self.current_threshold and 
                time_since_last_beat > min_beat_interval and 
                len(self.energy_buffer) > 15):
                
                self.beat_count += 1
                self.beat_times.append(current_time)
                self.last_beat_time = current_time
                
                # Estimate current tempo
                current_tempo = self.estimate_current_tempo()
                if current_tempo > 0:
                    self.tempo_history.append(current_tempo)
                
                print(f"🎵 BEAT #{self.beat_count} | "
                      f"Tempo: {current_tempo:.1f} BPM | "
                      f"Energy: {energy:.4f}")
    
    def start_detection(self):
        """Start enhanced real-time detection"""
        print("🚀 Starting ENHANCED real-time beat detection...")
        print("   Features: Dynamic thresholding, Live tempo estimation")
        print("   Press Ctrl+C to stop\n")
        
        self.is_running = True
        self.start_time = time.time()
        
        try:
            with sd.InputStream(callback=self.audio_callback, 
                              channels=1,
                              samplerate=self.sample_rate,
                              blocksize=self.block_size):
                while self.is_running:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop_detection()
    
    def stop_detection(self):
        """Stop real-time detection"""
        self.is_running = False
        print(f"\n🎉 Session Summary:")
        print(f"   Total beats: {self.beat_count}")
        if self.tempo_history:
            avg_tempo = np.mean(list(self.tempo_history))
            print(f"   Average tempo: {avg_tempo:.1f} BPM")

def main():
    detector = EnhancedRealTimeDetector()
    detector.start_detection()

if __name__ == "__main__":
    main()