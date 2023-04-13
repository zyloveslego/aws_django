from django.db import models


# Create your models here.
class GptHistory(models.Model):
    LANGUAGE_CHOICES = [
        ("English", "English"),
        ("Chinese", "Chinese"),
    ]

    RATING_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    APPLICATION_CHOICE = [
        (1, 1),
        (2, 2),
        (3, 3)
    ]

    # help_text
    pub_date = models.DateTimeField("pub date")
    textarea_input = models.CharField(max_length=200, null=True)
    prompt_used = models.CharField(max_length=200)
    language_used = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default="English")
    pic_name = models.CharField(max_length=50, null=True)
    generated_gpt = models.CharField(max_length=400)
    star_rating = models.IntegerField(choices=RATING_CHOICES, null=True)
    keywords = models.CharField(max_length=100)
    application = models.CharField(max_length=20, choices=APPLICATION_CHOICE, default=1)
    # user
    # user_info = models.ForeignKey()


# save pics
class UploadPic(models.Model):
    title = models.CharField(max_length=200, default='user1.jpg')
    photo = models.ImageField(upload_to='', default='user1.jpg')

