import json

with open("json/kkutu_all_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

suffixes = ("릅", "늡", "컥", "컁", "꿜", "퀑", "쫙", "줅", "좍", "쇅", "둬", "탓", "놔", "츨", "닺", "똔", "휙")
filtered_words = [w for w in words if not w["word"].endswith(suffixes)]

with open("json/kkutu_all_words.json", "w", encoding="utf-8") as f:
    json.dump(filtered_words, f, ensure_ascii=False, indent=2)
