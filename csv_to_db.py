import csv

with open('fichier.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    my_list = [row for row in reader]

print(headers)
print(my_list)
