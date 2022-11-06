import os

files_res = []
for file_line in ['1.txt', '2.txt', '3.txt']:
    with open(os.path.join(os.getcwd(), file_line), 'rt', encoding='utf-8') as file:
        data = file.readlines()
        files_res .append([file_line + '\n', str(len(data)) + '\n', data])

files_res .sort(key=lambda i: i[1])

with open(os.path.join(os.getcwd(), 'files_res.txt'), 'wt', encoding='utf-8') as file:
    for file_line in files_res:
        file.writelines([file_line[0], file_line[1]])
        file.writelines(file_line[2])
        file.write('\n')