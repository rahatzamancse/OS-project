import json
import ast
from sre_constants import CATEGORY_NOT_WORD

def load_dataset():
    f = open('top10users.txt', 'r')
    users = {}
    lineNum = 0
    for line in f:
        lineNum += 1
        print(lineNum)
        items = line.split('~')
        users[items[0]] = []
        events = ast.literal_eval(items[1])
        for e in events:
            e = str(e).replace('\'', '\"')
            users[items[0]].append(json.loads(e))
        break

    return users

def get_app_list(users):
    app_list = set()
    for u in users:
        for e in users[u]:
            for app in e['apps']:
                if app not in app_list:
                    app_list.add(app)

    return app_list

def get_categories():
    f = open('categories.csv')
    app_to_category = {}
    for line in f:
        items = line.split(';')
        if len(items) < 2:
            items = line.split(':')
        app_to_category[items[0]] = items[1].strip()

    category_ram = {
        'FINANCE' : 400,
        'ART_AND_DESIGN' : 700,
        'COMICS' : 150,
        'GAME_MUSIC' : 650,
        'BUSINESS' : 200,
        'TRAVEL_AND_LOCAL' : 250,
        'NEWS_AND_MAGAZINES' : 150,
        'GAME_ARCADE' : 700,
        'MEDIA_AND_VIDEO' : 200,
        'DATING' : 200,
        'FOOD_AND_DRINK' : 150,
        'AUTO_AND_VEHICLES' : 200,
        'PARENTING' : 150,
        'PERSONALIZATION' : 150,
        'ENTERTAINMENT' : 300,
        'GAME_WORD' : 600,
        'BOOKS_AND_REFERENCE' : 150,
        'VIDEO_PLAYERS' : 200,
        'GAME_SIMULATION' : 700,
        'GAME_CARD' : 450,
        'PHOTOGRAPHY' : 600,
        'LIBRARIES_AND_DEMO' : 200,
        'MAPS_AND_NAVIGATION' : 350,
        'WEATHER' : 150,
        'COMMUNICATION' : 150,
        'SHOPPING' : 150,
        'GAME_CASUAL' : 350,
        'EVENTS' : 150,
        'GAME_ADVENTURE' : 700,
        'GAME_TRIVIA' : 400,
        'GAME_STRATEGY' : 450,
        'SPORTS' : 250,
        'GAME_RACING' : 850,
        'GAME_PUZZLE' : 400,
        'TOOLS' : 100,
        'GAME_ROLE_PLAYING' : 750,
        'HEALTH_AND_FITNESS' : 300,
        'GAME_ACTION' : 1000,
        'MUSIC_AND_AUDIO' : 150,
        'SOCIAL' : 250,
        'GAME_EDUCATIONAL' : 400,
        'BEAUTY' : 200,
        'PRODUCTIVITY' : 250,
        'TRANSPORTATION': 200,
        'GAME_SPORTS' : 550,
        'EDUCATION' : 200,
        'MEDICAL' : 250,
        'GAME_BOARD' : 500,
        'LIFESTYLE' : 200,
        'GAME_CASINO' : 350,
        'HOUSE_AND_HOME' : 200,
        'OTHER' : 100
    }


    return app_to_category, category_ram