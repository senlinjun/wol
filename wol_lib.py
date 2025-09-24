import socket
import struct
 
class WOL_SEND():
    def __init__(self,wake_ip,wake_mac):
        self.wake_ip  = wake_ip
        self.wake_mac = wake_mac
 
    def create_wol_package(self):
        wake_mac_list = self.wake_mac.split(":")
        print(wake_mac_list)
        mac = struct.pack("BBBBBB", *[int(wake_mac_list[i],16) for i in range(6)]) # 将mac地址转二进制
        broadcast_mac = b"\xff"*6 # 生成6字节的FF
 
        wol = broadcast_mac+mac*16 #将6字节FF与目标mac的16次进行合并得到wol幻数据包
        return wol
 
    def send_wol_package(self):
        sockets = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sockets.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #设置广播
        sockets.sendto(self.create_wol_package(), (self.wake_ip, 8))
