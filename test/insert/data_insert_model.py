# import json
# import os
# import re

# file_path = os.path.join("database.json")

# result = []

# print("단어를 입력하세요. 'end'를 입력하면 종료됩니다.")

# while True:
#     line = input().strip()
#     if line.lower() == 'end':
#         break

#     match = re.match(r"^(.*?)(?: 단어 길이|$)", line)
#     if match:
#         word = match.group(1).strip()
#         if word and not word.startswith("단어 길이"):
#             result.append({"word": word})

# if os.path.exists(file_path):
#     with open(file_path, "r", encoding="utf-8") as json_file:
#         existing_data = json_file.read()
# else:
#     existing_data = "[]"

# last_bracket_index = existing_data.rfind("]")
# if last_bracket_index != -1:
#     new_data = existing_data[:last_bracket_index] + ",\n"
#     for i, item in enumerate(result):
#         new_data += f'    {json.dumps(item, ensure_ascii=False)}'
#         if i != len(result) - 1:
#             new_data += ',\n'
#         else:
#             new_data += '\n'
#     new_data += existing_data[last_bracket_index:]
# else:
#     new_data = '[\n'
#     for i, item in enumerate(result):
#         new_data += f'    {json.dumps(item, ensure_ascii=False)}'
#         if i != len(result) - 1:
#             new_data += ',\n'
#         else:
#             new_data += '\n'
#     new_data += ']'

# with open(file_path, "w", encoding="utf-8") as json_file:
#     json_file.write(new_data)

# print(f"결과가 '{file_path}'에 저장되었습니다.")

























#################################################################################################################################





















import json
import os
import re

file_path = os.path.join("database.json")

result = []

print("단어를 입력하세요. 'end'를 입력하면 종료됩니다.")

while True:
    line = input().strip()
    if line.lower() == 'end':
        break

    match = re.match(r"^(.*?)\s*(?:단어 길이|후속 단어 수|$)", line)
    if match:
        word = match.group(1).strip()
        if word:
            result.append({"word": word})

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        existing_data = json_file.read()
else:
    existing_data = "[]"

last_bracket_index = existing_data.rfind("]")
if last_bracket_index != -1:
    new_data = existing_data[:last_bracket_index]

    if new_data.endswith("}\n"):
        new_data += ',\n'

    for i, item in enumerate(result):
        if i == 0:
            new_data += f'    {json.dumps(item, ensure_ascii=False)}'
        else:
            new_data += f',\n    {json.dumps(item, ensure_ascii=False)}'

    new_data += '\n' + existing_data[last_bracket_index:]  
else:
    new_data = '[\n'
    for i, item in enumerate(result):
        if i == 0:
            new_data += f'    {json.dumps(item, ensure_ascii=False)}'
        else:
            new_data += f',\n    {json.dumps(item, ensure_ascii=False)}'
    new_data += '\n]'

with open(file_path, "w", encoding="utf-8") as json_file:
    json_file.write(new_data)

print(f"결과가 '{file_path}'에 저장되었습니다.")















