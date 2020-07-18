from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from utils.date_parse import *
from utils.logsave import *
import re,time

class jobUtils():
    def __init__(self,driver,username):
        self.init_url = "http://tao-moss/sites/IPT-CP71/Lists/JobSheet/AllItems.aspx"
        self.driver = driver
        self.username = username
        self.productList = []
        #self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(10)

    def get_userlist(self):
        self.userlist = []
        try:
            self.driver.get(self.init_url)
            # time.sleep(10)
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"""//*[@id="117608"]/tbody/tr/td[1]/a""")))
        except TimeoutError:
            raise RuntimeError("request %s failed,Please check network env")
        try:
            self.driver.find_element(By.XPATH,"""//*[@id="117608"]/tbody/tr/td[1]/a""").click()
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"""//td[@class="ms-vb-title"]/table/tbody/tr/td[1]/a""")))
            Items = self.driver.find_elements(By.XPATH,"""//td[@class="ms-vb-title"]/table/tbody/tr/td[1]/a""")
            for item in Items:
                self.userlist.append(item.text)
            print(self.userlist)
            return self.userlist
        except Exception as e:
            print(e)
            raise RuntimeError(e,"get user list failed!")

    def get_productlist(self):
        try:
            logger.info(self.init_url)
            self.driver.get(self.init_url)
            # time.sleep(10)
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"""//*[@id="117608"]/tbody/tr/td[1]/a""")))
            self.driver.find_element(By.XPATH, """//*[@id="117608"]/tbody/tr/td[1]/a""").click()
        except TimeoutError as e:
            logger.error(e)
            logger.error("request %s failed,Please check network env")
            raise RuntimeError("request %s failed,Please check network env")
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                 u"""//td[@class="ms-vb-user"]//a[contains(text(),"%s IES")]/ancestor::td[@class="ms-vb-user"]/../td[@class="ms-vb-title"]//tbody/tr/td[1]/a""" % self.username)))
            self.driver.find_element(By.XPATH,
                                     """//td[@class="ms-vb-user"]//a[contains(text(),"%s IES")]/ancestor::td[@class="ms-vb-user"]/../td[@class="ms-vb-title"]//tbody/tr/td[1]/a""" % self.username).click()
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"""//*[@id="zz10_NewMenu"]""")))
            self.driver.find_element(By.XPATH,"""//*[@id="zz10_NewMenu"]""").click()
            items = self.driver.find_elements(By.XPATH,"""//*[@id="ctl00_m_g_a4f28019_4087_4e77_a1cc_6367e06d048b_ctl00_ctl04_ctl02_ctl00_ctl00_ctl04_ctl00_ctl00_QueryLookUpDropDown"]/option""")
            for item in items:
                self.productList.append(item.text)
            print(self.productList)
            logger.info(self.productList)
            logger.info("获取产品成功")
            return self.productList
        except Exception as e:
            print(e)
            logger.error(e)
            logger.error("获取产品失败")
            raise RuntimeError("Get Product list failed")

    def readjob(self):
        self.row_table = []
        try:
            logger.info("开始获取Jobsheet")
            logger.info("self.init_url")
            self.driver.get(self.init_url)
            # time.sleep(10)
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"""//*[@id="117608"]/tbody/tr/td[1]/a""")))
            self.driver.find_element(By.XPATH, """//*[@id="117608"]/tbody/tr/td[1]/a""").click()
        except TimeoutError as e:
            logger.info(e)
            logger.info("获取Jobsheet失败")
            raise RuntimeError("request %s failed,Please check network env")
        try:
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,u"""//td[@class="ms-vb-user"]//a[contains(text(),"%s IES")]/ancestor::td[@class="ms-vb-user"]/../td[@class="ms-vb-title"]//tbody/tr/td[1]/a""" % self.username)))
            self.driver.find_element(By.XPATH,"""//td[@class="ms-vb-user"]//a[contains(text(),"%s IES")]/ancestor::td[@class="ms-vb-user"]/../td[@class="ms-vb-title"]//tbody/tr/td[1]/a""" % self.username).click()
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"""//*[@id="zz10_NewMenu"]""")))
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"""//*[@id="{41867749-D21A-43E5-9EE8-52834BECD140}-{CCBDA5B4-1096-4C8E-81B4-7FD222482561}"]/tbody""")))
            table = self.driver.find_element(By.XPATH,"""//*[@id="{41867749-D21A-43E5-9EE8-52834BECD140}-{CCBDA5B4-1096-4C8E-81B4-7FD222482561}"]/tbody""")
            table_tr_list = table.find_elements(By.XPATH,"./tr")
            # print(self.table_tr_list)
            for tr in table_tr_list:
                table_td_list = tr.find_elements(By.XPATH,'./td')
                row_list = []
                # print(table_td_list)
                for td in table_td_list:
                    row_list.append(td.text)
                print(row_list)
                logger.info(row_list)
                if row_list:
                    self.row_table.append(row_list)
                    logger.info(self.row_table)
            # return th_list,self.row_table
            return  self.row_table
        except Exception as e:
            print(e)
            logger.error(e)
            logger.error("Get JobSheet Failed")
            raise RuntimeError("Get JobSheet Failed")

    def readywt(self):
        try:
            logger.info(self.init_url)
            self.driver.get(self.init_url)
            # time.sleep(10)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, """//*[@id="117608"]/tbody/tr/td[1]/a""")))
            self.driver.find_element(By.XPATH, """//*[@id="117608"]/tbody/tr/td[1]/a""").click()
        except TimeoutError as e:
            logger.error("request %s failed,Please check network env")
            raise RuntimeError("request %s failed,Please check network env")
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                 u"""//td[@class="ms-vb-user"]//a[contains(text(),"%s IES")]/ancestor::td[@class="ms-vb-user"]/../td[@class="ms-vb-title"]//tbody/tr/td[1]/a""" % self.username)))
            self.driver.find_element(By.XPATH,
                                     """//td[@class="ms-vb-user"]//a[contains(text(),"%s IES")]/ancestor::td[@class="ms-vb-user"]/../td[@class="ms-vb-title"]//tbody/tr/td[1]/a""" % self.username).click()
        except Exception as e:
            logger.error("Get user failed")
            print(e)
            raise ("Get user failed")

    def startwrite(self,job_list):
            product = job_list[0]
            from_date = job_list[1]
            date = formatdate(job_list[1])
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, """//*[@id="zz10_NewMenu"]""")))
                self.driver.find_element(By.XPATH, """//*[@id="zz10_NewMenu"]""").click()
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-input")))
                input_date = self.driver.find_element_by_class_name('ms-input')
                input_date.clear()
                input_date.send_keys(date)
                select_ele = self.driver.find_element_by_xpath(
                    '//*[@id="ctl00_m_g_a4f28019_4087_4e77_a1cc_6367e06d048b_ctl00_ctl04_ctl02_ctl00_ctl00_ctl04_ctl00_ctl00_QueryLookUpDropDown"]')
                s = Select(select_ele)
                s.select_by_value(product)
                self.driver.find_element_by_xpath(
                    '//*[@id="ctl00_m_g_a4f28019_4087_4e77_a1cc_6367e06d048b_ctl00_ctl04_ctl03_ctl00_ctl00_ctl04_ctl00_ctl00_TextField"]').send_keys(
                    '8')
                ok_btn = self.driver.find_element_by_class_name("ms-ButtonHeightWidth")
                ok_btn.click()
                logger.info("Jobsheet product:%s date:%s time:8 wirte successful" %  (product,from_date))
                return "Jobsheet product:%s date:%s time:8 wirte successful" %  (product,from_date)
            except Exception as e:
                print(e)
                logger.error("Jobsheet  product:%s data:%s time:8 wirte failed" % (product,from_date))
                raise RuntimeError("Jobsheet  product:%s data:%s time:8 wirte failed" % (product,from_date))


if __name__ == '__main__':
    tester = jobUtils(webdriver.Chrome(),"Wang Simon")
    tester.readjob()