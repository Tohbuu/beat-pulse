# download_organizer.py
import os
import shutil

def setup_music_directory():
    """Create the music directory structure"""
    base_dir = "music"
    genres = ['electronic', 'classical', 'jazz', 'rock', 'hiphop', 'acoustic']
    
    # Create directories
    for genre in genres:
        os.makedirs(os.path.join(base_dir, genre), exist_ok=True)
    
    print("🎵 Music directory structure created!")
    print("📁 Now download these files into the appropriate folders:")
    
    download_list = {
        'electronic': [
            'grimes_genesis.mp3 - Clear electronic beats (~140 BPM)',
            'deadmau5_strobe.mp3 - Progressive house (~128 BPM)'
        ],
        'classical': [
            'beethoven_symphony5.mp3 - Dramatic orchestral (~108 BPM)',
            'mozart_nachtmusik.mp3 - Classical structure (~126 BPM)'
        ],
        'jazz': [
            'miles_davis_so_what.mp3 - Modal jazz (~150 BPM)',
            'brubeck_take_five.mp3 - 5/4 time signature (~174 BPM)'
        ],
        'rock': [
            'acdc_back_in_black.mp3 - Iconic rock (~93 BPM)',
            'deep_purple_smoke.mp3 - Classic riff (~112 BPM)'
        ],
        'hiphop': [
            'dr_dre_next_episode.mp3 - West coast hip-hop (~95 BPM)',
            'biggie_juicy.mp3 - East coast hip-hop (~94 BPM)'
        ],
        'acoustic': [
            'dylan_blowin_wind.mp3 - Folk acoustic (~96 BPM)',
            'chapman_fast_car.mp3 - Acoustic storytelling (~112 BPM)'
        ]
    }
    
    for genre, files in download_list.items():
        print(f"\n🎼 {genre.upper()}:")
        for file_desc in files:
            print(f"   📄 {file_desc}")

def check_downloaded_files():
    """Check which files have been downloaded"""
    expected_files = {
        'electronic': ['grimes_genesis.mp3', 'deadmau5_strobe.mp3'],
        'classical': ['beethoven_symphony5.mp3', 'mozart_nachtmusik.mp3'],
        'jazz': ['miles_davis_so_what.mp3', 'brubeck_take_five.mp3'],
        'rock': ['acdc_back_in_black.mp3', 'deep_purple_smoke.mp3'],
        'hiphop': ['dr_dre_next_episode.mp3', 'biggie_juicy.mp3'],
        'acoustic': ['dylan_blowin_wind.mp3', 'chapman_fast_car.mp3']
    }
    
    print("\n🔍 Checking downloaded files...")
    
    for genre, files in expected_files.items():
        genre_path = os.path.join("music", genre)
        if os.path.exists(genre_path):
            existing_files = os.listdir(genre_path)
            print(f"\n🎵 {genre.upper()}:")
            for expected_file in files:
                status = "✅" if expected_file in existing_files else "❌"
                print(f"   {status} {expected_file}")

if __name__ == "__main__":
    setup_music_directory()
    check_downloaded_files()