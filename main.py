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
    mes = read_excel.get_measurement("/Users/k2data/Desktop/env.xlsx")
    for l in range(0,len(host_list)):
        mes_list = mes.get(host_list[l])
        for m in range(0,len(mes_list)):
            n = 0
            w = 0
            u = 0

            warning_n = read_excel.get_threshold("/Users/k2data/Desktop/env.xlsx").get(mes_list[m])[0]
            unusual_n = read_excel.get_threshold("/Users/k2data/Desktop/env.xlsx").get(mes_list[m])[1]
            if result.get(host_list[l]).get(mes_list[m]) is not None:
                value = results.get(host_list[l]).get(mes_list[m])[0].get('value')
            else:
                value = None
            if value < warning_n and value is not None:
                n += 1
            if value >= warning_n and value < unusual_n:
                w += 1
            if value >= unusual_n and value is None:
                u += 1
        if u != 0:
            global unusual
            unusual += 1
        if u == 0 & w != 0:
            global warning
            warning += 1
        else:
            global normal
            normal += 1
    return
def insert():
    end_table = {"normal": normal, "warning": warning, "unusual": unusual}
    for table, len_table in end_table.items():
        insert_sql = [{
            "measurement": table,
            "tags": {"status": table},
            "fields": {"value": len_table * 1.0},
            "time": stop_time}]
        print insert_sql
        client.write_points(insert_sql)
    return
if __name__ == '__main__':

    start_time = int((int(time.time()) - 60 * 1000) * 10 ** 9)
    stop_time = int(int(time.time()) * 10 ** 9)
    result = search(read_excel.get_env("/Users/k2data/Desktop/env.xlsx"),start_time,stop_time)
    judge_result(result)
    print normal
    print warning
    print unusual






