import requests
import time
import csv
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from UI import Ui_MainWindow

'''
url = "https://fsis.thu.edu.tw/wwwstud/COURSE/05_deptopServer.php"
i_year = ""
i_term = ""
i_week = ""
i_dsep = ""
i_majr = ""
i_stype = ""
i_teac = ""
i_cour = ""
data = {'i_year':i_year,
        'i_term':i_term,
        'i_week':i_week,
        'i_dsep':i_dsep,
        'i_majr':i_majr,
        'i_stype':i_stype,
        'i_teac':i_teac,
        'i_cour':i_cour
        }
'''
d_terms = {'第一學期':'1','第二學期':'2','暑修上期':'3','暑修下期':'4'}
d_majrs = {'文學院':'100','中文系':'110','中文在職專班':'117','外文系':'120','外文系教學組':'121','外文系文學組':'122','歷史系':'130','華語教學碩士學程':'140','日文系':'150','宗教研究所':'180','哲學系':'190','哲學在職專班':'197',
           '理學院':'200','應物系':'210','應物系材料組':'211','應物系光電組':'212','化學系':'220','化學系化學組':'221','化學系化生組':'222','生科系':'230','生科系生醫組':'231','生科系生態組':'232','應數系':'240','生醫材料博士學程':'250','生物多樣性博士學程':'260',
           '工學院':'300','化材系':'310','工工系':'330','工工在職專班':'337','環工系':'340','資工系':'350','資工系資電組':'351','資工系數創組':'352','資工系軟工組':'253','資訊在職專班':'357','資碩專大數據物聯網':'358','資碩專高階資訊經營':'359','電機系':'360','電機系IC通訊組':'361','電機系奈米能源組':'362','數創碩士學位學程':'370',
           '管理學院':'400','企管系':'410','高階企業經營專班':'417','國貿系':'420','會計系':'430','財金系':'440','統計系':'470','資管系':'490',
           '社科院':'500','經濟系':'520','政治系':'530','行政系':'540','社會系':'550','社工系':'560',
           '農學院':'600','畜產系':'610','食科系':'620','餐旅系':'660','健康與運動學程':'680',
           '創意學院':'700','美術系':'710','音樂系':'720','建築系':'730','工設系':'740','景觀系':'750',
           '法學院':'800','法律系':'810',
           '國際學院':'900','國經學程':'910','永續學程':'920','國際學院不分系':'930',
           '雲創學院':'A00',
           '通識人文':'S01','通識自然':'S02','通識社會':'S03','多元學習(共選修)':'S04','遠距教學':'S05','第二外國語':'S06','師資中心':'S07','日文課程':'S08','軍訓一':'S18','護理一':'S19','軍訓二':'S20','中文課程':'S25','歷史課程':'S26','大一英文':'S27','體育選修課程':'S34','選修英文':'S36','通識文明與經典':'S38','大二英文':'S39','通識領導與倫理':'S40','AI思維與程式設計':'S43','通識議題導向領域':'S44','大一大二體育':'S61','暑修':'S68','英文畢業門檻替代課程':'engsub'}
d_stypes = {'日間學士班':'A','進修學士班':'E','研究所':'F'}


