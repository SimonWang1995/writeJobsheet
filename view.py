from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import time
from utils.date_parse import *
from random import choice
from utils.logsave import *
import subfun as fg


class MyTreeview(ttk.Treeview):
    def __init__(self,master,headers,widths):
        self.scrollbar = Scrollbar(master)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.root = master
        ttk.Treeview.__init__(self,master,show="headings", columns=headers, yscrollcommand=self.scrollbar.set)
        for col,v in zip(headers,widths):
            self.column(col,width=v,anchor="center")
            self.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(_col, False))
        self.scrollbar.config(command=self.yview)

    def treeview_sort_column(self, col, reverse):  # Treeview、列名、排列方式
        l = [(self.set(k, col), k) for k in self.get_children('')]
        print(self.get_children(''))
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            self.move(k, '', index)
            print(k)
        self.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def inserttext(self,values):
        for i,list in enumerate(values):
            self.insert('',i,value=tuple(list))
            self.update()

    def callmenu(self, Event):
        self.menu = Menu(self.root, tearoff=False)
        self.menu.add_command(label="删除", command=self.delete_select)
        self.menu.add_command(label="编辑")
        self.menu.post(Event.x_root, Event.y_root)

    def delete_select(self):
        if askyesno(title="Delete",message="确认删除吗？"):
            for item in self.selection():
                self.delete(item)


class showKaoqian(Frame):
    """
    用于显示考勤信息的
    """
    def __init__(self,master,kaoqian):
        Frame.__init__(self,master)
        self.root = master
        self.kaoqian = kaoqian
        self.flag=0
        self.creatpage()

    def creatpage(self):
        self.headers = ["日期","工号","姓名","班次","刷卡时间","加班时间","请假时间","上班时数(小时)","状态"]
        wd_list = [100, 60, 50, 20, 100, 20, 20, 20, 40]
        self.treeview = MyTreeview(self, self.headers, wd_list)
        self.treeview.pack(expand=YES,fill=BOTH)

    def insert(self):
        if self.flag==0:
            try:
                logger.info("获取考勤信息")
                self.table_list = fg.getkaoqian(self.root,self.kaoqian)
                self.treeview.inserttext(self.table_list)
                self.flag = 1
            except Exception as e:
                logger.error("e")
                raise e

