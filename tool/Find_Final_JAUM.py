import json

FINAL_JAUM = set([
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ',
    'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ',
    'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
])

def is_jaum_only(char):
    return char in FINAL_JAUM

def find_words_ending_with_jaum(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for entry in data:
        word = entry['word']
        if word and is_jaum_only(word[-1]):
            results.append(word)

    return results

if __name__ == "__main__":
    filepath = 'json/kkutu_all_words.json'
    words = find_words_ending_with_jaum(filepath)
    for w in words:
        print(w)
    print(f"\n총 {len(words)}개 단어가 자음 문자로 끝.")
