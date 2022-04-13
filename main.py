from pprint import pprint
import csv
import re


def open_contacts():
    with open("phonebook_raw.csv") as f:
        return list(csv.reader(f, delimiter=","))


def save_contacts(data_list):
    with open("phonebook.csv", "w", newline='') as f:
        data = csv.writer(f, delimiter=',')
        data.writerows(data_list)


def read_titles(file_contacts):
    title_phonebook = []
    for item in file_contacts[0]:
        title_phonebook.append(item)
    return title_phonebook


def read_contacts(file_contacts, file_titles):
    phonebook = []
    first_row = True
    for row in file_contacts:
        if not first_row:
            i = 0
            rec_item = dict()
            while i < len(file_titles):
                rec_item[file_titles[i]] = row[i]
                i += 1
            phonebook.append(rec_item)
        first_row = False
    return phonebook


def check_names(contacts, titles):
    for item in contacts:
        fullname = item[titles[0]] + ' ' + item[titles[1]] + ' ' + item[titles[2]]
        result = re.findall('[\w]+', fullname, re.U)
        for i in range(0, len(result)):
            item[titles[i]] = result[i]
    return contacts


def check_phones(contacts, titles):
    for item in contacts:
        item_phone = (item[titles[5]])
        if item_phone:
            result_search = re.search('доб', item_phone)
            if result_search:
                key_position = result_search.span()[0]
                res_1 = ''.join(re.findall(r'\d', item_phone[:key_position]))
                res_2 = ''.join(re.findall(r'\d', item_phone[key_position:]))
                # item[titles[5]] = res_1 + ' & ' + res_2
            else:
                res_1 = ''.join(re.findall(r'\d', item_phone))
                res_2 = ''
            phone = '+7(' + res_1[1:4] + ")"+res_1[4:7]+'-'+res_1[7:9]+'-'+res_1[9:11]
            if res_2:
                phone = phone + ' доб.' + res_2
            item[titles[5]] = phone
    return contacts


def merge_info(main_item, duplicated_item):
    for key, value in main_item.items():
        new_value = duplicated_item.get(key)
        if not value and new_value:
            main_item[key] = new_value


def check_duplicated_records(contacts, titles):
    for item in contacts:
        fullname = item[titles[0]]+item[titles[1]]
        first_encounter = True
        i = 0
        while i < len(contacts):
            current_row = contacts[i]
            if fullname == current_row[titles[0]]+current_row[titles[1]]:
                if first_encounter:
                    first_encounter = False
                    i += 1
                else:
                    merge_info(item, current_row)
                    contacts.pop(i)
            else:
                i += 1
    return contacts


def regulation_contacts(file_contacts, file_titles):
    check_names(file_contacts, file_titles)
    check_phones(file_contacts, file_titles)
    check_duplicated_records(file_contacts, file_titles)


def merge_data(titles, data_list):
    return_value = list()
    return_value.append(titles)
    return_value += (list(value.values()) for value in data_list)

    return return_value


file = open_contacts()
titles_phonebook = read_titles(file)
contacts_list = read_contacts(file, titles_phonebook)
regulation_contacts(contacts_list, titles_phonebook)
save_contacts(merge_data(titles_phonebook, contacts_list))
with open("phonebook.csv") as f:
        pprint(list(csv.reader(f, delimiter=",")))