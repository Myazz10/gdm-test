from django.shortcuts import render
from .models import Photo, Video, Audio, special_characters
from django.core.files import File
from pytube import YouTube
import os
from website.settings import DEFAULT_FILE_STORAGE, BASE_DIR
from moviepy.audio.io.AudioFileClip import AudioFileClip  # pip install moviepy
# from moviepy.editor import VideoFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip


def home(request):
    """if DEFAULT_FILE_STORAGE:
        path = os.listdir(DEFAULT_FILE_STORAGE)
        print(path)

        for item in path:
            print(item)"""

    return render(request, 'home.html')


def photo(request):
    context = {}

    if request.method == 'POST':
        img_file = request.FILES['file-upload']

        photo = Photo()
        photo.image = img_file
        photo.save()

    photos = get_photos()
    context['photos'] = photos

    return render(request, 'photo.html', context)


def get_photos():
    photos = Photo.objects.all()

    return photos


def video(request):
    context = {}

    if request.method == 'POST':
        url = request.POST['search-url']
        get_mp4(url)

    videos = get_videos()
    context['videos'] = videos

    return render(request, 'video.html', context)


def get_videos():
    videos = Video.objects.all()

    return videos


def get_mp4(url):
    youtube_video = YouTube(url)
    # youtube_video.streams.get_highest_resolution().download(output_path=DEFAULT_FILE_STORAGE)

    # vid = File(open(youtube_video.streams.get_highest_resolution().download(filename=youtube_video.title, output_path=DEFAULT_FILE_STORAGE), mode='rb'))

    # To update these lines... START
    # youtube_video.streams.get_highest_resolution().download(output_path=DEFAULT_FILE_STORAGE)
    youtube_video.streams.get_highest_resolution().download()

    title = special_characters(youtube_video.title)
    mp4_file = f'{title}.mp4'
    mp4_created = f'{title.islower}.mp4'

    mp4_file_path = os.path.join(DEFAULT_FILE_STORAGE, mp4_file)
    mp4_created_path = os.path.join(DEFAULT_FILE_STORAGE, mp4_created)

    '''clip = VideoFileClip(mp4_file_path)
    clip.write_videofile(mp4_created_path)
    clip.close()'''

    # To update these lines... END

    video = Video()
    # video.mp4 = vid
    video.mp4 = File(open(mp4_file, mode='rb')) # To update these lines...
    # video.image = img
    video.image = youtube_video.thumbnail_url
    video.name = youtube_video.title
    video.save()

    if mp4_file in os.listdir(BASE_DIR):
        os.remove(mp4_file)




def audio(request):
    context = {}

    if request.method == 'POST':
        url = request.POST['search-url']
        get_mp3(url)

    audios = get_audios()
    context['audios'] = audios

    return render(request, 'audio.html', context)


def get_audios():
    audios = Audio.objects.all()

    return audios


def get_mp3(url):
    youtube_video = YouTube(url)
    
    title = special_characters(youtube_video.title)

    # Converting MP4 to MP3
    mp3_file = f'{title}.mp3'
    mp4_file = f'{title}.mp4'

    youtube_video.streams.filter(only_audio=True).first().download()

    mp3_file_path = os.path.join(BASE_DIR, mp3_file)
    mp4_file_path = os.path.join(BASE_DIR, mp4_file)
    
    clip = AudioFileClip(mp4_file_path)
    clip.write_audiofile(mp3_file_path)
    clip.close()

    # os.remove(mp4_file_path)
    
    audio = Audio()
    audio.mp3 = File(open(mp3_file, mode='rb'))
    # audio.image = img
    audio.image = youtube_video.thumbnail_url
    audio.name = youtube_video.title
    audio.save()

    if mp4_file in os.listdir(BASE_DIR):
        os.remove(mp4_file)
    
    if mp3_file in os.listdir(BASE_DIR):
        os.remove(mp3_file)


