from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pyperclip


# 네이버 captcha 를 회피하기 위한 복사 & 붙여넣기
def clipboard_input(driver, user_xpath, user_input_value):
    temp_user_input_value = pyperclip.paste()
    pyperclip.copy(user_input_value) # input을 클립보드로 복사
    driver.find_element_by_xpath(user_xpath).click() # element focus 설정
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform() # Ctrl+V 전달
    pyperclip.copy(temp_user_input_value)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
    time.sleep(1)

driver = webdriver.Chrome("C:/Users/TREX/Downloads/교육자료/일단공부/chromedriver.exe")
driver.implicitly_wait(3)

driver.get("https://nid.naver.com/nidlogin.login")

#driver.find_element_by_id("id").send_keys("trex99")
#driver.find_element_by_id("pw").send_keys("Tjdwjd8*")
clipboard_input(driver, '//*[@id="id"]', "trex99")
clipboard_input(driver, '//*[@id="pw"]', "Tjdwjd8*")
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

time.sleep(1)  # captcha가 나타나면 이 값을 20이상으로 수정한 후 수동 로그인하고 다시 1로 수정

driver.get("https://admin.blog.naver.com/AdminNaverCommentManageView.nhn?paging.commentSearchType=0&paging.economyTotalCount=58&paging.commentSearchValue=&blogId=trex99&paging.currentPage=2")
driver.implicitly_wait(5)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

writer = soup.select('span.hand._writer')
contents = soup.select('span._replyRealContents')

print(writer)
print(contents)

#for n in writer:
#    print(n.text.strip())
#soup.select('p > span.price')[0].text   
