from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from cloudinary.models import CloudinaryField


class TaharaImage(models.Model):
    ANSWERS = (
        ('good', 'טהור'),
        ('bad', 'טמא'),
        ('rabbi_q', 'שאלת רב'),
        ('cant_see', 'לא רואים ברור'),
    )
    rabbi_name = models.ForeignKey(User, on_delete=models.CASCADE)
    first_pesak = models.CharField(max_length=250, choices=ANSWERS)
    release_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    logo = models.TextField(blank=True)
    # image = CloudinaryField('image')
    image = CloudinaryField('image', default=None)  # models.ImageField(null=True, blank=True, upload_to='logo')
    image2 = CloudinaryField('image2', default=None)
    showed_to = models.CharField(max_length=250, null=True, blank=True, choices=((user.first_name, user.first_name) for user in User.objects.all()))
    second_pesak = models.CharField(max_length=250, null=True, blank=True, choices=ANSWERS, default='', verbose_name="פסק")

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


# def image_to_b64(image_file):
#     import base64
#     with open(image_file.path, "rb") as f:
#         encoded_string = base64.b64encode(f.read())
#         return encoded_string
#
# # https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
# @receiver(post_save, sender=TaharaImage)
# def create_base64_str(sender, instance=None, created=False, **kwargs):
#     if created:
#         print("instance.logo: ", instance.logo)
#         print("instance.logo_image: ", instance.logo_image)
#         if not instance.logo:
#             instance.logo = image_to_b64(instance.logo_image)
#             # instance.logo_image.delete()
#             instance.save()