class showJobsheet(Frame):
    """
    用于显示JobSheet 填写信息
    """
    def __init__(self,master,jobsheet):
        Frame.__init__(self,master)
        self.root = master
        self.jobsheet = jobsheet
        self.creatpage()

    def creatpage(self):
        self.headers = ["Type", "Title", "Date", "Project", "Hours", "Comment", "Created By"]
        wd_list = [40, 60, 80, 120, 40, 80, 120]
        self.treeview = MyTreeview(self, self.headers, wd_list)
        self.treeview.pack(expand=YES,fill=BOTH)
        # self.treeview.bind("<Button-3>",self.refresh(Event))

    def insert(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        try:
            self.table_list = self.jobsheet.readjob()
            self.treeview.inserttext(self.table_list)
        except Exception as e:
            raise e

class showInfo(Frame):
    """
    用于显示用户的信息
    部门：
    工号：
    姓名：
    """
    def __init__(self,master,user_info):
        Frame.__init__(self,master)
        self.root = master
        self.dick_info = user_info
        self.creatpage()

    def creatpage(self):
        print(self.dick_info)
        for i,(key,value) in enumerate(self.dick_info.items()):
            Label(self,text ="%s:" % key.rjust(5),font=('楷体',12)).place(relx=0.2,rely=0.1+0.15*i,relwidth = 0.2,relheight=0.1)
            Label(self,text = "%s" % value.ljust(20),font=('楷体',12)).place(relx=0.4,rely=0.1+0.15*i,relwidth=0.4,relheight=0.1)


class inputdayPage(Frame):
    """
    按天填写的页面
    """
    def __init__(self, master, jobsheet):
        Frame.__init__(self, master)
        self.root = master
        self.flag = 0
        self.jobsheet = jobsheet
        self.product_list = []

    def initsubpage(self):
        if self.flag == 0:
            self.product_list = fg.get_productlist(self.root,self.jobsheet)

            self.date = StringVar()
            self.date.set(time.strftime("%Y/%m/%d", time.localtime(time.time())))
            self.hours = IntVar()
            self.hours.set(8)

            self.pduct=ttk.Combobox(self,values=self.product_list,state="readonly")
            self.pduct.place(relx=0.05,rely=0.02,relwidth=0.3,relheight=0.06)
            Entry(self, textvariable=self.date).place(relx=0.4, rely=0.02, relwidth=0.25, relheight=0.06)
            Entry(self, textvariable=self.hours).place(relx=0.7, rely=0.02, relwidth=0.15, relheight=0.06)
            Button(self,text="添加",command=self.add_click).place(relx=0.9,rely=0.02,relwidth=0.07,relheight=0.06)

            self.treeview = MyTreeview(self, ["Product", "Date", "Hours"], [250, 150, 100])
            self.treeview.bind("<Button-3>",self.treeview.callmenu)
            self.treeview.place(relx=0,rely=0.1,relwidth=0.9,relheight=0.9)
            self.startbutton=Button(self,text="Start",bd=4,bg="green",font=("楷体",12),command=self.startclick)
            self.startbutton.place(relx=0.91,rely=0.45,relwidth=0.07,relheight=0.1)
            self.flag=1


    def add_click(self):
        date_list = []
        for item in self.treeview.get_children():
            date_list.append(self.treeview.item(item,option="value")[1])
        # print(date_list)
        product=self.pduct.get()
        date = self.date.get()
        # print(date)
        hours = self.hours.get()
        value = [product,date,hours]
        myre = re.compile(r"20\d{2}(-|\/)((0[1-9])|(1[0-2]))(-|\/)((0[1-9])|([1-2][0-9])|(3[0-1]))")
        if myre.match(self.date.get()) and self.pduct.get() in self.product_list and 24>self.hours.get()>0 :
            if not date in date_list:
                self.treeview.insert('',0,value=tuple(value))
                self.treeview.update()
                date_list.append(date)
            else:
                showinfo(message="%s  exists" % date)
        else:
            if not myre.match(self.date.get()):
                showinfo(message="Date failed,Please check it!")
            if not self.pduct.get() in self.product_list:
                showinfo(message="product failed,please check it!")
            if self.hours.get()<0 or self.hours.get()>24:
                showinfo(message="Hours failed,Please check it!")

    def startclick(self):
        fg.startwrite(self.startbutton, self.treeview, self.jobsheet)


class inputmonthPage(Frame):
    """
    按月填写的页面
    """
    def __init__(self,master,jobsheet):
        Frame.__init__(self,master)
        self.root=master
        self.jobsheet = jobsheet
        self.date_list=[]
        self.flag = 0



    def initsubpage(self):
        if self.flag == 0:
            self.page1 = Frame(self)
            self.page1.pack(expand=YES,fill=BOTH)
            self.page2 = Frame(self)
            self.createpage1()
            self.createpage2()
            self.flag = 1

    def createpage1(self):
        self.yearmonth=StringVar()
        Label(self.page1,text="填写年月:",font=("楷体",'12')).place(relx=0.2,rely=0.45,relwidth=0.2,relheight=0.1)
        Entry(self.page1,font=("楷体",'12'),textvariable=self.yearmonth).place(relx=0.4,rely=0.45,relwidth=0.2,relheight=0.1)
        self.yearmonth.set(time.strftime("%Y/%m", time.localtime(time.time())))
        self.typebox = ttk.Combobox(self.page1,values=["随机","顺序"],state="readonly",font=("楷体",'12'))
        self.typebox.current(0)
        self.typebox.place(relx=0.65,rely=0.45,relwidth=0.1,relheight=0.1)
        Button(self.page1,text="下一步",command=self.nextclick,font=("楷体",'12')).place(relx=0.92,rely=0.92,width=60,relheight=0.06)

    def createpage2(self):
        self.product_list = fg.get_productlist(self.root,self.jobsheet)

        self.days = IntVar()
        self.hours = IntVar()
        self.hours.set(8)

        self.pduct = ttk.Combobox(self.page2, values=self.product_list, state="readonly")
        self.pduct.place(relx=0.05, rely=0.02, relwidth=0.3, relheight=0.06)
        self.selectbox=ttk.Combobox(self.page2,state="readonly",textvariable=self.days,values=[x+1 for x in range(len(self.date_list))])
        self.selectbox.place(relx=0.4, rely=0.02, relwidth=0.25, relheight=0.06)
        Entry(self.page2, textvariable=self.hours).place(relx=0.7, rely=0.02, relwidth=0.15, relheight=0.06)
        Button(self.page2, text="添加", command=self.add_click).place(relx=0.9, rely=0.02, relwidth=0.07, relheight=0.06)

        self.treeview = MyTreeview(self.page2, ["Product", "Date", "Hours"], [250, 150, 100])
        self.treeview.bind("<Button-3>", self.treeview.callmenu)
        self.treeview.place(relx=0, rely=0.1, relwidth=0.9, relheight=0.9)
        self.startbutton = Button(self.page2, text="Start", bd=4, bg="green", font=("楷体", 12), command=self.startclick)
        self.startbutton.place(relx=0.91, rely=0.45, relwidth=0.07, relheight=0.1)
        Button(self.page2,text="返回",command=self.backclick,font=("楷体",'12')).place(relx=0.92,rely=0.92,width=60, relheight=0.06)


    def startclick(self):
        fg.startwrite(self.startbutton, self.treeview, self.jobsheet)


    def add_click(self):
        if self.pduct.get() and 24 > self.hours.get() > 0:
            for i in range(self.days.get()):
                date = choice(self.date_list)
                product=self.pduct.get()
                # print(date)
                hours = self.hours.get()
                value = [product,date,hours]
                self.treeview.insert('',0,value=tuple(value))
                self.treeview.update()
                self.date_list.remove(date)
                self.selectbox.config(values=[ x+1 for x in range(len(self.date_list))])
                self.page2.update()
                self.days.set(self.days.get()-1)
        else:
            showinfo(title="添加失败",message="输入信息错误，请检查！")


    def nextclick(self):
        self.date_list.clear()
        reym = re.compile("\d{4}/(([1-9])|(0[1-9])|(1[0-2]))")
        if reym.match(self.yearmonth.get()):
            yearmonth = self.yearmonth.get()
            self.date_list = get_dates(yearmonth)
            self.type = self.typebox.get()
            self.page1.pack_forget()
            self.page2.pack(expand=YES,fill=BOTH)
            showinfo(message="This month hava %d workdays" % len(self.date_list))
            self.selectbox.config(values=[x+1 for x in range(len(self.date_list))])
            self.page2.update()
        else:
            showinfo(message="Please input year/month(such as:2020/03")

    def backclick(self):
        self.page2.pack_forget()
        self.page1.pack(expand=YES,fill=BOTH)



class inputkqPage(Frame):
    """
    按考勤填写页面
    """
    def __init__(self,master,jobsheet,kaoqian):
        Frame.__init__(self,master)
        self.root = master
        self.jobsheet = jobsheet
        self.kaoqian = kaoqian
        self.flag = 0


    def initsubpage(self):
        if self.flag == 0 :
            self.product_list = fg.get_productlist(self.root, self.jobsheet)
            self.workday_list = fg.get_total(self.root,self.kaoqian)

            self.days = IntVar()
            self.hours = IntVar()
            self.hours.set(8)

            self.pduct = ttk.Combobox(self, values=self.product_list, state="readonly")
            self.pduct.place(relx=0.05, rely=0.02, relwidth=0.3, relheight=0.06)
            self.selectbox = ttk.Combobox(self, state="readonly", textvariable=self.days, values=[x+1 for x in range(len(self.workday_list))])
            self.selectbox.place(relx=0.4, rely=0.02, relwidth=0.25, relheight=0.06)
            Entry(self, textvariable=self.hours).place(relx=0.7, rely=0.02, relwidth=0.15, relheight=0.06)
            Button(self, text="添加", command=self.add_click).place(relx=0.9, rely=0.02, relwidth=0.07, relheight=0.06)

            self.treeview = MyTreeview(self, ["Product", "Date", "Hours"], [250, 150, 100])
            self.treeview.bind("<Button-3>", self.treeview.callmenu)
            self.treeview.place(relx=0, rely=0.1, relwidth=0.9, relheight=0.9)
            self.startbutton = Button(self, text="Start", bd=4, bg="green", font=("楷体", 12), command=self.startclick)
            self.startbutton.place(relx=0.91, rely=0.45, relwidth=0.07, relheight=0.1)
            self.flag = 1

    def startclick(self):
        # fg.startwrite(self.startbutton, self.treeview, self.jobsheet)
        self.startbutton.config(bg="yellow", text="Ongoing")
        for item in self.treeview.get_children():
            value = self.treeview.item(item, option="value")
            try:
                self.jobsheet.readywt()
                self.jobsheet.startwrite(value)
                self.treeview.delete(item)
                self.treeview.update()
            except Exception as e:
                print(e)
                showinfo(message=e)
                self.startbutton.config(bg="red", text="Stop")
        self.startbutton.config(bg="green", text="Start")

    def add_click(self):
        if self.pduct.get() and 24 > self.hours.get() > 0:
            for i in range(self.days.get()):
                date = choice(self.workday_list)
                product=self.pduct.get()
                # print(date)
                hours = self.hours.get()
                value = [product,date,hours]
                self.treeview.insert('',0,value=tuple(value))
                self.treeview.update()
                self.workday_list.remove(date)
                self.selectbox.config(values=[ x+1 for x in range(len(self.workday_list))])
                self.update()
                self.days.set(self.days.get()-1)
        else:
            showinfo(title="添加失败",message="输入信息错误，请检查！")
