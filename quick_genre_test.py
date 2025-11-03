# quick_genre_test.py
from genre_analysis import GenreAnalyzer
import os

def test_all_genres():
    analyzer = GenreAnalyzer()
    
    # Test files with expected tempos for comparison
    test_files = [
        ("music/electronic/grimes_genesis.mp3", "Electronic", 140),
        ("music/electronic/deadmau5_strobe.mp3", "Electronic", 128),
        ("music/classical/beethoven_symphony5.mp3", "Classical", 108),
        ("music/classical/mozart_nachtmusik.mp3", "Classical", 126),
        ("music/jazz/miles_davis_so_what.mp3", "Jazz", 150),
        ("music/jazz/brubeck_take_five.mp3", "Jazz", 174),
        ("music/rock/acdc_back_in_black.mp3", "Rock", 93),
        ("music/rock/deep_purple_smoke.mp3", "Rock", 112),
        ("music/hiphop/dr_dre_next_episode.mp3", "HipHop", 95),
        ("music/hiphop/biggie_juicy.mp3", "HipHop", 94),
        ("music/acoustic/dylan_blowin_wind.mp3", "Acoustic", 96),
        ("music/acoustic/chapman_fast_car.mp3", "Acoustic", 112)
    ]
    
    results = []
    
    for file_path, genre, expected_tempo in test_files:
        if os.path.exists(file_path):
            print(f"\n{'='*60}")
            print(f"🎵 Testing: {os.path.basename(file_path)}")
            print(f"🎼 Genre: {genre} | Expected: {expected_tempo} BPM")
            print('='*60)
            
            try:
                analysis_results = analyzer.detector.analyze_audio_file_enhanced(file_path, visualize=True)
                
                if analysis_results:
                    detected_tempo = analysis_results['final_tempo']
                    accuracy = (1 - abs(detected_tempo - expected_tempo) / expected_tempo) * 100
                    
                    print(f"📊 RESULTS:")
                    print(f"   ✅ Detected: {detected_tempo:.1f} BPM")
                    print(f"   🎯 Expected: {expected_tempo} BPM") 
                    print(f"   📈 Accuracy: {accuracy:.1f}%")
                    print(f"   🥁 Beats: {len(analysis_results['energy_beats'])}")
                    
                    results.append({
                        'genre': genre,
                        'file': os.path.basename(file_path),
                        'expected_tempo': expected_tempo,
                        'detected_tempo': detected_tempo,
                        'accuracy': accuracy,
                        'beats_detected': len(analysis_results['energy_beats'])
                    })
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    # Summary
    if results:
        print(f"\n{'='*80}")
        print("🎯 GENRE TESTING SUMMARY")
        print('='*80)
        
        for genre in set(r['genre'] for r in results):
            genre_results = [r for r in results if r['genre'] == genre]
            avg_accuracy = sum(r['accuracy'] for r in genre_results) / len(genre_results)
            print(f"\n🎵 {genre.upper()}: {avg_accuracy:.1f}% average accuracy")
            for result in genre_results:
                print(f"   📄 {result['file']}: {result['detected_tempo']:.1f} BPM ({result['accuracy']:.1f}%)")

if __name__ == "__main__":
    test_all_genres()