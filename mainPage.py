from tkinter import *
from tkinter.messagebox import *
from webutils.jobUtils import jobUtils
from view import *
from webutils.getchecking import *
from selenium import webdriver
from utils.logsave import *
import subfun as fg
from threading import Thread

class mainPage():
    """
    主页面显示
    """
    def __init__(self,master,driver):
        self.root = master
        self.root.geometry("%dx%d" % (800,500))
        self.driver = driver

        logger.info("实例化考勤类")
        self.Kaoqian = getKqian(self.driver)
        self.user_info = fg.getuserinfo(self.root, self.Kaoqian)

        logger.info("实例化jobsheet 类")
        self.Jobsheet = jobUtils(self.driver, self.user_info["姓名"])
        self.initpage()


    def initpage(self):
        logger.info("实例化模块")
        try:
            self.kaoqian = showKaoqian(self.root,self.Kaoqian)
            self.jobsheet = showJobsheet(self.root,self.Jobsheet)
            self.write_day = inputdayPage(self.root,self.Jobsheet)
            self.write_month = inputmonthPage(self.root,self.Jobsheet)
            self.write_kq = inputkqPage(self.root,self.Jobsheet,self.Kaoqian)
            self.showinfo = showInfo(self.root,self.user_info)
            self.showinfo.pack(expand=YES, fill=BOTH)
        except Exception as e:
            logger.error(e)
            logger.error("初始化失败")


        self.mainmenu = Menu(self.root)
        self.viewmenu = Menu(self.mainmenu)
        self.editmenu = Menu(self.mainmenu)

        self.editmenu.add_command(label="考勤填写",command=self.callwrite_kaoqian)
        self.editmenu.add_command(label="按天填写",command=self.callwrite_day)
        self.editmenu.add_command(label="按月填写", command=self.callwrite_month)

        self.viewmenu.add_command(label="考勤",command=self.callkaoqian)
        self.viewmenu.add_command(label="JobSheet",command=self.calljobsheet)

        # 关于
        # self.infomenu = Menu(self.mainmenu)

        self.mainmenu.add_cascade(label="查看",menu = self.viewmenu)
        self.mainmenu.add_cascade(label="填写",menu=self.editmenu)
        self.mainmenu.add_command(label="用户信息",command=self.callinfo)
        self.root["menu"] = self.mainmenu



    def callinfo(self):
        self.kaoqian.pack_forget()
        self.jobsheet.pack_forget()
        self.write_kq.pack_forget()
        self.write_day.pack_forget()
        self.write_month.pack_forget()
        self.showinfo.pack(expand=YES,fill=BOTH)


    def callkaoqian(self):
        self.jobsheet.pack_forget()
        self.write_kq.pack_forget()
        self.write_day.pack_forget()
        self.write_month.pack_forget()
        self.showinfo.pack_forget()
        self.kaoqian.pack(expand=YES,fill=BOTH)
        self.kaoqian.insert()


    def calljobsheet(self):
        self.kaoqian.pack_forget()
        self.write_kq.pack_forget()
        self.write_day.pack_forget()
        self.write_month.pack_forget()
        self.showinfo.pack_forget()
        self.jobsheet.pack(expand=YES,fill=BOTH)
        self.jobsheet.insert()

    def callwrite_kaoqian(self):
        self.kaoqian.pack_forget()
        self.jobsheet.pack_forget()
        self.write_day.pack_forget()
        self.write_month.pack_forget()
        self.showinfo.pack_forget()
        self.write_kq.pack(expand=YES,fill=BOTH)
        self.write_kq.initsubpage()


    def callwrite_day(self):
        self.kaoqian.pack_forget()
        self.jobsheet.pack_forget()
        self.write_kq.pack_forget()
        self.write_month.pack_forget()
        self.showinfo.pack_forget()
        self.write_day.pack(expand=YES,fill=BOTH)
        self.write_day.initsubpage()

    def callwrite_month(self):
        self.kaoqian.pack_forget()
        self.jobsheet.pack_forget()
        self.write_kq.pack_forget()
        self.write_day.pack_forget()
        self.showinfo.pack_forget()
        self.write_month.pack(expand=YES, fill=BOTH)
        self.write_month.initsubpage()


if __name__ == '__main__':
    root = Tk()
    root.title("JobSheet")
    root.iconbitmap('jobsheet.ico')
    # driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    try:
        mainPage(root, driver)
        root.mainloop()
    finally:
        driver.close()