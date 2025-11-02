import numpy as np
import matplotlib.pyplot as plt
import librosa
import sounddevice as sd
import soundfile as sf
import argparse
import os
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, find_peaks


class BeatDetector:
    def __init__(self, sample_rate=22050, frame_size=1024, hop_size=512):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        
    def load_audio(self, file_path):
        """Load audio file and convert to mono"""
        print(f"Loading audio file: {file_path}")
        
        try:
            # Method 1: Try using soundfile first (more reliable for MP3)
            try:
                audio, sr = sf.read(file_path)
                # If stereo, convert to mono
                if len(audio.shape) > 1:
                    audio = np.mean(audio, axis=1)
                # Resample if necessary
                if sr != self.sample_rate:
                    import librosa
                    audio = librosa.resample(audio, orig_sr=sr, target_sr=self.sample_rate)
                    sr = self.sample_rate
                    
            except Exception as e:
                print(f"SoundFile failed, trying Librosa: {e}")
                # Method 2: Use librosa as fallback
                import librosa
                audio, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)
            
            print(f"Audio loaded: {len(audio)/sr:.2f} seconds, Sample rate: {sr} Hz")
            return audio, sr
            
        except Exception as e:
            print(f"Error loading audio: {e}")
            return None, None
    
    def bandpass_filter(self, audio, lowcut=80, highcut=16000):
        """Apply bandpass filter to focus on percussive elements"""
        print("Applying bandpass filter...")
        nyquist = self.sample_rate / 2
        low = lowcut / nyquist
        high = highcut / nyquist
        
        # Butterworth bandpass filter
        b, a = butter(4, [low, high], btype='band')
        filtered_audio = filtfilt(b, a, audio)
        return filtered_audio
    
    def compute_energy(self, audio):
        """Compute energy envelope of the signal"""
        print("Computing energy envelope...")
        energy = []
        frames = len(audio) // self.hop_size
        
        for i in range(frames):
            start = i * self.hop_size
            end = start + self.frame_size
            if end < len(audio):
                frame = audio[start:end]
                energy.append(np.sum(frame ** 2))
        
        return np.array(energy)
    
    def compute_spectral_flux(self, audio):
        """Compute spectral flux for beat detection"""
        print("Computing spectral flux...")
        frames = len(audio) // self.hop_size
        flux = []
        prev_spectrum = None
        
        for i in range(frames):
            start = i * self.hop_size
            end = start + self.frame_size
            if end < len(audio):
                frame = audio[start:end]
                windowed = frame * np.hanning(len(frame))
                spectrum = np.abs(np.fft.fft(windowed)[:len(windowed)//2])
                
                if prev_spectrum is not None:
                    diff = spectrum - prev_spectrum
                    diff[diff < 0] = 0  # Only consider increases
                    flux.append(np.sum(diff))
                else:
                    flux.append(0)
                
                prev_spectrum = spectrum
        
        return np.array(flux)
    
    def detect_beats(self, energy_signal, threshold_factor=1.5):
        """Detect beats from energy signal"""
        # Dynamic threshold
        threshold = np.mean(energy_signal) * threshold_factor
        
        # Find peaks that exceed threshold
        min_distance = self.sample_rate // (self.hop_size * 4)  # Prevent too close beats
        peaks, properties = find_peaks(energy_signal, height=threshold, distance=min_distance)
        
        print(f"Detected {len(peaks)} beats with threshold factor {threshold_factor}")
        return peaks
    
    def estimate_tempo(self, beat_times, method='autocorrelation'):
        """Estimate tempo from beat intervals"""
        if len(beat_times) < 2:
            return 0
            
        if method == 'interval':
            # Simple average of intervals
            intervals = np.diff(beat_times)
            avg_interval = np.median(intervals)
            tempo = 60.0 / avg_interval if avg_interval > 0 else 0
            
        elif method == 'autocorrelation':
            # Use autocorrelation for more robust tempo estimation
            beat_signal = np.zeros(int(beat_times[-1] * self.sample_rate) + 1)
            for beat in beat_times:
                idx = int(beat * self.sample_rate)
                if idx < len(beat_signal):
                    beat_signal[idx] = 1
            
            # Compute autocorrelation
            correlation = np.correlate(beat_signal, beat_signal, mode='full')
            correlation = correlation[len(correlation)//2:]
            
            # Find peaks in autocorrelation (excluding zero lag)
            min_lag = int(0.3 * self.sample_rate)  # ~200 BPM max
            max_lag = int(2.0 * self.sample_rate)  # ~30 BPM min
            
            correlation = correlation[min_lag:max_lag]
            peaks, _ = find_peaks(correlation, distance=int(0.5 * self.sample_rate))
            
            if len(peaks) > 0:
                main_peak = peaks[0] + min_lag
                beat_period = main_peak / self.sample_rate
                tempo = 60.0 / beat_period
            else:
                tempo = 0
                
        return tempo

    def analyze_audio_file(self, file_path, visualize=True):
        """Complete analysis of an audio file"""
        print(f"\n=== Analyzing: {file_path} ===")
        
        # Load and process audio
        audio, sr = self.load_audio(file_path)
        if audio is None:
            return None
            
        # Update sample rate if different from loaded file
        if sr != self.sample_rate:
            self.sample_rate = sr
            
        audio = self.bandpass_filter(audio)
        
        # Compute features
        energy = self.compute_energy(audio)
        spectral_flux = self.compute_spectral_flux(audio)
        
        # Detect beats
        energy_beats = self.detect_beats(energy)
        flux_beats = self.detect_beats(spectral_flux, threshold_factor=1.3)
        
        # Convert to time
        time_axis = np.arange(len(energy)) * self.hop_size / sr
        energy_beat_times = time_axis[energy_beats]
        flux_beat_times = time_axis[flux_beats]
        
        # Estimate tempo
        tempo_energy = self.estimate_tempo(energy_beat_times)
        tempo_flux = self.estimate_tempo(flux_beat_times)
        
        print(f"\n=== RESULTS ===")
        print(f"Tempo (Energy method): {tempo_energy:.1f} BPM")
        print(f"Tempo (Spectral Flux): {tempo_flux:.1f} BPM")
        print(f"Detected {len(energy_beat_times)} beats (Energy method)")
        print(f"Detected {len(flux_beat_times)} beats (Spectral Flux method)")
        
        if visualize:
            self.visualize_results(audio, sr, energy, spectral_flux, 
                                 energy_beats, flux_beats, time_axis,
                                 energy_beat_times, flux_beat_times)
        
        return {
            'tempo_energy': tempo_energy,
            'tempo_flux': tempo_flux,
            'energy_beats': energy_beat_times,
            'flux_beats': flux_beat_times,
            'audio_length': len(audio)/sr
        }
    
    def visualize_results(self, audio, sr, energy, spectral_flux, 
                         energy_beats, flux_beats, time_axis,
                         energy_beat_times, flux_beat_times):
        """Visualize the analysis results"""
        print("Generating visualization...")
        
        plt.figure(figsize=(15, 10))
        
        # Plot 1: Original audio
        plt.subplot(4, 1, 1)
        time_audio = np.arange(len(audio)) / sr
        plt.plot(time_audio, audio, alpha=0.7)
        plt.title('Original Audio Signal')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Energy with beats
        plt.subplot(4, 1, 2)
        plt.plot(time_axis, energy, label='Energy Envelope', linewidth=1)
        plt.plot(energy_beat_times, energy[energy_beats], 'ro', markersize=4, label='Detected Beats')
        plt.title('Energy-based Beat Detection')
        plt.xlabel('Time (s)')
        plt.ylabel('Energy')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 3: Spectral flux with beats
        plt.subplot(4, 1, 3)
        plt.plot(time_axis, spectral_flux, label='Spectral Flux', linewidth=1, color='orange')
        plt.plot(flux_beat_times, spectral_flux[flux_beats], 'ro', markersize=4, label='Detected Beats')
        plt.title('Spectral Flux-based Beat Detection')
        plt.xlabel('Time (s)')
        plt.ylabel('Spectral Flux')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 4: Combined view
        plt.subplot(4, 1, 4)
        plt.plot(energy_beat_times, np.ones_like(energy_beat_times), 'ro', markersize=8, label='Energy Beats')
        plt.plot(flux_beat_times, 0.5 * np.ones_like(flux_beat_times), 'bo', markersize=8, label='Flux Beats')
        plt.yticks([0.5, 1.0], ['Flux', 'Energy'])
        plt.title('Beat Timeline Comparison')
        plt.xlabel('Time (s)')
        plt.ylabel('Method')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def real_time_beat_detection():
    """Real-time beat detection using microphone input"""
    print("Starting real-time beat detection...")
    print("Press Ctrl+C to stop")
    
    detector = BeatDetector()
    energy_history = []
    beat_count = 0
    
    def audio_callback(indata, frames, time, status):
        nonlocal beat_count
        if status:
            print(status)
        
        audio = indata[:, 0]  # Use first channel
        energy = np.sum(audio ** 2)
        energy_history.append(energy)
        
        # Keep only recent history
        if len(energy_history) > 50:
            energy_history.pop(0)
        
        # Dynamic threshold based on recent history
        if len(energy_history) > 10:
            threshold = np.mean(energy_history) * 2.0
            if energy > threshold and len(energy_history) > 20:
                beat_count += 1
                print(f"BEAT #{beat_count}! ♪ Energy: {energy:.4f}")
    
    try:
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=22050, blocksize=1024):
            while True:
                sd.sleep(100)
    except KeyboardInterrupt:
        print(f"\nStopped. Total beats detected: {beat_count}")

def main():
    parser = argparse.ArgumentParser(description='Beat Detection and Tempo Estimation')
    parser.add_argument('--file', type=str, help='Audio file to analyze')
    parser.add_argument('--realtime', action='store_true', help='Run real-time beat detection')
    
    args = parser.parse_args()
    
    detector = BeatDetector()
    
    if args.realtime:
        real_time_beat_detection()
    elif args.file:
        if os.path.exists(args.file):
            results = detector.analyze_audio_file(args.file)
            if results:
                print(f"\nFinal Tempo Estimate: {np.mean([results['tempo_energy'], results['tempo_flux']]):.1f} BPM")
        else:
            print(f"File not found: {args.file}")
    else:
        print("Beat Detection System Ready!")
        print("\nUsage options:")
        print("1. Analyze audio file: python beat_detector.py --file <audio_file>")
        print("2. Real-time detection: python beat_detector.py --realtime")
        print("3. Demo with test signal: python beat_detector.py --file demo")

if __name__ == "__main__":
    main()