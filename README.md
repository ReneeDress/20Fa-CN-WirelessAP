# 2020-2021学年秋季学期《计算机网络》研讨
# Python实现Mac OS X下无线AP操作

**Created Date**: 2020-09-25 13:46:12

**Last Upgraded Date**: 2020-09-27 16:22:37

[Blog Link](https://blog.yijunstudio.xyz/2020/09/25/Python%E5%AE%9E%E7%8E%B0Mac%20OS%20X%E4%B8%8B%E6%97%A0%E7%BA%BFAP%E6%93%8D%E4%BD%9C/)

# 操作环境

>macOS Catalina Version 10.15.5
>
>Python 3.7
>
>Pycharm Professional  2020.1.3

## How To Start
```shell
python3 gui.py
```

# networksetup命令

networksetup命令可以在Terminal操作电脑的网络连接状态，其中涉及到无线网络的主要有以下几种：

显示所有网络硬件端口，可获取网络设备名称

```shell
networksetup -listallhardwareports
-------------------------------------------------------
Hardware Port: Wi-Fi
Device: en0
Ethernet Address: 88:e9:fe:手:动:马赛克

Hardware Port: Bluetooth PAN
Device: en6
Ethernet Address: 88:e9:fe:手:动:马赛克

Hardware Port: Thunderbolt 1
Device: en1
Ethernet Address: 82:87:0f:手:动:马赛克

Hardware Port: Thunderbolt 2
Device: en2
Ethernet Address: 82:87:0f:手:动:马赛克

Hardware Port: Thunderbolt 3
Device: en3
Ethernet Address: 82:87:0f:手:动:马赛克

Hardware Port: Thunderbolt 4
Device: en4
Ethernet Address: 82:87:0f:手:动:马赛克

Hardware Port: Thunderbolt Bridge
Device: bridge0
Ethernet Address: 82:87:0f:手:动:马赛克

VLAN Configurations
===================
```

查看Wi-Fi状态

```shell
networksetup -getairportpower en0
```

启用或禁用Wi-Fi

```shell
networksetup -setairportpower en0 on (or off)
```

使用Terminal加入一个Wi-Fi网络

```shell
networksetup -setairportnetwork en0 WIFI_SSID_I_WANT_TO_JOIN WIFI_PASSWORD
```

# Terminal Airport模块

## 为Airport模块建立软链接

Terminal输入以下命令 建立软链接

```shell
sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport /usr/local/bin/airport
```

后续在Terminal直接键入

```shell
airport
```

即可使用Airport模块

## Airport模块常用参数

```shell
LEGACY COMMANDS:
Supported arguments:
 -c[<arg>] --channel=[<arg>]    Set arbitrary channel on the card
 -z        --disassociate       Disassociate from any network
 -I        --getinfo            Print current wireless status, e.g. signal info, BSSID, port type etc.
 -s[<arg>] --scan=[<arg>]       Perform a wireless broadcast scan.
				   Will perform a directed scan if the optional <arg> is provided
 -x        --xml                Print info as XML
 -P        --psk                Create PSK from specified pass phrase and SSID.
				   The following additional arguments must be specified with this command:
                                  --password=<arg>  Specify a WPA password
                                  --ssid=<arg>      Specify SSID when creating a PSK
 -h        --help               Show this help
```

Terminal键入

```shell
aiport scan
```

可获取如下输出

```shell
                            SSID BSSID             RSSI CHANNEL HT CC SECURITY (auth/unicast/group)
                         HONGSHI b0:95:8e:8a:60:ab -75  11,-1   Y  CN WPA(PSK/AES/AES) WPA2(PSK/AES/AES) 
                           NSTOR dc:fe:18:25:54:2b -87  157     Y  -- WPA(PSK/TKIP,AES/TKIP) WPA2(PSK/TKIP,AES/TKIP) 
               Ulstein-Secondary d0:76:e7:c6:d5:cd -78  153     Y  CN WPA(PSK/AES/AES) WPA2(PSK/AES/AES) 
                 5G-Greenland_LH 64:05:e9:1e:b7:7a -88  153     Y  CN WPA2(PSK/AES/AES) 
      绿地滨江Club Free WiFi 64:05:e9:1e:b7:79 -89  153     Y  CN NONE
                    Greenland_LH 64:05:e9:1e:b7:78 -88  153     Y  CN WPA(PSK/AES,TKIP/TKIP) WPA2(PSK/AES,TKIP/TKIP) 
                            HHDS 8c:fd:f0:60:97:a5 -85  108,+1  Y  US WPA2(PSK/AES/AES) 
                          DaHua1 9c:b7:93:ef:60:90 -88  100     Y  DB WPA2(PSK/AES/AES) 
             DIRECT-HMKIRKDUmsLi a2:af:bd:e8:72:f4 -67  11      Y  -- WPA2(PSK/AES/AES) 
                 DIRECT-27666458 fa:d0:27:66:e4:58 -56  7       Y  -- WPA2(PSK/AES/AES) 
                         KASAKII 74:05:a5:8f:db:f8 -50  7,-1    Y  -- WPA(PSK/AES,TKIP/TKIP) WPA2(PSK/AES,TKIP/TKIP) 
                   ChinaNet-qnpj 02:0e:5e:4c:21:2a -74  1       Y  CN WPA2(PSK/TKIP,AES/TKIP) 
               Ulstein-Secondary d0:76:e7:c6:d5:cb -62  1,+1    Y  CN WPA(PSK/AES/AES) WPA2(PSK/AES/AES) 
                       KASAKII5G 74:05:a5:8f:db:fd -55  36      Y  -- WPA(PSK/AES,TKIP/TKIP) WPA2(PSK/AES,TKIP/TKIP) 
                          H3C_5G 4c:e9:e4:b8:6d:dd -72  36      Y  -- WPA(PSK/AES/AES) WPA2(PSK/AES/AES) 

```



# 无线AP常用术语详解

## 无线AP - 无线访问接入点 - Wireless Access Point

无线AP是移动计算机用户进入有线网络的接入点，主要用于宽带家庭、大楼内部以及园区内部，可以覆盖几十米至上百米。无线AP（又称会话点或存取桥接器）是一个包含很广的名称，它不仅包含单纯性无线接入点（无线AP），同样也是无线路由器（含无线网关、无线网桥）等类设备的统称。

### 单纯型AP - 一般指无线AP

缺少路由功能，相当于无线交换机；

仅有无线信号发射功能，将双绞线传来的电信号转换为无线电讯号；

功率影响网络覆盖程度。

### 扩展型AP - 一般指无线路由器

带有无线覆盖功能的路由器；

实现家庭无线网络中的Internet连接共享；

实现ADSL和小区宽带的无线共享接入；

短距离可用。

## 802.11x

### 2.4GHz - 802.11b/g/n/ax

![Graphical representation of overlapping 20 MHz channels within the 2.4 GHz band](./pics/799px-2.4_GHz_Wi-Fi_channels_(802.11b,g_WLAN).svg.png)

![**Most countries** Graphical representation of Wireless LAN channels in 2.4 GHz band. Note "channel 3" in the 40 MHz diagram above is often labelled with the 20 MHz channel numbers "1+5" or "1" with "+ Upper" or "5" with "+ Lower" in router interfaces, and "11" as "9+13" or "9" with "+ Upper" or "13" with "+ Lower"](./pics/425px-NonOverlappingChannels2.4GHzWLAN-en.svg.png)

### 5 GHz or 5.9 GHz - 802.11a/h/j/n/ac/ax

为满足移动宽带通信的发展需求，根据《中华人民共和国无线电频率划分规定》及我国频谱使用情况，参照国际电信联盟《无线电规则》，经研究，现规划5150-5350兆赫兹（MHz）频段用于无线接入系统。

工作频率范围：5150-5350MHz； 最大等效全向辐射功率（EIRP）:200mW；最大等效全向功率谱密度:10dBm/MHz......

为与无线电测定等其他业务共存，工作于 5250-5350MHz频段的无线接入设备应采用发射功率控制（TPC）及动态频率选择（DFS）干扰抑制技术。TPC范围不小于6dB；如无TPC，则发射功率、等效全向辐射功率和最大功率谱密度均应降低3dB。

上述频段的无线接入系统仅限室内使用，且距离同频段的卫星无线电测定（空对地）业务和卫星固定（空对地）业务的地球站大于3km。

无限制信道：36（5180，5170-5190）、40（5200，5190-5210）、44（5220，5210-5230）、48（5240，4230-5250）；DFC/TPC信道：52（5260，5250-5270）、56（5280，5270-5290）、60（5300，5290-5310）、64（5320，5310-5330）。

## SSID - Service Set IDentifier

无线网络名称。

SSID = name of Network

### An SSID is the Name of a Network

Because multiple WLANs can coexist in one airspace, each WLAN needs a unique name—this name is the service set ID (SSID) of the network. Your wireless device can see the SSIDs for all available networks—therefore, when you click a wireless icon, the SSIDs recognized by device are listed. For example, suppose your wireless list consists of three SSIDs named Student, Faculty, and Voice. This means that an administrator has created three WLAN Service profiles and, as part of each WLAN service profile, provided the SSID name Student, Faculty, or Voice. 

As a WLAN user, you are concerned only with the SSIDs. You select one from the list on your laptop or other device, provide your username and a password, and use the SSID. You might not have access to all SSIDs—the authentication and access privileges are usually different for different WLANs and their associated SSIDs.

## BSSID - Basic Service Set IDentifier

如果在一个基础架构网络中，该BSSID的默认是对应的网卡的MAC地址，如果增加出来的虚拟BSSID就是在其对应MAC地址上进行增加。如果在一个IBSS网络（也就是Ad-hoc）模式，BSSID是一个随机值，与本地MAC地址无关。

BSSID = AP MAC Address

### BSSIDs Identify Access Points and Their Clients

Packets bound for devices within the WLAN need to go to the correct destination. The SSID keeps the packets within the correct WLAN, even when overlapping WLANs are present. However, there are usually multiple access points within each WLAN, and there has to be a way to identify those access points and their associated clients. This identifier is called a basic service set identifier (BSSID) and is included in all wireless packets.

As a user, you are usually unaware of which basic service set (BSS) you currently belong to. When you physically move your laptop from one room to another, the BSS you use can change because you moved from the area covered by one access point to the area covered by another access point, but this does not affect the connectivity of your laptop.

As an administrator, you are interested in the activity within each BSS. This tells you what areas of the network might be overloaded, and it helps you locate a particular client. By convention, an access point’s MAC address is used as the ID of a BSS (BSSID). Therefore, if you know the MAC address, you know the BSSID—and, because all packets contain the originator’s BSSID, you can trace a packet. This works fine for an access point with one radio and one WLAN configured.

Most often, there are different BSSIDs on an access point for each WLAN configured on a radio. If you have an access point with 2 radios and 32 WLANs configured on each, you would have 64 BSSIDs plus the base access point BSSID. To accommodate the multiple BSSIDs, each access point is assigned a unique block of 64 MAC addresses. Each radio has 32 MAC addresses and supports up to 32 service set identifiers (SSIDs), with one MAC address assigned to each SSID as a basic service set identification (BSSID). All MAC addresses for an access point are assigned based on the base MAC address of the access point.

> **NOTE** 
>
> The access point MAC address block is listed on a label on the back of the access point.
>
> To view a list of SSIDs for a network, look at the list of WLAN Service Profiles in Network Director.

#### Ad-Hoc Networks Do Not Have a MAC Address

Every BSS needs a BSSID, and using the access point’s MAC address works fine most of the time. However, an ad-hoc network, a network that forwards traffic from node to node, has no access point. When a BSS does not have a physical access point, in an ad-hoc network for example, the network generates a 48-bit string of numbers that looks and functions just like a MAC address, and that BSSID goes in every packet.

## ESSID - Extended Service Set IDentifier

ESSID是在漫游的时候才会出现。在无线基本架构中，存在单cell的情况，即IBSS情况，只有一个AP，并且在这个AP身上只有一个SSID。也存在扩展BSS的情况，应该就是EBSS，扩展服务集的模式。那么就有多个AP，并且这些AP身上都布置了相同的SSID，故由于每一个设备不同，这里BSSID就会不同，但是由于SSID相同，那么其还是可以进行漫游的。

### An ESS Consists of BSSs

An extended basic service set (ESS) consists of all of the BSSs in the network. For all practical purposes, the ESSID identifies the same network as the SSID does. The term SSID is used most often.

## RSSI - Received Signal Strength Indication

接收的信号强度指示。

## Reference

[Techopedia: IEEE-802.11x](https://www.techopedia.com/definition/508/ieee-80211x#:~:text=802.11x%20is%20generic%20term,or%20between%20two%20wireless%20clients.)

[Zhihu: 多个无线路由应该怎样设置WiFi 信道？](https://www.zhihu.com/question/35339958)

[Zhihu: SSID、BSSID、ESSID区别？](https://www.zhihu.com/question/24362037)

[Juniper: Understanding the Network Terms SSID, BSSID, and ESSID](https://www.juniper.net/documentation/en_US/junos-space-apps/network-director3.7/topics/concept/wireless-ssid-bssid-essid.html)



# 无线路由器加密办法

## WEP - Wired Equivalent Privacy



## WPA - Wi-Fi Protected Access



## WPA2 - Wi-Fi Protected Access version 2



## WPA3 - Wi-Fi Protected Access version 3



## Reference

[NetSpot: Wireless Security Protocols: WEP, WPA, WPA2, and WPA3](https://www.netspotapp.com/wifi-encryption-and-security.html)



# 无线密码破解

## 使用Airport开启无线网卡监听

```shell
airport en0 sniff CHANNEL
```

其中CHANNEL是你想要监听的信道，与想要破解的wifi一致。

如果手贱不小心没有退出监听就关闭Terminal，可以使用

```shell
ps -A|grep airport
```

找到进程，从大杀到小，直到恢复。

```shell
sudo kill -9 进程号
```

## 使用Aircrack-ng

### Aircrack-ng简介

Aircrack-ng是一个与802.11标准的无线网络分析有关的安全软件，主要功能有：网络侦测，数据包嗅探，WEP和WPA/WPA2-PSK破解。Aircrack-ng可以工作在任何支持监听模式的无线网卡上（设备列表请参阅其官方网站）并嗅探802.11a，802.11b，802.11g的数据。

### 安装aircrack-ng

```shell
brew install aircrack-ng
```

### 打开监听获得的cap文件

```shell
sudo aircrack-ng /tmp/airportSniff[某个自动生成的字段].cap
```

### 使用字典破解

```shell
sudo aircrack-ng -w PycharmProjects/WLAN/dict.txt -b [BSSID] /tmp/airportSniff[某个自动生成的字段].cap
```

## 使用CUPP生成字典

其实并不是很好用。