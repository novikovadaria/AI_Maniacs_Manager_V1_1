import json
import os
import pandas as pd
from datetime import datetime
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip, TextClip

class VideoCreator:
    def __init__(self, pictures_path, captions_list, background_music_path, save_path):
        self.pictures_path = pictures_path
        self.captions_list = captions_list
        self.background_music_path = background_music_path
        self.save_path = save_path
        self.clips = []

    def create_video_clip(self, image_path, title, duration=5):
        clip = ImageClip(image_path).set_duration(duration)
        txt_clip = self.create_text_clip(title, clip.size)
        return CompositeVideoClip([clip, txt_clip])

    def create_text_clip(self, text, clip_size, fontsize=48, color='white', bg_color='black'):
        txt_clip = TextClip(text, fontsize=fontsize, color=color, bg_color=bg_color)
        txt_pos = (15, clip_size[1] - txt_clip.size[1] - 15)
        return txt_clip.set_position(txt_pos).set_duration(5)

    def get_sorted_folders(self, path):
        folder_paths = [os.path.join(path, folder_name) for folder_name in os.listdir(path) if os.path.isdir(os.path.join(path, folder_name))]
        return sorted(folder_paths, key=lambda x: os.path.getmtime(x), reverse=False)

    def get_image_files(self, folder_path):
        return [f for f in sorted(os.listdir(folder_path)) if f.endswith(('.png', '.jpg', '.jpeg'))]

    def add_audio_track(self, clip, audio_path):
        audio = AudioFileClip(audio_path).subclip(0, clip.duration)
        return clip.set_audio(audio)

    def save_video(self, clip, save_path):
        file_name = os.path.join(save_path, f"final_video.mp4")
        clip.write_videofile(file_name, fps=24)

    def create_video(self):
        caption_index = 0
        for folder_path in self.get_sorted_folders(self.pictures_path):
            for image_file in self.get_image_files(folder_path):
                video = self.create_video_clip(os.path.join(folder_path, image_file), self.captions_list[caption_index])
                self.clips.append(video)
                caption_index += 1

        final_clip = concatenate_videoclips(self.clips, method="compose")
        final_clip = self.add_audio_track(final_clip, self.background_music_path)
        self.save_video(final_clip, self.save_path)

