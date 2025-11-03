import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import threading
import os
import time
from beat_detector import BeatDetector

class EnhancedBeatDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Advanced DSP Beat Detection Analyzer")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        self.detector = BeatDetector()
        self.current_file = None
        self.results = None
        self.current_figures = []
        
        # Configure style
        self.setup_styles()
        self.setup_gui()
        
    def setup_styles(self):
        """Configure modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('TLabelframe', background='#2b2b2b', foreground='white')
        style.configure('TLabelframe.Label', background='#2b2b2b', foreground='white')
        style.configure('TNotebook', background='#2b2b2b')
        style.configure('TNotebook.Tab', background='#404040', foreground='white')
        
    def setup_gui(self):
        """Setup the enhanced GUI layout"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title section
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame, 
                              text="🎵 ADVANCED BEAT DETECTION & TEMPO ANALYSIS",
                              font=('Arial', 16, 'bold'),
                              bg='#2b2b2b', fg='#4FC3F7')
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Digital Signal Processing Project - Multi-Algorithm Beat Detection",
                                 font=('Arial', 10),
                                 bg='#2b2b2b', fg='#B0BEC5')
        subtitle_label.pack()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Analysis Tab
        self.analysis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_tab, text="🎼 Audio Analysis")
        
        # Visualization Tab
        self.viz_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_tab, text="📊 Visualization")
        
        # Results Tab
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="📈 Results")
        
        self.setup_analysis_tab()
        self.setup_visualization_tab()
        self.setup_results_tab()
        
    def setup_analysis_tab(self):
        """Setup the analysis tab"""
        # File selection section
        file_frame = ttk.LabelFrame(self.analysis_tab, text="📁 Audio File Selection", padding="15")
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        file_grid = ttk.Frame(file_frame)
        file_grid.pack(fill=tk.X)
        
        self.file_label = tk.Label(file_grid, text="No file selected", 
                                  bg='#2b2b2b', fg='#E0E0E0', font=('Arial', 9),
                                  wraplength=600, justify=tk.LEFT)
        self.file_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        btn_frame = ttk.Frame(file_grid)
        btn_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(btn_frame, text="Browse Audio File", 
                  command=self.browse_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Create Demo Files", 
                  command=self.create_demo_files).pack(side=tk.LEFT, padx=5)
        
        # Analysis options section
        options_frame = ttk.LabelFrame(self.analysis_tab, text="⚙️ Analysis Options", padding="15")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        analysis_btn_frame = ttk.Frame(options_frame)
        analysis_btn_frame.pack(fill=tk.X)
        
        ttk.Button(analysis_btn_frame, text="🚀 Run Basic Analysis", 
                  command=self.run_basic_analysis).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(analysis_btn_frame, text="🔬 Run Enhanced Analysis", 
                  command=self.run_enhanced_analysis).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(analysis_btn_frame, text="🎤 Real-time Detection", 
                  command=self.start_realtime).pack(side=tk.LEFT)
        
        # Progress section
        self.progress_frame = ttk.LabelFrame(self.analysis_tab, text="📊 Analysis Progress", padding="15")
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_label = tk.Label(self.progress_frame, text="Ready to analyze...",
                                      bg='#2b2b2b', fg='#E0E0E0', font=('Arial', 9))
        self.progress_label.pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
    def setup_visualization_tab(self):
        """Setup the visualization tab"""
        viz_container = ttk.Frame(self.viz_tab)
        viz_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Visualization controls
        controls_frame = ttk.Frame(viz_container)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(controls_frame, text="🔄 Generate Visualizations", 
                  command=self.generate_visualizations).pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="💾 Save Plots", 
                  command=self.save_plots).pack(side=tk.LEFT, padx=(10, 0))
        
        # Visualization canvas
        self.viz_frame = ttk.Frame(viz_container)
        self.viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder for visualizations
        self.viz_placeholder = tk.Label(self.viz_frame, 
                                       text="Visualizations will appear here after analysis\n\nRun analysis first, then click 'Generate Visualizations'",
                                       bg='#2b2b2b', fg='#757575', font=('Arial', 12),
                                       justify=tk.CENTER)
        self.viz_placeholder.pack(expand=True)
        
    def setup_results_tab(self):
        """Setup the results tab"""
        results_container = ttk.Frame(self.results_tab)
        results_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(results_container, 
                                                     wrap=tk.WORD,
                                                     width=80, 
                                                     height=25,
                                                     font=('Consolas', 10),
                                                     bg='#1e1e1e',
                                                     fg='#ffffff',
                                                     insertbackground='white')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Results controls
        results_controls = ttk.Frame(results_container)
        results_controls.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(results_controls, text="📋 Copy Results", 
                  command=self.copy_results).pack(side=tk.LEFT)
        ttk.Button(results_controls, text="💾 Save Results", 
                  command=self.save_results).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(results_controls, text="🧹 Clear Results", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=(10, 0))
        
    def browse_file(self):
        """Browse for audio file"""
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.flac *.m4a *.aac"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.current_file = filename
            file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
            self.file_label.config(
                text=f"📄 {os.path.basename(filename)}\n"
                     f"📁 {os.path.dirname(filename)}\n"
                     f"💾 {file_size:.1f} MB"
            )
            self.update_progress("File selected - Ready for analysis")
            
    def create_demo_files(self):
        """Create demo beat files"""
        def create_demos():
            try:
                self.update_progress("Creating demo files...")
                from demo_signal import create_demo_beat_signal
                
                tempos = [90, 120, 140]
                for tempo in tempos:
                    self.update_progress(f"Creating {tempo} BPM demo file...")
                    create_demo_beat_signal(f"demo_{tempo}bpm.wav", tempo=tempo, duration=10)
                    time.sleep(0.5)
                
                self.update_progress("Demo files created successfully! ✅")
                messagebox.showinfo("Success", "Demo files created:\n• demo_90bpm.wav\n• demo_120bpm.wav\n• demo_140bpm.wav")
                
            except Exception as e:
                self.update_progress(f"Error creating demo files: {e}")
                messagebox.showerror("Error", f"Failed to create demo files: {e}")
        
        threading.Thread(target=create_demos, daemon=True).start()
        
    def run_basic_analysis(self):
        """Run basic beat detection analysis"""
        if not self.current_file:
            messagebox.showerror("Error", "Please select an audio file first!")
            return
        
        def analysis_thread():
            try:
                self.progress.start()
                self.update_progress("Starting basic analysis...")
                
                # Run basic analysis
                self.update_progress("Loading audio file...")
                self.results = self.detector.analyze_audio_file(self.current_file, visualize=False)
                
                if self.results:
                    self.root.after(0, self.display_basic_results)
                    self.update_progress("Basic analysis completed! ✅")
                else:
                    self.update_progress("Analysis failed - no results returned")
                    
            except Exception as e:
                self.update_progress(f"Analysis error: {e}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {e}"))
            finally:
                self.progress.stop()
        
        threading.Thread(target=analysis_thread, daemon=True).start()
        
    def run_enhanced_analysis(self):
        """Run enhanced beat detection analysis"""
        if not self.current_file:
            messagebox.showerror("Error", "Please select an audio file first!")
            return
        
        def analysis_thread():
            try:
                self.progress.start()
                self.update_progress("Starting enhanced analysis...")
                
                # Run enhanced analysis
                self.update_progress("Loading audio with enhanced features...")
                self.results = self.detector.analyze_audio_file_enhanced(self.current_file, visualize=False)
                
                if self.results:
                    self.root.after(0, self.display_enhanced_results)
                    self.update_progress("Enhanced analysis completed! ✅")
                else:
                    self.update_progress("Enhanced analysis failed - no results returned")
                    
            except Exception as e:
                self.update_progress(f"Enhanced analysis error: {e}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Enhanced analysis failed: {e}"))
            finally:
                self.progress.stop()
        
        threading.Thread(target=analysis_thread, daemon=True).start()
        
    def display_basic_results(self):
        """Display basic analysis results"""
        if not self.results:
            return
            
        results_text = f"""
🎵 BASIC BEAT DETECTION RESULTS
{'='*50}

📊 ANALYSIS SUMMARY:
• Audio Duration: {self.results['audio_length']:.2f} seconds
• Sample Rate: {self.detector.sample_rate} Hz

🎼 TEMPO ANALYSIS:
• Energy Method: {self.results['tempo_energy']:.1f} BPM
• Spectral Flux: {self.results['tempo_flux']:.1f} BPM
• Final Estimate: {np.mean([self.results['tempo_energy'], self.results['tempo_flux']]):.1f} BPM

🥁 BEAT DETECTION:
• Energy Beats: {len(self.results['energy_beats'])} beats
• Flux Beats: {len(self.results['flux_beats'])} beats
• Beat Density: {len(self.results['energy_beats'])/self.results['audio_length']:.2f} beats/sec

📈 BEAT INTERVALS:
• Min Interval: {np.min(np.diff(self.results['energy_beats'])):.3f}s
• Max Interval: {np.max(np.diff(self.results['energy_beats'])):.3f}s  
• Avg Interval: {np.mean(np.diff(self.results['energy_beats'])):.3f}s
• Consistency: {np.std(np.diff(self.results['energy_beats'])):.3f}s std dev

{'='*50}
        """
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results_text)
        self.notebook.select(self.results_tab)
        
    def display_enhanced_results(self):
        """Display enhanced analysis results"""
        if not self.results:
            return
            
        # Calculate additional metrics
        tempo_stability = np.std(self.results['tempo_over_time']) if self.results['tempo_over_time'] else 0
        tempo_range = f"{min(self.results['tempo_over_time']):.1f}-{max(self.results['tempo_over_time']):.1f}" if self.results['tempo_over_time'] else "N/A"
        
        results_text = f"""
🎵 ENHANCED BEAT DETECTION RESULTS
{'='*60}

📊 COMPREHENSIVE ANALYSIS:
• Audio Duration: {self.results['audio_length']:.2f} seconds
• Sample Rate: {self.detector.sample_rate} Hz
• Processing Method: Multi-Algorithm Fusion

🎼 ADVANCED TEMPO ANALYSIS:
• Primary Tempo: {self.results['final_tempo']:.1f} BPM
• Energy Method: {self.results['tempo_energy']:.1f} BPM  
• Spectral Flux: {self.results['tempo_flux']:.1f} BPM
• Tempo Range: {tempo_range} BPM
• Tempo Stability: {tempo_stability:.1f} BPM std dev

🥁 RHYTHMIC STRUCTURE:
• Total Beats: {len(self.results['energy_beats'])} beats
• Downbeats: {len(self.results['downbeats'])} strong beats
• Weak Beats: {len(self.results['weak_beats'])} weak beats
• Downbeat Ratio: {len(self.results['downbeats'])/len(self.results['energy_beats'])*100:.1f}%

📈 BEAT PATTERN ANALYSIS:
• Beat Density: {len(self.results['energy_beats'])/self.results['audio_length']:.2f} beats/sec
• Dynamic Thresholding: ✅ Active
• Tempo Smoothing: ✅ Applied
• Downbeat Detection: ✅ Implemented

🎯 ALGORITHM PERFORMANCE:
• Energy Detection: {len(self.results['energy_beats'])} beats
• Spectral Flux: {len(self.results['flux_beats'])} beats  
• Algorithm Agreement: {'High' if abs(self.results['tempo_energy'] - self.results['tempo_flux']) < 20 else 'Moderate'}

{'='*60}
💡 MUSICAL INTERPRETATION:
This analysis suggests a {'consistent' if tempo_stability < 10 else 'varied'} rhythmic structure
with {'clear' if len(self.results['downbeats']) > len(self.results['energy_beats'])/8 else 'subtle'} downbeat emphasis.
        """
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results_text)
        self.notebook.select(self.results_tab)
        
    def generate_visualizations(self):
        """Generate and display visualizations"""
        if not self.results:
            messagebox.showwarning("Warning", "Please run analysis first!")
            return
            
        try:
            # Clear previous visualizations
            for widget in self.viz_frame.winfo_children():
                widget.destroy()
                
            # Create new visualizations
            if hasattr(self.detector, 'analyze_audio_file_enhanced'):
                # Use enhanced visualization
                audio, sr = self.detector.load_audio(self.current_file)
                energy = self.detector.compute_energy(audio)
                spectral_flux = self.detector.compute_spectral_flux(audio)
                time_axis = np.arange(len(energy)) * self.detector.hop_size / sr
                
                self.detector.visualize_enhanced_results(
                    audio, sr, energy, spectral_flux,
                    self.results['energy_beats'], 
                    self.results.get('downbeats', []),
                    self.results.get('tempo_over_time', []),
                    self.results.get('tempo_times', []),
                    self.results.get('flux_beats', [])
                )
            else:
                # Use basic visualization
                self.detector.analyze_audio_file(self.current_file, visualize=True)
                
            self.update_progress("Visualizations generated! ✅")
            self.notebook.select(self.viz_tab)
            
        except Exception as e:
            messagebox.showerror("Error", f"Visualization failed: {e}")
            
    def start_realtime(self):
        """Start real-time beat detection"""
        def realtime_thread():
            from real_time_detector import simple_real_time_detection
            simple_real_time_detection()
            
        threading.Thread(target=realtime_thread, daemon=True).start()
        self.update_progress("Real-time detection started... Speak or play music!")
        
    def update_progress(self, message):
        """Update progress label"""
        def update():
            self.progress_label.config(text=message)
        self.root.after(0, update)
        
    def copy_results(self):
        """Copy results to clipboard"""
        results = self.results_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(results)
        self.update_progress("Results copied to clipboard! ✅")
        
    def save_results(self):
        """Save results to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(self.results_text.get(1.0, tk.END))
            self.update_progress(f"Results saved to {filename} ✅")
            
    def save_plots(self):
        """Save current plots"""
        if hasattr(self, 'current_figures') and self.current_figures:
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filename:
                try:
                    self.current_figures[0].savefig(filename, dpi=300, bbox_inches='tight')
                    self.update_progress(f"Plot saved to {filename} ✅")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save plot: {e}")
        else:
            messagebox.showwarning("Warning", "No plots available to save")
            
    def clear_results(self):
        """Clear results"""
        self.results_text.delete(1.0, tk.END)
        self.update_progress("Results cleared")

def main():
    root = tk.Tk()
    app = EnhancedBeatDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()