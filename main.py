import re
import converter
import csv
from pprint import pprint as pp


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)

    new_contact_list = converter.create_new_contact_list(contacts_list)
    # pp(new_contact_list)

    fixed_new_contact_list = converter.fix_twins(new_contact_list)
    # pp(fixed_new_contact_list)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
      datawriter = csv.writer(f, delimiter=',')
      datawriter.writerows(fixed_new_contact_list)
