from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ocr.models import TaharaImage, WaitTime
from PIL import Image
import requests
from io import BytesIO


def process_img(img):
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
    pixel_total = w * h
    for k, v in pixel_num.items():
        if v > 0:
            pixel_avg[k] = v / pixel_total
        print('k: ', k, ' v: ', v)

    return dict(size=size, pixel_num=pixel_num, pixel_avg=pixel_avg)  # , pix_val=pix_val


# https://devcenter.heroku.com/articles/scheduling-custom-django-management-commands
class Command(BaseCommand):
    help = 'calculate image colors and save to DB'

    # https://stackoverflow.com/questions/41401202/django-command-throws-typeerror-handle-got-an-unexpected-keyword-argument
    def handle(self, *args, **options):
        # for t in TaharaImage.objects.all():
        #     print(t.id)
        #     print(t.color_percentage)
        qs = TaharaImage.objects.filter(color_percentage__exact={})

        print('qs.count() : ', qs.count())
        if qs.count() > 0:
            url = qs[0].image.url
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            # image1 = image_to_color_percentage(img)
            color_percentage = process_img(img)
            image_instance = qs[0]
            image_instance.color_percentage = dict(image1=color_percentage)
            image_instance.save()  #update_fields=color_percentage
            print('image_instance.color_percentage : ', image_instance.color_percentage)

            self.stdout.write(self.style.SUCCESS('Successfully calculated color percent'))
        return