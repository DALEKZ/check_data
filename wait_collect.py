from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import re
import time
from PIL import Image
import yzm_rec


# 获取待采集的数据，非原页面数据
def get_rows(type_name, driver):
    driver.find_element(By.ID, "collectType").click()
    dropdown = driver.find_element(By.ID, "collectType")
    dropdown.find_element(By.XPATH, "//option[. = '{}']".format(type_name)).click()

    ele = driver.find_elements_by_tag_name('tr')
    rows = []
    for i in ele:
        rows.append(i.text.split())
    del rows[0]
    del rows[-1]

    return rows


# 信鸽协会
def xinge_xiehui(driver, rows):
    row_num = 0
    for i in rows:
        collect_times = i[4]
        collect_times = re.sub("\D", "", collect_times)
        if collect_times == "": collect_times = 0
        if int(collect_times) > 10:
            # 查看原页面
            driver.find_elements(By.LINK_TEXT, "查看")[row_num].click()
            driver.switch_to.window(driver.window_handles[1])
            xgxh_url = driver.current_url


            if xgxh_url == 'http://c.crpa.net.cn/cc/alogin.aspx':
                driver.save_screenshot('D:\\ps.png')
                ele = driver.find_element_by_xpath('//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[3]/img')
                location = ele.location
                size = ele.size
                rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                          int(location['y'] + size['height']))
                i = Image.open('D:\\ps.png')
                frame4 = i.crop(rangle)
                frame4.save('save.png')
                text = yzm_rec.recognize_text(r'save.png')
                driver.find_element_by_xpath('//*[@id="txtCheckCode"]').send_keys(text)
                driver.find_element_by_xpath('//*[@id="Button1"]').click()

                while driver.current_url == 'http://c.crpa.net.cn/cc/alogin.aspx':
                    driver.refresh()
                    driver.save_screenshot('D:\\ps.png')
                    ele = driver.find_element_by_xpath('//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[3]/img')
                    location = ele.location
                    size = ele.size
                    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                              int(location['y'] + size['height']))
                    i = Image.open('D:\\ps.png')
                    frame4 = i.crop(rangle)
                    frame4.save('save.png')
                    text = yzm_rec.recognize_text(r'save.png')
                    driver.find_element_by_xpath('//*[@id="txtCheckCode"]').clear()
                    driver.find_element_by_xpath('//*[@id="txtCheckCode"]').send_keys(text)
                    driver.find_element_by_xpath('//*[@id="Button1"]').click()

                else:
                    text = driver.find_element_by_xpath('//*[@id="FormView1_home_numLabel"]').text
                    if text == '':
                        driver.switch_to.window(driver.window_handles[0])
                        driver.switch_to.frame(0)
                        driver.find_elements(By.LINK_TEXT, "删除")[row_num].click()
                        driver.switch_to_alert().accept()
                        time.sleep(1)
                        driver.switch_to_alert().accept()

                    else:
                        row_num = row_num + 1

            else:
                text = driver.find_element_by_xpath('//*[@id="FormView1_home_numLabel"]').text
                if text == '':
                    driver.switch_to.window(driver.window_handles[0])
                    driver.switch_to.frame(0)
                    driver.find_elements(By.LINK_TEXT, "删除")[row_num].click()
                    driver.switch_to_alert().accept()
                    time.sleep(1)
                    driver.switch_to_alert().accept()
        else:
            row_num = row_num + 1


# 安捷协会 原页面无数据自动删除 未完成调试
def anjie_xiehui(driver, rows):
    row_num = 0
    for i in rows:
        collect_times = i[4]
        collect_times = re.sub("\D", "", collect_times)
        if collect_times == '':
            collect_times = 0
        if int(collect_times) > 10:
            # 查看原页面
            driver.find_elements(By.LINK_TEXT, "查看")[row_num].click()
            driver.switch_to.window(driver.window_handles[1])
            anjie_uri = driver.current_url

            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.frame(0)
            if anjie_uri == 'http://gh.aj52zx.com/race.aspx':
                print(collect_times)
                driver.find_element(By.LINK_TEXT, "删除").click()
                driver.switch_to_alert().accept()
                time.sleep(1)
                driver.switch_to_alert().accept()
            else:
                row_num = row_num + 1
        else:
            row_num = row_num + 1


# 岭东资讯 原页面无数据自动删除 未完成调试
def lingdong_zixun(driver, rows):
    row_num = 0
    for i in rows:
        collect_times = i[4]
        collect_times = re.sub("\D", "", collect_times)
        if collect_times == '': collect_times = 0
        if int(collect_times) > 10:
            # 查看原页面
            driver.find_elements(By.LINK_TEXT, "查看")[row_num].click()
            driver.switch_to.window(driver.window_handles[1])
            content = driver.find_element_by_xpath("//tbody//tbody//tbody//tbody//font").text

            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.frame(0)
            if content == '目前并无归返资料':
                driver.find_elements(By.LINK_TEXT, "删除")[row_num].click()
                driver.switch_to_alert().accept()
                time.sleep(1)
                driver.switch_to_alert().accept()
            else:
                row_num = row_num + 1


def main():
    driver = webdriver.Chrome()
    driver.get("http://47.97.123.142:8780/pigeonDataCollect/superLogin.html")
    driver.implicitly_wait(10)
    driver.maximize_window()

    # 登录
    driver.find_element(By.ID, "username").send_keys("checkAdmin")
    driver.find_element(By.ID, "password").send_keys("0592zhangjing")
    driver.find_element(By.CSS_SELECTOR, ".button").click()

    driver.find_element(By.LINK_TEXT, "待采集任务").click()
    driver.switch_to.frame(0)

    xinge_rows = get_rows("信鸽协会", driver)
    if len(xinge_rows) > 0:
        xinge_xiehui(driver, xinge_rows)

    ajxh_rows = get_rows("安捷协会", driver)
    if len(ajxh_rows) > 0:
        anjie_xiehui(driver, ajxh_rows)

    # ldzx_rows = get_rows("岭东资讯", driver)
    # if len(ldzx_rows) > 2:
    #     lingdong_zixun(driver, ldzx_rows)

    # lsajxh_rows = get_rows("临时安捷协会", driver)
    # if len(lsajxh_rows) > 0:
    #     anjie_xiehui(driver, lsajxh_rows)
    driver.quit()


if __name__ == "__main__":
    main()
