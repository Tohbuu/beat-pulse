# genre_analysis.py
import os
import pandas as pd
from beat_detector import BeatDetector
import matplotlib.pyplot as plt

class GenreAnalyzer:
    def __init__(self):
        self.detector = BeatDetector()
        self.results = []
    
    def analyze_genre_directory(self, directory_path, genre_name):
        """Analyze all audio files in a directory for a specific genre"""
        print(f"\n🎵 Analyzing {genre_name} music...")
        
        if not os.path.exists(directory_path):
            print(f"Directory not found: {directory_path}")
            return
        
        audio_files = [f for f in os.listdir(directory_path) 
                      if f.lower().endswith(('.wav', '.mp3', '.flac'))]
        
        if not audio_files:
            print(f"No audio files found in {directory_path}")
            return
        
        for audio_file in audio_files:
            file_path = os.path.join(directory_path, audio_file)
            print(f"\n📁 Analyzing: {audio_file}")
            
            try:
                results = self.detector.analyze_audio_file_enhanced(file_path, visualize=False)
                
                if results:
                    # Calculate additional metrics
                    beat_intervals = np.diff(results['energy_beats'])
                    tempo_stability = np.std(results['tempo_over_time']) if results['tempo_over_time'] else 0
                    
                    genre_result = {
                        'genre': genre_name,
                        'file': audio_file,
                        'duration': results['audio_length'],
                        'tempo_energy': results['tempo_energy'],
                        'tempo_flux': results['tempo_flux'],
                        'final_tempo': results['final_tempo'],
                        'total_beats': len(results['energy_beats']),
                        'downbeats': len(results.get('downbeats', [])),
                        'beat_density': len(results['energy_beats']) / results['audio_length'],
                        'tempo_stability': tempo_stability,
                        'interval_consistency': np.std(beat_intervals) if len(beat_intervals) > 1 else 0,
                        'algorithm_agreement': abs(results['tempo_energy'] - results['tempo_flux'])
                    }
                    
                    self.results.append(genre_result)
                    print(f"   ✅ Tempo: {results['final_tempo']:.1f} BPM | Beats: {len(results['energy_beats'])}")
                    
            except Exception as e:
                print(f"   ❌ Error analyzing {audio_file}: {e}")
    
    def generate_genre_report(self):
        """Generate comprehensive genre analysis report"""
        if not self.results:
            print("No results to analyze!")
            return
        
        df = pd.DataFrame(self.results)
        
        print("\n" + "="*80)
        print("🎵 GENRE ANALYSIS REPORT")
        print("="*80)
        
        # Summary by genre
        genre_summary = df.groupby('genre').agg({
            'final_tempo': ['mean', 'std'],
            'beat_density': 'mean',
            'tempo_stability': 'mean',
            'algorithm_agreement': 'mean',
            'file': 'count'
        }).round(2)
        
        print("\n📊 Genre Performance Summary:")
        print(genre_summary)
        
        # Create visualizations
        self.plot_genre_comparison(df)
        
        return df
    
    def plot_genre_comparison(self, df):
        """Create comparison plots across genres"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('DSP Beat Detection - Genre Performance Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Tempo distribution by genre
        genres = df['genre'].unique()
        tempo_data = [df[df['genre'] == genre]['final_tempo'] for genre in genres]
        
        axes[0,0].boxplot(tempo_data, labels=genres)
        axes[0,0].set_title('Tempo Distribution by Genre')
        axes[0,0].set_ylabel('BPM')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Plot 2: Beat density by genre
        density_data = [df[df['genre'] == genre]['beat_density'] for genre in genres]
        axes[0,1].boxplot(density_data, labels=genres)
        axes[0,1].set_title('Beat Density by Genre (beats/second)')
        axes[0,1].set_ylabel('Beats/Second')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Plot 3: Tempo stability by genre
        stability_data = [df[df['genre'] == genre]['tempo_stability'] for genre in genres]
        axes[1,0].boxplot(stability_data, labels=genres)
        axes[1,0].set_title('Tempo Stability by Genre (BPM std dev)')
        axes[1,0].set_ylabel('BPM Standard Deviation')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Plot 4: Algorithm agreement by genre
        agreement_data = [df[df['genre'] == genre]['algorithm_agreement'] for genre in genres]
        axes[1,1].boxplot(agreement_data, labels=genres)
        axes[1,1].set_title('Algorithm Agreement by Genre (BPM difference)')
        axes[1,1].set_ylabel('Energy vs Flux BPM Difference')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
        
    def analyze_single_file_detailed(self, file_path, genre="Unknown"):
        """Detailed analysis of a single file with visualization"""
        print(f"\n🔬 Detailed Analysis: {os.path.basename(file_path)}")
        print(f"🎵 Genre: {genre}")
        
        try:
            results = self.detector.analyze_audio_file_enhanced(file_path, visualize=True)
            
            if results:
                print(f"\n📈 Detailed Metrics:")
                print(f"   • Duration: {results['audio_length']:.2f}s")
                print(f"   • Final Tempo: {results['final_tempo']:.1f} BPM")
                print(f"   • Energy Method: {results['tempo_energy']:.1f} BPM")
                print(f"   • Flux Method: {results['tempo_flux']:.1f} BPM")
                print(f"   • Total Beats: {len(results['energy_beats'])}")
                print(f"   • Downbeats: {len(results.get('downbeats', []))}")
                print(f"   • Beat Density: {len(results['energy_beats'])/results['audio_length']:.2f} beats/sec")
                
                if results['tempo_over_time']:
                    print(f"   • Tempo Range: {min(results['tempo_over_time']):.1f}-{max(results['tempo_over_time']):.1f} BPM")
                    print(f"   • Tempo Stability: {np.std(results['tempo_over_time']):.1f} BPM std dev")
                
                # Genre-specific insights
                self.provide_genre_insights(genre, results)
                
        except Exception as e:
            print(f"❌ Error in detailed analysis: {e}")

    def provide_genre_insights(self, genre, results):
        """Provide genre-specific insights"""
        print(f"\n💡 {genre.upper()} MUSIC INSIGHTS:")
        
        if genre.lower() in ['electronic', 'edm', 'techno']:
            if results['tempo_stability'] < 5:
                print("   ✅ Typical electronic music: Consistent tempo")
            else:
                print("   ⚠️  Unusual: Electronic music usually has very stable tempo")
                
        elif genre.lower() in ['classical', 'orchestral']:
            if results['tempo_stability'] > 10:
                print("   ✅ Expected: Classical often has tempo variations (rubato)")
            if results['beat_density'] < 1.5:
                print("   ✅ Expected: Sparse beat patterns common in classical")
                
        elif genre.lower() in ['jazz']:
            if results['algorithm_agreement'] > 20:
                print("   ✅ Expected: Jazz rhythms often challenge beat detection")
            if results['tempo_stability'] > 8:
                print("   ✅ Expected: Jazz frequently has tempo flexibility")
                
        elif genre.lower() in ['rock', 'metal']:
            if 100 <= results['final_tempo'] <= 160:
                print("   ✅ Typical rock tempo range")
            if results['downbeats'] / len(results['energy_beats']) > 0.15:
                print("   ✅ Clear downbeat emphasis typical in rock")
                
        elif genre.lower() in ['hiphop', 'rap']:
            if 70 <= results['final_tempo'] <= 120:
                print("   ✅ Common hip-hop tempo range")
            if results['beat_density'] > 2.0:
                print("   ✅ High beat density typical in hip-hop")

def main():
    analyzer = GenreAnalyzer()
    
    print("🎵 DSP BEAT DETECTION - GENRE ANALYSIS TOOL")
    print("="*60)
    
    # Test different genres (modify paths as needed)
    genre_directories = {
        'Electronic': 'music/electronic',
        'Classical': 'music/classical', 
        'Jazz': 'music/jazz',
        'Rock': 'music/rock',
        'HipHop': 'music/hiphop',
        'Acoustic': 'music/acoustic'
    }
    
    # Analyze each genre directory
    for genre, directory in genre_directories.items():
        analyzer.analyze_genre_directory(directory, genre)
    
    # Generate comprehensive report
    if analyzer.results:
        df = analyzer.generate_genre_report()
        
        # Save results to CSV
        df.to_csv('genre_analysis_results.csv', index=False)
        print(f"\n💾 Results saved to 'genre_analysis_results.csv'")
        
        # Show top performing genres
        avg_agreement = df.groupby('genre')['algorithm_agreement'].mean().sort_values()
        print(f"\n🏆 Best Performing Genres (by algorithm agreement):")
        for genre, agreement in avg_agreement.items():
            print(f"   {genre}: {agreement:.1f} BPM difference")

if __name__ == "__main__":
    main()