import os, time, subprocess, signal, glob   # 系统 - 时间 - 子进程 - 没有解决ctrl+c - 文件筛选
import pandas as pd                         # 处理scan后的数据
import tkinter as tk                        # tkinter主要模块
import tkinter.messagebox                   # tkinter消息提示框


# 连接Wi-Fi函数
def connect(ssid, pwd):
    print('Try connection to', ssid, '.')               # 命令行连接提示
    if tk.messagebox.askokcancel('连接提示', '正在连接至' + ssid + '，请确认。', parent=window):
        print('Confirmed.')                             # 用户端连接提示
        cmd = 'networksetup -setairportnetwork en0 '    # 连接Wi-Fi的networksetup命令
        cmd += '\'' + ssid + '\' ' + pwd.get()          # 连接Wi-Fi的networksetup命令
        connection = os.popen(cmd).read()               # 获取连接后命令行结果
        if connection == '':                            # 不返回任何信息代表连接成功
            tk.messagebox.showinfo('连接提示', ssid + '\r\n连接成功', parent=window)
            f = open('pwd.txt', 'a')                    # 用户端连接成功提示 + 打开本地密码文件
            f.write(ssid + '#' + pwd.get() + '\r\n')    # 保存密码
            f.close()                                   # 关闭文件
        elif connection[0] == 'F':                      # Failed开头代表连接失败 - 此处统一处理成密码错误 - 实际应该查看错误码
            tk.messagebox.showerror('连接提示', ssid + '\r\n连接失败：密码错误', parent=window)
        elif connection[0] == 'C':                      # Could not Foung开头代表连接失败 - 网络不存在 - 存在于信号不稳定的网络中
            tk.messagebox.showerror('连接提示', ssid + '\r\n连接失败：网络不存在', parent=window)
        else:                                           # 其余开头统一处理成未知错误连接失败 - 实际应该查看错误码
            tk.messagebox.showerror('连接提示', ssid + '\r\n连接失败：未知原因', parent=window)
    else:
        print('Cancelled.')                             # 命令行用户取消连接提示


# 监听Wi-Fi函数
def sniff(curcnl):
    print('Starting sniff.')                            # 命令行监听提示
    curcnl = curcnl.split(',')[0]                       # 获取需要监听的信道
    # 监听命令 - 超级管理员权限 - 此命令可用 - 但Pycharm直接Run会出错 - 必须python3 gui.py启动
    sniffprocess = subprocess.Popen('echo \'061224renee\' | sudo -S airport en0 sniff ' + curcnl, shell=True)
    '''TODO 以下均无效
            主要为ctrl+c无法模拟
            ctrl+c功能应放于ctrlc()函数'''
    time.sleep(5)   # 此句有效但无用
    os.kill(sniffprocess.pid, signal.SIGINT)
    sniffprocess.send_signal(signal.SIGINT)
    # sniffreturn = subprocess.popen('echo \'061224renee\' | sudo -S airport en0 sniff ' + curcnl).read()


# 停止监听Wi-Fi函数
def ctrlc():
    latest = 0                                          # tmp文件夹下最新cap文件时间戳
    cap = '/tmp/'                                       # 最新cap文件绝对路径
    for filename in glob.glob(r'/tmp/*.cap'):           # 筛选所有cap后缀文件
        if latest < os.path.getmtime(filename):         # 循环遍历判断最新cap文件时间戳
            latest = os.path.getmtime(filename)
            cap = filename
    # 使用aircrack打开最新cap文件
    capprocess = subprocess.Popen('aircrack-ng ' + cap, shell=True)
    '''TODO 此处需要解决命令行返回信息抓取
            可能subprocess的返回需要再研究一下
            然后在包中检索所需的mac地址
            判断是否抓取到WPA握手
            若抓取到WPA握手
            则echo相应序号完成包的选择
            自动进入dodict()函数
            否则提醒用户再次进行监听或放弃破解'''


