import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class AdvancedTempoEstimator:
    def __init__(self, sr=22050):
        self.sr = sr
    
    def estimate_tempo_librosa(self, file_path):
        """Use librosa's advanced tempo estimation"""
        print(f"Advanced tempo analysis for: {file_path}")
        
        try:
            # Load audio
            y, sr = librosa.load(file_path, sr=self.sr)
            
            # Compute tempo and beats
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            beat_times = librosa.frames_to_time(beats, sr=sr)
            
            # Compute onset strength
            onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
            times = librosa.times_like(onset_env, sr=sr, hop_length=512)
            
            # Compute tempogram
            tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr, hop_length=512)
            
            # Plot results
            self.plot_advanced_analysis(y, sr, onset_env, times, beat_times, tempogram, tempo)
            
            print(f"Librosa Estimated Tempo: {tempo:.1f} BPM")
            print(f"Detected {len(beats)} beats")
            
            return tempo, beat_times
            
        except Exception as e:
            print(f"Error in advanced analysis: {e}")
            return None, None
    
    def plot_advanced_analysis(self, y, sr, onset_env, times, beat_times, tempogram, tempo):
        """Plot advanced analysis results"""
        plt.figure(figsize=(15, 12))
        
        # Plot 1: Waveform with beats
        plt.subplot(4, 1, 1)
        librosa.display.waveshow(y, sr=sr, alpha=0.6)
        plt.vlines(beat_times, -1, 1, color='r', alpha=0.8, linewidth=2, label='Detected Beats')
        plt.title(f'Audio Waveform with Beat Detection - Estimated Tempo: {tempo:.1f} BPM', fontsize=14)
        plt.xlabel('')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Onset strength envelope
        plt.subplot(4, 1, 2)
        plt.plot(times, onset_env, label='Onset Strength', linewidth=1.5)
        plt.vlines(beat_times, 0, onset_env.max(), color='r', alpha=0.8, linewidth=2, label='Beats')
        plt.title('Onset Strength Envelope', fontsize=14)
        plt.xlabel('Time (s)')
        plt.ylabel('Strength')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 3: Tempogram
        plt.subplot(4, 1, 3)
        librosa.display.specshow(tempogram, sr=sr, hop_length=512, 
                               x_axis='time', y_axis='tempo', cmap='magma')
        plt.colorbar(format='%0.0f')
        plt.title('Tempogram - Temporal Evolution of Tempo', fontsize=14)
        plt.xlabel('Time (s)')
        plt.ylabel('Tempo (BPM)')
        
        # Plot 4: Beat intervals
        plt.subplot(4, 1, 4)
        if len(beat_times) > 1:
            intervals = np.diff(beat_times)
            plt.plot(beat_times[1:], intervals, 'o-', linewidth=2, markersize=4)
            plt.axhline(y=np.mean(intervals), color='r', linestyle='--', label=f'Avg: {np.mean(intervals):.3f}s')
            plt.title('Beat Intervals', fontsize=14)
            plt.xlabel('Time (s)')
            plt.ylabel('Interval (s)')
            plt.legend()
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def compare_methods(self, file_path):
        """Compare different tempo estimation methods"""
        print(f"Comparing tempo estimation methods for: {file_path}")
        
        y, sr = librosa.load(file_path, sr=self.sr)
        
        # Method 1: Default beat tracking
        tempo1, beats1 = librosa.beat.beat_track(y=y, sr=sr)
        
        # Method 2: With different parameters
        tempo2, beats2 = librosa.beat.beat_track(y=y, sr=sr, tightness=100)
        
        # Method 3: Using dynamic programming
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
        beats_plp = librosa.util.peak_pick(pulse, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.5, wait=10)
        tempo_plp = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)[0]
        
        print(f"\n=== METHOD COMPARISON ===")
        print(f"Default method: {tempo1:.1f} BPM")
        print(f"Tight method: {tempo2:.1f} BPM")
        print(f"PLP method: {tempo_plp:.1f} BPM")
        
        return {
            'default': tempo1,
            'tight': tempo2,
            'plp': tempo_plp
        }

def main():
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        estimator = AdvancedTempoEstimator()
        
        # Run basic analysis
        tempo, beats = estimator.estimate_tempo_librosa(file_path)
        
        # Compare methods
        if tempo:
            estimator.compare_methods(file_path)
    else:
        print("Usage: python advanced_tempo.py <audio_file>")

if __name__ == "__main__":
    main()