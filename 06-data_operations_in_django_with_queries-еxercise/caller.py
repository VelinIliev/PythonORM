import os
from datetime import date
from decimal import Decimal

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# Create queries within functions

# 01. Pet

def create_pet(name, species):
    new_pet = Pet.objects.create(
        name=name,
        species=species
    )
    new_pet.save()
    return f"{name} is a very cute {species}!"


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# 02. Artifact

def create_artifact(name, origin, age, description, is_magical):
    new_artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    new_artifact.save()
    return f'The artifact {name} is {age} years old!'


# print(create_artifact(
#     'Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# print(create_artifact(
#     'Crystal Amulet', 'Mystic Forest', 300, 'A magical amulet believed to bring good fortune', True))
# print(create_artifact(
#     'Stone Tablet', 'Ruined Temple', 1000, 'An ancient tablet covered in mysterious inscriptions', False))

def delete_all_artifacts():
    artifacts = Artifact.objects.all()
    for artifact in artifacts:
        artifact.delete()


# delete_all_artifacts()


# 03. Location

def create_location(name, region, population, description, is_capital):
    new_location = Location.objects.create(
        name=name,
        region=region,
        population=population,
        description=description,
        is_capital=is_capital
    )


# create_location(
#     'Sofia', 'Sofia Region', 1329000, 'The capital of Bulgaria and the largest city in the country', False)
# create_location(
#     'Plovdiv', 'Plovdiv Region', 346942, 'The second-largest city in Bulgaria with a rich historical heritage', False)
# create_location(
#     'Varna', 'Varna Region', 330486, 'A city known for its sea breeze and beautiful beaches on the Black Sea', False)

def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    return '\n'.join(f"{location.name} has a population of {location.population}!"
                     for location in locations)


# print(show_all_locations())


def new_capital():
    capital = Location.objects.first()
    capital.is_capital = True
    capital.save()


# new_capital()


def get_capitals():
    capitals = Location.objects.filter(is_capital=True).values('name')
    return capitals


# print(get_capitals())

def delete_first_location():
    Location.objects.first().delete()


# delete_first_location()


# 04. Car

def create_car(model, year, color, price):
    new_car = Car.objects.create(
        model=model,
        year=year,
        color=color,
        price=price
    )
    new_car.save()


# create_car('Mercedes C63 AMG', 2019, 'white', 120000)
# create_car('Audi Q7 S line', 2023, 'black', 183900)
# create_car('Chevrolet Corvette', 2021, 'dark grey', 199999)


def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        discount = 1 - sum(int(x) for x in str(car.year)) / 100
        car.price_with_discount = car.price * Decimal(discount)
        car.save()


# apply_discount()

def get_recent_cars():
    recent_cars = Car.objects.filter(year__gte=2020).values('model', 'price_with_discount')
    return recent_cars


# print(get_recent_cars())

def delete_last_car():
    last_car = Car.objects.last()
    last_car.delete()


# delete_last_car()


# 05. Task Encoder


def create_task(title, description, due_date, is_finished):
    new_task = Task.objects.create(
        title=title,
        description=description,
        due_date=due_date,
        is_finished=is_finished
    )
    new_task.save()


# create_task('Simple Task', 'This is a sample task description', '2023-10-31', False)
# create_task('Simple Task2', 'This is a sample task description', '2023-10-30', False)
# create_task('Simple Task3', 'This is a sample task description', '2023-10-29', False)


def show_unfinished_tasks():
    tasks = Task.objects.filter(is_finished=False)
    return '\n'.join(f'Task - {task.title} needs to be done until {task.due_date}!'
                     for task in tasks)


# print(show_unfinished_tasks())


def complete_odd_tasks():
    tasks = Task.objects.all()
    for task in tasks:
        if task.pk % 2 != 0:
            task.is_finished = True
            task.save()


# complete_odd_tasks()


def encode_and_replace(text, task_title):
    tasks = Task.objects.filter(title=task_title)
    encoded_text = ''
    for char in text:
        encoded_text += chr(ord(char) - 3)

    for task in tasks:
        task.description = encoded_text
        task.save()


# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")


# 06. Hotel Room


def create_room(room_number, room_type, capacity, amenities, price_per_night):
    new_room = HotelRoom.objects.create(
        room_number=room_number,
        room_type=room_type,
        capacity=capacity,
        amenities=amenities,
        price_per_night=price_per_night
    )


# create_room(101, 'Standard', 2, 'Tv', 100)
# create_room(201, 'Deluxe', 3, 'Wi-Fi', 200)
# create_room(501, 'Deluxe', 6, 'Jacuzzi', 400)

def get_deluxe_rooms():
    rooms = HotelRoom.objects.filter(room_type='Deluxe')
    output = []
    for room in rooms:
        if room.pk % 2 == 0:
            output.append(f'Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!')
    return '\n'.join(output)


# print(get_deluxe_rooms())

# def increase_room_capacity():
#     rooms = HotelRoom.objects.all().order_by('id')
#
#     prev_room = 0
#     for room in rooms:
#         if room.is_reserved:
#             if prev_room == 0 or prev_room == 1:
#                 prev_room = room.capacity
#                 room.capacity += room.pk
#             else:
#                 prev_room = room.capacity
#                 room.capacity += prev_room
#             room.save()

def increase_room_capacity():
    rooms = HotelRoom.objects.order_by('id')

    for idx, room in enumerate(rooms):
        if room.is_reserved:
            if idx == 0:
                room.capacity += room.id
            elif room.is_reserved:
                room.capacity += rooms[idx - 1].capacity
            room.save()


# increase_room_capacity()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


# reserve_first_room()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if last_room.is_reserved:
        last_room.delete()


# delete_last_room()


# 07. Character
# def create_characters():
#     character1 = Character.objects.create(
#         name="Gandalf",
#         class_name="Mage",
#         level=10,
#         strength=15,
#         dexterity=20,
#         intelligence=25,
#         hit_points=100,
#         inventory="Staff of Magic, Spellbook",
#     )
#
#     character2 = Character.objects.create(
#         name="Hector",
#         class_name="Warrior",
#         level=12,
#         strength=30,
#         dexterity=15,
#         intelligence=10,
#         hit_points=150,
#         inventory="Sword of Troy, Shield of Protection",
#     )


# create_characters()

def update_characters():
    characters = Character.objects.all()
    for character in characters:
        if character.class_name == 'Mage':
            character.level += 3
            character.intelligence -= 7
        elif character.class_name == 'Warrior':
            character.hit_points /= 2
            character.dexterity += 4
        elif character.class_name in ('Assassin', 'Scout'):
            character.inventory = 'The inventory is empty'
        character.save()


# update_characters()

def fuse_characters(first_character, second_character):
    inventory = ''
    if first_character.class_name in ('Mage', 'Scout'):
        inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    elif first_character.class_name in ('Warrior', 'Assassin'):
        inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=f'{first_character.name} {second_character.name}',
        class_name="Fusion",
        level=int((first_character.level + second_character.level) // 2),
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
    Character.objects.update(dexterity=30)


# grand_dexterity()

def grand_intelligence():
    Character.objects.update(intelligence=40)


# grand_intelligence()

def grand_strength():
    Character.objects.update(strength=50)


# grand_strength()

def delete_characters():
    Character.objects.filter(inventory__contains='The inventory is empty').delete()

# delete_characters()



