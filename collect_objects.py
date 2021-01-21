from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import re
import time
from PIL import Image
import yzm_rec


class Xinge_Xiehui():

    def wait_collect(self, driver, rows):
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

