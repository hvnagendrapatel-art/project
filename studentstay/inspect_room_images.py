import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentstay.settings')
django.setup()

from rooms.models import Room
from django.conf import settings

print('DEBUG =', settings.DEBUG)
print('MEDIA_URL =', settings.MEDIA_URL)
print('MEDIA_ROOT =', settings.MEDIA_ROOT)
print('MEDIA_ROOT exists =', Path(settings.MEDIA_ROOT).exists())
print('---')
for room in Room.objects.all():
    print('ROOM', room.pk, room.title)
    images = list(room.images.all())
    if not images:
        print('  no images attached')
    for img in images:
        path = Path(settings.MEDIA_ROOT) / img.image.name
        print('  image.name=', img.image.name)
        print('  image.url=', img.image.url)
        print('  image.path=', img.image.path)
        print('  exists=', path.exists())
