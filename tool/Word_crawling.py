from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import json
import time

def generate_all_hangul_syllables():
    return [chr(code) for code in range(0xAC00, 0xD7A4)]

all_words = []

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
driver.get("https://kkutudic.pythonanywhere.com/")

driver.find_element(By.ID, "settings-btn").click()
time.sleep(1)
driver.execute_script("""
    var checkbox = document.getElementById('unlimited');
    if (!checkbox.checked) checkbox.click();
""")
print("'단어 표시 제한 해제' 옵션 적용 완료")

search_keywords = generate_all_hangul_syllables()

for keyword in search_keywords:
    print(f"검색: {keyword}")
    
    driver.execute_script(f"""
        var input = document.getElementsByName("start")[0];
        input.value = "{keyword}";
        input.dispatchEvent(new Event('input'));
    """)

    driver.execute_script('document.getElementById("search-button").click();')

    try:
        WebDriverWait(driver, 10).until(
            lambda d: "검색 중입니다." not in d.find_element(By.CLASS_NAME, "output").text and d.find_element(By.CLASS_NAME, "output").text.strip() != ""
        )
    except:
        print(f"⚠ '{keyword}' 검색 실패 또는 결과 없음")
        continue

    results = driver.find_elements(By.CSS_SELECTOR, ".output .word")
    words = [r.text for r in results]

    for word in words:
        all_words.append({"word": word})

    print(f"{len(words)}개 단어 수집됨 for '{keyword}'")

driver.quit()

with open("kkutu_all_words.json", "w", encoding="utf-8") as f:
    json.dump(all_words, f, ensure_ascii=False, indent=2)

print(f"총 수집 단어 수: {len(all_words)}개 → 'kkutu_all_words.json' 저장 완료")
