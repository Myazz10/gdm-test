from django.db import models
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video  # To use this: pip install pyhton-magic and pip install python-magic-bin
import os
from website.settings import DEFAULT_FILE_STORAGE
from django.utils import timezone



class Photo(models.Model):
    image = models.ImageField(upload_to="images/")


class Video(models.Model):
    name = models.CharField(max_length=100)
    mp4 = models.FileField(upload_to='videos/', blank=True, storage=VideoMediaCloudinaryStorage(), validators=[validate_video])
    image = models.ImageField(upload_to='images/', blank=True)


class Audio(models.Model):
    name = models.CharField(max_length=100)
    mp3 = models.FileField(upload_to='audios/', blank=True, storage=VideoMediaCloudinaryStorage(), validators=[validate_video])
    image = models.ImageField(upload_to='images/', blank=True)


    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.remove_audio()  # Calling a custom delete method before remove this object from the database.
        self.mp3.delete()
        return super(Audio, self).delete(*args, **kwargs)


    def remove_audio(self):
        title = self.name

        path = os.listdir(DEFAULT_FILE_STORAGE)

        # Updating the title to compare it with the mp4 file that exist for it in this folder...
        title = special_characters(title)

        # Loop through the path to save the files to the database.
        for mp3_file in path:
            if mp3_file.endswith('mp3') and mp3_file.__contains__(title):
                os.remove(mp3_file)
                break

    def __str__(self):
        return f'{self.name}'


class ErrorCharacter(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'


# To clear the potential problems with the titles that contains special characters that will throw an error
def special_characters(title):
    error_characters = ErrorCharacter.objects.all()

    if not error_characters.exists():
        error_characters = ['"', '.', '$', ',', '#', "'", '\\', '/']

        for character in title:
            if character in error_characters:
                title = title.replace(character, "")

        # Converting the list to a string to save it to the database
        error_characters = ", ".join(error_characters)

        errors = ErrorCharacter()
        errors.name = error_characters
        errors.save()
    else:
        # Converting the string back to a list to loop over it...
        errors_list = list(error_characters.first().name.split(", "))
        for character in title:
            if character in errors_list:
                title = title.replace(character, "")

    return title