# 破解Wi-Fi函数
def dodict(bssid):                                      # TODO 此处重新获取cap完全是因为懒 未来实现ctrlc()函数后两个函数应该可以合并
    latest = 0                                          # tmp文件夹下最新cap文件时间戳
    cap = '/tmp/'                                       # 最新cap文件绝对路径
    for filename in glob.glob(r'/tmp/*.cap'):           # 筛选所有cap后缀文件
        if latest < os.path.getmtime(filename):         # 循环遍历判断最新cap文件时间戳
            latest = os.path.getmtime(filename)
            cap = filename
    # 使用aircrack和本机字典打开最新cap文件破解制定bssid的Wi-Fi的密码
    dictprocess = subprocess.Popen('aircrack-ng -w dict.txt -b' + bssid + ' ' + cap, shell=True)
    '''TODO 此处需要解决命令行返回信息抓取
            可能subprocess的返回需要再研究一下
            在返回中判断是否破解成功
            破解成功则抓取返回值中的KEY FOUND
            提示用户密码破解成功
            选择是否连接至该网络以及是否保存密码
            连接网络跳回至主界面实现
            自动关闭破解窗口
            破解失败则说明本机字典无法破解该密码
            点击确定自动关闭破解窗口'''


# 破解窗口创建函数
def crack(ssid, bssid, channel):
    print('Try to crack', ssid, '.')                    # 命令行破解提示
    if tk.messagebox.askokcancel('连接提示', '正在破解' + ssid + '的密码，请确认。\r\n' + 'Wi-Fi Mac地址：' + bssid + '\r\nWi-Fi端口：' + channel, parent=window):
        print('Confirmed.')                             # 用户端破解提示
        wincrack = tk.Toplevel()                        # 创建Toplevel窗口 - wincrack
        wincrack.title('破解Wi-Fi')                      # 设置wincrack窗口标题
        # 设置窗口大小
        wincrackWidth = 400
        wincrackHeight = 300
        # 获取屏幕分辨率
        crackscreenWidth = wincrack.winfo_screenwidth()
        crackscreenHeight = wincrack.winfo_screenheight()
        x = int((crackscreenWidth - wincrackWidth) / 2)
        y = int((crackscreenHeight - wincrackHeight) / 2)
        # 设置窗口初始位置在屏幕居中
        wincrack.geometry("%sx%s+%s+%s" % (wincrackWidth, wincrackHeight, x, y))
        wincrack.resizable(0, 0)                    # 设置窗口宽高固定
        tk.Button(wincrack,                         # 创建开启监听按钮 - 绑定sniff函数 - 传值信道
                  text="开启监听", width=10, pady=3,
                  command=lambda:sniff(channel)).place(relx=0.2, rely=0.2)
        tk.Button(wincrack,                         # 创建停止监听按钮 - 绑定ctrl函数
                  text="停止监听", width=10, pady=3,
                  command=ctrlc).place(relx=0.5, rely=0.2)
        tk.Button(wincrack,                         # 创建开始破解按钮 - 绑定dodict函数 - 传值bssid
                  text="开始破解", width=10, pady=3,
                  command=lambda:dodict(bssid)).place(relx=0.2, rely=0.3)
        '''TODO 此处停止监听和开始破解按钮未来大概率合并
                完成完全自动化破解'''


