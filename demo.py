# -*- coding: utf-8 -*-

# 导入需要用到的工具
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # 添加PIL库来处理图片
import os  # 添加os模块来处理路径
import random  # 添加random模块用于生成随机数

# 创建主窗口
window = tk.Tk()
window.title('滚动数字程序')
window.geometry('300x400')

# 创建显示数字的标签
数字标签 = tk.Label(
    window, 
    text='点击开始按钮开始滚动',
    font=('Arial', 48),
    fg='#FF4444'
)
数字标签.pack(pady=40)  # 在顶部显示数字

# 初始化变量
当前数字 = 1
正在运行 = False
最终数字 = 1  # 添加变量存储最终要显示的随机数

# 控制按钮状态的函数
def 设置按钮状态(状态):
    # 设置所有按钮的状态（'normal' 或 'disabled'）
    button1.config(state=状态)
    button3.config(state=状态)

# 定义滚动数字的函数
def 滚动数字():
    global 当前数字, 正在运行
    if not 正在运行:
        return
        
    # 更新数字
    数字标签.config(text=str(当前数字))
    
    # 准备下一个数字
    当前数字 += 1
    if 当前数字 > 8:
        当前数字 = 1
        
    # 50毫秒后再次更新
    window.after(50, 滚动数字)

# 定义停止函数
def 停止滚动():
    global 正在运行, 当前数字
    正在运行 = False
    # 生成1-8的随机数并显示
    当前数字 = random.randint(1, 8)
    数字标签.config(text=str(当前数字))
    设置按钮状态('normal')  # 启用所有按钮

# 创建第一个按钮（开始按钮）
def 开始按钮被点击():
    global 正在运行, 当前数字
    if not 正在运行:
        正在运行 = True
        当前数字 = 1
        设置按钮状态('disabled')  # 禁用所有按钮
        滚动数字()
        # 3秒后自动停止并显示随机数
        window.after(3000, 停止滚动)
    
button1 = tk.Button(window, 
    text='开始滚动',
    highlightbackground='#FF4444',
    background='#FF4444',
    fg='white',
    width=20,
    height=2,
    command=开始按钮被点击
)
button1.pack(pady=20)

# 创建第三个按钮
def 第三个按钮被点击():
    图片窗口()  # 创建并显示图片窗口
    
button3 = tk.Button(window,
    text='显示图片',
    highlightbackground='#44FF44',
    background='#44FF44',
    fg='white',
    width=20,
    height=2,
    command=第三个按钮被点击
)
button3.pack(pady=20)

# 创建显示图片窗口的类
class 图片窗口:
    def __init__(self):
        # 创建新窗口
        self.window = tk.Toplevel()
        self.window.title('图片���示')
        self.window.geometry('400x400')  # 增加窗口高度以容纳按钮
        
        # 创建一个框架来容纳图片和按钮
        self.frame = tk.Frame(self.window)
        self.frame.pack(expand=True)
        
        try:
            # 使用相对路径加载图片
            图片路径 = os.path.join('images', 'display.jpg')
            image = Image.open(图片路径)
            # 调整图片大小以适应窗口
            image = image.resize((380, 280), Image.Resampling.LANCZOS)
            # 转换图片格式
            self.photo = ImageTk.PhotoImage(image)
            
            # 创建标签显示图片
            self.label = tk.Label(self.frame, image=self.photo)
            self.label.pack(pady=10)
            
        except Exception as e:
            # 如果加载图片失败，显示错误信息
            tk.Label(self.frame, 
                text='请将图片放在images文件夹中\n并命名为display.jpg',
                font=('Arial', 14)
            ).pack(pady=10)
        
        # 创建"停止加持"按钮
        self.button = tk.Button(
            self.frame,
            text='停止加持',
            highlightbackground='#FF4444',  # 使用红色突出显示
            background='#FF4444',
            fg='white',
            width=20,
            height=2,
            command=self.停止加持按钮被点击
        )
        self.button.pack(pady=20)
    
    def 停止加持按钮被点击(self):
        messagebox.showwarning('确认', '你确定放弃成功率加持么？')

# 运行程序
window.mainloop() 
