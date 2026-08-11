from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentstay.settings')
django.setup()

from rooms.models import Room, RoomImage
from django.conf import settings

media_root = Path(settings.MEDIA_ROOT)
out_dir = media_root / 'rooms'
out_dir.mkdir(parents=True, exist_ok=True)

room_mapping = {
    1: 2,  # room1 -> Greenview Shared Flat
    2: 3,  # room2 -> Campus Corner PG
    3: 4,  # room3 -> Lakeview Single Room
    4: 1,  # room4 -> Sunrise Student PG
}

font = ImageFont.load_default()
for image_id, room_pk in room_mapping.items():
    try:
        room = Room.objects.get(pk=room_pk)
    except Room.DoesNotExist:
        print(f'Room pk {room_pk} not found, skipping image {image_id}')
        continue

    filename = f'room{image_id}.png'
    output_path = out_dir / filename

    if not output_path.exists():
        img = Image.new('RGB', (1200, 700), color=(235, 245, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(20, 20), (1180, 140)], fill=(28, 62, 111))
        text = f'Room {image_id} - {room.title}'
        draw.text((40, 50), text, fill='white', font=font)
        img.save(output_path)
        print(f'Created placeholder image: {output_path}')
    else:
        print(f'Image already exists: {output_path}')

    RoomImage.objects.get_or_create(room=room, image=f'rooms/{filename}')
    print(f'Attached {filename} to room: {room.title}')