# 选择Wi-Fi后显示详细信息函数
def getValue(ap):
    '''TODO 目前只能强制全白清除
            但依然会遗留超出部分的显示
            如标点符号等
            后续可改进'''
    blank = '                                                                                                                                                                                                        \r\n' + \
            '                                                                                                                                                                                                        \r\n' + \
            '                                                                                                                                                                                                        \r\n' + \
            '                                                                                                                                                                                                        \r\n'
    tk.Label(window, text=blank, justify='left').place(relx=0.15, rely=0.4)
    window.update()                                     # 更新窗口 - 清空信息
    curwifi = var.get().split('@')                      # 传参中分离ssid与bssid
    curmac = curwifi[1]                                 # 获取bssid
    curwifi = curwifi[0]                                # 获取ssid
    print('Choose', curwifi, '@', curmac)               # 命令行提示选择的ssid及bssid
    for i in range(0, len(ap)):                         # 遍历获取该ssid与bssid对应的详细信息 - 其实只有bssid是唯一的
        if ap[i]['SSID'] == curwifi and ap[i]['BSSID'] == curmac:
                                                        # 命令行提示匹配的ssid几bssid
            print('Match', ap[i]['SSID'], '@', ap[i]['BSSID'])
            ssid = ap[i]['SSID']                        # 获取ssid - 换变量
            bssid = ap[i]['BSSID']                      # 获取bssid - 换变量
            channel = ap[i]['CHANNEL']                  # 获取信道channel
            # 显示字段编辑格式
            cur = 'Wi-Fi名称：          ' + ap[i]['SSID'] + '\r\n' + \
                  'Wi-Fi MAC地址： ' + ap[i]['BSSID'] + '\r\n' + \
                  'Wi-Fi信道：          ' + ap[i]['CHANNEL'] + '\r\n' + \
                  '安全加密方式：     ' + ap[i]['SECURITY(auth/unicast/group)'] + '\r\n'
            tk.Label(window,                            # 详细信息内容及位置确定
                     text=cur, justify='left').place(relx=0.15, rely=0.5)
            tk.Entry(window,                            # 密码输入框数据绑定及位置确定
                     textvariable=pwd, show='*').place(relx=0.15, rely=0.3)
            tk.Label(window,                            # 破解密码提示信息内容及位置确定
                     text='使用本机dict破解（不保证成功率）', justify='left').place(relx=0.15, rely=0.4)
            tk.Button(window,                           # 创建连接Wi-Fi按钮 - 绑定connect函数 - 传值ssid及pwd
                      text="连接Wi-Fi", width=10, pady=3,
                      command=lambda:connect(ssid, pwd)).place(relx=0.68, rely=0.3)
            tk.Button(window,                           # 创建破解Wi-Fi按钮 - 绑定crack函数 - 传值ssid、bssid及channel
                      text="破解Wi-Fi", width=10, pady=3,
                      command=lambda:crack(ssid, bssid, channel)).place(relx=0.68, rely=0.4)
            break                                       # 找到立即退出循环
    window.update()                                     # 更新窗口 - 显示信息


# 开关Wi-Fi函数
def open():
    if os.popen('networksetup -getairportpower en0').read()[-2] == 'f':
                                                        # 返回信息末位为f代表为Off - 状态为关闭
        opencmd = 'networksetup -setairportpower en0 on'
        os.popen(opencmd).read()                        # 打开Wi-Fi
        if os.popen('networksetup -getairportpower en0').read()[-2] == 'n':
                                                        # 返回信息末位为n代表为On - 状态为开启
            tk.messagebox.showinfo('打开提示', '打开Wi-Fi成功', parent=window)
        else:                                           # 用户端打开提示
            tk.messagebox.showerror('打开提示', '打开Wi-Fi失败\r\n未知错误', parent=window)
    else:                                               # 返回信息末位不为f代表为On - 状态为开启
        closecmd = 'networksetup -setairportpower en0 off'
        os.popen(closecmd).read()                       # 关闭Wi-Fi
        if os.popen('networksetup -getairportpower en0').read()[-2] == 'f':
                                                        # 返回信息末位为f代表为Off - 状态为关闭
            tk.messagebox.showinfo('关闭提示', '关闭Wi-Fi成功', parent=window)
        else:                                           # 用户端关闭提示
            tk.messagebox.showerror('关闭提示', '关闭Wi-Fi失败\r\n未知错误', parent=window)
    window.update()                                     # 更新窗口


# 刷新Wi-Fi函数
def refresh():
    if os.popen('networksetup -getairportpower en0').read()[-2] == 'f':
                                                        # 返回信息末位为f代表为Off - 状态为关闭
        opencmd = 'networksetup -setairportpower en0 on'
        os.popen(opencmd).read()                        # 打开Wi-Fi
    scan()                                              # 调用扫描函数
    window.update()                                     # 更新窗口 - 更新Wi-Fi列表


