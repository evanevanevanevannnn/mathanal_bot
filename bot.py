import time, vk_api, csv, requests, io, sys, random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from subprocess import check_output

#---------------константы------------------

Token = '55231cb8b6506f19461ce9d469269f702a28b2f6552e3e290eea74a5fb30bfc27a71b728cb9fca9a4c871'
FORCED = False
Peer_id = 2000000001
Peer_id2 = 2000000002
inf = 1000

ignored = set()

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
    return str(l).replace("'", "")

def otformatirovat2(d):
    string = str(d)
    string = string.replace('{', '')
    string = string.replace('}', '')
    string = string.replace("'", "")
    string = string.replace(', ', '\n')
    string = string.replace('1000', 'inf')

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

        if (len(l) != 1):
            return False

        if not (l >= 'а' and l <= 'я'):
            return False

        return True

def problem_comparator(problem):
    problem = problem[0]

    if (not seems_like_problem(problem)):
        return -inf

    ln, rn = problem.split('.')
    lt = 0

    if (rn.find('(') != -1):
        rn, lt = rn.replace('(', ' ').replace(')', '').split(' ')

    ln = int(ln)
    rn = int(rn)
    lt = ord(lt) - ord('а')   #русская а
    return (inf**2) * ln + inf * rn + lt

def sorted_by_key(d, Key, Mode):
    res = dict()

    for item in sorted(d.items(), key=Key):
        res[item[0]] = item[1]

        if (Mode == 1):
            res[item[0]] = item[1]
        elif (Mode == 2):
            res[item[0]] = sorted(item[1], key=lambda x: _106[x])

    return res

def read_table(file_id, g_id):
    url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv&gid={1}".format(file_id, g_id)

    r = requests.get(url)
    sio = io.StringIO( r.content.decode('utf-8'), newline=None)

    return csv.reader(sio, dialect=csv.excel)

def read_106():
    global _106

    file_id = '1JzzFqaHb04bA_w_V8RJNT2YdOhCCfQUtggZlZU4mqHc'
    g_id1, g_id2 = 0, 1979959699
    table = read_table(file_id, g_id1)

    unsorted_106 = dict()
    for row in table:

        if (row[0] == '' or row[0] == 'ФИО'):
            continue

        name = row[0].lower().split(' ')[0]
        points = sum(list(map(safe_int, row[1:])))

        unsorted_106[name] = points

    table = read_table(file_id, g_id2)
    for row in table:

        if (row[0] == '' or row[0] == 'ФИО'):
            continue

        name = row[0].lower().split(' ')[0]
        points = safe_int(row[7]) + safe_int(row[13]) + safe_int(row[27])

        unsorted_106[name] += points

    _106 = sorted_by_key(unsorted_106, lambda x:-x[1], 1)

def read_solved_problems():
    global solved_problems
    global _106

    f = open('solved_problems.txt', 'r')

    for line in f:
        lst = line.replace('\n', '').split(':')

        if (lst[0] == 'приоритет'):
            for man in lst[1][1:].split(','):
                if man in _106:
                    _106[man] = -inf
        else:
            solved_problems[lst[0]] = lst[1][1:].split(',')

    solved_problems = sorted_by_key(solved_problems, problem_comparator, 2)
    _106 = sorted_by_key(_106, lambda x: -x[1], 1)

def write_solved_problems():
    f = open('solved_problems.txt', 'w')
    solved_problems_in_str_form = ''

    for problem in solved_problems:
        line = problem + ':'
        for solution in solved_problems[problem]:
            line += ',' + solution

        solved_problems_in_str_form += line + '\n'

    high_pr = ''
    for man in _106:
        if (_106[man] == -inf):
            high_pr += ',' + man

    solved_problems_in_str_form += 'приоритет:' + high_pr

    f.write(solved_problems_in_str_form)

def get_distribution():
    argv = ['', '']

    argv[0] = './distribution/distribution'

    first = True
    for man in _106:
        if first:
            first = False
        else:
            argv[1] += ';'

        argv[1] += man + ':' + str(_106[man])

    argv[1] += '#'

    first = True
    for problem in solved_problems:
        if first:
            first = False
        else:
            argv[1] += ';'

        argv[1] += problem + ':'
        first = True
        for man in solved_problems[problem]:
            if first:
                first = False
            else:
                argv[1] += ','
            argv[1] += man

    try:
        distribution_str = check_output(argv).decode('utf-8')
    except Exception as e:
        print(e)
        return -1

    distribution = dict()
    for pair in distribution_str.split(';'):
        distribution[pair.split(':')[0]] = pair.split(':')[1]

    return distribution

def send_message(Text, Peer_id):
    try:
        vk.messages.send(message=Text, peer_id=Peer_id, random_id=time.time(), timeout=10)
    except Exception as e:
        print(e)
        send_message(Text, Peer_id)
    time.sleep(1)

#---------------команды бота-------------------

