from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 웹 드라이버 설정
driver = webdriver.Chrome()

# 페이지 열기
url = "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=d8e19bf8-90c1-41d4-99b0-fd24c62c5574&big_category=A01&mid_category=A0101&big_area=39"
driver.get(url)

try:
    # 페이지가 완전히 로드될 때까지 대기 (10초)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.inr p')))

    # .inr 내부에서 p 태그 텍스트 추출
    p_text_elements = driver.find_elements(By.CSS_SELECTOR, '.inr p')

    if not p_text_elements:
        print("p 태그를 찾을 수 없습니다.")
    else:
        for p in p_text_elements:
            text = p.text.strip()  # 텍스트 앞뒤 공백 제거
            if text:  # 텍스트가 비어 있지 않은 경우에만 출력
                print(text)

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    driver.quit()

