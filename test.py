from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# 데이터프레임 생성
df = pd.DataFrame(columns=['상세보기', '지역', '장소', '소개', '설명'])

# 첫 번째 URL (방문한 웹사이트)
base_url = "https://korean.visitkorea.or.kr/detail/rem_detail.do?cotid=3bec10cf-4219-4998-9499-ef7c472d821c"

# 웹 드라이버 설정
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# 페이지 열기
driver.get(base_url)

# 첫 번째 크롤링 작업
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tab_menu"))
)

driver.execute_script("arguments[0].scrollIntoView(true);", element)
driver.execute_script(
    "window.scrollBy(0, -window.innerHeight / 2 + arguments[0].offsetHeight / 2);",
    element
)

title_menu = soup.find('ul', {'class':'tab_menu'})
title_menu_ids = [li.get('id') for li in title_menu.find_all('li')]
title_menu_name = [li.text for li in title_menu.find_all('li')]

for idx, id in enumerate(title_menu_ids):
    input_button = driver.find_element("id", id)
    ActionChains(driver).move_to_element(input_button).click().perform()

    element = driver.find_element(By.CSS_SELECTOR, f'.region_box#{id}')
    sub_elements = element.find_elements(By.CSS_SELECTOR, '.swiper-slide.swiper-slide-active')

    sub_list = [a.get_attribute('href') for div in sub_elements for a in div.find_elements(By.TAG_NAME, 'a')]
    sub_list_text = [a.text for div in sub_elements for a in div.find_elements(By.TAG_NAME, 'a')]

    for idx2, link in enumerate(sub_list):
        driver.execute_script("window.open('');")
        tabs = driver.window_handles
        driver.switch_to.window(tabs[-1])
        driver.get(link)
        time.sleep(3)

        try:
            new_page_html = driver.page_source
            new_page_soup = BeautifulSoup(new_page_html, "html.parser")
            time.sleep(2)
            
            area_txt_view = driver.find_element(By.CSS_SELECTOR, '.area_txtView.bottom')
            driver.execute_script("arguments[0].scrollIntoView(true);", area_txt_view)
            
            plus_button = area_txt_view.find_element(By.CSS_SELECTOR, '.btn_more')
            ActionChains(driver).move_to_element(plus_button).click().perform()
            
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.inr p')))
            p_text_elements = driver.find_elements(By.CSS_SELECTOR, '.inr p')
            extracted_texts = []

            time.sleep(2)
            list_soup = new_page_soup.find_all('div', class_='inr')

            time.sleep(2)

            for p in p_text_elements:
                text = p.text.strip()
                if text:
                    extracted_texts.append(text)
                    if extracted_texts:
                        df = pd.DataFrame(extracted_texts, columns=["상세정보"])


            
            for div in list_soup:
                ul = div.find('ul')
                if ul:
                    li_items = ul.find_all('li')
                    for li in li_items:
                        strong = li.find('strong')
                        span = li.find('span')
                        if strong:
                            strong_text = strong.text.strip() 
                            span_text = span.text.strip() 
                            new_row = pd.DataFrame({'지역': [title_menu_name[idx]], '장소': [sub_list_text[idx2]],
                                                    '소개': [strong_text], '설명': [span_text]})
                            df1 = pd.concat([df1, new_row], ignore_index=True)

            driver.close()
            driver.switch_to.window(tabs[0])     
        except:
            driver.close()
            driver.switch_to.window(tabs[0]) 
            continue

    if not p_text_elements:
        print("p 태그를 찾을 수 없습니다.")
    else:
        for p in p_text_elements:
            text = p.text.strip()
            if text:
                extracted_texts.append(text)

    if extracted_texts:
        df2 = pd.DataFrame(extracted_texts, columns=["상세정보"])

# 엑셀 파일로 저장
df.to_excel("extracted_texts_combined.xlsx", index=False)
print("엑셀 파일로 저장되었습니다.")