def restart(message):
    if (vk_map[message['from_id']] not in admins):
        return

    global solved_problems, _106
    args = [i for i in message['text'].split(' ') if len(i) != 0][1:]

    if (len(args) == 0):
        solved_problems = dict()
        read_106()
    else:
        for arg in args:
            if (arg == 'points'):
                read_106()
                solved_problems = sorted_by_key(solved_problems, problem_comparator, 2)
            elif (arg == 'solved_problems'):
                solved_problems = dict()

    write_solved_problems()

def solved(message, forced=False):
    global solved_problems

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
        message_text = 'данные номера: ' + otformatirovat(not_problems) + ' выглядят так, будто вы описались. Убедитесь, что вы используете русские буквы. Если вы не описались используйте \\force_solved.'
        send_message(message_text, message['peer_id'])

    solved_problems = sorted_by_key(solved_problems, problem_comparator, 2)
    write_solved_problems()

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

    message_text = ''
    if (len(not_solved) != 0):
        message_text = 'не уверен, что вы решили следующие задачки: ' + otformatirovat(not_solved) + '. проверьте не описались ли вы))'
        send_message(message_text, message['peer_id'])

    write_solved_problems()

def increase_priority(message):
    global _106

    solvers = [i for i in message['text'].split(' ') if len(i) != 0][1:]
    not_in_106 = list()

    for solver in solvers:
        if (solver.lower() in _106):
            _106[solver.lower()] = -inf
        else:
            not_in_106.append(solver.lower())

    _106 = sorted_by_key(_106, lambda x: -x[1], 1)

    if (len(not_in_106) != 0):
        message_text = 'не нашел ' + otformatirovat(not_in_106) + ' в 106 группе)) Попробуйте написать фамилии по русски, желательно как в журнале Орлова.'
        send_message(message_text, message['peer_id'])

    write_solved_problems()
        
def distribution(message):
    if (len(solved_problems) == 0):
        send_message('никто ничего не решил)))', message['peer_id'])
        return

    distribution = get_distribution()
    message_text = ''

    if (distribution == -1):
        send_message('что-то сломалось, и вы вряд ли сможете что-то с этим сделать))', message['peer_id'])
        return

    for problem in solved_problems:
        if problem in distribution:
            solver = distribution[problem]
            message_text += problem + ': @id' + str(find_id(solver)) + '(' + solver + ')\n'
        else:
            message_text += problem + ': никто))' 

    if (len(message_text) != 0):
        send_message('распределение:\n' + message_text, message['peer_id'])

def wa(message):
    global solved_problems

    problems = [i for i in message['text'].split(' ') if len(i) != 0][1:]
    distribution = get_distribution()
    not_problems = list()
    message_text = ''

    if (distribution == -1):
        send_message('что-то сломалось, и вы вряд ли сможете что-то с этим сделать))', message['peer_id'])
        return

    for problem in problems:
        if (problem not in solved_problems):
            not_problems.append(problem)
            continue

        if (problem not in distribution):
            message_text += problem + ' : все еще никто)))\n' 
        else:
            solved_problems[problem].remove(distribution[problem])

            if (len(solved_problems[problem]) == 0):
                solved_problems.pop(problem)

    distribution = get_distribution()

    if (distribution == -1):
        send_message('что-то сломалось, и вы вряд ли сможете что-то с этим сделать))', message['peer_id'])
        return

    for problem in problems:
        if (problem in not_problems):
            continue

        if (problem not in distribution):
            message_text += problem + ' : никто)))\n'
        else:
            solver = distribution[problem]
            message_text += problem + ': @id' + str(find_id(solver)) + '(' + solver + ')\n'

    if (len(message_text) != 0):
        send_message(message_text, message['peer_id'])
    
    if (len(not_problems) != 0):
        message_text = 'не нашел данные номера: ' + otformatirovat(not_problems) + ' в моем блокнотике решений. проверьте, не описались ли вы))'
        send_message(message_text, message['peer_id'])

    write_solved_problems()

def debug(message):
    message_text = ''

    for problem in solved_problems:
        solutions = solved_problems[problem]
        message_text += problem + ': ' + otformatirovat(solutions) + '\n'

    if (len(message_text) != 0):
        high_pr = [i for i in _106 if _106[i] == -inf]
        if (len(high_pr) != 0):
            message_text += '\n\nНапоминаю, что следующим людям: ' + otformatirovat(high_pr) + ' желательно решить хотя бы одну задачку.'

        send_message('debug:\n' + message_text, message['peer_id'])
    else:
        send_message('никто ничего не решил))', message['peer_id'])

def debug_2(message):
    send_message('debug_2:\n' + otformatirovat2(_106), message['peer_id'])

def enable_forced(message):
    if (vk_map[message['from_id']] not in admins):
        return

    global FORCED
    mode = [i for i in message['text'].split(' ') if len(i) != 0][1]
    FORCED = (mode == '1')

