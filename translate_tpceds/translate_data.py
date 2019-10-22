# -*- conding:utf_8 -*-
import json
import numpy as np

class Formate_tpceds_data(object):
    '''
    为了用新版本的tpcds产生的数据，去去生成tpcds的报告，
    需要将其整容成 老板本的数据模板的样子
    '''
    def __init__(self, tpcds_oldPath,tpcds_newPath):
        with open(tpcds_oldPath, 'r') as f:
            self.tpcds_old = json.loads(f.read())
    
        with open(tpcds_newPath,'r') as f:
            self.tpcds_new = json.loads(f.read())

    def calc_second(self, secondFormat):
        '''
        example: 
            convert 0:1:1 to 61 
        '''
        secondList = secondFormat.split(':')
        second_sum = int(secondList[0]) * 3600
        second_sum += int(secondList[1]) * 60
        second_sum += int(secondList[2])
        return str(second_sum)

    def add_secondFormat(self, secondFormat1, secondFormat2):
        '''
        example:
            add 2:1:0 and 0:0:1
            get 2:1:1:
        '''
        secondList1 = secondFormat1.split(':')
        secondList2 = secondFormat2.split(':')
        hour = int(secondList1[0]) + int(secondList2[0])
        minute = int(secondList1[1]) + int(secondList2[1])
        second = int(secondList1[2]) + int(secondList2[2])
        if second >= 60:
            second -= 60
            minute += 1
        if minute >= 60:
            minute -= 60
            hour += 60
        secondFormat = "%d:%d:%d" % (hour, minute, second)
        return secondFormat

    def CalQuantile(self, timeList, quan):
        '''
        计算 TILE25 和 TILE75
        参数说明： timeList 是每组测试中的时间的列表
                  quan     是权重 75 对应 TILE75、 25 对应 TILE25
        '''
        if len(timeList) < 1:
            return -1
        timeList.sort()
        dQuantile = -1.0
        dQ = 0.0
        iIndex = 0

        if quan == 25:
            dQ = (len(timeList) + 1) / 4.0
            iIndex = int(dQ)
            if dQ - iIndex == 0:
                dQuantile = timeList[iIndex - 1]
            else:
                dQuantile = timeList[iIndex - 1] * 0.25 + timeList[iIndex] * 0.75                

        elif quan == 75:
            dQ = 3 * ((len(timeList) + 1) / 4.0)
            iIndex = int(dQ)
            if dQ - iIndex == 0:
                dQuantile = timeList[iIndex - 1]
            else:
                dQuantile = timeList[iIndex - 1] * 0.75 + timeList[iIndex] * 0.25

        return dQuantile

    def TABLE1_formate(self):
        '''
        create TABLE1 from new tpcds_data
        '''
        translate = [
        ['Power', 'PowerTest'],
        ['Thruput_1', 'ThroughputRun1'],
        ['Thruput_2', 'ThroughputRun2'],
        ]
        for index in range(3):
            self.tpcds_old['result']['TABLE1'][index]['TEST'] = translate[index][0]
            self.tpcds_old['result']['TABLE1'][index]['START'] = self.tpcds_new[translate[index][1]]['startTimeFormat']
            self.tpcds_old['result']['TABLE1'][index]['END'] = self.tpcds_new[translate[index][1]]['endTimeFormat']
            self.tpcds_old['result']['TABLE1'][index]['SECOND'] = self.calc_second(self.tpcds_new[translate[index][1]]['secondFormat'])
            self.tpcds_old['result']['TABLE1'][index]['FMT_TIME'] = self.tpcds_new[translate[index][1]]['secondFormat']

        self.tpcds_old['result']['TABLE1'][3]['TEST'] = 'DM_1'
        self.tpcds_old['result']['TABLE1'][3]['START'] = self.tpcds_new['DataMaintenance1']['startTimeFormat']
        self.tpcds_old['result']['TABLE1'][3]['END'] = self.tpcds_new['DataMaintenance2']['endTimeFormat']
        self.tpcds_old['result']['TABLE1'][3]['SECOND'] = self.calc_second(self.tpcds_new['DataMaintenance1']['secondFormat']) + self.calc_second(self.tpcds_new['DataMaintenance2']['secondFormat'])
        self.tpcds_old['result']['TABLE1'][3]['FMT_TIME'] = self.add_secondFormat(self.tpcds_new['DataMaintenance1']['secondFormat'], self.tpcds_new['DataMaintenance2']['secondFormat'])

        self.tpcds_old['result']['TABLE1'][4]['TEST'] = 'DM_2'
        self.tpcds_old['result']['TABLE1'][4]['START'] = self.tpcds_new['DataMaintenance3']['startTimeFormat']
        self.tpcds_old['result']['TABLE1'][4]['END'] = self.tpcds_new['DataMaintenance4']['endTimeFormat']
        self.tpcds_old['result']['TABLE1'][4]['SECOND'] = self.calc_second(self.tpcds_new['DataMaintenance3']['secondFormat']) + self.calc_second(self.tpcds_new['DataMaintenance4']['secondFormat'])
        self.tpcds_old['result']['TABLE1'][4]['FMT_TIME'] = self.add_secondFormat(self.tpcds_new['DataMaintenance4']['secondFormat'], self.tpcds_new['DataMaintenance3']['secondFormat'])

        out = json.dumps(self.tpcds_old['result']['TABLE1'], indent=4)
        print(out,'TABLE1')

    def TABLE2_formate(self):
        '''
        create TABLE2 from new tpcds_data
        '''
        self.tpcds_old['result']['TABLE2'][0]['STREAM'] = 'Pt-0'
        self.tpcds_old['result']['TABLE2'][0]['SECOND'] = self.calc_second(self.tpcds_new['PowerTest']['secondFormat'])
        self.tpcds_old['result']['TABLE2'][0]['START'] = self.tpcds_new['PowerTest']['startTimeFormat']
        self.tpcds_old['result']['TABLE2'][0]['END'] = self.tpcds_new['PowerTest']['endTimeFormat']
        self.tpcds_old['result']['TABLE2'][0]['FMT_TIME'] = self.tpcds_new['PowerTest']['secondFormat']

        for i in range(1,9):
            if i <= 4:
                throughputRun = 'ThroughputRun1'
            elif i >= 5 :
                throughputRun = 'ThroughputRun2'

            query = 'query_%d.sql' % i 
            self.tpcds_old['result']['TABLE2'][i]['STREAM'] = throughputRun
            self.tpcds_old['result']['TABLE2'][i]['SECOND'] = self.calc_second(self.tpcds_new[throughputRun][query]['secondFormat'])
            self.tpcds_old['result']['TABLE2'][i]['START'] = self.tpcds_new[throughputRun][query]['startTimeFormat']
            self.tpcds_old['result']['TABLE2'][i]['END'] = self.tpcds_new[throughputRun][query]['endTimeFormat']
            self.tpcds_old['result']['TABLE2'][i]['FMT_TIME'] = self.tpcds_new[throughputRun][query]['secondFormat']

        for i in range(9,13):
            DataMaintenance = 'DataMaintenance%d' % (i - 8)

            self.tpcds_old['result']['TABLE2'][i]['STREAM'] = DataMaintenance
            self.tpcds_old['result']['TABLE2'][i]['SECOND'] = self.calc_second(self.tpcds_new[DataMaintenance]['secondFormat'])
            self.tpcds_old['result']['TABLE2'][i]['START'] = self.tpcds_new[throughputRun]['startTimeFormat']
            self.tpcds_old['result']['TABLE2'][i]['END'] = self.tpcds_new[throughputRun]['endTimeFormat']
            self.tpcds_old['result']['TABLE2'][i]['FMT_TIME'] = self.tpcds_new[throughputRun]['secondFormat']
        out = json.dumps(self.tpcds_old['result']['TABLE2'], indent=4)
        print(out)

    def TABLE3_formate(self):
        '''
        create TABLE3 from new tpcds_data
        '''
        for i in range(99):
            self.tpcds_old['result']['TABLE3'][i]['QUERY'] = str(i + 1)
            self.tpcds_old['result']['TABLE3'][i]['STREAM0'] = self.tpcds_new['PowerTest']['sqls'][i]['second']

            self.tpcds_old['result']['TABLE3'][i]['STREAM1'] = str(self.tpcds_new['ThroughputRun1']['query_1.sql']['sqls'][i]['second'])
            self.tpcds_old['result']['TABLE3'][i]['STREAM2'] = str(self.tpcds_new['ThroughputRun1']['query_2.sql']['sqls'][i]['second'])
            self.tpcds_old['result']['TABLE3'][i]['STREAM3'] = str(self.tpcds_new['ThroughputRun1']['query_3.sql']['sqls'][i]['second'])
            self.tpcds_old['result']['TABLE3'][i]['STREAM4'] = str(self.tpcds_new['ThroughputRun1']['query_4.sql']['sqls'][i]['second'])
            streams_1 = [float(self.tpcds_old['result']['TABLE3'][i]['STREAM1']),
                        float(self.tpcds_old['result']['TABLE3'][i]['STREAM2']),
                        float(self.tpcds_old['result']['TABLE3'][i]['STREAM3']),
                        float(self.tpcds_old['result']['TABLE3'][i]['STREAM4'])]
            self.tpcds_old['result']['TABLE3'][i]['MAX'] = str(max(streams_1))
            self.tpcds_old['result']['TABLE3'][i]['MIN'] = str(min(streams_1))
            self.tpcds_old['result']['TABLE3'][i]['MEDIAN'] = str(np.median(streams_1))
            self.tpcds_old['result']['TABLE3'][i]['TILE25'] = self.CalQuantile(streams_1, 25)
            self.tpcds_old['result']['TABLE3'][i]['TILE75'] = self.CalQuantile(streams_1, 75)

            self.tpcds_old['result']['TABLE3'][i]['STREAM4'] = self.tpcds_new['ThroughputRun2']['query_5.sql']['sqls'][i]['second']
            self.tpcds_old['result']['TABLE3'][i]['STREAM6'] = self.tpcds_new['ThroughputRun2']['query_6.sql']['sqls'][i]['second']
            self.tpcds_old['result']['TABLE3'][i]['STREAM7'] = self.tpcds_new['ThroughputRun2']['query_7.sql']['sqls'][i]['second']
            self.tpcds_old['result']['TABLE3'][i]['STREAM8'] = self.tpcds_new['ThroughputRun2']['query_8.sql']['sqls'][i]['second']
            streams_2 = [float(self.tpcds_old['result']['TABLE3'][i]['STREAM5']),
                        float(self.tpcds_old['result']['TABLE3'][i]['STREAM6']),
                        float(self.tpcds_old['result']['TABLE3'][i]['STREAM7']),
                        float(self.tpcds_old['result']['TABLE3'][i]['STREAM8'])]
            self.tpcds_old['result']['TABLE3'][i]['MAX_2'] = str(max(streams_2))
            self.tpcds_old['result']['TABLE3'][i]['MIN_2'] = str(min(streams_2))
            self.tpcds_old['result']['TABLE3'][i]['MEDIAN_2'] = str(np.median(streams_2))
            self.tpcds_old['result']['TABLE3'][i]['TILE25_2'] = self.CalQuantile(streams_2, 25)
            self.tpcds_old['result']['TABLE3'][i]['TILE75_2'] = self.CalQuantile(streams_2, 75)

        out = json.dumps(self.tpcds_old['result']['TABLE3'], indent=4)
        print(out)

    def TABLE4_formate(self):
        '''
        create TABLE4 from new tpcds_data
        '''
        for i in range(11):
            self.tpcds_old['result']['TABLE4'][i]['RUN1'] = str(self.tpcds_new['DataMaintenance1']['sqls'][i]['second'])
            self.tpcds_old['result']['TABLE4'][i]['RUN2'] = str(self.tpcds_new['DataMaintenance2']['sqls'][i]['second'])
            self.tpcds_old['result']['TABLE4'][i]['RUN3'] = str(self.tpcds_new['DataMaintenance3']['sqls'][i]['second'])
            self.tpcds_old['result']['TABLE4'][i]['RUN4'] = str(self.tpcds_new['DataMaintenance4']['sqls'][i]['second'])
            streams = [float(self.tpcds_old['result']['TABLE4'][i]['RUN1']),
                        float(self.tpcds_old['result']['TABLE4'][i]['RUN2']),
                        float(self.tpcds_old['result']['TABLE4'][i]['RUN3']),
                        float(self.tpcds_old['result']['TABLE4'][i]['RUN4'])]
            self.tpcds_old['result']['TABLE4'][i]['MIN'] = str(min(streams))
            self.tpcds_old['result']['TABLE4'][i]['MAX'] = str(max(streams))
            self.tpcds_old['result']['TABLE4'][i]['MEDIAN'] = str(np.median(streams))
            self.tpcds_old['result']['TABLE4'][i]['DMFX'] = self.tpcds_new['DataMaintenance1']['sqls'][i]['filename'][:-4]
            self.tpcds_old['result']['TABLE4'][i]['TILE25'] = self.CalQuantile(streams, 25)
            self.tpcds_old['result']['TABLE4'][i]['TILE75'] = self.CalQuantile(streams, 75)
        out = json.dumps(self.tpcds_old['result']['TABLE4'], indent=4)
        print(out)


if __name__ == '__main__':
    tpcds_oldPath = 'oldreport/tpcds_result_old.json'
    tpcds_newPath = 'oldreport/tpcds_result_14.json'
    formate = Formate_tpceds_data(tpcds_oldPath, tpcds_newPath)
    formate.TABLE4_formate()






