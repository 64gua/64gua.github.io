#2024-6-24 v1.2  2024-10-18 v1.3 2025-08-16v1.4 
#2026-03-22 v2.0   2026-06-10 v2.1增加多关键词查询&功能
#2026-06-24 v3.0 修改原来的数据源统一入口与画图逻辑

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl
import sys, shutil,os,re
from datetime import datetime
import sqlite3                                                     
import codeToName
import sixyao
import akshare_plotly as akPlot
from  dataSourcePlotly import drawKline
from  dataSource import Ktype
import markdown
import add_ganzhi_field

DB_NAME='Guas.db'
main_ui = "db_search_v3.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(main_ui)
insert_ui="insert_db_v31.ui"
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(insert_ui)

class MyWindow2(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.btn_insert.clicked.connect(self.insert_data)

    def insert_data(self):
        cont=self.textEdit.toPlainText()
        lines=cont.splitlines()
        i=0
        for line in lines:
            i=i+1
            #print(line)
            if "," in line:
                items=line.split(",")
            else:
                items=line.split("，")
            print(items)
            #csv文件格式为卦名，日期 时间，东方财富-本周走势.三个字段，分离出相关字段。
            gua=items[0]
            day=items[1].split(" ")[0]     #具体日期如2026-06-24
            if " " in day:                    #如果有空格，则分离出时与分
                exacttime=items[1].split(" ")[1]   #3时5分 或3：45
            else:
                exacttime=""
            origincode=items[2].split("-")[0]
            subject=items[2].split("-")[1]
            code,name=codeToName.get_stock_tuple(origincode)
            subject=name+subject+exacttime
            #content=sixyao.paipan(day1,namestr)
            query = (gua,code,day)
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM stockGuas WHERE guaName=? and stockName=? and guaDate=?   ',query)
            db_result=cursor.fetchall()
            if len(db_result)==0:
                tuple=(gua, day,code,subject)
                cursor.execute("INSERT INTO stockGuas (guaName, guaDate,stockname,guaSubject)  VALUES (?,?,?,?)", tuple )
                print(i,'插入新数据csv record inserted Successfully')
            else:
                print(i, "原记录已经存在，不会重新插入!......")
            conn.commit()
            conn.close()
        self.btn_insert.setText("填加成功")
   
class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
#class MyWindow(QtBaseClass, Ui_MainWindow):
    def __init__(self):
        self.switch=1
       # QtWidgets.QMainWindow.__init__(self)
        QtBaseClass.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.tableGua.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableGua.setSelectionMode(QTableWidget.SingleSelection  )
        for i in range(0,8):
            self.tableGua.setColumnWidth(i, 80) 
        self.btn_search.clicked.connect(self.loadInfo)
        self.btn_draw.clicked.connect(self.drawPicture)
        self.tableGua.cellDoubleClicked.connect(self.displayGua)
        self.btn_save_markdown.clicked.connect(self.saveAction)
        self.btn_paipan.clicked.connect(self.paipan_action)
        self.btn_transform.clicked.connect(self.code_transform)
        self.btn_save_img.clicked.connect(self.saveJPG)
        self.actDelete.triggered.connect(self.deleteWaste)
        self.actRemove.triggered.connect(self.removeRecord)
        self.act_all_in.triggered.connect(self.allInOneMarkdownHtml)
        self.act_new.triggered.connect(self.refreshText)
        # self.act_generate_pics.triggered.connect(self.generatePics)
        self.act_add_ganzhi.triggered.connect(self.addGanZhi)
        self.btn_wash.clicked.connect(self.washContent)
        self.btn_del_image.clicked.connect(self.delete_useless_image)
        self.radioButton_html.toggled.connect(self.htmlformat)
        self.act_insert_data.triggered.connect(self.openNewWindow)
        self.spinBox.valueChanged.connect(self.displayImages)
        self.insert_mode=False

    def openNewWindow(self):
        self.window2 = MyWindow2()
        self.window2.show()

    def addGanZhi(self):
        add_ganzhi_field.add_gangzhi()
        add_ganzhi_field.add_xunkong()
        add_ganzhi_field.add_gong()
        print("everything is OK!!!")

    def loadInfo(self):
        # self.mode=searchmode
        connection=sqlite3.connect(DB_NAME)
        cursor=connection.cursor()
        mainsql='select postTitle,guaDate, stockName,guaName,user,guaContent,CAST(rowid as text),guaSubject, gong from StockGuas where 1==1  '
        orderby= '  order by cast( substr(guaDate,6,2) as integer),guaDate '
        strGuaName1=self.txtSearchGuaName.text().strip()
        strDay=self.txtSunMoon.text().strip()
        strXunKong=self.txtXunKong.text().strip()
        startday=self.txtStartDay.text().strip()
        endday=self.txtEndDay.text().strip()
        strKeyWord=self.txtTitle.text().strip()
        strGong=self.txtGong.text().strip()
        if strGuaName1:
            mainsql+=f' and guaName like "%{strGuaName1}%"  '
        if strDay:
            mainsql+=f' and gangZhi like "%{strDay}%"  '
        if strXunKong:
            mainsql+=f' and xunKong like "%{strXunKong}%"  '
        # elif searchmode==0:  #按照时间段搜索
        if startday and endday:
            mainsql+=f' and guaDate between"{startday}" and "{endday}"   '          
       # if strKeyWord:
       #     mainsql+=f' and  guaSubject like "%{strKeyWord}%"   '

        # 修改 strKeyWord 的处理逻辑，支持 & 符号的多关键词同时包含
        if strKeyWord:
            if '&' in strKeyWord:
            # 按 & 分割关键词
                keywords = [kw.strip() for kw in strKeyWord.split('&')]
            # 为每个关键词添加 like 条件，使用 AND 连接
                for kw in keywords:
                    if kw:  # 确保关键词不为空
                        mainsql+=f' and guaSubject like "%{kw}%"  '
            else:
            # 原有逻辑，单个关键词
                mainsql+=f' and guaSubject like "%{strKeyWord}%"   '
        if strGong!="":
            mainsql+=f' and gong like "%{strGong}%"  '
        query=mainsql+orderby
        print("query: ",query)
        result=cursor.execute(query)
      #  self.tableGua.setRowCount(0)
        print("result is is OK!")
        rows=cursor.fetchall()
        #self.tableGua.clearContents()
        self.tableGua.setRowCount(0)
        for x,row in enumerate(rows):
            #print(x)
            self.tableGua.insertRow (x)
            for y, info in enumerate(row):
                item= QtWidgets.QTableWidgetItem(info)
                self.tableGua.setItem(x,y,item)            
        cursor.close()
        connection.close()

    def displayGua(self):
        self.label_pic.clear()
        items=self.tableGua.selectedItems()
        self.row = self.tableGua.currentRow() 
        postTitle=items[0].text()
        guaContent=items[5].text()
        self.row_id=items[6].text()
        guaName=items[3].text()
        guaSubject=items[7].text()
        if not postTitle in guaContent:
            guaContent="主帖标题: "+postTitle+"\n"+guaContent
        rawStock=items[2].text()
        gDate=items[1].text()
        # self.txtContent.setPlainText(guaContent)
        self.txtContent.setPlainText(guaContent)
        self.content_md_format=guaContent
        self.radioButton_html.setChecked(False)
        self.txtStockCode.setText(rawStock)
        self.txtStockName.setText("")
        self.txtGuaDate.setText(gDate)
        self.txtGuaName.setText(guaName)
        self.txtSubject.setText(guaSubject)
        self.radioButton_30d.setChecked(True)
        self.content_md_format=guaContent
        self.displayImages()


    def code_transform(self):
        origin_code=self.txtStockCode.text()
        code,name=codeToName.get_stock_tuple(origin_code)
        self.txtStockCode.setText(code)
        self.txtStockName.setText(name)
   
    def displayImages(self):
        cont=self.content_md_format
        print("cont:",cont)
        re1=r'images.+jpg|images.+.jpeg|images.+png'
        images=re.findall(re1,cont)
        num=len(images)
        self.label_num_of_images.setText(f'{num}张图')
        value=self.spinBox.value()
        if value>=num:
            value=num-1
        if value<0:
            value=0
        print("value:",value)
        self.spinBox.setValue(value)
        if images:
            pixmap=QPixmap(images[value])
            self.current_image=images[value]
        else:
            pixmap=QPixmap("moneygod.png")     
        self.label_pic.setPixmap(pixmap) 

    def htmlformat(self):
        if self.radioButton_html.isChecked():
            cont=self.content_md_format.replace("\n","\n\n")
            html_content = markdown.markdown(cont, extensions=['extra'])
            html_header='''<style>
                        body  {color: black;  font-size: 12px; background-color: rgb(255, 255, 255);}
                        img {width:100%; height:auto; } 
                        </style>'''
            html_content=html_header+html_content
            with open("current.html", 'w',encoding="utf-8") as file:
                file.write(html_content)
            self.browser1.load(QUrl("C:/stock6yao/current.html"))
        else:
            self.browser1.load(QUrl("C:/stock6yao/welcome.html"))

    def drawPicture(self):
        guaDate=self.txtGuaDate.text()
        stockCode=self.txtStockCode.text()
        datasource = self.comboDatasource.currentText()
        kline_type=Ktype.DAILY
        before=10    #日K线默认多画前10根K线
        print(stockCode,guaDate,datasource,kline_type)
        if self.txtStockCode.text()=="NULL" or self.txtGuaDate.text()=="NULL":
            QMessageBox.information(None, "警告", "缺少股票代号或日期？")
            return
        if self.radioButton_365d.isChecked():
            kline_type=Ktype.MONTHLY
            before=3
            after=12
            self.drawType="Y"    
        else:
            if self.radioButton_15d.isChecked():
                after=15
                self.drawType="15d"  
            if self.radioButton_30d.isChecked():
                after=35
                self.drawType="30d"
            if self.radioButton_60d.isChecked():
                after=60
                self.drawType="60d"
        imgfile=drawKline(stockCode,guaDate,kline_type,before=before,after=after,source=datasource)   
        pixmap=QPixmap(imgfile)
        self.label_pic.setPixmap(pixmap) 
        if imgfile=="alert.png":
            QMessageBox.information(None, "警告", "股票名字或代号出错，是否退市？") 
        
    def saveAction(self):
        if self.insert_mode == True:
            self.insertNewRecord()
            self.refreshText()
            self.btn_save_markdown.setText("更新")
            self.insert_mode=False
        else:
            self.saveContentChange()

    def saveContentChange(self):
        QMessageBox.information(None, "注意", "当前界面的:卦内容-卦名-股票名-日期-主题，均被更新存入数据库")
        #row = self.tableGua.currentRow()      
        #rowid = self.tableGua.item(row, 6).text()
        rowid=self.row_id
        new_stockCode=self.txtStockCode.text()
        new_guaName=self.txtGuaName.text()
        new_content = self.txtContent.toPlainText()
        new_guaDate=self.txtGuaDate.text()
        new_subject=self.txtSubject.text()
        print(new_content)
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query='UPDATE StockGuas  SET guaDate="{}", stockName = "{}", guaName="{}", guaContent ="{}",guaSubject="{}"  WHERE rowid = {}  '.format( new_guaDate, new_stockCode, new_guaName, new_content, new_subject, rowid)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        print("saving Change is OK")
        self.loadInfo()
        self.tableGua.setCurrentCell(self.row, 1) 
        self.content_md_format=new_content
        self.displayImages()

    def insertNewRecord(self):
        #row = self.tableGua.currentRow()
        #rowid = self.tableGua.item(row, 6).text()
        new_stockCode=self.txtStockCode.text()
        new_guaName=self.txtGuaName.text()
        new_content = self.txtContent.toPlainText()
        new_guaDate=self.txtGuaDate.text()
        new_subject=self.txtSubject.text()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO stockGuas (guaDate,stockName,guaName,guaContent,guaSubject ) VALUES (?, ?, ?, ?,?) ", 
                         (new_guaDate, new_stockCode, new_guaName, new_content,new_subject))
        conn.commit()
        #cursor.close()
        conn.close()
        self.btn_save_markdown.setDisabled(False)
        print("insert new record is OK!")


    def washContent(self):
        cont=self.txtContent.toPlainText()
        cont=re.sub(r'农历.*\s.*\s.*\s干支','\n干支',cont)
        cont=re.sub(r'农历.*','',cont)
        cont=re.sub(r'.*元亨利贞网.*','',cont)
        cont=re.sub(r'出生.*性别[；：]','',cont)
        cont=re.sub(r'神煞.*','',cont)
        cont=re.sub(r'\n{2}',"\n",cont)
        cont=re.sub(r'《周易》.*','',cont,flags=re.DOTALL)
        cont=cont.replace("?","")
        cont=cont.replace("<br>","\n")
        guaname=self.txtGuaName.text()
        # if "静卦" in guaname:
        #     cont=re.sub(r'')
        self.txtContent.setPlainText(cont)

    def deleteWaste(self):
        result=QMessageBox.information(None, "危险！", "当前帖子重复或数据无效，请确认将被删除！",QMessageBox.Ok)
        if result==QMessageBox.Ok:
            row = self.tableGua.currentRow()
            rowid = self.tableGua.item(row, 6).text()
            connection = sqlite3.connect(DB_NAME)
            cursor = connection.cursor()
            query='delete from  StockGuas  WHERE rowid = {}  '.format(rowid)
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            print("deleting is finished")
            self.loadInfo()
            self.tableGua.setCurrentCell(row, 1) 

    def removeRecord(self):
        QMessageBox.information(None, "警告！", "当前帖子将被移除到futures表格！")
        row = self.tableGua.currentRow()
        rowid = self.tableGua.item(row, 6).text()
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query1='insert into futures  select * from  StockGuas  WHERE rowid = {}  '.format(rowid)
        query2='delete from stockGuas where rowid={}  '.format(rowid)
        cursor.execute(query1)
        cursor.execute(query2)
        connection.commit()
        cursor.close()
        connection.close()
        print("deleting is finished")
        self.loadInfo()
        self.tableGua.setCurrentCell(row, 1) 

    def refreshMark(self):            
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query='update StockGuas set markdown=1 '+self.modestr
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def allInOneMarkdownHtml(self):
        diag=QFileDialog()
        options = diag.Options()
        QMessageBox.information(None, "注意", "搜索结果即将全部汇总写入HTML文件，文件默认目录为E:/stock6yao")
        htmldir = "c:/stock6yao/"
        xsize=self.tableGua.rowCount() 
        ysize=self.tableGua.columnCount()
        guaNameStr=self.txtSearchGuaName.text().strip()
        list=[]
        totalContent=""
        for x in range(0,xsize):
            stock=self.tableGua.item(x,2).text()
            if stock!="热点" and stock!="无名" and stock!="NULL" :
                cont=self.tableGua.item(x,5).text()
                totalContent=totalContent+cont+"\n---\n"
            # 将文本字段内容转义为 HTML 格式
        #escaped_text = html.escape(totalContent)
        #html_cont = escaped_text.replace("\n", "<br>")
        #html_content = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2">', html_cont)
        cont=totalContent.replace("\n","\n\n")
        html_content = markdown.markdown(cont, extensions=['extra'])
        html_header='''<style>
                        body  {color: black;  font-size: 12px; background-color: rgb(250, 240, 230);}
                        img {width:80%; height:auto; } 
                        </style>'''
        html_content=html_header+html_content
        defaultHtml = htmldir+f"{guaNameStr}.html"
        html_file, _ = diag.getSaveFileName(self, "保存文件", defaultHtml, "HTML Files (*.html);", options=options)
        if html_file:
            with open(html_file, 'w',encoding="utf-8") as file:
                file.write(html_content)
          #  html_file_git="D:/git/64gua.github.io/"+os.path.basename(html_file)
          #  shutil.copy(html_file, html_file_git)
        #print(html_file,html_file_git)
        # query='update StockGuas set markdown=1 where rowid={}  '.format(rowid)
            
    def paipan_action(self):
        day1=self.txtGuaDate.text()
        namestr=self.txtGuaName.text()
        sub1=self.txtSubject.text()+"\n"
        if day1=="":
            today=datetime.today()
            day1=today.strftime("%Y-%m-%d")
            self.txtGuaDate.setText(day1)
        guacont=sixyao.paipan(day1,namestr)
        self.txtContent.append(sub1+guacont)

    def refreshText(self):
        self.txtGuaName.clear()
        self.txtStockCode.clear()
        self.txtStockName.clear()
        self.txtGuaDate.clear()
        self.txtContent.clear()
        self.txtSubject.clear()
        self.label_pic.clear()
        self.insert_mode=True
        self.btn_save_markdown.setText("插入")

    def saveJPG(self):
        diag=QFileDialog()
        options = diag.Options()
        mddir = "c:/stock6yao/images/"
        secNum=self.txtStockCode.text()  
        originDay=self.txtGuaDate.text()
        filename=secNum+"_"+originDay+"_"+self.drawType+".jpg"
        defaultFile=mddir+filename
        print("defaultfile is : ", defaultFile)
        newfile, _ = diag.getSaveFileName(self, "保存文件", defaultFile, "jpg Files (*.jpg);; png file(*.png)", options=options)
        #newfile_git="D:/git/64gua.github.io/images/"+os.path.basename(newfile)
        print("save jpg as :", newfile)
        if newfile:
            src="temp100.jpg"
            shutil.copy(src, newfile)
         #   shutil.copy(newfile,newfile_git)
         #   print(newfile,newfile_git)
        mdlink="images/"+os.path.basename(newfile)
        self.txtContent.append( f'![]({mdlink})')
        
    
    def delete_useless_image(self):
        basedir="c:/stock6yao/"
      #  gitdir="D:/git/64gua.github.io/"
        QMessageBox.information(None, "警告", self.current_image+"此图片即将删除，需要删除？") 
        print(basedir+self.current_image)
        os.remove(basedir+self.current_image)
       # os.remove(gitdir+self.current_image)
        print(f"image in both folders: {self.current_image} has been Deleted! ")
    
    def generatePics(self):
        xsize=self.tableGua.rowCount() 
        mddir="C:/stock6yao/images/"
        #ysize=self.tableGua.columnCount()
        #self.drawType="D"
        for x in range(0,xsize):        
            postTitle=self.tableGua.item(x,0).text()
            stockDate=self.tableGua.item(x,1).text()
            rawStock=self.tableGua.item(x,2).text()
            guaContent=self.tableGua.item(x,5).text()
            rowid = self.tableGua.item(x, 6).text()
            stockCode,stockName=code2name.extractStockName(rawStock)
            re1=r'images.+jpg|images.+.jpeg|images.+png'
            images=re.findall(re1,guaContent)
            num=len(images)
            if stockCode=="NULL" or stockName=="NULL":
                stockCode,stockName=code2name.extractStockName(postTitle) 
            if stockCode=="NULL" or num>0:
                continue
            else:
                scr=akPlot.drawDailyLine(stockCode,stockDate,35)
                #pixmap=QPixmap(imgfile)
                filename=stockCode+"_"+stockDate+"_35d.jpg"
                # print(rowid,stockCode,stockDate,filename )
                newfile=mddir+filename
              #  newfile_git="D:/git/64gua.github.io/images/"+filename
                shutil.copy(scr, newfile)
              #  shutil.copy(scr, newfile_git)
                print(newfile+ " is created  OK")
                mdlink="images/"+os.path.basename(newfile)
                newguaContent=guaContent+"\n"+f'![]({mdlink})'
                connection = sqlite3.connect(DB_NAME)
                cursor = connection.cursor()
                query='UPDATE StockGuas  SET  guaContent ="{}" WHERE rowid = {}  '.format(newguaContent, rowid)
                cursor.execute(query)
                connection.commit()
                cursor.close()
                connection.close()
                print( "Content is changed  OK")
        print("batch saving images is OK")
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("金融易经案例库")
    window.show()
    sys.exit(app.exec_())
