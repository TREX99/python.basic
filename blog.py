from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome("C:/Users/TREX/Downloads/교육자료/일단공부/chromedriver.exe")
driver.implicitly_wait(3)

driver.get("https://nid.naver.com/nidlogin.login")

driver.find_element_by_id("id").send_keys("trex99")
driver.find_element_by_id("pw").send_keys("Tjdwjd8*")
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

time.sleep(20)  # 수동 로그인할 때까지 기다린다.

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
