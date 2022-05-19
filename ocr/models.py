from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, pre_save
from cloudinary.models import CloudinaryField
from PIL import Image
from collections import Counter
# https://stackoverflow.com/questions/34548768/django-no-such-table-exception


def make_choices(model):
    return ((inst.choice, inst.choice) for inst in model.objects.all())


class Answers(models.Model):
    choice = models.CharField(max_length=250)

    def __str__(self):
        return self.choice


class Light(models.Model):
    choice = models.CharField(max_length=250)

    def __str__(self):
        return self.choice


class CameraDevice(models.Model):
    choice = models.CharField(max_length=250)

    def __str__(self):
        return self.choice


class CameraConfig(models.Model):
    choice = models.CharField(max_length=250)

    def __str__(self):
        return self.choice


class Comment(models.Model):
    choice = models.CharField(max_length=250)

    def __str__(self):
        return self.choice


class WaitTime(models.Model):
    days = models.PositiveIntegerField()

    def __str__(self):
        return str(self.days)


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
    image2 = CloudinaryField('image2', default=None, null=True, blank=True)
    showed_to = models.CharField(max_length=250, null=True, blank=True)  # ,choices=((user.username, user.username) for user in User.objects.all()))
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
    color_percentage = models.JSONField(default=dict(), blank=True)  # , blank=True

    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.title, public_id)

    def __str__(self):
        return str(self.id)

    # @staticmethod
    # def pesak_in_hebrew(pesak):
    #     for a in TaharaImage.ANSWERS:
    #         if a[0] == pesak:
    #             return a[1]
    #  https://bhch.github.io/posts/2018/12/django-how-to-editmanipulate-uploaded-images-on-the-fly-before-saving/

    def save(self, *args, **kwargs):
        if self.light is None:  # Set default reference
            self.light = Light.objects.get(id=3)
        if self.user_agent is None:  # Set default reference
            self.user_agent = self.rabbi_name.last_name
        super(TaharaImage, self).save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     image1 = image_to_color_percentage(self.image)
    #     image2 = image_to_color_percentage(self.image2)
    #     self.color_percentage = dict(image1=image1, image2=image2)
    #     print("image size: ", self.color_percentage)
    #     super().save(*args, **kwargs)


def image_to_color_percentage(image_file):
    img = Image.open(image_file)
    size = w, h = img.size
    pixel_num = {
        'redAVG': 0,
        'dark<40': 0,
        '240<red<255,green<40,blue<40': 0,
        '240<red<255,green<100,blue<40': 0,
        '240<red<255,green<150,blue<40': 0,
        '220<red<240,green<40,blue<40': 0,
        '220<red<240,green<100,blue<40': 0,
        '220<red<240,green<150,blue<40': 0,
        '200<red<220,green<40,blue<40': 0,
        '200<red<220,green<100,blue<40': 0,
        '200<red<220,green<150,blue<40': 0,
    }
    # https: // stackoverflow.com / questions / 47520048 / how - to - count - bright - pixels - in -an - image
    # https://stackoverflow.com/questions/50545192/count-different-colour-pixels-python
    for pixel in img.getdata():
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        color = ''
        brightness = ''
        avg = (r + g + b) / 3
        if r != 0:
            if avg / r < 0.9:
                pixel_num['redAVG'] += 1
        if b < 40:
            if g < 40:
                if r < 40:
                    pixel_num['dark<40'] += 1
                elif 240 < r < 255:
                    pixel_num['240<red<255,green<40,blue<40'] += 1
                elif 220 < r < 240:
                    pixel_num['220<red<240,green<40,blue<40'] += 1
                elif 200 < r < 220:
                    pixel_num['200<red<220,green<40,blue<40'] += 1
            elif g < 100:
                if 240 < r < 255:
                    pixel_num['240<red<255,green<100,blue<40'] += 1
                elif 220 < r < 240:
                    pixel_num['220<red<240,green<100,blue<40'] += 1
                elif 200 < r < 220:
                    pixel_num['200<red<220,green<100,blue<40'] += 1
            elif g < 150:
                if 240 < r < 255:
                    pixel_num['240<red<255,green<150,blue<40'] += 1
                elif 220 < r < 240:
                    pixel_num['220<red<240,green<150,blue<40'] += 1
                elif 200 < r < 220:
                    pixel_num['200<red<220,green<150,blue<40'] += 1
        # else if avg < 80 then brightness = 'dark'
        # else if avg > 220 then brightness = 'white'
        # else if avg > 150 then brightness = 'light'
        # if avg / r > 0.9 then hue = 'red'
    pixel_avg = {}
    pixel_total = w*h
    for k, v in pixel_num.items():
        if v > 0:
            pixel_avg[k] = v/pixel_total
        print('k: ', k, ' v: ', v)

    return dict(size=size, pixel_num=pixel_num, pixel_avg=pixel_avg)  # , pix_val=pix_val


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


@receiver(pre_save, sender=TaharaImage)
def my_callback(sender, instance, *args, **kwargs):
    try:
        print(instance.image)
        if type(instance.image) == "<class 'cloudinary.CloudinaryResource'>":
            pass
        else:
            image1 = image_to_color_percentage(instance.image)
            # image2 = image_to_color_percentage(instance.image2)
            instance.color_percentage = dict(image1=image1) #, image2=image2)
        print("image size: ", instance.color_percentage)
    except AttributeError as e:
        print(e)
