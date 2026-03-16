try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
except (ImportError, ModuleNotFoundError):
    from moviepy.editor import VideoFileClip
# Укажите путь к видеофайлу

def load_audio(video_path: str):
    """
    функция для импорта звука из видео
    """
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile('.'.join(video_path.split('.')[:-1])+".mp3")
    audio.close()
    video.close()

if __name__ == "__main__":
    load_audio("video_2025-11-17_18-46-49.mp4")