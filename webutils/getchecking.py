from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logsave import *
import pprint

class getKqian():
    def __init__(self,driver=None):
        self.driver = driver
        self.url = "http://www.ies.inventec/default.aspx"
        self.table = []
        self.driver.implicitly_wait(10)

    def getuserinfo(self):
        self.__info_url = "http://ies-hrweb.ies.inventec/NewES/"
        self.__info_dick = {"部門":"","工號":"","姓名":""}
        try:
            logger.info("请求%s" % self.__info_url)
            self.driver.get(self.__info_url)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"""//*[@id="F2"]/frame[1]""")))
        except :
            logger.error("请求%s 失败" % self.__info_url)
            raise RuntimeError("Requests %s failed" % self.__info_url)
        try:
            self.driver.switch_to.frame(self.driver.find_element_by_xpath("""//*[@id="F2"]/frame[1]"""))
            id_name = self.driver.find_element_by_xpath("""//*[@id="lb_name"]""").text
            self.__info_dick["部門"] = self.driver.find_element_by_xpath("""//*[@id="lb_depname"]""").text
            self.__info_dick["工號"] = id_name.split('-')[0]
            self.__info_dick["姓名"] = id_name.split('-')[1]
            return self.__info_dick
        except Exception as e:
            logger.error("获取用户信息失败")
            raise ("Get User Info failed! program exit")


    def get_kaoqian(self):
        try:
            self.kq_url = "http://ies-hrweb.ies.inventec/ES1/Att/aAttendent1.asp"
            # self.driver.get(self.url)
            logger.info("请求http://ies-hrweb.ies.inventec/NewES/")
            self.driver.get(self.kq_url)
            # WebDriverWait(self.driver,15).until(EC.presence_of_element_located((By.XPATH,"""//*[@id="F2"]/frame[1]""")))
            # time.sleep(3)
            # self.driver.switch_to.frame(self.driver.find_element_by_xpath("""//*[@id="F2"]/frame[1]"""))
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, """//*[@id="TreeView1n29"]""")))
            # # try:
            # self.driver.find_element(By.XPATH, """//*[@id="TreeView1n29"]""").click()
            # time.sleep(3)
            # self.driver.find_element(By.XPATH,"""//*[@id="TreeView1t32"]""").click()
            # self.driver.switch_to.default_content()
            # self.driver.switch_to.frame(self.driver.find_element_by_xpath("""//*[@id="F2"]/frame[2]"""))
            self.table_tr_list = self.driver.find_elements(By.XPATH, """/html/body/div/table/tbody/tr[@onmouseover]""")
            for tr in self.table_tr_list:
                td_list = tr.find_elements(By.XPATH, "./td")
                td_row_list = []
                for td in td_list:
                    td_row_list.append(td.text)
                logger.info(td_row_list)
                print(td_row_list)
                self.table.append(td_row_list)
                logger.info(self.table)
            logger.info("获取考勤成功")
            return self.table
        except Exception as e:
            logger.error(e)
            logger.error("获取考勤失败")
            print(e)
            raise ("check on work attendance failed")

    def paser_td(self):
        table = []
        for tr in self.table_tr_list:
            td_list = tr.find_elements(By.XPATH,"./td")
            td_row_list = []
            for td in td_list:
                td_row_list.append(td.text())
            print(td_row_list)
            table.append(td_row_list)

if __name__ == '__main__':
    getKqian().get_kaoqian()