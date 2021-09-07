import re
import csv
from pprint import pprint as pp

phone_pattern = {
    'main': re.compile(r"[\s+]*(7|8)*"  # 1
                       r"[\s\-\(]*(\d{3})"  # 2
                       r"[\s\-\)]*(\d{3})"  # 3
                       r"[\s\-]*(\d{2})"  # 4
                       r"[\s\-]*(\d{2}).*"),  # 5
    "additional": re.compile(r"[\s\S]*(\d{4})")
}
i = 0
# Для временного хранения, 100% можно было не занимать столько места
names_list = []
organizations_list = []
positions_list = []
phones_list = []
emails_list = []
merge_contact_list = []


# Тут вычлиняем и редактируем, где это требуется, стобцы из исходного файла
def correct_names(contact_list):
    for contact in contact_list:
        names = contact[0:3]
        for i, name in enumerate(names):
            # Для строк, где ФИ находятся в Ф, делаем разбивку на Ф, И
            if len(name.split()) == 2 and i == 0:
                names[0] = ''
                name = name.split()
                for i in range(len(name)):
                    names[i] = name[i]
                    i += 1
            # Для строк, где ИО находятся в И, делаем разбивку на И, О
            elif len(name.split()) == 2 and i == 1:
                names[1] = ''
                name = name.split()
                for i in range(len(name)):
                    names[i + 1] = name[i]
                    i += 1
            # Для строк, где ФИО находятся в 1 месте, делаем разбивку на Ф, И, О
            elif len(name.split()) > 2:
                name = name.split()
                for i in range(len(name)):
                    names[i] = name[i]
                    i += 1
        names_list.append(names)
    return names_list


# print(correct_names(contacts_list))

def correct_organizations(contact_list):
    for contact in contact_list:
        organization = contact[3]
        organizations_list.append(organization)
    return organizations_list


# print(correct_organizations(contacts_list))

def correct_position(contact_list):
    for contact in contact_list:
        position = contact[4]
        positions_list.append(position)
    return positions_list


# print(correct_position(contacts_list))

def correct_phone(contact_list):
    for contact in contact_list:
        phones = contact[5]
        phones = phones.split('доб.')
        phone = phone_pattern['main'].sub(fr'+7(\2)\3-\4-\5', phones[0])
        if len(phones) > 1:
            additional_part = phone_pattern['additional'].match(phones[1]).groups()
            phone = f'{phone} доб.{additional_part[0]}'
        phones_list.append(phone)
    return phones_list


# pp(correct_phone(contacts_list))


def correct_emails(contact_list):
    for contact in contact_list:
        emails = contact[6]
        emails_list.append(emails)
    return emails_list


# pp(correct_emails(contacts_list))

# Соединяем всё в 1 файл
def merge_all(contact_list, names, oraginizations, positions, phones, emails):
    for i in range(len(contact_list)):
        names[i].append(oraginizations[i])
        names[i].append(positions[i])
        names[i].append(phones[i])
        names[i].append(emails[i])
    merge_contact_list = names
    return merge_contact_list


# pp(merge_all(correct_names(contacts_list), correct_organizations(contacts_list),correct_position(contacts_list),correct_phone(contacts_list),correct_emails(contacts_list)))


# Делаем функцию, чтобы это выглядело поэстетичнее
def create_new_contact_list(contact_list):
    new_contacts_list = merge_all(contact_list, correct_names(contact_list),
                     correct_organizations(contact_list),
                     correct_position(contact_list),
                     correct_phone(contact_list),
                     correct_emails(contact_list))

    return new_contacts_list



# pp(new_contacts_list)

# Сердце проги [подфункция в fix_twins()]
def merge_rows(first_contact=list, second_contact=list):
    result = first_contact[:]
    for i in range(len(first_contact)):
        if second_contact[i] != '':
            result[i] = second_contact[i]
    return result


# pp(merge_rows(new_contacts_list[2],new_contacts_list[4]))


# Проверяем дубль по ФИО или нет [подфункция в need_to_merge()]
def twins(first_name=list, second_name=list):
    len_both_names = set(first_name[0:2] + second_name[0:2])
    len_both_names = ' '.join(len_both_names).strip().split(' ')
    if len(len_both_names) > 3:
        return False
    return True


# print(twins(contacts_list[0],contacts_list[1]))


# Проверяем надо мержить стори или нет [подфункция в fix_twins()]
def need_to_merge(first_contact=list, second_contact=list):
    if first_contact == second_contact:
        return False

    if not twins(first_contact, second_contact):
        return False

    for tip1, tip2 in zip(first_contact, second_contact):
        if not (tip1 == '' or tip2 == '' or tip1 == tip2):
            return False
    return True


# print(need_to_merge(contacts_list[0],contacts_list[1]))


# Самое потное из всей части программы
def fix_twins(contact_list=list):
    fixed_list = [contact_list[0]]

    for item in contact_list[1:]:
        for fix_idx, fix_item in enumerate(fixed_list):
            # Проверяем надо ли слиять строки, если да , то делаем, иначе строка уникальная аппендим её
            if need_to_merge(item, fix_item):
                fixed_list[fix_idx] = merge_rows(fix_item, item)
                break
        else:
            fixed_list.append(item)

    return fixed_list

# pp(fix_twins(new_contacts_list))
#
# if __name__ == '__main__':
#     print('Hello')