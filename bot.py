import time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import csv
import requests
import io

Token = '55231cb8b6506f19461ce9d469269f702a28b2f6552e3e290eea74a5fb30bfc27a71b728cb9fca9a4c871'
Peer_id = 2000000001
vk_map = {
    510092998: 'дмитриенков',
    265757761: 'магомедов',
    268340486: 'цехмистер',
    556622382: 'чиркова',
    146319341: 'лебков',
    165848592: 'лисов',
    165027741: 'зимин',
    211965783: 'плешкова',
    434612352: 'цыкин',
    298723748: 'ким',
     95963726: 'федоренко',
    122290708: 'карасева',
    208036899: 'васенков',
    222042752: 'смирнов',
    145400170: 'шумицкая',
    282120314: 'гончаренко',
    545343775: 'каретин',
    279339376: 'николайчук',
    251258693: 'фролов',
    248058692: 'акопян',
    532586453: 'булатов',
     93744418: 'потапов',
    124448529: 'демидович',
    286950429: 'бердников',
    201678639: 'синюков',
    369807714: 'сухов'
}

def safe_int(string):
    try:
        return int(string)
    except:
        return 0

def dict_to_str(d):
    string = str(d)
    string = string.replace('{', '')
    string = string.replace('}', '')
    string = string.replace("'", '')
    string = string.replace('[', '')
    string = string.replace(']', '')
    string = string.replace(', ', '\n')

    return string

def read_106():
    file_id = '1JzzFqaHb04bA_w_V8RJNT2YdOhCCfQUtggZlZU4mqHc'
    url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(file_id)

    r = requests.get(url)
    sio = io.StringIO( r.content.decode('utf-8'), newline=None)

    reader = csv.reader(sio, dialect=csv.excel)

    _106 = dict()

    for row in reader:

        if (row[0] == '' or row[0] == 'ФИО'):
            continue

        name = row[0].lower().split(' ')[0]
        points = sum(list(map(safe_int, row[1:])))

        _106[name] = points

    return _106

vk_session = vk_api.VkApi(token=Token)
longpoll = VkBotLongPoll(vk_session, 164613215)
vk = vk_session.get_api()

solved_problems = dict()
solved_something = set()
_106 = read_106()

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.message
        
        if (message['from_id'] not in vk_map):
            continue

        text = [i for i in message['text'].split(' ') if len(i) != 0]

        if (text[0] == '\\distribution'):
            answer_text = ''

            for problem in solved_problems:
                solutions = sorted(solved_problems[problem], key=lambda x: _106[x])
                unique_solutions = [i for i in solutions if i not in solved_something]
                try:
                    solver = unique_solutions[0] if len(unique_solutions) != 0 else solutions[0]
                except:
                    solver = 'fucking nobody'

                solved_something.add(solver)
                answer_text += problem + ' : ' + solver + '\n'

            vk.messages.send(peer_id=Peer_id, message=answer_text, random_id=time.time())

            solved_problems = dict()
            solved_something = set()
            _106 = read_106()

        elif (text[0] == '\\solved'):
            problems = text[1:]

            for problem in problems:
                if (problem not in solved_problems):
                    solved_problems[problem] = list()
                solved_problems[problem].append(vk_map[message['from_id']])

        elif (text[0] == '\\not_solved'):
            problems = text[1:]

            for problem in problems:
                if (problem in solved_problems):
                    solved_problems[problem].remove(vk_map[message['from_id']])

                    if (len(solved_problems[problem]) == 0):
                        solved_problems.pop(problem, None)

        elif (text[0] == '\\important'):
            problems = text[1:]

            for problem in problems:
                if (problem not in solved_problems):
                    solved_problems[problem] = list()

        elif (text[0] == '\\debug'):
            vk.messages.send(peer_id=Peer_id, message=dict_to_str(solved_problems), random_id=time.time())

        elif (text[0] == '\\debug_2'):
            vk.messages.send(peer_id=Peer_id, message=dict_to_str(_106), random_id=time.time())

        elif (text[0] == '\\exit'):
            exit(0)