'''
def getdata(i_year,i_term,i_week,i_dsep,i_majr,i_stype,i_teac,i_cour):
    html = requests.post(url,data)
    sp = BeautifulSoup(html.text,'lxml')
    courses = sp.find_all('td')
    
    onlygrade = []
    choosecode_name = []
    teacher = []
    grade = []
    haveto = []
    point = []
    day = []
    option = []
    classcode = []
    index = 0
    cd = ['一','二','三','四','五','六','七']
    for course in courses:
        if index%9==0 and int(index/9)!=0:
            onlygrade.append(course.text)
        if index%9==1 and int(index/9)!=0:
            choosecode_name.append(course.text.split('&nbsp')[0].split(' ')[-1]+course.text.split('&nbsp')[1])
            #print(course.text.split('&nbsp')[0].split(' ')[-1]+course.text.split('&nbsp')[1])
        if index%9==2 and int(index/9)!=0:
            teacher.append(course.text)
        if index%9==3 and int(index/9)!=0:
            grade.append(course.text)
        if index%9==4 and int(index/9)!=0:
            haveto.append(course.text)
        if index%9==5 and int(index/9)!=0:
            point.append(course.text)
        if index%9==6 and int(index/9)!=0:
            day_text = course.text.split(',')
            day_list = []
            now = ""
            for dat in day_text:
                if dat=="":
                    day_list.append("")
                elif dat[0] in cd:
                    if '[' not in dat:
                        day_list.append(dat[0]+dat[2:])
                    else :
                        day_list.append(dat[0]+dat[2:].split('[')[0])
                    now = dat[0]
                else:
                    if '[' not in dat:
                        day_list.append(now+dat)
                    else:
                        day_list.append(now+dat.split('[')[0])
            day.append(day_list)
        if index%9==7 and int(index/9)!=0:
            option.append(course.text)
        if index%9==8 and int(index/9)!=0:
            classcode.append(course.text)
        index += 1
    for i in range(len(onlygrade)):
        print(onlygrade[i])
        print(choosecode_name[i])
        print(teacher[i])
        print(grade[i])
        print(haveto[i])
        print(point[i])
        print(day[i])
        print(option[i])
        print(classcode[i])
    return onlygrade,choosecode_name,teacher,grade,haveto,point,day,option,classcode
'''
'''
class ThreadTask(QThread):
        T_onlygrade = pyqtSignal(list)
        T_choosecode_name = pyqtSignal(list)
        T_teacher = pyqtSignal(list)
        T_grade = pyqtSignal(list)
        T_haveto = pyqtSignal(list)
        T_point = pyqtSignal(list)
        T_day = pyqtSignal(list)
        T_option = pyqtSignal(list)
        T_classcode = pyqtSignal(list)

        def crawler(self):
            onlygrade,choosecode_name,teacher,grade,haveto,point,day,option,classcode = getdata()
            self.T_choosecode_name.emit(choosecode_name)
'''

        

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        

    def setup_control(self):
        self.onlygrade = []
        self.choosecode_name = []
        self.teacher = []
        self.grade = []
        self.haveto = []
        self.point = []
        self.day = []
        self.option = []
        self.classcode = []
        years = self.get_year()
        self.ui.years.addItems(years)
        terms = ['第一學期','第二學期','暑修上期','暑修下期']
        self.ui.term.addItems(terms)
        majrs = ['文學院', '中文系', '中文在職專班', '外文系', '外文系教學組', '外文系文學組', '歷史系', '華語教學碩士學程', '日文系', '宗教研究所', '哲學系', '哲學在職專班', '理學院', '應物系', '應物系材料組', '應物系光電組', '化學系', '化學系化學組', '化學系化生組', '生科系', '生科系生醫組', '生科系生態組', '應數系', '生醫材料博士學程', '生物多樣性博士學程', '工學院', '化材系', '工工系', '工工在職專班', '環工系', '資工系', '資工系資電組', '資工系數創組', '資工系軟工組', '資訊在職專班', '資碩專大數據物聯網', '資碩專高階資訊經營', '電機系', '電機系IC通訊組', '電機系奈米能源組', '數創碩士學位學程', '管理學院', '企管系', '高階企業經營專班', '國貿系', '會計系', '財金系', '統計系', '資管系', '社科院', '經濟系', '政治系', '行政系', '社會系', '社工系', '農學院', '畜產系', '食科系', '餐旅系', '健康與運動學程', '創意學院', '美術系', '音樂系', '建築系', '工設系', '景觀系', '法學院', '法律系', '國際學院', '國經學程', '永續學程', '國際學院不分系', '雲創學院', '通識人文', '通識自然', '通識社會', '多元學習(共選修)', '遠距教學', '第二外國語', '師資中心', '日文課程', '軍訓一', '護理一', '軍訓二', '中文課程', '歷史課程', '大一英文', '體育選修課程', '選修英文', '通識文明與經典', '大二英文', '通識領導與倫理', 'AI思維與程式設計', '通識議題導向領域', '大一大二體育', '暑修', '英文畢業門檻替代課程']
        self.ui.majr.addItems(majrs)
        stypes = ['日間學士班','進修學士班','研究所']
        self.ui.stype.addItems(stypes)
        self.ui.button_submit.clicked.connect(self.submitClicked)
        self.table = [['','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','']]
        self.istable = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        self.ui.button_add.clicked.connect(self.add_course)
        self.ui.button_del.clicked.connect(self.delect_course)
        self.ui.button_load.clicked.connect(self.load_file)
        self.ui.button_write.clicked.connect(self.write_file)


        
    def submitClicked(self):
        i_year = self.ui.years.currentText()
        i_term = d_terms[self.ui.term.currentText()]
        i_week = self.ui.week.text()
        i_dsep = self.ui.dsep.text()
        i_majr = d_majrs[self.ui.majr.currentText()]
        i_stype = d_stypes[self.ui.stype.currentText()]
        i_teac = self.ui.teac.text()
        i_cour = self.ui.cour.text()
        '''
        self.ui.d7_0.setText(i_year)
        self.ui.d7_1.setText(i_term)
        self.ui.d7_2.setText(i_week)
        self.ui.d7_3.setText(i_dsep)
        self.ui.d7_4.setText(i_majr)
        self.ui.d7_5.setText(i_stype)
        self.ui.d7_6.setText(i_teac)
        self.ui.d7_7.setText(i_cour)
        '''
        try:
            self.ui.courselist.clear()
            self.onlygrade,self.choosecode_name,self.teacher,self.grade,self.haveto,self.point,self.day,self.option,self.classcode = self.get_name(i_year,i_term,i_week,i_dsep,i_majr,i_stype,i_teac,i_cour)
            self.ui.state.setText("找到 {0} 個課程".format(len(self.onlygrade)))
            findcourse = []
            for i in range(len(self.onlygrade)):
                string = ""
                string = self.choosecode_name[i] + self.grade[i]
                findcourse.append(string)
            self.ui.courselist.addItems(findcourse)
            #print(choosecode_name)
            #time.sleep(3)
            #clist = ""
            #for i in range(len(onlygrade)):
            #    clist += choosecode_name[i]+'\n'
            #self.ui.courselist.setText(clist)
        except:
            print('error here getdata')
        '''
        self.qthread = ThreadTask()
        self.qthread.T_choosecode_name.connect(self.get_name)
        self.qthread.crawler()
        '''
    def add_course(self):
        list_day = []
        day_name = ""
        day_teacher = ""
        
        try:
            for i in range(len(self.choosecode_name)):
              if self.ui.courselist.currentText()==self.choosecode_name[i]+self.grade[i]:
                  list_day=self.day[i]
                  day_name = self.choosecode_name[i]
                  day_teacher = self.teacher[i]
        except:
            self.ui.state.setText("請先選課1")
        
        
        try:    
            for i in range(len(list_day)):
                if list_day[0]!='':
                    up = list_day[i][0]
                    down = list_day[i][1:]
                    if up=='一':
                        up = '0'
                    if up=='二':
                        up = '1'
                    if up=='三':
                        up = '2'
                    if up=='四':
                        up = '3'
                    if up=='五':
                        up = '4'
                    if up=='六':
                        up = '5'
                    if up=='七':
                        up = '6'

                    #確認是否已加入
                    is_selected = 0
                    up = int(up)
                    if int(down)<5:
                        down = int(down)
                    elif down=="45":
                        down = 5
                    else:
                        down = int(down)+1
                    #print("{0} {1}".format(up,down))
                    for j in range(self.istable[up][down]):
                        current = self.table[up][down].split('\n')[j*2]
                        if current in self.ui.courselist.currentText():
                            is_selected = 1
                    if is_selected==0:
                        self.table[up][down] += day_name+'\n'+day_teacher + '\n'
                        self.istable[up][down] += 1
                    self.ui.state.setText("加入課程")
                else:
                    self.ui.state.setText("此課程無日期")
            self.print_course()
        except:
            self.ui.state.setText("請先選課2")
        
            
    def delect_course(self):    
        list_day = []

        try:
            for i in range(len(self.choosecode_name)):
              if self.ui.courselist.currentText()==self.choosecode_name[i]+self.grade[i]:
                  list_day=self.day[i]
        except:
            self.ui.state.setText("請先選課1")
        try:    
            for i in range(len(list_day)):
                if list_day[0]!='':
                    up = list_day[i][0]
                    down = list_day[i][1:]
                    if up=='一':
                        up = '0'
                    if up=='二':
                        up = '1'
                    if up=='三':
                        up = '2'
                    if up=='四':
                        up = '3'
                    if up=='五':
                        up = '4'
                    if up=='六':
                        up = '5'
                    if up=='七':
                        up = '6'

                    #確認是否已加入
                    is_selected = 0
                    up = int(up)
                    if int(down)<5:
                        down = int(down)
                    elif down=="45":
                        down = 5
                    else:
                        down = int(down)+1
                    for j in range(self.istable[up][down]):
                        current = self.table[up][down].split('\n')[j*2]
                        if current in self.ui.courselist.currentText():
                            is_selected = 1
                    if is_selected==1:
                        changelist = ""
                        for j in range(self.istable[up][down]):
                            current = self.table[up][down].split('\n')[j*2]
                            if current not in self.ui.courselist.currentText():
                                changelist += self.table[up][down].split('\n')[j*2]+"\n"+self.table[up][down].split('\n')[j*2+1]+"\n"
                        self.table[up][down] = changelist
                        self.istable[up][down] -= 1
                    self.ui.state.setText("刪除課程")
                else:
                    self.ui.state.setText("此課程無日期")
            self.print_course()
            
        except:
            self.ui.state.setText("請先選課2")

    def load_file(self):
        try:
            with open('course.csv',newline='') as file:
                rows = csv.reader(file)
                for row in rows:
                    if row[0] == "節次":
                        continue
                    else:
                        if row[0]=='0':
                            self.table[0][0] = row[1]
                            self.istable[0][0] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][0] = row[2]
                            self.istable[1][0] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][0] = row[3]
                            self.istable[2][0] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][0] = row[4]
                            self.istable[3][0] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][0] = row[5]
                            self.istable[4][0] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][0] = row[6]
                            self.istable[5][0] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][0] = row[7]
                            self.istable[6][0] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='1':
                            self.table[0][1] = row[1]
                            self.istable[0][1] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][1] = row[2]
                            self.istable[1][1] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][1] = row[3]
                            self.istable[2][1] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][1] = row[4]
                            self.istable[3][1] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][1] = row[5]
                            self.istable[4][1] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][1] = row[6]
                            self.istable[5][1] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][1] = row[7]
                            self.istable[6][1] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='2':
                            self.table[0][2] = row[1]
                            self.istable[0][2] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][2] = row[2]
                            self.istable[1][2] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][2] = row[3]
                            self.istable[2][2] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][2] = row[4]
                            self.istable[3][2] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][2] = row[5]
                            self.istable[4][2] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][2] = row[6]
                            self.istable[5][2] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][2] = row[7]
                            self.istable[6][2] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='3':
                            self.table[0][3] = row[1]
                            self.istable[0][3] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][3] = row[2]
                            self.istable[1][3] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][3] = row[3]
                            self.istable[2][3] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][3] = row[4]
                            self.istable[3][3] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][3] = row[5]
                            self.istable[4][3] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][3] = row[6]
                            self.istable[5][3] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][3] = row[7]
                            self.istable[6][3] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='4':
                            self.table[0][4] = row[1]
                            self.istable[0][4] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][4] = row[2]
                            self.istable[1][4] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][4] = row[3]
                            self.istable[2][4] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][4] = row[4]
                            self.istable[3][4] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][4] = row[5]
                            self.istable[4][4] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][4] = row[6]
                            self.istable[5][4] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][4] = row[7]
                            self.istable[6][4] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='5':
                            self.table[0][5] = row[1]
                            self.istable[0][5] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][5] = row[2]
                            self.istable[1][5] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][5] = row[3]
                            self.istable[2][5] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][5] = row[4]
                            self.istable[3][5] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][5] = row[5]
                            self.istable[4][5] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][5] = row[6]
                            self.istable[5][5] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][5] = row[7]
                            self.istable[6][5] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='6':
                            self.table[0][6] = row[1]
                            self.istable[0][6] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][6] = row[2]
                            self.istable[1][6] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][6] = row[3]
                            self.istable[2][6] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][6] = row[4]
                            self.istable[3][6] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][6] = row[5]
                            self.istable[4][6] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][6] = row[6]
                            self.istable[5][6] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][6] = row[7]
                            self.istable[6][6] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='7':
                            self.table[0][7] = row[1]
                            self.istable[0][7] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][7] = row[2]
                            self.istable[1][7] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][7] = row[3]
                            self.istable[2][7] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][7] = row[4]
                            self.istable[3][7] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][7] = row[5]
                            self.istable[4][7] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][7] = row[6]
                            self.istable[5][7] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][7] = row[7]
                            self.istable[6][7] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='8':
                            self.table[0][8] = row[1]
                            self.istable[0][8] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][8] = row[2]
                            self.istable[1][8] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][8] = row[3]
                            self.istable[2][8] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][8] = row[4]
                            self.istable[3][8] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][8] = row[5]
                            self.istable[4][8] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][8] = row[6]
                            self.istable[5][8] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][8] = row[7]
                            self.istable[6][8] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='9':
                            self.table[0][9] = row[1]
                            self.istable[0][9] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][9] = row[2]
                            self.istable[1][9] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][9] = row[3]
                            self.istable[2][9] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][9] = row[4]
                            self.istable[3][9] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][9] = row[5]
                            self.istable[4][9] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][9] = row[6]
                            self.istable[5][9] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][9] = row[7]
                            self.istable[6][9] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='10':
                            self.table[0][10] = row[1]
                            self.istable[0][10] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][10] = row[2]
                            self.istable[1][10] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][10] = row[3]
                            self.istable[2][10] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][10] = row[4]
                            self.istable[3][10] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][10] = row[5]
                            self.istable[4][10] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][10] = row[6]
                            self.istable[5][10] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][10] = row[7]
                            self.istable[6][10] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='11':
                            self.table[0][11] = row[1]
                            self.istable[0][11] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][11] = row[2]
                            self.istable[1][11] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][11] = row[3]
                            self.istable[2][11] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][11] = row[4]
                            self.istable[3][11] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][11] = row[5]
                            self.istable[4][11] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][11] = row[6]
                            self.istable[5][11] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][11] = row[7]
                            self.istable[6][11] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='12':
                            self.table[0][12] = row[1]
                            self.istable[0][12] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][12] = row[2]
                            self.istable[1][12] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][12] = row[3]
                            self.istable[2][12] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][12] = row[4]
                            self.istable[3][12] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][12] = row[5]
                            self.istable[4][12] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][12] = row[6]
                            self.istable[5][12] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][12] = row[7]
                            self.istable[6][12] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='13':
                            self.table[0][13] = row[1]
                            self.istable[0][13] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][13] = row[2]
                            self.istable[1][13] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][13] = row[3]
                            self.istable[2][13] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][13] = row[4]
                            self.istable[3][13] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][13] = row[5]
                            self.istable[4][13] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][13] = row[6]
                            self.istable[5][13] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][13] = row[7]
                            self.istable[6][13] = int((len(row[7].split('\n'))-1)/2)
                        if row[0]=='14':
                            self.table[0][14] = row[1]
                            self.istable[0][14] = int((len(row[1].split('\n'))-1)/2)
                            self.table[1][14] = row[2]
                            self.istable[1][14] = int((len(row[2].split('\n'))-1)/2)
                            self.table[2][14] = row[3]
                            self.istable[2][14] = int((len(row[3].split('\n'))-1)/2)
                            self.table[3][14] = row[4]
                            self.istable[3][14] = int((len(row[4].split('\n'))-1)/2)
                            self.table[4][14] = row[5]
                            self.istable[4][14] = int((len(row[5].split('\n'))-1)/2)
                            self.table[5][14] = row[6]
                            self.istable[5][14] = int((len(row[6].split('\n'))-1)/2)
                            self.table[6][14] = row[7]
                            self.istable[6][14] = int((len(row[7].split('\n'))-1)/2)
            file.close()
            self.print_course()
            self.ui.state.setText("導入course.csv檔案")
        except:
            self.ui.state.setText("未有course.csv檔案,請先導出")

    def write_file(self):
        with open('course.csv','w',newline='') as file:
            writer = csv.writer(file)

            writer.writerow(['節次','星期一','星期二','星期三','星期四','星期五','星期六','星期日'])
            writer.writerow(['0', self.table[0][0], self.table[1][0], self.table[2][0], self.table[3][0], self.table[4][0], self.table[5][0], self.table[6][0]])
            writer.writerow(['1', self.table[0][1], self.table[1][1], self.table[2][1], self.table[3][1], self.table[4][1], self.table[5][1], self.table[6][1]])
            writer.writerow(['2', self.table[0][2], self.table[1][2], self.table[2][2], self.table[3][2], self.table[4][2], self.table[5][2], self.table[6][2]])
            writer.writerow(['3', self.table[0][3], self.table[1][3], self.table[2][3], self.table[3][3], self.table[4][3], self.table[5][3], self.table[6][3]])
            writer.writerow(['4', self.table[0][4], self.table[1][4], self.table[2][4], self.table[3][4], self.table[4][4], self.table[5][4], self.table[6][4]])
            writer.writerow(['5', self.table[0][5], self.table[1][5], self.table[2][5], self.table[3][5], self.table[4][5], self.table[5][5], self.table[6][5]])
            writer.writerow(['6', self.table[0][6], self.table[1][6], self.table[2][6], self.table[3][6], self.table[4][6], self.table[5][6], self.table[6][6]])
            writer.writerow(['7', self.table[0][7], self.table[1][7], self.table[2][7], self.table[3][7], self.table[4][7], self.table[5][7], self.table[6][7]])
            writer.writerow(['8', self.table[0][8], self.table[1][8], self.table[2][8], self.table[3][8], self.table[4][8], self.table[5][8], self.table[6][8]])
            writer.writerow(['9', self.table[0][9], self.table[1][9], self.table[2][9], self.table[3][9], self.table[4][9], self.table[5][9], self.table[6][9]])
            writer.writerow(['10',self.table[0][10], self.table[1][10], self.table[2][10], self.table[3][10], self.table[4][10], self.table[5][10], self.table[6][10]])
            writer.writerow(['11',self.table[0][11], self.table[1][11], self.table[2][11], self.table[3][11], self.table[4][11], self.table[5][11], self.table[6][11]])
            writer.writerow(['12',self.table[0][12], self.table[1][12], self.table[2][12], self.table[3][12], self.table[4][12], self.table[5][12], self.table[6][12]])
            writer.writerow(['13',self.table[0][13], self.table[1][13], self.table[2][13], self.table[3][13], self.table[4][13], self.table[5][13], self.table[6][13]])
            writer.writerow(['14',self.table[0][14], self.table[1][14], self.table[2][14], self.table[3][14], self.table[4][14], self.table[5][14], self.table[6][14]])
        file.close()
        self.ui.state.setText("導出course.csv檔案")





        

    def print_course(self):
        try:
            self.ui.d1_0.setText(self.table[0][0])
            self.ui.d1_1.setText(self.table[0][1])
            self.ui.d1_2.setText(self.table[0][2])
            self.ui.d1_3.setText(self.table[0][3])
            self.ui.d1_4.setText(self.table[0][4])
            self.ui.d1_45.setText(self.table[0][5])
            self.ui.d1_5.setText(self.table[0][6])
            self.ui.d1_6.setText(self.table[0][7])
            self.ui.d1_7.setText(self.table[0][8])
            self.ui.d1_8.setText(self.table[0][9])
            self.ui.d1_9.setText(self.table[0][10])
            self.ui.d1_10.setText(self.table[0][11])
            self.ui.d1_11.setText(self.table[0][12])
            self.ui.d1_12.setText(self.table[0][13])
            self.ui.d1_13.setText(self.table[0][14])
            self.ui.d2_0.setText(self.table[1][0])
            self.ui.d2_1.setText(self.table[1][1])
            self.ui.d2_2.setText(self.table[1][2])
            self.ui.d2_3.setText(self.table[1][3])
            self.ui.d2_4.setText(self.table[1][4])
            self.ui.d2_45.setText(self.table[1][5])
            self.ui.d2_5.setText(self.table[1][6])
            self.ui.d2_6.setText(self.table[1][7])
            self.ui.d2_7.setText(self.table[1][8])
            self.ui.d2_8.setText(self.table[1][9])
            self.ui.d2_9.setText(self.table[1][10])
            self.ui.d2_10.setText(self.table[1][11])
            self.ui.d2_11.setText(self.table[1][12])
            self.ui.d2_12.setText(self.table[1][13])
            self.ui.d2_13.setText(self.table[1][14])
            self.ui.d3_0.setText(self.table[2][0])
            self.ui.d3_1.setText(self.table[2][1])
            self.ui.d3_2.setText(self.table[2][2])
            self.ui.d3_3.setText(self.table[2][3])
            self.ui.d3_4.setText(self.table[2][4])
            self.ui.d3_45.setText(self.table[2][5])
            self.ui.d3_5.setText(self.table[2][6])
            self.ui.d3_6.setText(self.table[2][7])
            self.ui.d3_7.setText(self.table[2][8])
            self.ui.d3_8.setText(self.table[2][9])
            self.ui.d3_9.setText(self.table[2][10])
            self.ui.d3_10.setText(self.table[2][11])
            self.ui.d3_11.setText(self.table[2][12])
            self.ui.d3_12.setText(self.table[2][13])
            self.ui.d3_13.setText(self.table[2][14])
            self.ui.d4_0.setText(self.table[3][0])
            self.ui.d4_1.setText(self.table[3][1])
            self.ui.d4_2.setText(self.table[3][2])
            self.ui.d4_3.setText(self.table[3][3])
            self.ui.d4_4.setText(self.table[3][4])
            self.ui.d4_45.setText(self.table[3][5])
            self.ui.d4_5.setText(self.table[3][6])
            self.ui.d4_6.setText(self.table[3][7])
            self.ui.d4_7.setText(self.table[3][8])
            self.ui.d4_8.setText(self.table[3][9])
            self.ui.d4_9.setText(self.table[3][10])
            self.ui.d4_10.setText(self.table[3][11])
            self.ui.d4_11.setText(self.table[3][12])
            self.ui.d4_12.setText(self.table[3][13])
            self.ui.d4_13.setText(self.table[3][14])
            self.ui.d5_0.setText(self.table[4][0])
            self.ui.d5_1.setText(self.table[4][1])
            self.ui.d5_2.setText(self.table[4][2])
            self.ui.d5_3.setText(self.table[4][3])
            self.ui.d5_4.setText(self.table[4][4])
            self.ui.d5_45.setText(self.table[4][5])
            self.ui.d5_5.setText(self.table[4][6])
            self.ui.d5_6.setText(self.table[4][7])
            self.ui.d5_7.setText(self.table[4][8])
            self.ui.d5_8.setText(self.table[4][9])
            self.ui.d5_9.setText(self.table[4][10])
            self.ui.d5_10.setText(self.table[4][11])
            self.ui.d5_11.setText(self.table[4][12])
            self.ui.d5_12.setText(self.table[4][13])
            self.ui.d5_13.setText(self.table[4][14])
            self.ui.d6_0.setText(self.table[5][0])
            self.ui.d6_1.setText(self.table[5][1])
            self.ui.d6_2.setText(self.table[5][2])
            self.ui.d6_3.setText(self.table[5][3])
            self.ui.d6_4.setText(self.table[5][4])
            self.ui.d6_45.setText(self.table[5][5])
            self.ui.d6_5.setText(self.table[5][6])
            self.ui.d6_6.setText(self.table[5][7])
            self.ui.d6_7.setText(self.table[5][8])
            self.ui.d6_8.setText(self.table[5][9])
            self.ui.d6_9.setText(self.table[5][10])
            self.ui.d6_10.setText(self.table[5][11])
            self.ui.d6_11.setText(self.table[5][12])
            self.ui.d6_12.setText(self.table[5][13])
            self.ui.d6_13.setText(self.table[5][14])
            self.ui.d7_0.setText(self.table[6][0])
            self.ui.d7_1.setText(self.table[6][1])
            self.ui.d7_2.setText(self.table[6][2])
            self.ui.d7_3.setText(self.table[6][3])
            self.ui.d7_4.setText(self.table[6][4])
            self.ui.d7_45.setText(self.table[6][5])
            self.ui.d7_5.setText(self.table[6][6])
            self.ui.d7_6.setText(self.table[6][7])
            self.ui.d7_7.setText(self.table[6][8])
            self.ui.d7_8.setText(self.table[6][9])
            self.ui.d7_9.setText(self.table[6][10])
            self.ui.d7_10.setText(self.table[6][11])
            self.ui.d7_11.setText(self.table[6][12])
            self.ui.d7_12.setText(self.table[6][13])
            self.ui.d7_13.setText(self.table[6][14])
            if self.istable[0][0]>1:
                self.ui.d1_0.setStyleSheet("background:pink")
            else:
                self.ui.d1_0.setStyleSheet("background:white")
            if self.istable[0][1]>1:
                self.ui.d1_1.setStyleSheet("background:pink")
            else:
                self.ui.d1_1.setStyleSheet("background:white")
            if self.istable[0][2]>1:
                self.ui.d1_2.setStyleSheet("background:pink")
            else:
                self.ui.d1_2.setStyleSheet("background:white")
            if self.istable[0][3]>1:
                self.ui.d1_3.setStyleSheet("background:pink")
            else:
                self.ui.d1_3.setStyleSheet("background:white")
            if self.istable[0][4]>1:
                self.ui.d1_4.setStyleSheet("background:pink")
            else:
                self.ui.d1_4.setStyleSheet("background:white")
            if self.istable[0][5]>1:
                self.ui.d1_45.setStyleSheet("background:pink")
            else:
                self.ui.d1_45.setStyleSheet("background:white")
            if self.istable[0][6]>1:
                self.ui.d1_5.setStyleSheet("background:pink")
            else:
                self.ui.d1_5.setStyleSheet("background:white")
            if self.istable[0][7]>1:
                self.ui.d1_6.setStyleSheet("background:pink")
            else:
                self.ui.d1_6.setStyleSheet("background:white")
            if self.istable[0][8]>1:
                self.ui.d1_7.setStyleSheet("background:pink")
            else:
                self.ui.d1_7.setStyleSheet("background:white")
            if self.istable[0][9]>1:
                self.ui.d1_8.setStyleSheet("background:pink")
            else:
                self.ui.d1_8.setStyleSheet("background:white")
            if self.istable[0][10]>1:
                self.ui.d1_9.setStyleSheet("background:pink")
            else:
                self.ui.d1_9.setStyleSheet("background:white")
            if self.istable[0][11]>1:
                self.ui.d1_10.setStyleSheet("background:pink")
            else:
                self.ui.d1_10.setStyleSheet("background:white")
            if self.istable[0][12]>1:
                self.ui.d1_11.setStyleSheet("background:pink")
            else:
                self.ui.d1_11.setStyleSheet("background:white")
            if self.istable[0][13]>1:
                self.ui.d1_12.setStyleSheet("background:pink")
            else:
                self.ui.d1_12.setStyleSheet("background:white")
            if self.istable[0][14]>1:
                self.ui.d1_13.setStyleSheet("background:pink")
            else:
                self.ui.d1_13.setStyleSheet("background:white")
            if self.istable[1][0]>1:
                self.ui.d2_0.setStyleSheet("background:pink")
            else:
                self.ui.d2_0.setStyleSheet("background:white")
            if self.istable[1][1]>1:
                self.ui.d2_1.setStyleSheet("background:pink")
            else:
                self.ui.d2_1.setStyleSheet("background:white")
            if self.istable[1][2]>1:
                self.ui.d2_2.setStyleSheet("background:pink")
            else:
                self.ui.d2_2.setStyleSheet("background:white")
            if self.istable[1][3]>1:
                self.ui.d2_3.setStyleSheet("background:pink")
            else:
                self.ui.d2_3.setStyleSheet("background:white")
            if self.istable[1][4]>1:
                self.ui.d2_4.setStyleSheet("background:pink")
            else:
                self.ui.d2_4.setStyleSheet("background:white")
            if self.istable[1][5]>1:
                self.ui.d2_45.setStyleSheet("background:pink")
            else:
                self.ui.d2_45.setStyleSheet("background:white")
            if self.istable[1][6]>1:
                self.ui.d2_5.setStyleSheet("background:pink")
            else:
                self.ui.d2_5.setStyleSheet("background:white")
            if self.istable[1][7]>1:
                self.ui.d2_6.setStyleSheet("background:pink")
            else:
                self.ui.d2_6.setStyleSheet("background:white")
            if self.istable[1][8]>1:
                self.ui.d2_7.setStyleSheet("background:pink")
            else:
                self.ui.d2_7.setStyleSheet("background:white")
            if self.istable[1][9]>1:
                self.ui.d2_8.setStyleSheet("background:pink")
            else:
                self.ui.d2_8.setStyleSheet("background:white")
            if self.istable[1][10]>1:
                self.ui.d2_9.setStyleSheet("background:pink")
            else:
                self.ui.d2_9.setStyleSheet("background:white")
            if self.istable[1][11]>1:
                self.ui.d2_10.setStyleSheet("background:pink")
            else:
                self.ui.d2_10.setStyleSheet("background:white")
            if self.istable[1][12]>1:
                self.ui.d2_11.setStyleSheet("background:pink")
            else:
                self.ui.d2_11.setStyleSheet("background:white")
            if self.istable[1][13]>1:
                self.ui.d2_12.setStyleSheet("background:pink")
            else:
                self.ui.d2_12.setStyleSheet("background:white")
            if self.istable[1][14]>1:
                self.ui.d2_13.setStyleSheet("background:pink")
            else:
                self.ui.d2_13.setStyleSheet("background:white")
            if self.istable[2][0]>1:
                self.ui.d3_0.setStyleSheet("background:pink")
            else:
                self.ui.d3_0.setStyleSheet("background:white")
            if self.istable[2][1]>1:
                self.ui.d3_1.setStyleSheet("background:pink")
            else:
                self.ui.d3_1.setStyleSheet("background:white")
            if self.istable[2][2]>1:
                self.ui.d3_2.setStyleSheet("background:pink")
            else:
                self.ui.d3_2.setStyleSheet("background:white")
            if self.istable[2][3]>1:
                self.ui.d3_3.setStyleSheet("background:pink")
            else:
                self.ui.d3_3.setStyleSheet("background:white")
            if self.istable[2][4]>1:
                self.ui.d3_4.setStyleSheet("background:pink")
            else:
                self.ui.d3_4.setStyleSheet("background:white")
            if self.istable[2][5]>1:
                self.ui.d3_45.setStyleSheet("background:pink")
            else:
                self.ui.d3_45.setStyleSheet("background:white")
            if self.istable[2][6]>1:
                self.ui.d3_5.setStyleSheet("background:pink")
            else:
                self.ui.d3_5.setStyleSheet("background:white")
            if self.istable[2][7]>1:
                self.ui.d3_6.setStyleSheet("background:pink")
            else:
                self.ui.d3_6.setStyleSheet("background:white")
            if self.istable[2][8]>1:
                self.ui.d3_7.setStyleSheet("background:pink")
            else:
                self.ui.d3_7.setStyleSheet("background:white")
            if self.istable[2][9]>1:
                self.ui.d3_8.setStyleSheet("background:pink")
            else:
                self.ui.d3_8.setStyleSheet("background:white")
            if self.istable[2][10]>1:
                self.ui.d3_9.setStyleSheet("background:pink")
            else:
                self.ui.d3_9.setStyleSheet("background:white")
            if self.istable[2][11]>1:
                self.ui.d3_10.setStyleSheet("background:pink")
            else:
                self.ui.d3_10.setStyleSheet("background:white")
            if self.istable[2][12]>1:
                self.ui.d3_11.setStyleSheet("background:pink")
            else:
                self.ui.d3_11.setStyleSheet("background:white")
            if self.istable[2][13]>1:
                self.ui.d3_12.setStyleSheet("background:pink")
            else:
                self.ui.d3_12.setStyleSheet("background:white")
            if self.istable[2][14]>1:
                self.ui.d3_13.setStyleSheet("background:pink")
            else:
                self.ui.d3_13.setStyleSheet("background:white")
            if self.istable[3][0]>1:
                self.ui.d4_0.setStyleSheet("background:pink")
            else:
                self.ui.d4_0.setStyleSheet("background:white")
            if self.istable[3][1]>1:
                self.ui.d4_1.setStyleSheet("background:pink")
            else:
                self.ui.d4_1.setStyleSheet("background:white")
            if self.istable[3][2]>1:
                self.ui.d4_2.setStyleSheet("background:pink")
            else:
                self.ui.d4_2.setStyleSheet("background:white")
            if self.istable[3][3]>1:
                self.ui.d4_3.setStyleSheet("background:pink")
            else:
                self.ui.d4_3.setStyleSheet("background:white")
            if self.istable[3][4]>1:
                self.ui.d4_4.setStyleSheet("background:pink")
            else:
                self.ui.d4_4.setStyleSheet("background:white")
            if self.istable[3][5]>1:
                self.ui.d4_45.setStyleSheet("background:pink")
            else:
                self.ui.d4_45.setStyleSheet("background:white")
            if self.istable[3][6]>1:
                self.ui.d4_5.setStyleSheet("background:pink")
            else:
                self.ui.d4_5.setStyleSheet("background:white")
            if self.istable[3][7]>1:
                self.ui.d4_6.setStyleSheet("background:pink")
            else:
                self.ui.d4_6.setStyleSheet("background:white")
            if self.istable[3][8]>1:
                self.ui.d4_7.setStyleSheet("background:pink")
            else:
                self.ui.d4_7.setStyleSheet("background:white")
            if self.istable[3][9]>1:
                self.ui.d4_8.setStyleSheet("background:pink")
            else:
                self.ui.d4_8.setStyleSheet("background:white")
            if self.istable[3][10]>1:
                self.ui.d4_9.setStyleSheet("background:pink")
            else:
                self.ui.d4_9.setStyleSheet("background:white")
            if self.istable[3][11]>1:
                self.ui.d4_10.setStyleSheet("background:pink")
            else:
                self.ui.d4_10.setStyleSheet("background:white")
            if self.istable[3][12]>1:
                self.ui.d4_11.setStyleSheet("background:pink")
            else:
                self.ui.d4_11.setStyleSheet("background:white")
            if self.istable[3][13]>1:
                self.ui.d4_12.setStyleSheet("background:pink")
            else:
                self.ui.d4_12.setStyleSheet("background:white")
            if self.istable[3][14]>1:
                self.ui.d4_13.setStyleSheet("background:pink")
            else:
                self.ui.d4_13.setStyleSheet("background:white")
            if self.istable[4][0]>1:
                self.ui.d5_0.setStyleSheet("background:pink")
            else:
                self.ui.d5_0.setStyleSheet("background:white")
            if self.istable[4][1]>1:
                self.ui.d5_1.setStyleSheet("background:pink")
            else:
                self.ui.d5_1.setStyleSheet("background:white")
            if self.istable[4][2]>1:
                self.ui.d5_2.setStyleSheet("background:pink")
            else:
                self.ui.d5_2.setStyleSheet("background:white")
            if self.istable[4][3]>1:
                self.ui.d5_3.setStyleSheet("background:pink")
            else:
                self.ui.d5_3.setStyleSheet("background:white")
            if self.istable[4][4]>1:
                self.ui.d5_4.setStyleSheet("background:pink")
            else:
                self.ui.d5_4.setStyleSheet("background:white")
            if self.istable[4][5]>1:
                self.ui.d5_45.setStyleSheet("background:pink")
            else:
                self.ui.d5_45.setStyleSheet("background:white")
            if self.istable[4][6]>1:
                self.ui.d5_5.setStyleSheet("background:pink")
            else:
                self.ui.d5_5.setStyleSheet("background:white")
            if self.istable[4][7]>1:
                self.ui.d5_6.setStyleSheet("background:pink")
            else:
                self.ui.d5_6.setStyleSheet("background:white")
            if self.istable[4][8]>1:
                self.ui.d5_7.setStyleSheet("background:pink")
            else:
                self.ui.d5_7.setStyleSheet("background:white")
            if self.istable[4][9]>1:
                self.ui.d5_8.setStyleSheet("background:pink")
            else:
                self.ui.d5_8.setStyleSheet("background:white")
            if self.istable[4][10]>1:
                self.ui.d5_9.setStyleSheet("background:pink")
            else:
                self.ui.d5_9.setStyleSheet("background:white")
            if self.istable[4][11]>1:
                self.ui.d5_10.setStyleSheet("background:pink")
            else:
                self.ui.d5_10.setStyleSheet("background:white")
            if self.istable[4][12]>1:
                self.ui.d5_11.setStyleSheet("background:pink")
            else:
                self.ui.d5_11.setStyleSheet("background:white")
            if self.istable[4][13]>1:
                self.ui.d5_12.setStyleSheet("background:pink")
            else:
                self.ui.d5_12.setStyleSheet("background:white")
            if self.istable[4][14]>1:
                self.ui.d5_13.setStyleSheet("background:pink")
            else:
                self.ui.d5_13.setStyleSheet("background:white")
            if self.istable[5][0]>1:
                self.ui.d6_0.setStyleSheet("background:pink")
            else:
                self.ui.d6_0.setStyleSheet("background:white")
            if self.istable[5][1]>1:
                self.ui.d6_1.setStyleSheet("background:pink")
            else:
                self.ui.d6_1.setStyleSheet("background:white")
            if self.istable[5][2]>1:
                self.ui.d6_2.setStyleSheet("background:pink")
            else:
                self.ui.d6_2.setStyleSheet("background:white")
            if self.istable[5][3]>1:
                self.ui.d6_3.setStyleSheet("background:pink")
            else:
                self.ui.d6_3.setStyleSheet("background:white")
            if self.istable[5][4]>1:
                self.ui.d6_4.setStyleSheet("background:pink")
            else:
                self.ui.d6_4.setStyleSheet("background:white")
            if self.istable[5][5]>1:
                self.ui.d6_45.setStyleSheet("background:pink")
            else:
                self.ui.d6_45.setStyleSheet("background:white")
            if self.istable[5][6]>1:
                self.ui.d6_5.setStyleSheet("background:pink")
            else:
                self.ui.d6_5.setStyleSheet("background:white")
            if self.istable[5][7]>1:
                self.ui.d6_6.setStyleSheet("background:pink")
            else:
                self.ui.d6_6.setStyleSheet("background:white")
            if self.istable[5][8]>1:
                self.ui.d6_7.setStyleSheet("background:pink")
            else:
                self.ui.d6_7.setStyleSheet("background:white")
            if self.istable[5][9]>1:
                self.ui.d6_8.setStyleSheet("background:pink")
            else:
                self.ui.d6_8.setStyleSheet("background:white")
            if self.istable[5][10]>1:
                self.ui.d6_9.setStyleSheet("background:pink")
            else:
                self.ui.d6_9.setStyleSheet("background:white")
            if self.istable[5][11]>1:
                self.ui.d6_10.setStyleSheet("background:pink")
            else:
                self.ui.d6_10.setStyleSheet("background:white")
            if self.istable[5][12]>1:
                self.ui.d6_11.setStyleSheet("background:pink")
            else:
                self.ui.d6_11.setStyleSheet("background:white")
            if self.istable[5][13]>1:
                self.ui.d6_12.setStyleSheet("background:pink")
            else:
                self.ui.d6_12.setStyleSheet("background:white")
            if self.istable[5][14]>1:
                self.ui.d6_13.setStyleSheet("background:pink")
            else:
                self.ui.d6_13.setStyleSheet("background:white")
            if self.istable[6][0]>1:
                self.ui.d7_0.setStyleSheet("background:pink")
            else:
                self.ui.d7_0.setStyleSheet("background:white")
            if self.istable[6][1]>1:
                self.ui.d7_1.setStyleSheet("background:pink")
            else:
                self.ui.d7_1.setStyleSheet("background:white")
            if self.istable[6][2]>1:
                self.ui.d7_2.setStyleSheet("background:pink")
            else:
                self.ui.d7_2.setStyleSheet("background:white")
            if self.istable[6][3]>1:
                self.ui.d7_3.setStyleSheet("background:pink")
            else:
                self.ui.d7_3.setStyleSheet("background:white")
            if self.istable[6][4]>1:
                self.ui.d7_4.setStyleSheet("background:pink")
            else:
                self.ui.d7_4.setStyleSheet("background:white")
            if self.istable[6][5]>1:
                self.ui.d7_45.setStyleSheet("background:pink")
            else:
                self.ui.d7_45.setStyleSheet("background:white")
            if self.istable[6][6]>1:
                self.ui.d7_5.setStyleSheet("background:pink")
            else:
                self.ui.d7_5.setStyleSheet("background:white")
            if self.istable[6][7]>1:
                self.ui.d7_6.setStyleSheet("background:pink")
            else:
                self.ui.d7_6.setStyleSheet("background:white")
            if self.istable[6][8]>1:
                self.ui.d7_7.setStyleSheet("background:pink")
            else:
                self.ui.d7_7.setStyleSheet("background:white")
            if self.istable[6][9]>1:
                self.ui.d7_8.setStyleSheet("background:pink")
            else:
                self.ui.d7_8.setStyleSheet("background:white")
            if self.istable[6][10]>1:
                self.ui.d7_9.setStyleSheet("background:pink")
            else:
                self.ui.d7_9.setStyleSheet("background:white")
            if self.istable[6][11]>1:
                self.ui.d7_10.setStyleSheet("background:pink")
            else:
                self.ui.d7_10.setStyleSheet("background:white")
            if self.istable[6][12]>1:
                self.ui.d7_11.setStyleSheet("background:pink")
            else:
                self.ui.d7_11.setStyleSheet("background:white")
            if self.istable[6][13]>1:
                self.ui.d7_12.setStyleSheet("background:pink")
            else:
                self.ui.d7_12.setStyleSheet("background:white")
            if self.istable[6][14]>1:
                self.ui.d7_13.setStyleSheet("background:pink")
            else:
                self.ui.d7_13.setStyleSheet("background:white")

        except:
            print('error')

    def get_name(self,i_year,i_term,i_week,i_dsep,i_majr,i_stype,i_teac,i_cour):
        url = "https://fsis.thu.edu.tw/wwwstud/COURSE/05_deptopServer.php"
        data = {'i_year':i_year,
                'i_term':i_term,
                'i_week':i_week,
                'i_dsep':i_dsep,
                'i_majr':i_majr,
                'i_teac':i_teac,
                'i_cour':i_cour
                }
        d_terms = {'第一學期':'1','第二學期':'2','暑修上期':'3','暑修下期':'4'}
        d_majrs = {'文學院':'100','中文系':'110','中文在職專班':'117','外文系':'120','外文系教學組':'121','外文系文學組':'122','歷史系':'130','華語教學碩士學程':'140','日文系':'150','宗教研究所':'180','哲學系':'190','哲學在職專班':'197',
                   '理學院':'200','應物系':'210','應物系材料組':'211','應物系光電組':'212','化學系':'220','化學系化學組':'221','化學系化生組':'222','生科系':'230','生科系生醫組':'231','生科系生態組':'232','應數系':'240','生醫材料博士學程':'250','生物多樣性博士學程':'260',
                   '工學院':'300','化材系':'310','工工系':'330','工工在職專班':'337','環工系':'340','資工系':'350','資工系資電組':'351','資工系數創組':'352','資工系軟工組':'253','資訊在職專班':'357','資碩專大數據物聯網':'358','資碩專高階資訊經營':'359','電機系':'360','電機系IC通訊組':'361','電機系奈米能源組':'362','數創碩士學位學程':'370',
                   '管理學院':'400','企管系':'410','高階企業經營專班':'417','國貿系':'420','會計系':'430','財金系':'440','統計系':'470','資管系':'490',
                   '社科院':'500','經濟系':'520','政治系':'530','行政系':'540','社會系':'550','社工系':'560',
                   '農學院':'600','畜產系':'610','食科系':'620','餐旅系':'660','健康與運動學程':'680',
                   '創意學院':'700','美術系':'710','音樂系':'720','建築系':'730','工設系':'740','景觀系':'750',
                   '法學院':'800','法律系':'810',
                   '國際學院':'900','國經學程':'910','永續學程':'920','國際學院不分系':'930',
                   '雲創學院':'A00',
                   '通識人文':'S01','通識自然':'S02','通識社會':'S03','多元學習(共選修)':'S04','遠距教學':'S05','第二外國語':'S06','師資中心':'S07','日文課程':'S08','軍訓一':'S18','護理一':'S19','軍訓二':'S20','中文課程':'S25','歷史課程':'S26','大一英文':'S27','體育選修課程':'S34','選修英文':'S36','通識文明與經典':'S38','大二英文':'S39','通識領導與倫理':'S40','AI思維與程式設計':'S43','通識議題導向領域':'S44','大一大二體育':'S61','暑修':'S68','英文畢業門檻替代課程':'engsub'}
        d_stypes = {'日間學士班':'A','進修學士班':'E','研究所':'F'}

        
        html = requests.post(url,data)
        sp = BeautifulSoup(html.text,'lxml')
        courses = sp.find_all('td')
        
        onlygrade = []
        choosecode_name = []
        teacher = []
        grade = []
        haveto = []
        point = []
        day = []
        option = []
        classcode = []
        index = 0
        cd = ['一','二','三','四','五','六','七']
        for course in courses:
            if index%9==0 and int(index/9)!=0:
                onlygrade.append(course.text)
            if index%9==1 and int(index/9)!=0:
                choosecode_name.append(course.text.split('&nbsp')[0].split(' ')[-1]+course.text.split('&nbsp')[1])
                #print(course.text.split('&nbsp')[0].split(' ')[-1]+course.text.split('&nbsp')[1])
            if index%9==2 and int(index/9)!=0:
                teacher.append(course.text)
            if index%9==3 and int(index/9)!=0:
                grade.append(course.text)
            if index%9==4 and int(index/9)!=0:
                haveto.append(course.text)
            if index%9==5 and int(index/9)!=0:
                point.append(course.text)
            if index%9==6 and int(index/9)!=0:
                day_text = course.text.split(',')
                day_list = []
                now = ""
                for dat in day_text:
                    if dat=="":
                        day_list.append("")
                    elif dat[0] in cd:
                        if '[' not in dat:
                            day_list.append(dat[0]+dat[2:])
                        else :
                            day_list.append(dat[0]+dat[2:].split('[')[0])
                        now = dat[0]
                    else:
                        if '[' not in dat:
                            day_list.append(now+dat)
                        else:
                            day_list.append(now+dat.split('[')[0])
                day.append(day_list)
            if index%9==7 and int(index/9)!=0:
                option.append(course.text)
            if index%9==8 and int(index/9)!=0:
                classcode.append(course.text)
            index += 1
        '''
        for i in range(len(onlygrade)):
            print(onlygrade[i])
            print(choosecode_name[i])
            print(teacher[i])
            print(grade[i])
            print(haveto[i])
            print(point[i])
            print(day[i])
            print(option[i])
            print(classcode[i])
        '''
        return onlygrade,choosecode_name,teacher,grade,haveto,point,day,option,classcode

    def get_year(self):
        url = "https://fsis.thu.edu.tw/wwwstud/frontend/CourseList.php"
        html = requests.get(url)
        sp = BeautifulSoup(html.text,'lxml')
        getyears = sp.find_all('select',class_='j-select')
        getyears = getyears[0].find_all('option')
        returnyear = []
        for getyear in getyears:
            returnyear.append(getyear.text)
        return returnyear
'''
    def get_name(self,value):
        choosecode_name = value
        #print(choosecode_name)
        #print(len(choosecode_name))
        self.ui.d7_0.setText(choosecode_name[0])
        #self.ui.listWidget.addItems(choosecode_name)
'''
