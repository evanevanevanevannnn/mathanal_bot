import time, vk_api, csv, requests, io, sys
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

#---------------константы------------------

Token = '55231cb8b6506f19461ce9d469269f702a28b2f6552e3e290eea74a5fb30bfc27a71b728cb9fca9a4c871'
Peer_id = 2000000002

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

admins = [
    'сухов'
]

vk_session = vk_api.VkApi(token=Token)
longpoll = VkBotLongPoll(vk_session, 164613215)
vk = vk_session.get_api()

solved_problems = dict()
solved_something = set()
_106 = dict()

#-------------вспомогательные функции------------------

def find_id(name):
    for _id in vk_map:
        if (vk_map[_id] == name):
            return _id
    return 0

def safe_int(string):
    try:
        return int(string)
    except:
        return 0

def otformatirovat(l):
    string = str(l)
    string = string.replace('[', '')
    string = string.replace(']', '')
    string = string.replace("'", "")

    return string

def otformatirovat2(d):
    string = str(d)
    string = string.replace('{', '')
    string = string.replace('}', '')
    string = string.replace("'", "")
    string = string.replace(', ', '\n')

    return string

def seems_like_problem(problem):
    t = problem.split('.')

    if (len(t) != 2):
        return False

    N = t[0]
    try:
        N = int(N)
    except:
        return False

    n = t[1]
    if (n.find('(') == -1):
        try:
            n = int(n)
            return True
        except:
            return False
    else:
        n = n.replace('(', ' ')
        n = n.replace(')', '')

        t2 = n.split(' ')

        if (len(t2) != 2):
            return False

        n = t2[0]
        l = t2[1]

        try:
            n = int(n)
        except:
            return False

        if not (l >= 'а' and l <= 'я'):
            return False

        return True

def sorted_by_key(d):
    res = dict()

    for item in sorted(d.items(), key=lambda x: -x[1]):
        res[item[0]] = item[1]

    return res

def read_106():
    file_id = '1JzzFqaHb04bA_w_V8RJNT2YdOhCCfQUtggZlZU4mqHc'
    url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(file_id)

    r = requests.get(url)
    sio = io.StringIO( r.content.decode('utf-8'), newline=None)

    reader = csv.reader(sio, dialect=csv.excel)

    unsorted_106 = dict()
    for row in reader:

        if (row[0] == '' or row[0] == 'ФИО'):
            continue

        name = row[0].lower().split(' ')[0]
        points = sum(list(map(safe_int, row[1:])))

        unsorted_106[name] = points

    return sorted_by_key(unsorted_106)

def read_solved_problems(): #yet unused
    global solved_problems

    f = open('solved_problems.txt', 'r')

    for line in f:
        solved_problems[line.split(':')[0]] = line.split(':')[1][1:].split(',')

def write_solved_problems(): #yet unused
    f = open('solved_problems.txt', 'w')

    for problem in solved_problems:
        line = problem + ':'
        for solution in solved_problems[problem]:
            line += ',' + solution

    line += '\n'
    f.write(line)

#---------------команды бота-------------------

def restart(message):
    global solved_problems, solved_something, _106

    if (vk_map[message['from_id']] in admins):
        solved_problems = dict()
        solved_something = set()
        _106 = read_106()

def solved(message, forced=False):
    problems = [i for i in message['text'].split(' ') if len(i) != 0][1:]
    solver = vk_map[message['from_id']]
    not_problems = list()

    for problem in problems:
        if not (seems_like_problem(problem) or forced):
            not_problems.append(problem)
            continue

        if (problem not in solved_problems):
            solved_problems[problem] = list()
        if (solver not in solved_problems[problem]):
            solved_problems[problem].append(solver)

    if (len(not_problems) != 0):
        message_text = 'данные номера: ' + otformatirovat(not_problems) + ' выглядят так, будто вы описались. если это не так используйте \\force_solved.'
        vk.messages.send(peer_id=Peer_id, message=message_text, random_id=time.time())
        time.sleep(1)

def not_solved(message):
    problems = [i for i in message['text'].split(' ') if len(i) != 0][1:]
    solver = vk_map[message['from_id']]
    not_solved = list()

    for problem in problems:
        if (problem in solved_problems):
            solved_problems[problem].remove(solver)

            if (len(solved_problems[problem]) == 0):
                solved_problems.pop(problem)
        else:
            not_solved.append(problem)

    if (len(not_solved) != 0):
        message_text = 'не уверен, что вы решили следующие задачки: ' + otformatirovat(not_solved) + '. проверьте не описались ли вы))'
        vk.messages.send(peer_id=Peer_id, message=message_text, random_id=time.time())
        time.sleep(1)

def increase_priority(message):
    global _106

    solvers = [i for i in message['text'].split(' ') if len(i) != 0][1:]
    not_in_106 = list()

    for solver in solvers:
        if (solver.lower() in _106):
            _106[solver.lower()] = -1
        else:
            not_in_106.append(solver.lower())

    _106 = sorted_by_key(_106)

    if (len(not_in_106) != 0):
        message_text = 'не нашел ' + otformatirovat(not_in_106) + ' в 106 группе)) Попробуйте написать фамилии по русски, желательно как в журнале Орлова.'
        vk.messages.send(peer_id=Peer_id, message=message_text, random_id=time.time())
        time.sleep(1)

def distribution():
    message_text = 'распределение:\n'

    for problem in solved_problems:
        solutions = sorted(solved_problems[problem], key=lambda x: _106[x])
        unique_solutions = [i for i in solutions if i not in solved_something]

        solver = unique_solutions[0] if len(unique_solutions) != 0 else solutions[0]

        solved_something.add(solver)
        message_text += problem + ' : @id' + str(find_id(solver)) + '(' + solver + ')' + '\n'

    debug()
    if (len(message_text) != 0):
        vk.messages.send(peer_id=Peer_id, message=message_text, random_id=time.time())
        time.sleep(1)

def debug():
    message_text = ''

    for problem in solved_problems:
        solutions = sorted(solved_problems[problem], key=lambda x: _106[x])
        message_text += problem + ': ' + otformatirovat(solutions) + '\n\n'

    if (len(message_text) != 0):
        vk.messages.send(peer_id=Peer_id, message=message_text, random_id=time.time())
    else:
        vk.messages.send(peer_id=Peer_id, message='никто ничего не решил))', random_id=time.time())
    time.sleep(1)

def debug_2():
    vk.messages.send(peer_id=Peer_id, message=otformatirovat2(_106), random_id=time.time())
    time.sleep(1)

def help(message):
    documentation =  '''надо бы написать документацию'''

    vk.messages.send(peer_id=Peer_id, message=documentation, random_id=time.time())
    time.sleep(1)

def stop_bot(message):
    if (vk_map[message['from_id']] in admins):
        exit(0)

#--------------сам бот----------------

_106 = read_106()

if (len(sys.argv) > 1):
    read_solved_problems()

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.message
        text = [i for i in message['text'].split(' ') if len(i) != 0]

        if (len(text) == 0):
            continue

        command = text[0]
        print(command)

        if (command == '\\restart'):
            restart(message)

        elif (command == '\\solved'):
            solved(message)

        elif (command == '\\force_solved'):
            solved(message, True)

        elif (command == '\\not_solved'):
            not_solved(message)

        elif (command == '\\high_priority'):
            increase_priority(message)

        elif (command == '\\distribution'):
            distribution()

        elif (command == '\\debug'):
            debug()

        elif (command == '\\debug_2'):
            debug_2()

        elif (command == '\\help'):
            help(message)

        elif (command == '\\exit'):
            stop_bot(message)