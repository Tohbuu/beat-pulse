# test_installation.py
def test_installation():
    print("Testing DSP project installation...")
    
    try:
        import numpy as np
        print(f"✓ NumPy {np.__version__}")
        
        import scipy
        print(f"✓ SciPy {scipy.__version__}")
        
        import librosa
        print(f"✓ Librosa {librosa.__version__}")
        
        import matplotlib
        print(f"✓ Matplotlib {matplotlib.__version__}")
        
        import sounddevice as sd
        print(f"✓ SoundDevice {sd.__version__}")
        
        import soundfile as sf
        print(f"✓ SoundFile")
        
        # Test basic DSP functionality
        print("\nTesting basic DSP operations...")
        t = np.linspace(0, 1, 44100)
        signal = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
        energy = np.sum(signal ** 2)
        print(f"✓ Basic signal processing - 440Hz sine wave energy: {energy:.2f}")
        
        # Test FFT
        spectrum = np.fft.fft(signal)
        freq = np.fft.fftfreq(len(signal), 1/44100)
        peak_freq = np.abs(freq[np.argmax(np.abs(spectrum))])
        print(f"✓ FFT test - Peak frequency: {peak_freq:.1f} Hz")
        
        print("\n🎉 All tests passed! Your DSP environment is ready.")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    test_installation()