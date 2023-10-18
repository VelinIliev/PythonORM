from decimal import Decimal
import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# Create queries within functions

# 01. Pet

def create_pet(name, species):
    pet = Pet(
        name=name,
        species=species
    )
    pet.save()

    return f'{name} is a very cute {species}!'


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# 	02. Artifact

def create_artifact(name, origin, age, description, is_magical):
    artifact = Artifact(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    artifact.save()

    return f'The artifact {name} is {age} years old!'


def delete_all_artifacts():
    for artifact in Artifact.objects.all():
        artifact.delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500,
#                       'A legendary sword with a rich history', True))
# print(create_artifact('Crystal Amulet', 'Mystic Forest', 300,
#                       'A magical amulet believed to bring good fortune', True))


# 03. Location

def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    return '\n'.join(f'{location.name} has a population of {location.population}!'
                     for location in locations)


def new_capital():
    capital = Location.objects.first()
    capital.is_capital = True
    capital.save()


def get_capitals():
    capitals = Location.objects.filter(is_capital=True).values('name')
    return capitals


def delete_first_location():
    first = Location.objects.first()
    first.delete()


# print(show_all_locations())
# print(new_capital())
# print(get_capitals())
# delete_first_location()

# 04. Car

def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        percentage = 1 - (sum([int(x) for x in str(car.year)]) / 100)
        new_price = float(car.price) * percentage
        car.price_with_discount = Decimal(str(new_price))
        car.save()


def get_recent_cars():
    recent_cars = Car.objects.filter(year__gte=2020).values('model', 'price_with_discount')
    return recent_cars


def delete_last_car():
    last_car = Car.objects.last()
    last_car.delete()


# apply_discount()
# print(get_recent_cars())
# delete_last_car()

# 05. Task Encoder
# TODO: 75/100

def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)
    return '\n'.join(
        f'Task - {task.title} needs to be done until {task.due_date}!'
        for task in unfinished_tasks
    )


# print(show_unfinished_tasks())


def complete_odd_tasks():
    tasks = Task.objects.all()
    for task in tasks:
        if task.id % 2 != 0 and task.is_finished is False:
            task.is_finished = True
            task.save()


# complete_odd_tasks()


def encode_and_replace(text, task_title):
    tasks = Task.objects.filter(title=task_title)
    new_descr = ''.join(chr(ord(x) - 3) for x in text)
    for task in tasks:
        task.description = new_descr
        task.save()


# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task').description)

# 06. Hotel Room
# TODO: 0/100

def get_deluxe_rooms():
    rooms = HotelRoom.objects.filter(room_type='Deluxe')
    output = []
    for room in rooms:
        if room.id % 2:
            output.append(
                f'Deluxe room with number {room.room_number} '
                f'costs {room.price_per_night}$ per night!'
            )
    return '\n'.join(output)


# print(get_deluxe_rooms())


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    prev_room = 0
    for room in rooms:
        if prev_room == 0 or prev_room == 1:
            room.capacity = room.capacity + room.id
        else:
            room.capacity = room.capacity + prev_room
        room.save()


# increase_room_capacity()

def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


# reserve_first_room()

def delete_last_room():
    room = HotelRoom.objects.last()
    room.delete()


# delete_last_room()

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=101).is_reserved)

# 07. Character

def create_characters():
    character1 = Character.objects.create(
        name="Gandalf",
        class_name="Mage",
        level=10,
        strength=15,
        dexterity=20,
        intelligence=25,
        hit_points=100,
        inventory="Staff of Magic, Spellbook",
    )

    character2 = Character.objects.create(
        name="Hector",
        class_name="Warrior",
        level=12,
        strength=30,
        dexterity=15,
        intelligence=10,
        hit_points=150,
        inventory="Sword of Troy, Shield of Protection",
    )


# create_characters()

def update_characters():
    characters = Character.objects.all()
    for character in characters:
        if character.class_name == 'Mage':
            character.level += 3
            character.intelligence -= 7
        elif character.class_name == 'Warrior':
            character.hit_point /= 2
            character.dexterity += 4
        else:
            character.inventory = 'The inventory is empty'
        character.save()


# update_characters()

def fuse_characters(first_character, second_character):
    if first_character.class_name in ['Mage', 'Scout']:
        inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    else:
        inventory = 'Dragon Scale Armor, Excalibur'

    character = Character.objects.create(
        name=f'{first_character.name} {second_character.name}',
        class_name="Fusion",
        level=int((first_character.level + second_character.level) / 2),
        strength=int((first_character.strength + second_character.strength) * 1.2),
        dexterity=int((first_character.dexterity + second_character.dexterity) * 1.4),
        intelligence=int((first_character.intelligence + second_character.intelligence) * 1.5),
        hit_points=int(first_character.hit_points + second_character.hit_points),
        inventory=inventory,
    )
    first_character.delete()
    second_character.delete()


# character1 = Character.objects.create(
#     name="Gandalf",
#     class_name="Mage",
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory="Staff of Magic, Spellbook",
# )
#
# character2 = Character.objects.create(
#     name="Hector",
#     class_name="Warrior",
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory="Sword of Troy, Shield of Protection",
# )

# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()
#
# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)

def grand_dexterity():
    characters = Character.objects.all()
    for character in characters:
        character.dexterity = 30
        character.save()


# grand_dexterity()

def grand_intelligence():
    characters = Character.objects.all()
    for character in characters:
        character.intelligence = 40
        character.save()


# grand_intelligence()

def grand_strength():
    characters = Character.objects.all()
    for character in characters:
        character.strength = 50
        character.save()


# grand_strength()

def delete_characters():
    characters = Character.objects.filter(inventory='The inventory is empty')
    for ch in characters:
        ch.delete()


# delete_characters()
