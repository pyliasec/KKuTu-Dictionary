# import json
# import os
# import re

# # json 폴더가 없으면 생성
# if not os.path.exists("json"):
#     os.makedirs("json")

# # 파일 이름 입력받기
# file_name = input("저장할 JSON 파일 이름을 입력하세요(확장자 제외): ").strip()
# file_path = os.path.join("json", f"{file_name}.json")

# # 결과를 저장할 리스트
# result = []

# print("단어를 입력하세요. 'end'를 입력하면 종료됩니다.")

# while True:
#     line = input().strip()
#     if line.lower() == 'end':  # 종료 조건
#         break

#     # 단어만 추출: "단어 길이" 등의 추가 정보를 제외
#     match = re.match(r"^(.*?)(?: 단어 길이|$)", line)
#     if match:
#         word = match.group(1).strip()
#         # "단어 길이"나 빈 문자열을 제외한 유효 단어만 추가
#         if word and not word.startswith("단어 길이"):
#             result.append({"word": word})

# # JSON 파일로 저장 (정확한 형식으로 저장)
# with open(file_path, "w", encoding="utf-8") as json_file:
#     # 정상적인 JSON 형식으로 저장
#     json.dump(result, json_file, ensure_ascii=False, indent=4)

# print(f"결과가 '{file_path}'에 저장되었습니다.")


import json
import os
import re

# json 폴더가 없으면 생성
if not os.path.exists("json"):
    os.makedirs("json")

# 파일 이름 입력받기
file_name = input("저장할 JSON 파일 이름을 입력하세요(확장자 제외): ").strip()
file_path = os.path.join("json", f"{file_name}.json")

# 결과를 저장할 리스트
result = []

print("단어를 입력하세요. 'end'를 입력하면 종료됩니다.")

while True:
    line = input().strip()
    if line.lower() == 'end':  # 종료 조건
        break

    # 단어만 추출: "단어 길이" 등의 추가 정보를 제외
    match = re.match(r"^(.*?)(?: 단어 길이|$)", line)
    if match:
        word = match.group(1).strip()
        # "단어 길이"나 빈 문자열을 제외한 유효 단어만 추가
        if word and not word.startswith("단어 길이"):
            result.append({"word": word})

# JSON 파일로 저장 (줄바꿈 없이 한 줄로 출력)
with open(file_path, "w", encoding="utf-8") as json_file:
    json_file.write('[\n')  # 첫 번째 대괄호와 줄바꿈 추가
    for i, item in enumerate(result):
        # 각 항목을 줄바꿈하고, 마지막 항목에는 쉼표 없이 추가
        json_file.write(f'    {json.dumps(item, ensure_ascii=False)}')
        if i != len(result) - 1:  # 마지막 항목이 아니면 쉼표 추가
            json_file.write(',\n')
        else:
            json_file.write('\n')
    json_file.write(']')  # 마지막 대괄호

print(f"결과가 '{file_path}'에 저장되었습니다.")
