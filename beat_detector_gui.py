import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
from beat_detector import BeatDetector
from real_time_detector import RealTimeBeatDetector
import os

class BeatDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSP Beat Detection App")
        self.root.geometry("1000x700")
        
        self.detector = BeatDetector()
        self.current_file = None
        self.results = None
        
        self.setup_gui()
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🎵 Beat Detection & Tempo Estimation", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Audio File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(file_frame, text="Browse Audio File", 
                  command=self.browse_file).grid(row=0, column=1, padx=(10, 0))
        ttk.Button(file_frame, text="Analyze", 
                  command=self.analyze_file).grid(row=0, column=2, padx=(10, 0))
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.results_text = tk.Text(results_frame, height=8, width=80, font=('Courier', 10))
        self.results_text.grid(row=0, column=0, columnspan=2)
        
        # Visualization frame
        viz_frame = ttk.LabelFrame(main_frame, text="Visualization", padding="10")
        viz_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create matplotlib figure
        self.fig, self.axes = plt.subplots(2, 1, figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Real-time section
        realtime_frame = ttk.LabelFrame(main_frame, text="Real-time Detection", padding="10")
        realtime_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(realtime_frame, text="Start Real-time Detection", 
                  command=self.start_realtime).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(realtime_frame, text="Stop Real-time", 
                  command=self.stop_realtime).grid(row=0, column=1)
        
        self.realtime_status = ttk.Label(realtime_frame, text="Ready")
        self.realtime_status.grid(row=0, column=2, padx=(20, 0))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.flac *.m4a"),
                ("WAV files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.current_file = filename
            self.file_label.config(text=os.path.basename(filename))
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"File selected: {os.path.basename(filename)}\n")
    
    def analyze_file(self):
        if not self.current_file:
            messagebox.showerror("Error", "Please select an audio file first!")
            return
        
        def analysis_thread():
            try:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "Analyzing... Please wait...\n")
                self.results_text.update()
                
                # Run analysis
                self.results = self.detector.analyze_audio_file(self.current_file, visualize=False)
                
                # Update results in GUI
                self.root.after(0, self.update_results)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
        
        # Run analysis in separate thread to avoid freezing GUI
        threading.Thread(target=analysis_thread, daemon=True).start()
    
    def update_results(self):
        if self.results:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "=== BEAT DETECTION RESULTS ===\n\n")
            self.results_text.insert(tk.END, f"Tempo (Energy method): {self.results['tempo_energy']:.1f} BPM\n")
            self.results_text.insert(tk.END, f"Tempo (Spectral Flux): {self.results['tempo_flux']:.1f} BPM\n")
            self.results_text.insert(tk.END, f"Average Tempo: {np.mean([self.results['tempo_energy'], self.results['tempo_flux']]):.1f} BPM\n\n")
            self.results_text.insert(tk.END, f"Detected beats (Energy): {len(self.results['energy_beats'])}\n")
            self.results_text.insert(tk.END, f"Detected beats (Flux): {len(self.results['flux_beats'])}\n")
            self.results_text.insert(tk.END, f"Audio duration: {self.results['audio_length']:.2f} seconds\n")
            
            # Create simple visualization
            self.create_simple_visualization()
    
    def create_simple_visualization(self):
        """Create a simplified visualization for the GUI"""
        for ax in self.axes:
            ax.clear()
        
        if self.results and len(self.results['energy_beats']) > 0:
            # Plot 1: Beat timeline
            self.axes[0].vlines(self.results['energy_beats'], 0, 1, color='red', alpha=0.7, linewidth=2, label='Energy Beats')
            self.axes[0].vlines(self.results['flux_beats'], 0, 0.5, color='blue', alpha=0.7, linewidth=2, label='Flux Beats')
            self.axes[0].set_title('Beat Timeline')
            self.axes[0].set_xlabel('Time (seconds)')
            self.axes[0].set_ylabel('Method')
            self.axes[0].legend()
            self.axes[0].grid(True, alpha=0.3)
            
            # Plot 2: Beat intervals
            if len(self.results['energy_beats']) > 1:
                intervals = np.diff(self.results['energy_beats'])
                self.axes[1].plot(self.results['energy_beats'][1:], intervals, 'o-')
                self.axes[1].axhline(y=np.mean(intervals), color='r', linestyle='--', 
                                   label=f'Avg: {np.mean(intervals):.3f}s')
                self.axes[1].set_title('Beat Intervals')
                self.axes[1].set_xlabel('Time (seconds)')
                self.axes[1].set_ylabel('Interval (seconds)')
                self.axes[1].legend()
                self.axes[1].grid(True, alpha=0.3)
        
        self.canvas.draw()
    
    def start_realtime(self):
        def realtime_thread():
            from real_time_detector import simple_real_time_detection
            simple_real_time_detection()
        
        threading.Thread(target=realtime_thread, daemon=True).start()
        self.realtime_status.config(text="Running...")
    
    def stop_realtime(self):
        # Note: This is a simple implementation. For proper control, we'd need to modify the realtime detector
        self.realtime_status.config(text="Stopped")
        messagebox.showinfo("Info", "Real-time detection stopped")

def main():
    root = tk.Tk()
    app = BeatDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()