from pathlib import Path

media_rooms = Path('media/rooms')
renames = [
    ('room1.jpeg', 'room1.png'),
    ('room2.jpeg', 'room2.png'),
    ('room3.jpg', 'room3.png'),
    ('room4.jpg', 'room4.png'),
]
for old, new in renames:
    old_path = media_rooms / old
    new_path = media_rooms / new
    if old_path.exists():
        if new_path.exists():
            print(f'Skipping {old_path}: {new_path} already exists')
        else:
            old_path.rename(new_path)
            print(f'Renamed {old_path} -> {new_path}')
    else:
        print(f'File not found: {old_path}')
