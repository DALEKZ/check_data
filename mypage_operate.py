#coding:utf-8


import re
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
import operator
import pandas  as pd
from collections import Counter



#
# 返回： 所有>=10的待采集数据
def over_ten_data(driver):
    page_num = 0
    data_ele = [1]
    url_list = []
    rows = []
    while len(data_ele) != 0:
        # 换页
        js = "javascript:submitPost('{}')".format(page_num)
        driver.execute_script(js)

        # 当页 <tr>
        data_ele = driver.find_elements_by_tag_name('tr')
        del data_ele[0]
        del data_ele[-1]

        # 当页 <a>
        url_ele = driver.find_elements_by_xpath("//tbody//tr//a[1]")
        del url_ele[0]
        del url_ele[-1]

        # 获取所有查看url
        for url in url_ele:
            url = url.get_attribute("href")
            url_list.append(url)

        # 获取所有行数据
        for row in data_ele:
            rows.append(row.text.split())

        page_num = page_num + 1

    # url+rows
    # rows:所有待采集的数据
    num = 0
    for row in rows:
        row.append(url_list[num])
        num = num + 1

    # 大于10的待采集数据
    over_ten_rows = []
    for row in rows:
        times = row[4]
        times = int(re.sub("\D","", times))
        if times >= 10:
            over_ten_rows.append(row)

    return over_ten_rows


# 参数：源数据来源机构类型
# 返回：指定类型的待采集的任务数据
# ps: 只获取单页
def get_rows(type_name, driver):
    driver.find_element(By.ID, "collectType").click()
    dropdown = driver.find_element(By.ID, "collectType")
    dropdown.find_element(By.XPATH, "//option[. = '{}']".format(type_name)).click()

    ele = driver.find_elements_by_tag_name('tr')
    rows = []
    for i in ele:
        rows.append(i.text.split())

    return rows, len(rows)


# 使用模拟点击删除待处理任务
def delete(driver, row_num):
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.frame(0)
    driver.find_elements(By.LINK_TEXT, "删除")[row_num].click()
    driver.switch_to_alert().accept()
    time.sleep(1)
    driver.switch_to.accept()


def delete_by_api(task_id):
    ...


def count_by_type(rows):
    df = pd.DataFrame(rows)
    count = df[1].value_counts()
    print("-------------包含大于等于10数据的采集类型-------------")
    print(count)
    return count

def check_webpage(driver, rows):
    ...

def main():
    driver = webdriver.Chrome()
    driver.get("http://47.97.123.142:8780/pigeonDataCollect/superLogin.html")
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.find_element(By.ID, "username").send_keys("checkAdmin")
    driver.find_element(By.ID, "password").send_keys("0592zhangjing")
    driver.find_element(By.CSS_SELECTOR, ".button").click()
    driver.find_element(By.LINK_TEXT, "待采集任务").click()
    driver.switch_to.frame(0)

    over_ten_rows = over_ten_data(driver)
    count_by_type(over_ten_rows)

    driver.quit()
    #rows = [['1532806519', 'shangHaiXiehuiSecond', '2020年12月21日', '23时21分', '134次', '2020年12月24日', '23时21分', '否', '否', '查看', '删除', 'http://www.srpa.com.cn/matchresult.aspx?matchid=7529'], ['1532806524', 'shangHaiXiehuiSecond', '2020年12月21日', '23时21分', '134次', '2020年12月24日', '23时21分', '否', '否', '查看', '删除', 'http://www.srpa.com.cn/matchresult.aspx?matchid=7535'], ['1532806522', 'shangHaiXiehuiSecond', '2020年12月21日', '23时21分', '134次', '2020年12月24日', '23时21分', '否', '否', '查看', '删除', 'http://www.srpa.com.cn/matchresult.aspx?matchid=7531'], ['1534961405', 'shangHaiXiehuiSecond', '2020年12月24日', '23时21分', '122次', '2020年12月27日', '23时21分', '否', '否', '查看', '删除', 'http://www.srpa.com.cn/matchresult.aspx?matchid=7541'], ['1534961411', 'shangHaiXiehuiSecond', '2020年12月24日', '23时21分', '122次', '2020年12月27日', '23时21分', '否', '否', '查看', '删除', 'http://www.srpa.com.cn/matchresult.aspx?matchid=7543'], ['1534961415', 'shangHaiXiehuiSecond', '2020年12月24日', '23时21分', '122次', '2020年12月27日', '23时21分', '否', '否', '查看', '删除', 'http://www.srpa.com.cn/matchresult.aspx?matchid=7545'], ['1535847494', 'shangHaiXiehuiSecond', '2020年12月28日', '17时59分', '104次', '2020年12月31日', '17时59分', '否', '否', '查看', '删除', 'http://www.srpa.com.cn/matchresult.aspx?matchid=7555'], ['1535847492', 'shangHaiXiehuiSecond', '2020年12月28日', '17时59分', '105次', '2020年12月31日', '17时59分', '否', '否', '查看', '删除', 'http://www.srpa.com.cn/matchresult.aspx?matchid=7553'], ['1535847490', 'shangHaiXiehuiSecond', '2020年12月28日', '17时59分', '105次', '2020年12月31日', '17时59分', '否', '否', '查看', '删除', 'http://www.srpa.com.cn/matchresult.aspx?matchid=7551']]

if __name__ == "__main__":
    main()
