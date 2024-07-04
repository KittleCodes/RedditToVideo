'''
This Python script generates a video from top comments on a Reddit thread
and overlays subtitles using MoviePy library.
'''
import sys
import re
import random
import os
import requests
import nltk
from moviepy.editor import concatenate_audioclips, AudioFileClip, ImageClip, TextClip, VideoFileClip, CompositeVideoClip
from header_image import header_image
from tiktokvoice import tts

nltk.download('punkt')

BACKGROUND_VIDEO = "background/background_video.mp4"
# Be sure not to remove the ".json" part
REDDIT_URL = "https://www.reddit.com/r/AskReddit/comments/1dujmae/whats_an_open_secret_that_doesnt_have_a/" + ".json"
# Maximum duration of the video in seconds, may not be accurate as the TTS duration is estimated
TIME_LIMIT = 80
# Set to username you want in the header image
USERNAME = "Reddit User"

mp3_files = []

request = requests.get(REDDIT_URL, timeout=30)
if isinstance(request.json(), dict):
    print("Error: You have sent too many requests to Reddit. Wait a bit and try again.")
    sys.exit(0)
comments = request.json()[1]["data"]["children"]
data = request.json()[0]["data"]["children"][0]["data"]

header_image(data["title"], data["ups"], data["num_comments"], USERNAME)

with open('bad_words.txt', 'r', encoding="utf-8") as file:
    bad_words = [line.strip().lower() for line in file]

def contains_bad_word(text):
    '''
    Checks if given text contains any bad words.
    '''
    text = text.lower()
    for word in bad_words:
        if word in text:
            return True
    return False

filtered_comments = [comment for comment in comments if 'score' in comment['data']
                     and 'body' in comment['data']
                     and comment['data']['body'] != '[removed]'
                     and comment['data']['body'] != '[deleted]'
                     and comment['data']['body'] != ''
                     and not re.search(r'http[s]?://', comment['data']['body'])
                     and not contains_bad_word(comment['data']['body'])]
sorted_comments = sorted(filtered_comments, key=lambda x: x["data"]["score"], reverse=True)

def segment_comment_into_sentences(comment):
    '''
    Segments a comment into sentences using NLTK.
    '''
    text = comment["data"]["body"]
    return nltk.sent_tokenize(text)

def estimate_tts_duration(sentence):
    '''
    Estimates the duration of a sentence when spoken using TTS.
    '''
    words_per_minute = 200
    words = len(sentence.split())
    duration = words / (words_per_minute / 60)
    return duration

def generate_tts_for_sentence(sentence, output_file):
    '''
    Generates TTS for a sentence and saves it to an MP3 file.
    '''
    tts(sentence, "en_us_006", output_file, play_sound=False)

def generate_video_with_subtitles_and_audio(background_video, comments):
    '''
    Generates a video with subtitles and audio from a list of comments.
    '''
    video = VideoFileClip(background_video)

    subtitle_clips = []
    comment_audio_clips = []

    start_time = 0

    for idx, comment in enumerate(comments):
        sentences = segment_comment_into_sentences(comment)

        for sentence_idx, sentence in enumerate(sentences):
            audio_file = f"audio/comment_{idx + 1}_sentence_{sentence_idx + 1}.mp3"
            generate_tts_for_sentence(sentence, audio_file)
            comment_audio_clip = AudioFileClip(audio_file)
            comment_audio_clips.append(comment_audio_clip)

            duration = comment_audio_clip.duration

            if idx == 0:
                txt_clip = ImageClip("header.png")
                txt_clip = txt_clip.set_position(('center', 'center')).set_duration(duration)
            else:
                txt_clip = TextClip(sentence,
                                    font='Arial-Rounded-MT-Bold',
                                    fontsize=60,
                                    color='white',
                                    stroke_color='black',
                                    stroke_width=4,
                                    method='caption',
                                    size=(video.size[0]-200,video.size[1]-200))
                txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(duration)

            txt_clip = txt_clip.set_start(start_time)

            subtitle_clips.append(txt_clip)

            start_time += duration

    final_audio_clip = concatenate_audioclips(comment_audio_clips)

    random_start = random.randint(0, int(video.duration) - int(final_audio_clip.duration))
    trimmed_video = video.subclip(random_start, random_start + int(final_audio_clip.duration))

    final_video = CompositeVideoClip([trimmed_video] + subtitle_clips)
    final_video = final_video.set_audio(final_audio_clip)

    final_video.write_videofile("output.mp4", codec='libx264', fps=24)

    for audio_file in os.listdir("audio"):
        if audio_file.endswith(".mp3"):
            os.remove(os.path.join("audio", audio_file))

if __name__ == "__main__":
    comments_to_process = []
    CUMULATIVE_DURATION = 0

    for comment in sorted_comments:
        sentences = segment_comment_into_sentences(comment)
        comment_duration = sum(estimate_tts_duration(sentence) for sentence in sentences)
        if CUMULATIVE_DURATION + comment_duration > TIME_LIMIT:
            break
        CUMULATIVE_DURATION += comment_duration
        comments_to_process.append(comment)

    comments_to_process.insert(0, {"data": {"body": data["title"]}})
    generate_video_with_subtitles_and_audio(BACKGROUND_VIDEO, comments_to_process)
