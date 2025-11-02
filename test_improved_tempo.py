# test_improved_tempo.py
from beat_detector import BeatDetector

def test_improved_tempo():
    detector = BeatDetector()
    
    print("Testing improved tempo estimation on real music...")
    results = detector.analyze_audio_file_enhanced_v2("misc/SpotiMate.io - Baby_ Not Baby - SEULGI.mp3")
    
    if results:
        print(f"\n🎵 RESULTS:")
        print(f"   Tempo: {results['final_tempo']:.1f} BPM")
        print(f"   Downbeats: {len(results['downbeats'])}")
        print(f"   Expected: ~100 BPM")
        
        if abs(results['final_tempo'] - 100) < 10:
            print("   ✅ EXCELLENT - Close to actual tempo!")
        else:
            print("   ⚠️  Still some discrepancy")

if __name__ == "__main__":
    test_improved_tempo()