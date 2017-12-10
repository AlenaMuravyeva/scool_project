import pickle

MSG_TYPE_UNKNOWN = 0
MSG_TYPE_REGESTERING_REQUEST = 1
MSG_TYPE_REGESTERING_RESPONSE = 2
MSG_TYPE_STATATISTIC_DATA = 3

MSG_RESULT_OK = 200
MSG_RESULT_ERROR = 300

class MSG():
    def __init__(self):
        self.msg_type = MSG_TYPE_UNKNOWN
        self.data = ''

    def serialize(self):
        byte_stream = pickle.dumps(self)
        print("MSG::serialize(): serialized string=" + str(byte_stream))
        return byte_stream

    def deserialize(self, ser_data):
        msg_obj = pickle.loads(ser_data)
        self.msg_type=msg_obj.msg_type
        self.data=msg_obj.data
        print("MSG::deserialize(): MSG type=" + str(self.msg_type) + " deserialized data=" + str(self.data))


class STAT():

    def __init__(self):
        self.client_id=0
        self.stat_time=0
        self.user_cpu=0
        self.system_cpu=0
        self.idle_cpu=0
        self.total_memory=0
        self.available_memory=0
        self.used_memory=0
        self.total_d_u=0
        self.used_d_u=0
        self.free_d_u=0

    