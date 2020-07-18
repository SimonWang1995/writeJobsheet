from utils.logsave import *
from tkinter.messagebox import *
from threading import Thread
import re
from random import choice


def getuserinfo(root,kaoqian):
    try:
        logger.info("开始获取用户信息")
        user_info = kaoqian.getuserinfo()
        logger.info(user_info)
        return user_info
    except Exception as e:
        logger.error(e)
        showinfo(message=e)
        root.quit()

def getkaoqian(root,kaoqian):
    if not kaoqian.table:
        try:
            logger.info("开始获取考勤信息")
            kaoqian_list = kaoqian.get_kaoqian()
            logger.info(kaoqian_list)
            return kaoqian_list
        except Exception as e:
            logger.error(e)
            showinfo(message=e)
    else:
        return kaoqian.table

def get_total(root,kaoqian):
    work_days = []
    kq_list = getkaoqian(root,kaoqian)
    for value in kq_list:
        if value[3]=="日班" or value[8]=="加班":
            pat = re.compile("(\d+).(\d+).(\d+)")
            date_tuple = pat.search(value[0]).groups()
            date = '/'.join(date_tuple)
            work_days.append(date)
    showinfo(message="你这个月共上班 %s 天 , 详细请查看考勤" % len(work_days))
    return work_days



def get_productlist(root, jobsheet):
    if not jobsheet.productList:
        try:
            product_list = jobsheet.get_productlist()
            return product_list
        except Exception as e:
            showinfo(message=e)
    else:
        return jobsheet.productList

def create_treeview(Treeview,page,headers,widths):
    treeview = Treeview(page, show="headings", columns=headers)
    for col,v in zip(headers,widths):
        treeview.column(col,width=v,anchor="center")
        treeview.heading(col,text=col)
    return treeview


def startwrite(startbutton, treeview, jobsheet):
    startbutton.config(bg="yellow", text="Ongoing")
    for item in treeview.get_children():
        value = treeview.item(item, option="value")
        try:
            jobsheet.readywt()
            jobsheet.startwrite(value)
            treeview.delete(item)
            treeview.update()
        except Exception as e:
            print(e)
            showinfo(message=e)
            startbutton.config(bg="red", text="Stop")
    startbutton.config(bg="green", text="Start")

def add_value():
    pass


def thread_it(func, *args):
  '''将函数放入线程中执行'''
  # 创建线程
  t = Thread(target=func, args=args)
  # 守护线程
  t.setDaemon(True)
  # 启动线程
  t.start()

