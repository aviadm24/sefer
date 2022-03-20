from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from cloudinary.models import CloudinaryField
from PIL import Image
from collections import Counter


def make_choices(model):
    return ((inst.choice, inst.choice) for inst in model.objects.all())


class Answers(models.Model):
    choice = models.CharField(max_length=250)


class Light(models.Model):
    choice = models.CharField(max_length=250)


class CameraDevice(models.Model):
    choice = models.CharField(max_length=250)


class CameraConfig(models.Model):
    choice = models.CharField(max_length=250)


class Comment(models.Model):
    choice = models.CharField(max_length=250)


class TaharaImage(models.Model):
    # ANSWERS = (
    #     ('good', 'טהור'),
    #     ('bad', 'טמא'),
    #     ('rabbi_q', 'שאלת רב'),
    #     ('cant_see', 'לא רואים ברור'),
    # )
    rabbi_name = models.ForeignKey(User, on_delete=models.CASCADE)
    first_pesak = models.ForeignKey('Answers', related_name="%(app_label)s_%(class)s_first_pesak", blank=True,
                                    null=True, default='', on_delete=models.SET_NULL, help_text="")
    release_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    logo = models.TextField(blank=True)
    image = CloudinaryField('image', default=None)  # models.ImageField(null=True, blank=True, upload_to='logo')
    image2 = CloudinaryField('image2', default=None)
    showed_to = models.CharField(max_length=250, null=True, blank=True,
                                 choices=((user.username, user.username) for user in User.objects.all()))
    second_pesak = models.ForeignKey('Answers', related_name="%(app_label)s_%(class)s_second_pesak", blank=True,
                                    null=True, default='', on_delete=models.SET_NULL, help_text="", verbose_name="פסק")
    user_agent = models.CharField(max_length=1000, null=True, blank=True)
    light = models.ForeignKey('Light', blank=True, null=True, default='',
                                     on_delete=models.SET_NULL,
                                     help_text="", verbose_name="תאורה")
    camera_device = models.ForeignKey('CameraDevice', blank=True, null=True, default='',
                                     on_delete=models.SET_NULL,
                                     help_text="", verbose_name="ממה צולם")
    camera_config = models.ForeignKey('CameraConfig', blank=True, null=True, default='',
                                     on_delete=models.SET_NULL,
                                     help_text="", verbose_name="פרטי הצילום")
    comment = models.ForeignKey('Comment', blank=True, null=True, default='',
                                     on_delete=models.SET_NULL,
                                     help_text="", verbose_name="הערות")
    place_holder = models.CharField(max_length=1000, blank=True, null=True, default='')
    # https: // stackoverflow.com / questions / 42570194 / im - trying - to - display - the - percentage - of - red - color - in -my - image -
    # with-opencv - and -py
    color_percentage = models.JSONField(default=dict())

    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.title, public_id)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def pesak_in_hebrew(pesak):
        for a in TaharaImage.ANSWERS:
            if a[0] == pesak:
                return a[1]
    #  https://bhch.github.io/posts/2018/12/django-how-to-editmanipulate-uploaded-images-on-the-fly-before-saving/

    def save(self, *args, **kwargs):
        image1 = image_to_color_percentage(self.image)
        image2 = image_to_color_percentage(self.image2)
        self.color_percentage = dict(image1=image1, image2=image2)
        super().save(*args, **kwargs)


def image_to_color_percentage(image_file):
    img = Image.open(image_file)
    size = w, h = img.size
    pix_val = list(img.getdata())
    # data = img.load()
    # colors = []
    # for x in range(w):
    #     for y in range(h):
    #         color = data[x, y]
    #         hex_color = '#' + ''.join([hex(c)[2:].rjust(2, '0') for c in color])
    #         colors.append(hex_color)
    return dict(size=size, pix_val=pix_val)

# https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
# @receiver(post_save, sender=TaharaImage)
# def create_color_percentage(sender, instance=None, created=False, **kwargs):
#     if created:
#         print("instance.logo: ", instance.logo)
#         print("instance.logo_image: ", instance.logo_image)
#         if not instance.color_precentage:
#             image1 = image_to_color_percentage(instance.image)
#             image2 = image_to_color_percentage(instance.image2)
#             instance.color_percentage = dict(image1=image1, image2=image2)
#             # instance.logo_image.delete()
#             instance.save()