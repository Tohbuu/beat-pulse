#!/bin/bash
# setup.sh - DSP Project Setup Script

echo "Setting up Beat Detection DSP Project..."

# Create virtual environment
python -m venv dsp-env

# Activate virtual environment
source dsp-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "Installing Python packages..."
pip install numpy scipy librosa matplotlib sounddevice soundfile

echo "Setup complete! To activate the environment, run:"
echo "source dsp-env/bin/activate"
echo ""
echo "To run the beat detector:"
echo "python beat_detector.py"