import os
import sys
from gtts import gTTS
import pysrt
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def srt_to_audio(srt_file, output_file, language='en'):
    """
    Converts an SRT file to a single MP3 audio track synchronized with the subtitle timings.

    :param srt_file: Path to the SRT file.
    :param output_file: Path to save the output MP3 file.
    :param language: Language code for the text-to-speech conversion.
    """
    # Load subtitles from the SRT file
    subtitles = pysrt.open(srt_file)
    
    # Initialize an empty audio track
    full_audio = AudioSegment.silent(duration=0)

    for idx, subtitle in enumerate(subtitles, start=1):
        start_time = subtitle.start.ordinal  # Start time in milliseconds
        end_time = subtitle.end.ordinal  # End time in milliseconds
        text = subtitle.text.replace('\n', ' ')

        try:
            # Convert text to speech
            tts = gTTS(text=text, lang=language)
            temp_audio_file = f"temp_segment_{idx}.mp3"
            tts.save(temp_audio_file)
            
            # Load the audio segment
            segment_audio = AudioSegment.from_file(temp_audio_file)

            # Calculate duration of silence padding
            segment_duration = len(segment_audio)
            silence_padding = max(0, end_time - start_time - segment_duration)
            
            # Add the audio at the correct position
            silent_segment_before = AudioSegment.silent(duration=start_time - len(full_audio))
            full_audio += silent_segment_before
            full_audio += segment_audio

            print(f"Processed subtitle {idx}: '{text}'")

            # Remove temporary audio file
            os.remove(temp_audio_file)

        except Exception as e:
            print(f"Error processing subtitle {idx}: {e}")

    # Save the final synchronized audio track
    full_audio.export(output_file, format="mp3")
    print(f"Saved synchronized audio track to {output_file}")

# Example usage
if __name__ == "__main__":
    # Input SRT file and output MP3 file
    #input_srt = "test.srt"  # Replace with your SRT file
    #output_mp3 = "output_audio_track.mp3"  # Replace with your desired output MP3 file

    # Convert SRT to synchronized MP3
    #srt_to_audio(input_srt, output_mp3, language='en')
    
    
    # Check if the script is provided with an input SRT file
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_srt_file>")
        sys.exit(1)

    # Get the input SRT file from command-line arguments
    input_srt = sys.argv[1]

    # Ensure the input file exists and has the correct extension
    if not os.path.isfile(input_srt) or not input_srt.endswith(".srt"):
        print("Error: Input file must exist and have a .srt extension.")
        sys.exit(1)

    # Derive the output MP3 file name by replacing the .srt extension with .mp3
    output_mp3 = os.path.splitext(input_srt)[0] + ".mp3"

    # Convert SRT to synchronized MP3
    srt_to_audio(input_srt, output_mp3, language='en')