def switch_mute(message, state):
    if (vk_map[message['from_id']] not in admins):
        return

    name = [i for i in message['text'].split(' ') if len(i) != 0][1]

    if (name in _106):
        if (state):
            ignored.add(name)
        else:
            ignored.remove(name)
    else:
        if (state):
            for man in _106:
                ignored.add(man)
        else:
            ignored = set()

def remove_problem(message):
    if (vk_map[message['from_id']] not in admins):
        return

    problems = [i for i in message['text'].split(' ') if len(i) != 0][1:]

    for problem in problems:
        if (problem in solved_problems):
            solved_problems.pop(problem)

def add_solution(message):
    if (vk_map[message['from_id']] not in admins):
        return

    text = [i for i in message['text'].split(' ') if len(i) != 0][1:]
    global _106

    problem, name, mode = text[0], text[1], text[2]

    if (mode == '1'):
        if (problem not in solved_problems):
            return

        solved_problems[problem].remove(name)

        if (len(solved_problems[problem]) == 0):
            solved_problems.pop(problem)
    else:
        if (problem not in solved_problems):
            solved_problems[problem] = list()

        solved_problems[problem].append(name)

    for problem in solved_problems:
        solved_problems[problem] = sorted(solved_problems[problem], key=lambda x: _106[x])

def help(message):
    documentation =  '''Общие правила пользования:
                        В каждом сообщении бот воспринимает первое слово как команду, все остальные - как ее аргументы. Вызвать несколько команд одним сообщением нельзя.

                        Все команды, принимающие аргументы, примают их в неограниченном количестве. Все команды, не принимающие аргументы, все указанные аргументы игнорируют.

                        Полный список доступных комманд представлен ниже с недлинной документацией. Если документация не ответила на ваши вопросы спросите @id369807714(Евана).


                        Команды:

                        1) \\solved [PROBLEMS] - записывает вас в виртуальный блокнотик людей, решивших задачку. Выполняет проверку на дурачка*.

                        2) \\force_solved [PROBLEMS] - то же самое, что \\solved, но проверка на дурачка отключена.

                        3) \\not_solved [PROBLEMS] - вычеркивает вас из виртуального блокнотика людей, решивших задачку.

                        3) \\high_priority [PEOPLE] - повышает приоритет выбора решения указанных людей. Человек определяется фамилией, написанной русскими буквами(регистр не важен).

                        4) \\distribution - выводит распределение людей по задачам. Сам виртуальный блокнотик людей, решивших задачи при это не стирается, так что можно вызвать несколько раз и не бояться, что кто-нибудь все резко сотрет.

                        4) \\wa [PROBLEMS] - работает аналогично \\distribution, но только для указанных задач и в предположении, что первый человек в списке решил задачу неправильно. Используется, если Орлов в последний момент сказал WA. Может вызываться несколько раз.

                        5) \\debug_2 - выводит количество баллов у всех людей(в этот раз учитываются так же контрольные/самостоятельные/кдз).

                        6) \\debug - выводит виртуальный блокнотик людей, решивших задачку по всем задачкам.

                        7) \\help - выводит "документацию"

                        *в моем несложном понимании правильная запись номера представляется в виде: число.число[(русская буква)]''' 

    send_message(documentation, message['peer_id'])

def stop_bot(message):
    if (vk_map[message['from_id']] in admins):
        exit(0)

#--------------сам бот----------------

read_106()

if (len(sys.argv) > 1 and sys.argv[1] == '-r'):
    read_solved_problems()

def main():
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object.message

                if (message['peer_id'] != Peer_id and message['peer_id'] != Peer_id2):
                    continue

                text = [i for i in message['text'].split(' ') if len(i) != 0]

                if (len(text) == 0):
                    continue

                if (vk_map[message['from_id']] in ignored):
                    continue

                command = text[0]

                if (command == '\\restart'):
                    restart(message)

                elif (command == '\\solved'):
                    solved(message, FORCED)

                elif (command == '\\force_solved'):
                    solved(message, True)

                elif (command == '\\not_solved'):
                    not_solved(message)

                elif (command == '\\high_priority'):
                    increase_priority(message)

                elif (command == '\\distribution'):
                    distribution(message)

                elif (command == '\\wa'):
                    wa(message)

                elif (command == '\\debug'):
                    debug(message)

                elif (command == '\\debug_2'):
                    debug_2(message)

                elif (command == '\\help'):
                    help(message)

                elif (command == '\\mute'):
                    switch_mute(message, True)

                elif (command == '\\unmute'):
                    switch_mute(message, False)

                elif (command == '\\enable_forced'):
                    enable_forced(message)

                elif (command == '\\remove_problem'):
                    remove_problem(message)

                elif (command == '\\add_solution'):
                    add_solution(message)

                elif (command == '\\exit'):
                    stop_bot(message)
    except Exception as e:
        print(e)
        time.sleep(30)
        main()

main()