import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
import argparse


def extract_audio(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)

def split_audio(file_path, chunk_length_ms):
    audio = AudioSegment.from_file(file_path)
    length_ms = len(audio)
    chunks = []
    for start_ms in range(0, length_ms, chunk_length_ms):
        end_ms = start_ms + chunk_length_ms
        if end_ms > length_ms:
            end_ms = length_ms
        chunk = audio[start_ms:end_ms]
        chunks.append(chunk)
    return chunks

def recognize_speech_from_audio(file_path, language="en-US"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language=language)
        except sr.UnknownValueError:
            return "[Không thể nhận dạng]"
        except sr.RequestError as e:
            return f"[Lỗi yêu cầu: {e}]"


parser = argparse.ArgumentParser(description='Example script with a video argument')
parser.add_argument('--video', help='video to process')
args = parser.parse_args()


video_file = args.video
audio_file = "Tamarisk.wav"
chunk_length_ms = 10000  # Thời gian của mỗi phần (ví dụ: 30 giây)

# Trích xuất âm thanh và chia nhỏ
extract_audio(video_file, audio_file)
chunks = split_audio(audio_file, chunk_length_ms)

# Nhận dạng giọng nói cho từng phần và lưu vào file văn bản
subtitle_text = ""
for i, chunk in enumerate(chunks):
    chunk_name = f"chunk_{i}.wav"
    chunk.export(chunk_name, format="wav")
    text = recognize_speech_from_audio(chunk_name)
    subtitle_text += f"Phần {i+1}:\n{text}\n\n"
    os.remove(chunk_name)  # Xóa file chunk sau khi đã xử lý

with open("Tamarisk.txt", "w") as file:
    file.write(subtitle_text)
