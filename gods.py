#!/usr/bin/env python
import sys, csv
from collections import OrderedDict
debug = True
fields = ['Greek', 'Greek Romanized', 'Roman', 'Roman Anglicized', 'Etruscan', 'Egyptian', 'Description']
gods_dicts = []
for row in csv.DictReader(open('godinfos.csv','r'),delimiter='\t',fieldnames=fields, skipinitialspace=True):
    # replace empty fields with empty strings
    for key in row.keys():
        if row[key] is None:
            row[key] = ''
    gods_dicts.append(row)
used_names = []
exit_now = False

def read_csv_lines(filename, target_list, force_print_error=False):
    global debug
    try:
        for row in csv.reader(open(filename, 'r'), delimiter='\t'):
            # replace empty fields with empty strings
            for i, obj in row:
                if obj is None:
                    row[i] = ''
            target_list.append(row)
    except Exception as err:
        print('Error reading %s: %s' % (filename, type(err)))
        if force_print_error or debug:
            print(err)

def read_lines(filename, target_list, force_print_error=False):
    global debug
    try:
        for row in open(filename, 'r').readlines():
            row_stripped = row.strip()
            if row_stripped != "":
                target_list.append(row)
    except Exception as err:
        print('Error reading %s: %s' % (filename, type(err)))
        if force_print_error or debug:
            print(err)


def find_god_dict(name):
    for god in gods_dicts:
        if name.lower() in god['Greek Romanized'].lower():
            return god
    return None


def generate_god_info_lines(god_dict):
    lines = ['Name: %s (%s)' % (god_dict['Greek Romanized'], god_dict['Greek']),
             #'Roman: %s%s' % ("" if god_dict['Roman Anglicized'].strip() == "" else '%s / ' % god_dict['Roman Anglicized'], god_dict['Roman'])
    '']
    for field in fields[2:]:
        stripped_content = god_dict[field].strip()
        if stripped_content != "":
            lines.append('%s: %s' % (field, stripped_content))
    return lines


def print_god_info_text(god_name):
    god_dict = find_god_dict(god_name)
    if god_dict is None:
        print('No information available. :(')
        return
    lines = generate_god_info_lines(god_dict)
    print('\n'.join(lines))


def print_random_god():
    import random
    god_nr = random.randint(1, len(gods_dicts))
    print('Selecting random god #%i:' % god_nr)
    print('\n'.join(generate_god_info_lines(gods_dicts[god_nr - 1])))


def print_used_names(print_annotations):
    global used_names
    if print_annotations:
        print('Name\tAnnotation')
    for line in used_names:
        print(line[0].strip() + ('\t'+' '.join(line[1:]) if print_annotations else '')


def find_available_names():
    global used_names
    global gods_dicts
    to_check = used_names.copy()
    for god in gods_dicts:
        taken = False
        for i, name in to_check:
            if name.lower() in god['Greek Romanized'].lower():
                taken = True
                to_check.pop(i)
                break
        if not taken:
            yield god


def print_available_names():
    for god in find_available_names():
        print(god['Greek Romanized'])


def menu_pick_new_name():
    actions = OrderedDict(

    )


def edit_used_name_entry():
    pass

def print_actions(menu_name_and_actions):
    menu_name = menu_name_and_actions[0]
    actions = menu_name_and_actions[1]
    print('(%s) Available options:' % menu_name)
    for action in actions.items():
        print(action[0] + '\t' + action[1][0])

def show_menu(menu_name, actions)
    actions_cpy = actions.copy()
    actions_cpy['?'] = ('show this help', print_actions, (menu_name, actions))
    user_input = ''
    exit_menu = False
    while not exit_menu:
        print('(%s) What would you like to do? press ? to show available actions' % menu_name)
        if user_input not in actions:
            print('(%s) unrecognised action, try again. Your input should usually be a single character followed by return' % menu_name)
        user_input = sys.stdin.readline().strip()
    action = actions[user_input]
    action[1](action[2])


def menu_main():
    global exit_now
    actions =  OrderedDict(
        u=('Print used names', print_used_names, False),
        i=('get used names + associated system info', print_used_names, True),
        a=('print available names', print_available_names, None),
        n=('pick a new name and add it to the use list', menu_pick_new_name(), None),
         e=('edit or delete an entry in the used list', edit_used_name_entry(), None),
        q=('quit', exit, 0)
    )
    while not exit_now:
        show_menu('main menu', actions)


if __name__ == '__main__':
    names = []
    if len(sys.argv) > 1:
        argument = sys.argv[1].strip().lower()
        if len(argument) > 1:
            if argument.endswith('.txt'):
                names = open(sys.argv[1], 'r').readlines()
            else:
                names = [argument]
            for name in names:
                stripped_name = name.strip()
                if stripped_name != "":
                    print('Input: %s' % stripped_name)
                    print_god_info_text(stripped_name)
        else:
            print('no proper argument given.'
                  'either input nothing, a single name or the path to a text file (name ending with .txt!) with names')
    else:
        read_csv_lines('used_names.csv', used_names)

        menu_main()