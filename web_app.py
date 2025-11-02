from flask import Flask, render_template, request, jsonify, send_file
import os
import numpy as np
from beat_detector import BeatDetector
import tempfile
import soundfile as sf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

detector = BeatDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded file
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    
    try:
        # Analyze the file
        results = detector.analyze_audio_file(filename, visualize=False)
        
        # Clean up
        os.remove(filename)
        
        return jsonify({
            'success': True,
            'tempo_energy': round(results['tempo_energy'], 1),
            'tempo_flux': round(results['tempo_flux'], 1),
            'average_tempo': round(np.mean([results['tempo_energy'], results['tempo_flux']]), 1),
            'beat_count_energy': len(results['energy_beats']),
            'beat_count_flux': len(results['flux_beats']),
            'duration': round(results['audio_length'], 2)
        })
    
    except Exception as e:
        # Clean up on error too
        if os.path.exists(filename):
            os.remove(filename)
        return jsonify({'error': str(e)}), 500

@app.route('/demo')
def create_demo():
    """Generate a demo beat file"""
    from demo_signal import create_demo_beat_signal
    
    tempo = request.args.get('tempo', 120, type=int)
    filename = f"demo_{tempo}bpm.wav"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    create_demo_beat_signal(filepath, tempo=tempo, duration=10)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)