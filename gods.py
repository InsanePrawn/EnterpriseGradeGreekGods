#!/usr/bin/env python
from __future__ import print_function
import sys, csv, random
from copy import deepcopy
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
    god_nr = random.randint(1, len(gods_dicts))
    print('Selecting random god #%i:' % god_nr)
    print('\n'.join(generate_god_info_lines(gods_dicts[god_nr - 1])))


def print_used_names(print_annotations):
    global used_names
    if print_annotations:
        print('Name\tAnnotation')
    for line in used_names:
        print(line[0].strip() + ('\t'+' '.join(line[1:]) if print_annotations else ''))


def find_available_names():
    global used_names
    global gods_dicts
    to_check = deepcopy(used_names)
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


def menu_edit_used_name_entry():
    pass

def print_actions(menu_name, actions):
    print('Menu "%s"\nAvailable actions:' % menu_name)
    print('Key\tDescription')
    print('---\t-----------')
    for action_key, action_parameters in actions.items():
        print(action_key + '\t' + action_parameters[0])
    return False

def show_menu(menu_name, actions, add_return_option=True, return_val=False):
    if debug:
        print('----------------------')
    actions_cpy = deepcopy(actions)
    actions_cpy['?'] = ('show this help', print_actions, [menu_name, actions_cpy])
    if add_return_option:
        actions_cpy['b'] = ('exit this menu', lambda b: b, [True])
    exit_menu = False
    # is not True to catch 'None' as well
    print('(%s) What would you like to do? press ? to show available actions' % menu_name)
    while exit_menu is not True:
        print('(%s) > ' % menu_name, end="")
        user_input = sys.stdin.readline().strip()
        if user_input not in actions_cpy:
            print('(%s) unrecognised action, try again. Your input should usually be a single character followed by return' % menu_name)
        else:
            action = actions_cpy[user_input]
            exit_menu = action[1](*action[2])
    return return_val


def get_user_values(menu_name, values):
    #values should be a (dummy)-prefilled OrderedDict
    print('(%s) Please enter some information:' % menu_name)
    for key in values.keys:
        print('%s:' % key)
        values[key] = sys.stdin.readline().strip()
    print('done!')

def menu_confirm_values(menu_name, values, refresh_values_func, return_val=True):
    refresh_values_func(menu_name, values)
    print('(%s) Please confirm the following values:' % menu_name)
    for key, value in values:
        print('%s: %s' % (key, value))
    print('Are these values correct?')
    actions = OrderedDict(
        y=('yes', lambda b: b, [True]),
        n = ('no, try again',menu_confirm_values,[menu_name, values, refresh_values_func, True, return_val])
    )
    show_menu(menu_name+'/Confirm', actions)
    return return_val


# menu declarations follow

def get_random_suggestion(menu_name, results):
    results.clear()
    available = list(find_available_names())
    god_nr = random.randint(1, len(available))
    if debug:
        print('Random suggestion: #%i out of %i available' % (god_nr, len(available)))
    #print('\n'.join(generate_god_info_lines(available[god_nr - 1])))
    for key, value in available[god_nr - 1].items():
        results[key] = value

PICK_NEW_NAME_ACTIONS = OrderedDict(
    r=('get a random suggestion for a name', menu_confirm_values, ['random suggestion', OrderedDict(), get_random_suggestion])
)

EDIT_USED_NAME_ACTIONS = OrderedDict()



# end of menu declarations




def menu_main():
    actions = OrderedDict(
        u=('Print used names', print_used_names, [False]),
        p=('get used names + associated system info', print_used_names, [True]),
        a=('print available names', print_available_names, []),
        n=('pick a new name and add it to the use list', show_menu, ['Pick Name', PICK_NEW_NAME_ACTIONS]),
        e=('edit or delete an entry in the used name list',  show_menu, ['Edit Used', EDIT_USED_NAME_ACTIONS]),
        q=('quit', lambda a: a, [True])
    )
    show_menu('Main', actions, add_return_option=False)


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