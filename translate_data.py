import json

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
            add 2:1:0 and  0:0:1
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
            self.tpcds_old['result']['TABLE1'][index]['END'] = self.tpcds_new[translate[0][1]]['endTimeFormat']
            self.tpcds_old['result']['TABLE1'][index]['SECOND'] = self.calc_second(self.tpcds_new[translate[0][1]]['secondFormat'])
            self.tpcds_old['result']['TABLE1'][index]['FMT_TIME'] = self.tpcds_new[translate[0][1]]['secondFormat']

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
        pass


    def TABLE4_formate(self):
        '''
        create TABLE4 from new tpcds_data
        '''
        pass

if __name__ == '__main__':
    tpcds_oldPath = 'oldreport/tpcds_result_old.json'
    tpcds_newPath = 'oldreport/tpcds_result_14.json'
    formate = Formate_tpceds_data(tpcds_oldPath, tpcds_newPath)
    formate.TABLE1_formate()




