import socket
import struct
 
 
def createWolPackage(wake_mac:str):
    wake_mac_list = wake_mac.split(":")
    mac = struct.pack("BBBBBB", *[int(wake_mac_list[i],16) for i in range(6)]) # 将mac地址转二进制
    broadcast_mac = b"\xff"*6 # 生成6字节的FF

    wol = broadcast_mac+mac*16 #将6字节FF与目标mac的16次进行合并得到wol幻数据包
    return wol

def sendWolPackage(wake_mac:str,wake_ip:str="255.255.255.255"):
    sockets = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sockets.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #设置广播
    sockets.sendto(createWolPackage(wake_mac), (wake_ip, 8))
