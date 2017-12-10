#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import pickle
import sqlite3
import os
import threading
import msg
import sys
import logging

#Globals
SERVER_DB_NAME = "stat.db"
SERVER_DB_CLIENTS_TABLE = "clients"
SERVER_DB_STAT_DATA_TABLE="stat_data"


SERVER_IP='127.0.0.1'
SERVER_LISTEN_PORT=1490
SERVER_ADDRESS= SERVER_IP + ':' + str(SERVER_LISTEN_PORT)
PID=os.getpid()
MAX_CLIENTS = 10

CLIENTS_LIST=list() 
sqlite3.apilevel 
server_sock=socket.socket()


def init_sql():
    try:
        logger.info("Initialization SQL")
        conn_db=sqlite3.connect(SERVER_DB_NAME)
        cur=conn_db.cursor() 
        cur.execute("DROP TABLE IF EXISTS " + SERVER_DB_CLIENTS_TABLE)
        cur.execute("CREATE TABLE " + SERVER_DB_CLIENTS_TABLE + " (client_id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, port INTEGER)")

        cur.execute("DROP TABLE IF EXISTS " + SERVER_DB_STAT_DATA_TABLE)
        cur.execute("CREATE TABLE " + SERVER_DB_STAT_DATA_TABLE +
            " (client_id INTEGER, stat_time INTEGER, user_cpu INTEGER, system_cpu INTEGER, \
            idle_cpu INTEGER, total_memory INTEGER, \
            available_memory INTEGER, used_memory INTEGER, \
            total_d_u INTEGER, used_d_u INTEGER, free_d_u INTEGER, \
            CONSTRAINT client_id FOREIGN KEY(client_id) REFERENCES SERVER_DB_CLIENTS_TABLE(client_id) )") 
        logger.info("Create SQL name: stat.db, tables: clients, stat_data")
    except sqlite3.DatabaseError as err:
        print("init_sql(): DB creation FAIL (%s):" % err.args[0])
        if conn_db:
            conn_db.rollback()
            sys.exit(1)        
    finally:
        logger.info("init_sql(): DB is initialized OK...")
        print("init_sql(): DB is initialized OK...")
        conn_db.commit()


def init_comm_thread():
    thr = threading.Thread(target=server_comm)
    thr.start()
    print("init_comm_thread(): communication thread is created OK...")
    return thr

def init_server_socket():
    server_sock.bind((SERVER_IP,SERVER_LISTEN_PORT))
    server_sock.listen(MAX_CLIENTS)
    print("init_socket(): server socket is initialized OK...")
    logger.info("init_socket(): server socket is initialized OK...")


def server_comm():
    init_server_socket()
    while 1:
        client_sock, client_addr = server_sock.accept()
        print("server_comm(): new connection accepted. Client Addr="+str(client_addr))
        logger.info("server_comm(): new connection accepted. Client Addr="+str(client_addr))
        rcv_data = client_sock.recv(1024)
        process_data(rcv_data, client_sock,client_addr)

 
def process_data(data, client_sock,client_addr):
    try:
        rcv_msg = msg.MSG()
        rcv_msg.deserialize(data)

        req_result = msg.MSG_RESULT_ERROR

        if rcv_msg.msg_type == msg.MSG_TYPE_REGESTERING_REQUEST:
            print("Server():process_data(): received MSG_TYPE_REGESTERING_REQUEST")
            logger.info("Server():process_data(): received MSG_TYPE_REGESTERING_REQUEST")
            #TODO:add client registration logic here
            #add client to db 
            conn_db=sqlite3.connect(SERVER_DB_NAME)
            cur=conn_db.cursor() 
            t1=(rcv_msg.data,client_addr[0],client_addr[1])
            sql_list_clients= "INSERT INTO " + SERVER_DB_CLIENTS_TABLE + " VALUES(?,?,?)" 
            cur.execute(sql_list_clients,t1)
            conn_db.commit()
            req_result = msg.MSG_RESULT_OK

            reg_resp=msg.MSG()
            reg_resp.msg_type = msg.MSG_TYPE_REGESTERING_RESPONSE
            reg_resp.data=req_result
            client_sock.send(reg_resp.serialize())
            print("Server():process_data(): sent MSG_TYPE_REGESTERING_RESPONSE with code=" + str(req_result))
            logger.info("Server():process_data(): sent MSG_TYPE_REGESTERING_RESPONSE with code=" + str(req_result))
        
        elif rcv_msg.msg_type == msg.MSG_TYPE_STATATISTIC_DATA:
            print("Server():process_data(): received MSG_TYPE_STATATISTIC_DATA")
            logger.info("Server():process_data(): received MSG_TYPE_STATATISTIC_DATA")
            #TODO:add statistic data handling here
            conn_db=sqlite3.connect(SERVER_DB_NAME)
            cur=conn_db.cursor() 
            t2=(rcv_msg.data.client_id, rcv_msg.data.stat_time,rcv_msg.data.user_cpu,rcv_msg.data.system_cpu,
                rcv_msg.data.idle_cpu, rcv_msg.data.total_memory,rcv_msg.data.available_memory,
                rcv_msg.data.used_memory,rcv_msg.data.total_d_u, rcv_msg.data.used_d_u, rcv_msg.data.free_d_u)
            sql_list_stat= "INSERT INTO " + SERVER_DB_STAT_DATA_TABLE + " VALUES(?,?,?,?,?,?,?,?,?,?,?)" 
            cur.execute(sql_list_stat,t2)
            conn_db.commit()
            req_result = msg.MSG_RESULT_OK
        else:
            print("Server():process_data(): received unexpected type=", rcv_msg.msg_type)
    finally: 
        print("parse_data(): Finally server")
        logger.info("parse_data(): Finally server")

#MAIN THREAD
logger = logging.getLogger("logg")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logg1.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
init_sql()
comm_thr = init_comm_thread()
comm_thr.join()
