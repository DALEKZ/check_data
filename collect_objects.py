import re
from PIL import Image
import yzm_rec
from mypage_operate import *


# 操作页面：源数据所在网站
# class: 数据来源网站
# 作用：查看源数据网页的返回情况以及个别字段
# 缺点：                耦合度高
#


# 岭东资讯
class LingDong_ZiXun:

    def __init__(self, driver):
        self.driver = driver
        self.task_rows, self.rows_num = get_rows("岭东资讯", driver)

    def lingdong_zixun(self, rows):
        row_num = 0
        for i in rows:
            collect_times = i[4]
            collect_times = re.sub("\D", "", collect_times)
            if collect_times == '': collect_times = 0
            if int(collect_times) > 10:
                # 查看原页面
                self.driver.find_elements(By.LINK_TEXT, "查看")[row_num].click()
                self.driver.switch_to.window(self.driver.window_handles[1])
                content = self.driver.find_element_by_xpath("//tbody//tbody//tbody//tbody//font").text
                if content == '目前并无归返资料':
                    delete(self.driver, row_num)
                else:
                    row_num = row_num + 1
            else:
                row_num = row_num + 1


# 信鸽协会
class XinGeXieHui:

    def __init__(self, driver):
        self.driver = driver
        self.task_rows, self.rows_num = get_rows("信鸽协会", driver)

    def xinge_xiehui(self, row):

        # 查看原页面
        self.driver.get(row[-1])
        self.driver.switch_to.window(self.driver.window_handles[1])
        xgxh_url = self.driver.current_url
        if xgxh_url == 'http://c.crpa.net.cn/cc/alogin.aspx':
            self.check_yzm()
            while self.driver.current_url == 'http://c.crpa.net.cn/cc/alogin.aspx':
                self.driver.refresh()
                self.check_yzm()
            else:
                text = self.driver.find_element_by_xpath('//*[@id="FormView1_home_numLabel"]').text
                if text == '': ...
                # delete(self.driver, row_num)


        else:
            text = self.driver.find_element_by_xpath('//*[@id="FormView1_home_numLabel"]').text
            if text == '':
                ...
                # delete(self.driver, row_num)

    def check_yzm(self):
        self.driver.save_screenshot('D:\\ps.png')
        ele = self.driver.find_element_by_xpath('//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[3]/img')
        location = ele.location
        size = ele.size
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))
        i = Image.open('D:\\ps.png')
        frame4 = i.crop(rangle)
        frame4.save('save.png')
        text = yzm_rec.recognize_text(r'save.png')
        self.driver.find_element_by_xpath('//*[@id="txtCheckCode"]').clear()
        self.driver.find_element_by_xpath('//*[@id="txtCheckCode"]').send_keys(text)
        self.driver.find_element_by_xpath('//*[@id="Button1"]').click()


# 安捷协会
class AnJieXieHui:

    def __init__(self, driver):
        self.driver = driver
        self.task_rows, self.rows_num = get_rows("安捷协会", driver)
        self.data_rows = []

    def anjie_xiehui(self, rows):
        row_num = 0
        for i in rows:
            collect_times = i[4]
            collect_times = re.sub("\D", "", collect_times)
            if collect_times == '':
                collect_times = 0
            if int(collect_times) > 10:
                # 查看原页面
                self.driver.find_elements(By.LINK_TEXT, "查看")[row_num].click()
                self.driver.switch_to.window(self.driver.window_handles[1])
                anjie_uri = self.driver.current_url

                if anjie_uri == 'http://gh.aj52zx.com/race.aspx':
                    delete(self.driver, row_num)
                else:
                    self.data_rows.append(i[0])
                    row_num = row_num + 1
            else:
                row_num = row_num + 1


def login(driver):
    # 登录
    driver.find_element(By.ID, "username").send_keys("checkAdmin")
    driver.find_element(By.ID, "password").send_keys("0592zhangjing")
    driver.find_element(By.CSS_SELECTOR, ".button").click()
    driver.find_element(By.LINK_TEXT, "待采集任务").click()
    driver.switch_to.frame(0)


def main():
    driver = webdriver.Chrome()
    driver.get("http://47.97.123.142:8780/pigeonDataCollect/superLogin.html")
    driver.implicitly_wait(10)
    driver.maximize_window()
    login(driver)

    xgxh = XinGeXieHui(driver)
    if len(xgxh.task_rows) > 0:
        xgxh.xinge_xiehui(xgxh.task_rows)
        del_num = xgxh.rows_num - get_rows("信鸽协会", driver)[1]
        print("信鸽协会原有'{}'条数据".format(xgxh.rows_num))
        print("信鸽协会删除'{}'条".format(del_num))
        print("--------------------------")

    else:
        print("------信鸽协会无待采集任务------")

    ajxh = AnJieXieHui(driver)
    if len(ajxh.task_rows) > 0:
        ajxh.anjie_xiehui(ajxh.task_rows)
        del_num = ajxh.rows_num - get_rows("安捷协会", driver)[1]
        print("安捷协会原有'{}'条数据".format(ajxh.rows_num))
        print("安捷协会删除'{}'条".format(del_num))
        print("--------------------------")

    else:
        print("------安捷协会无待采集任务------")

    #
    ldzx = LingDong_ZiXun(driver)
    if len(ldzx.task_rows) > 0:
        ldzx.lingdong_zixun(ldzx.task_rows)
        del_num = ldzx.rows_num - get_rows("岭东资讯", driver)[1]
        print("岭东资讯原有'{}'条数据".format(ldzx.rows_num))
        print("岭东资讯删除'{}'条".format(del_num))
        print("--------------------------")

    else:
        print("------岭东资讯无待采集任务------")

    driver.quit()


if __name__ == "__main__":
    main()
