# test_enhanced_system.py
from beat_detector import BeatDetector

def main():
    detector = BeatDetector()
    
    print("Testing Enhanced Beat Detection System")
    print("=" * 50)
    
    # Test with demo files first
    test_files = ["demo_120bpm.wav", "demo_90bpm.wav", "demo_140bpm.wav"]
    
    for file in test_files:
        print(f"\n🎵 Testing: {file}")
        try:
            results = detector.analyze_audio_file_enhanced(file)
            if results:
                print(f"✅ Enhanced analysis completed!")
                print(f"   Final Tempo: {results['final_tempo']:.1f} BPM")
                print(f"   Downbeats: {len(results['downbeats'])}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test with real music
    print(f"\n🎵 Testing with real music...")
    try:
        results = detector.analyze_audio_file_enhanced("misc/SpotiMate.io - Baby_ Not Baby - SEULGI.mp3")
        if results:
            print(f"✅ Real music analysis completed!")
            print(f"   Final Tempo: {results['final_tempo']:.1f} BPM")
            print(f"   Downbeats: {len(results['downbeats'])}")
            print(f"   Tempo varied: {min(results['tempo_over_time']):.1f}-{max(results['tempo_over_time']):.1f} BPM")
    except Exception as e:
        print(f"❌ Error with real music: {e}")

if __name__ == "__main__":
    main()