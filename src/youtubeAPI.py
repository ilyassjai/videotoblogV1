import re
import csv
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

def extract_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except NoTranscriptFound:
        print("No transcript found for this video.")
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def merge_phrases(transcript, threshold=5.0):
    merged_transcript = []
    current_phrase = ''
    current_start = None
    current_duration = 0.0

    for entry in transcript:
        if current_start is None:
            current_start = entry['start']
        current_phrase += ' ' + entry['text']
        current_duration += entry['duration']

        if current_duration >= threshold:
            merged_transcript.append({
                'start': current_start,
                'end': current_start + current_duration,
                'text': current_phrase.strip()
            })
            current_phrase = ''
            current_start = None
            current_duration = 0.0

    # Add the last accumulated phrase if it exists
    if current_phrase:
        merged_transcript.append({
            'start': current_start,
            'end': current_start + current_duration,
            'text': current_phrase.strip()
        })

    return merged_transcript

def save_transcript_to_csv(transcript, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['start', 'end', 'text'])
        for entry in transcript:
            writer.writerow([entry['start'], entry['end'], entry['text']])

def transcription(url, duration_threshold=20.0):
    output_file = 'transcript.csv'

    try:
        video_id = extract_video_id(url)
        transcript = fetch_transcript(video_id)
        if transcript:
            merged_transcript = merge_phrases(transcript, duration_threshold)
            save_transcript_to_csv(merged_transcript, output_file)
            print(f"Transcript saved to {output_file}")
        else:
            print("Transcript could not be fetched.")
    except ValueError as e:
        print(e)

