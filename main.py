from influxdb import InfluxDBClient
import os
import read_excel
import time

host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
database = os.environ.get('DATABASE')
client = InfluxDBClient('192.168.131.3', '8086', 'root', '', 'opentsdb')

normal = 0
warning = 0
unusual = 0

def search(condition,starttime,endtime):

    results = {}
    for h, cond in condition.items():
        result = {}
        for measure,formula in cond.items():
            sql = 'select %s as value from "%s" where time > %s and time < %s and \"host\" = \'%s\''%(formula,measure,starttime,endtime,h)
           # print sql
            rs = client.query(sql)
            result[measure] = list(rs.get_points(measurement=measure))
            #print result
        results[h] = result
    #print results
    return results

def judge_result(results):

    host_list = read_excel.get_host("/Users/k2data/Desktop/env.xlsx")
    mes_list = read_excel.get_measurement("/Users/k2data/Desktop/env.xlsx")
    for l in range(0,len(host_list)):
        for m in rang(0,len(mes_list)):
            n = 0
            w = 0
            u = 0
            warning,unusual = read_excel.get_threshold("/Users/k2data/Desktop/env.xlsx").get(mes_list[m])
            value = results.get(host_list(l)).get(mes_list[m])
            if value < warning & value is not None:
                n += 1
            if value >= warning & value < u:
                w += 1
            if value >= u & value is None:
                u += 1
        if u != 0:
            unusual += 1
        if u == 0 & w != 0:
            warning += 1
        else:
            normal += 1
if __name__ == '__main__':

    start_time = int((int(time.time()) - 60 * 1000) * 10 ** 9)
    stop_time = int(int(time.time()) * 10 ** 9)
    search(read_excel.get_env("/Users/k2data/Desktop/env.xlsx"),start_time,stop_time)