# 扫描附近Wi-Fi函数
def scan():
    SSID = list()                                       # 值初始化
    BSSID = list()
    RSSI = list()
    CHANNEL = list()
    HT = list()
    CC = list()
    SECURITY = list()
    ap = list()
    wifi = list()
    scan = os.popen('airport scan').read()              # 使用airport命令扫描
    for i in range(0, len(scan.splitlines())):          # 逐行读取
        if i != 0:                                      # 跳过第1行
            dict = {}                                   # 每条Wi-Fi信息的暂存
            # Wi-Fi信息整理
            split = list(filter(None, scan.splitlines()[i].split(' ')))
            length = len(split)
            for l in range(0, length):
                if len(split[l]) > 3 and split[l][2] == ':':
                    for mix in range(0, l - 1):
                        split[0] += ' ' + split[1]
                        split.remove(split[1])
                        length -= 1
                    break
            if len(split) > len(key):
                split[-2] += ' ' + split[-1]
                split.remove(split[-1])
            for k2 in range(0, len(key)):
                dict[key[k2]] = split[k2]
            ap.append(dict)
            SSID.append(split[0])
            BSSID.append(split[1])
            RSSI.append(split[2])
            CHANNEL.append(split[3])
            HT.append(split[4])
            CC.append(split[5])
            SECURITY.append(split[6])
    # 命令行scan信息显示
    data = {'SSID': SSID,
            'BSSID': BSSID,
            'RSSI': RSSI,
            'CHANNEL': CHANNEL,
            'HT': HT, 'CC': CC,
            'SECURITY(auth/unicast/group)': SECURITY}
    df = pd.DataFrame(data)                             # 数据注入DataFrame
    pd.set_option('display.max_columns', None)          # 显示所有列
    pd.set_option('display.max_rows', None)             # 显示所有行
    pd.set_option('max_colwidth', 100)                  # 设置value的显示长度为100，默认为50
    pd.set_option('display.width', 5000)                # 设置整体的显示长度为5000
    print(df)                                           # 打印
    # Wi-Fi列表显示数据整理 - bssid唯一因此采用此种显示
    for n in range(0, len(SSID)):
        wifi.append(SSID[n] + '@' + BSSID[n])

    tk.OptionMenu(window, var, *wifi).place(relx=0.15, rely=0.2)
    tk.Button(window,                                   # 创建Wi-Fi开关按钮 - 绑定open函数
              text="Wi-Fi开关", width=10, pady=3,
              command=open).place(relx=0.68, rely=0.1)
    tk.Button(window,                                   # 创建选择Wi-Fi按钮 - 绑定getValue函数 - 传值ap
              text="选择Wi-Fi", width=10, pady=3,
              command=lambda:getValue(ap)).place(relx=0.68, rely=0.2)
    tk.Button(window,                                   # 创建刷新Wi-Fi按钮 - 绑定refresh函数
              text="刷新Wi-Fi", width=10, pady=3,
              command=refresh).place(relx=0.15, rely=0.1)
    window.update()                                     # 更新窗口 - 显示按钮


if __name__ == '__main__':
    # 设置全局变量
    global SSID, BSSID, RSSI, CHANNEL, HT, CC, SECURITY
    global ap, key, wifi, var, pwd
    # 初始化值与类型
    SSID = list()
    BSSID = list()
    RSSI = list()
    CHANNEL = list()
    HT = list()
    CC = list()
    SECURITY = list()
    ap = list()
    key = list()
    wifi = list()

    # 主窗口相关
    window = tk.Tk()                                    # 创建主窗口
    # 设置窗口大小
    winWidth = 600
    winHeight = 400
    # 获取屏幕分辨率
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
    window.title("计算机网络研讨无线AP")                   # 设置主窗口标题
    # 设置窗口初始位置在屏幕居中
    window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    # # 设置窗口图标 TODO 不知道为什么无效
    # window.iconbitmap("./image/icon.ico")
    window.resizable(0, 0)                              # 设置窗口宽高固定

    # Wi-Fi功能
    curwifi = 'None'                                    # Wi-Fi名称String
    var = tk.StringVar()                                # Wi-Fi名称数据绑定
    pwd = tk.StringVar()                                # Wi-Fi密码输入框数据绑定
    var.set("请选择需要连接的Wi-Fi")                       # Wi-Fi列表默认值设定
    if os.popen('networksetup -getairportpower en0').read()[-2] == 'f':
                                                        # 返回信息末位为f代表为Off - 状态为关闭
        opencmd = 'networksetup -setairportpower en0 on'
        os.popen(opencmd).read()                        # 打开Wi-Fi
    scanresult = os.popen('airport scan').read()        # 获取Wi-Fi扫描结果
    for i in range(0, len(scanresult.splitlines())):
        if i == 0:                                      # 仅获取第1行 - 得到信息字段
            for k in range(0, len(list(filter(None, scanresult.splitlines()[i].split(' '))))):
                key.append(list(filter(None, scanresult.splitlines()[i].split(' ')))[k])
            key[-2] += key[-1]
            key.remove(key[-1])
            break
    scan()                                              # 调用Wi-Fi扫描函数 - 正式扫描
    window.mainloop()                                   # 图形界面循环