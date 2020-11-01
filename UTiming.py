import os
from tkinter import *
from tkinter import filedialog, messagebox 

class UTiming(Tk):


    def __init__(self):
        super().__init__()      #TK初始化
        self.file_name = None 
        self._set_window_()     #设置主窗口相关参数
        self.create_menu_bar()  #创建菜单栏
        self.create_body()      #GUI设计与布局

    def _set_window_(self):
        self.title("UTiming")
        #设置主窗口尺寸
        self.geometry('1000x650') #FIXME
        self.protocol('WM_DELETE_WINDOW', self.exit_editor)# 设置“退出”时的行为
    
    def exit_editor(self):
        #用户点击退出时，弹出提示
        if messagebox.askokcancel('Exit','OK to Exit'):
            self.destroy() 
    
    def create_menu_bar(self):
        #创建菜单栏
        menu_bar =Menu(self)
        #在菜单栏中例化“文件”菜单
        file_menu = Menu(menu_bar,tearoff = 0)
        #在“文件”菜单中添加按钮
        file_menu.add_command(label="New Project" , accelerator = 'Ctrl+N',command=self.new_file)
        file_menu.add_command(label="Open Project", accelerator = 'Ctrl+O',command=self.open_file)
        # file_menu.add_command(label="Open Project", accelerator = 'Ctrl+O')
        file_menu.add_command(label="Save Project", accelerator = 'Ctrl+S',command=self.save) 
        file_menu.add_command(label="Save As"     , accelerator = 'Ctrl+Shift+S',command= self.save_as)         

        #将“文件”菜单添加到Menu中
        menu_bar.add_cascade(label='File',menu = file_menu,font=15)

        # menu_bar.add_cascade(label='文件')
        # menu_bar.add_cascade(label='文件')
        
        self['menu'] = menu_bar
    

    def new_file(self,event = None):
        # 新建工程的绑定函数
        self.title('New - UTiming')
        self.txtInput.delete(1.0,END)
        self.labelInputTitle.config(text="New Project")
        self.file_name = None

    def open_file(self,event = None):
        input_file = filedialog.askopenfilename(filetypes=[('所有文件','*.*'),('文本文档','*.txt')])  #弹出文件对话框，设置选择文件的类型   
        if input_file:   			                #如果用户选择了文本，则进行打开
            #print(input_file)   	                #这里可以调试，看一下选中文本的路径的形式（绝对路径）
            self.title('{} - EditorPlus'.format(os.path.basename(input_file))) 
                                                    #以文件的名称进行窗口标题的命名
            self.file_name = input_file 	        #将这个打开的文件对象命名为其原来文件的名称
            self.txtInput.delete(1.0,END)       #删除当前文本内容中的数据
            try:
                with open(input_file, 'r') as _file:
            	    self.txtInput.insert(1.0,_file.read())  #将要打开文件中的数据写入到文本内容中    
            except IOError:
                messagebox.showwarning("打开文件", "打开文件失败！")   #如果文件打开失败的话，会弹出消息对话框
            

    def save(self,event = None):
        #保存文件的绑定函数
        if self.file_name == None:
            self.save_as()
        else:
            self.write_to_file(self.file_name)

    def save_as(self,event = None):

        input_file = filedialog.asksaveasfilename(filetypes = [('所有文件','*.*'),('文本文档','*.txt')])
        #弹出文本保存对话框
        if input_file:
            self.file_name = input_file
            self.write_to_file(self.file_name)

    def write_to_file(self,file_name):
        try:
            content = self.txtInput.get(1.0,'end')
            with open(file_name,'w') as the_file:
                the_file.write(content)
                self.title("%s - UTiming" % os.path.basename(file_name))
                self.labelInputTitle.config(text=os.path.basename(file_name))
        except IOError:
            messagebox.showwarning("保存", "保存失败！")   #如果保存失败的话，会弹出消息对话框


    def update_line_num(self):
        row, col = self.txtInput.index("end").split('.') 
        line_num_content = "\n".join([str(i) for i in range(1, int(row))])  #获取文本行数据
        self.line_num_bar.config(state='normal')                            #将文本栏状态激活
        self.line_num_bar.delete('1.0', 'end')                              #删除原有的行号数据
        self.line_num_bar.insert('1.0', line_num_content)                   #插入行号文本数据
        self.line_num_bar.config(state='disabled')                          #再次封印行号栏

    def create_body(self):
        # frameTextInput和frameOfButtons帧都被包含在frameTextButton中
        self.frameTextButton= Frame(self)

        #输入文本相关例化在frameTextInput中
        self.frameTextInput= Frame(self.frameTextButton)
        #创建横竖两个滚动条
        self.scrInputTextVert=Scrollbar(self.frameTextInput,orient=VERTICAL)
        self.scrInputTextHori=Scrollbar(self.frameTextInput,orient=HORIZONTAL)
        #创建文本输入框
        self.txtInput = Text(self.frameTextInput,height=20,width=40,font=5,wrap=NONE,
                                        yscrollcommand=self.scrInputTextVert.set,
                                        xscrollcommand=self.scrInputTextHori.set)
        #创建行号栏
        self.line_num_bar = Text(self.frameTextInput,width = 3,padx =3,font=5,
                            takefocus = 0,border=0,background = '#F0E68C',
                            state = 'disabled')
        #创建输入文本标签
        self.labelInputTitle = Label(self.frameTextInput,text="New Project",font=8)
        
        #快捷键绑定 
        self.txtInput.bind('<Control-N>', self.new_file)
        self.txtInput.bind('<Control-n>', self.new_file)
        self.txtInput.bind('<Control-O>', self.open_file)
        self.txtInput.bind('<Control-o>', self.open_file)
        self.txtInput.bind('<Control-S>', self.save)
        self.txtInput.bind('<Control-s>', self.save)
        self.txtInput.bind('<Control-Shift-S>', self.save_as)
        self.txtInput.bind('<Control-Shift-s>', self.save_as)
        #绑定回调函数，在输入框中按下任意键，都更新行号
        self.txtInput.bind('<Any-KeyPress>', lambda e: self.update_line_num())

        #在frameTextButton帧中创建frameOfButtons帧
        self.frameOfButtons= Frame(self.frameTextButton)
        #在frameOfButtons中创建三个按钮
        self.Button1=Button(self.frameOfButtons,text="Expert Image")
        self.Button2=Button(self.frameOfButtons,text="Expert Image")
        self.Button3=Button(self.frameOfButtons,text="Image/Txt")

        #add Output Text widget
        self.outputText=Text(self,height=20,width=60,font=5,wrap=NONE,state=DISABLED)

        ###布局所有Widget

        #布局InputText Frame
        self.labelInputTitle.pack(side='top')
        #布局文本滚动条，在InputTextFrame中分别占据右和下方位置，同时与文本框绑定
        self.scrInputTextVert.pack(side=RIGHT,fill=Y)
        self.scrInputTextVert.config(command=self.txtInput.yview)

        self.scrInputTextHori.pack(side=BOTTOM,fill=X)
        self.scrInputTextHori.config(command=self.txtInput.xview)

        #将行号栏布局在TXT的左侧
        self.line_num_bar.pack(side=LEFT,fill=Y)

        # 布局文本输入框，填充整个InputTextFrame
        self.txtInput.pack(fill=BOTH,expand =1)

        #将frameTextInput布局在frameTextButton中的顶部
        self.frameTextInput.pack(side=TOP,padx=10,pady=10)

        # 在frameOfButtons中布局3个按钮
        self.Button1.pack(side=LEFT,anchor=W)
        self.Button2.pack(side=LEFT,anchor=CENTER)
        self.Button3.pack(side=RIGHT,anchor=E)
        # 将frameOfButtons布局到frameTextInput下方
        self.frameOfButtons.pack(side=BOTTOM,padx=10,pady=10,ipadx=10,ipady=10,fill=X)

        #将 frameTextButton 放到整个页面的左边
        self.frameTextButton.pack(side=LEFT,pady=10)
        #布局 将OutputText放到页面右边，同时设置填充和扩展标志
        self.outputText.pack(side=RIGHT,padx=10,pady=10,fill=BOTH,expand =1)




if __name__=='__main__':
    u_timing = UTiming()
    u_timing.mainloop()
 



