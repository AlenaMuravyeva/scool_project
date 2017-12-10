import socket
import psutil
import re
import pickle
import time
import os
import msg

SERVER_IP='127.0.0.1'
SERVER_LISTEN_PORT=1490
STATISTIC_DATA_SEND_PAUSE = 1
REGISTRATION_RESEND_PAUSE = 5
REG_STATE_UNREGIESTERED = 0
REG_STATE_REGISTERED = 1

class Client():

    def __init__(self, server_port):
        self.server_port=server_port
        self.server_ip=SERVER_IP
        self.proc_id=str(os.getpid())
        self.reg_state = REG_STATE_UNREGIESTERED

    def process_data(self, data):
        rcv_msg = msg.MSG()
        rcv_msg.deserialize(data)

        if rcv_msg.msg_type == msg.MSG_TYPE_REGESTERING_RESPONSE:
            print("Client():process_data(): received MSG_TYPE_REGESTERING_RESPONSE")

            if rcv_msg.data == msg.MSG_RESULT_OK:
                self.reg_state = REG_STATE_REGISTERED
                print("Client():process_data(): Client successfully registered to server. pid=" + str(self.proc_id))

    def send_statistic(self):
        all_data_cpu=psutil.cpu_times_percent()
        all_data_memory=psutil.virtual_memory()
        all_data_d_usage=psutil.disk_usage('/')

        stat_data=msg.STAT()
        stat_data.client_id=self.proc_id
        stat_data.stat_time=int(time.time())
        stat_data.user_cpu=all_data_cpu[0]
        stat_data.system_cpu=all_data_cpu[2]
        stat_data.idle_cpu=all_data_cpu[3]
        stat_data.total_memory=all_data_memory[0] / 1024 / 1024 #Mb
        stat_data.available_memory=all_data_memory[1] / 1024 / 1024 #Mb
        stat_data.used_memory=all_data_memory[3] / 1024 / 1024 #Mb
        stat_data.total_d_u=all_data_d_usage[0] / 1024 / 1024 #Mb
        stat_data.used_d_u=all_data_d_usage[1] / 1024 / 1024 #Mb
        stat_data.free_d_u=all_data_d_usage[2] / 1024 / 1024 #Mb
        
        msg_stat=msg.MSG()
        msg_stat.data=stat_data
        msg_stat.msg_type = msg.MSG_TYPE_STATATISTIC_DATA
        byte_stream = msg_stat.serialize()
        time.sleep(STATISTIC_DATA_SEND_PAUSE)

        self.client_sock=socket.socket()
        self.client_sock.connect((self.server_ip,self.server_port))
        self.client_sock.send(byte_stream)
        self.client_sock.close()

    
    def connection(self):
        self.client_sock=socket.socket()
        self.client_sock.connect((self.server_ip,self.server_port))

        reg_req=msg.MSG()
        reg_req.msg_type = msg.MSG_TYPE_REGESTERING_REQUEST
        reg_req.data=self.proc_id
        reg_send_byte_stream = reg_req.serialize()

        while(self.reg_state == REG_STATE_UNREGIESTERED):
            time.sleep(REGISTRATION_RESEND_PAUSE)
            self.client_sock.send(reg_send_byte_stream)
            print("Client():connection(): requested registration. pid =" + str(self.proc_id))
            rcv_data = self.client_sock.recv(1024)
            print("Client():connection(): received data=" + str(rcv_data))
            self.process_data(rcv_data)
            self.client_sock.close()

        while 1: 
            try:
                print("Client():connection(): before send_statistic()")
                self.send_statistic()
                time.sleep(STATISTIC_DATA_SEND_PAUSE)
            except Exception as e:
                print ("Client():connection(): ERROR send data: " + str(e))
            finally: print("Client():connection(): finally ok")


# MAIN THREAD
client1=Client(SERVER_LISTEN_PORT)
client1.connection()


