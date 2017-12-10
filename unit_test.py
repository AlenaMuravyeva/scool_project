import unittest
import mock
import client 
import server
import msg
import psutil
import uiserver2
import time
import sqlite3

SERVER_DB_NAME = "stat.db"
SERVER_DB_CLIENTS_TABLE = "clients"
SERVER_DB_STAT_DATA_TABLE="stat_data"


class Test(unittest.TestCase):
    def setUp(self):
        print('start')

    def test_serialization_desrialization(self):
        m = msg.MSG()
        test_str = "Hello World!!!"
        m.data = test_str
        ser_data = m.serialize()
        m.deserialize(ser_data)

        self.assertEqual(test_str, m.data)

    def test_db(self):
        server.init_sql()

        stat_data=msg.STAT()
        stat_data.client_id=1111
        stat_data.stat_time=int(time.time())

        max_records = 10

        for i in range(1,max_records + 1):
            all_data_cpu=psutil.cpu_times_percent()
            all_data_memory=psutil.virtual_memory()
            all_data_d_usage=psutil.disk_usage('/')

            stat_data.stat_time = stat_data.stat_time + 1
            stat_data.user_cpu=all_data_cpu[0]
            stat_data.system_cpu=all_data_cpu[2]
            stat_data.idle_cpu=all_data_cpu[3]
            stat_data.total_memory=all_data_memory[0] / 1024 / 1024 #Mb
            stat_data.available_memory=all_data_memory[1] / 1024 / 1024 #Mb
            stat_data.used_memory=all_data_memory[3] / 1024 / 1024 #Mb
            stat_data.total_d_u=all_data_d_usage[0] / 1024 / 1024 #Mb
            stat_data.used_d_u=all_data_d_usage[1] / 1024 / 1024 #Mb
            stat_data.free_d_u=all_data_d_usage[2] / 1024 / 1024 #Mb

            conn_db=sqlite3.connect(SERVER_DB_NAME)
            cur=conn_db.cursor() 
            t2=(stat_data.client_id, stat_data.stat_time, stat_data.user_cpu, stat_data.system_cpu,
                stat_data.idle_cpu, stat_data.total_memory, stat_data.available_memory,
                stat_data.used_memory, stat_data.total_d_u, stat_data.used_d_u, stat_data.free_d_u)
            sql_list_stat= "INSERT INTO " + SERVER_DB_STAT_DATA_TABLE + " VALUES(?,?,?,?,?,?,?,?,?,?,?)" 
            cur.execute(sql_list_stat,t2)
            conn_db.commit()

            print("sql record {} committed for time {}".format(i, stat_data.stat_time))

        xmin = 0
        xmax = max_records

        cur_time = int(time.time())
        xmax_time_back = cur_time - 0
        xmin_time_back = cur_time + xmax

        print("Times: xmax_time_back={}, xmin_time_back={}".format(xmax_time_back, xmin_time_back))

        ui = uiserver2.Ui_Form()

        #def fetch_range_time_data_from_db (self, xmin_time_back, xmax_time_back, cl_id):
        records = ui.fetch_range_time_data_from_db(xmin_time_back, xmax_time_back, str(stat_data.client_id))

        self.assertEqual(len(records), max_records)



        

        
test_cl = Test()

if __name__ =="__main__":
    unittest.main()
