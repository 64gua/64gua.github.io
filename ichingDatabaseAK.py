#2024-6-24 v1.2
import sys, shutil,os,re
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QUrl
from decimal import Decimal
import sqlite3
import sixyao
import akshare_plotly as akPlot
import html, markdown

main_ui = "db_search2.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(main_ui)
insert_ui="insert_db.ui"
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
            gua=items[0]
            day=items[1]
            code=items[2]
            subject=items[3]
            query = (gua,code,day)
            conn = sqlite3.connect('Guas.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM stockGuas WHERE guaName=? and stockName=? and guaDate=?   ',query)
            db_result=cursor.fetchall()
            if len(db_result)==0:
                tuple=(gua, day,code,subject)
                cursor.execute("INSERT INTO stockGuas (guaName, guaDate,stockname,guaSubject)  VALUES (?,?,?,?)", tuple )
                print(i,'csv record inserted Successfully')
            else:
                print(i, "Record already exists!......")
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
        self.btn_search.clicked.connect(lambda: self.loadInfo(1))
        self.btn_search_bytime.clicked.connect(lambda: self.loadInfo(0))
        self.btn_title.clicked.connect(lambda: self.loadInfo(2))
        self.btn_draw.clicked.connect(self.drawPicture)
        self.tableGua.cellDoubleClicked.connect(self.displayGua)
        self.btn_save_markdown.clicked.connect(self.saveAction)
        self.txtStockCode.editingFinished.connect(self.renewStockName)
        self.txtStockName.editingFinished.connect(self.renewStockCode)
        self.btn_paipan.clicked.connect(self.paipan)
        self.btn_save_img.clicked.connect(self.saveJPG)
        self.actDelete.triggered.connect(self.deleteWaste)
        self.actRemove.triggered.connect(self.removeRecord)
        self.act_all_in.triggered.connect(self.allInOneMarkdownHtml)
        self.act_new.triggered.connect(self.refreshText)
        self.act_generate_pics.triggered.connect(self.generatePics)
        self.act_save_new.triggered.connect(self.insertNewRecord)
        self.btn_wash.clicked.connect(self.washContent)
        self.btn_del_image.clicked.connect(self.delete_useless_image)
        self.radioButton_html.toggled.connect(self.htmlformat)
        self.act_insert_data.triggered.connect(self.openNewWindow)
        self.spinBox.valueChanged.connect(self.displayImages)
        self.insert_mode=False

    def openNewWindow(self):
        self.window2 = MyWindow2()
        self.window2.show()
        
    def loadInfo (self,searchmode) :
        self.mode=searchmode
        connection=sqlite3.connect('Guas.db')
        cursor=connection.cursor()
        mainsql='select postTitle,guaDate, stockName,guaName,user,guaContent,CAST(rowid as text),guaSubject, cast(markdown as text) from StockGuas '
        orderby= '  order by cast( substr(guaDate,6,2) as integer),guaDate '
        if searchmode==1:  #按照卦名搜索
            self.txtTitle.setText("")
            self.txtEndDay.setText("")
            self.txtStartDay.setText("")
            str=self.txtSearchGuaName.text().strip()
            self.modestr=f'where guaName like "{str}"  '
        elif searchmode==0:  #按照时间段搜索
            self.txtSearchGuaName.setText("")
            self.txtTitle.setText("")
            startday=self.txtStartDay.text().strip()
            endday=self.txtEndDay.text().strip()
            self.modestr=f'where guaDate between"{startday}" and "{endday}"   ' 
        elif searchmode==2:  #按照帖子标题搜索
            self.txtStartDay.setText("")
            self.txtEndDay.setText("")
            self.txtSearchGuaName.setText("")
            str=self.txtTitle.text().strip()
            self.modestr=f'where guaSubject like "%{str}%"    ' 
        query=mainsql+self.modestr+orderby
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
        stockCode,stockName=akPlot.extractStockName(rawStock)
        if stockCode=="NULL" or stockName=="NULL":
            stockCode,stockName=akPlot.extractStockName(postTitle)
        self.txtStockCode.setText(stockCode)
        self.txtStockName.setText(stockName)
        self.txtGuaDate.setText(gDate)
        self.txtGuaName.setText(guaName)
        self.txtSubject.setText(guaSubject)
        self.radioButton_30d.setChecked(True)
        self.content_md_format=guaContent
        self.displayImages()

    def displayImages(self):
        cont=self.content_md_format
        print("cont:",cont)
        re1=r'images.+jpg|images.+.jpeg|images.+png'
        images=re.findall(re1,cont)
        num=len(images)
        self.label_num_of_images.setText(f'{num}张图')
        #self.spinBox.setMinimum(0)
        #self.spinBox.setMaximum(num-1)
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
            pixmap=QPixmap("taiji.png")     
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

    def drawpicDaily(self,days):
        self.drawType=f'{days}d'
        guaDate=self.txtGuaDate.text()
        stockCode=self.txtStockCode.text()
        dateOrigin=guaDate
        imgfile=akPlot.drawDailyLine(stockCode,dateOrigin,time_period=days)
        print(imgfile)
        pixmap=QPixmap(imgfile)
        self.label_pic.setPixmap(pixmap)
        if imgfile=="alert.png":
            QMessageBox.information(None, "警告", "股票名字或代号出错，是否退市？") 

    def drawpicMonth(self):
        self.drawType="Y"
        guaDate=self.txtGuaDate.text()
        stockCode=self.txtStockCode.text()
        dateOrigin=guaDate
        imgfile=akPlot.drawMonthLine(stockCode,dateOrigin)
        print(imgfile)
        pixmap=QPixmap(imgfile)
        self.label_pic.setPixmap(pixmap) 
        if imgfile=="alert.png":
            QMessageBox.information(None, "警告", "股票名字或代号出错，是否退市？")  
    
    def drawPicture(self):
        print(" button draw is checked!")
        if self.txtStockCode.text()=="NULL" or self.txtGuaDate.text()=="NULL":
            QMessageBox.information(None, "警告", "缺少股票代号或日期？")
            return
        if self.radioButton_365d.isChecked():
            self.drawpicMonth()
        else:
            if self.radioButton_15d.isChecked():
                days=15  
            if self.radioButton_30d.isChecked():
                days=35
            if self.radioButton_60d.isChecked():
                days=60
            self.drawpicDaily(days)
        
    def saveAction(self):
        if self.insert_mode == True:
            self.insertNewRecord()
            self.refreshText()
            self.btn_save_markdown.setText("更新正文")
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
        connection = sqlite3.connect('Guas.db')
        cursor = connection.cursor()
        query='UPDATE StockGuas  SET guaDate="{}", stockName = "{}", guaName="{}", guaContent ="{}",guaSubject="{}"  WHERE rowid = {}  '.format( new_guaDate, new_stockCode, new_guaName, new_content, new_subject, rowid)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        print("saving Change is OK")
        self.loadInfo(self.mode)
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
        conn = sqlite3.connect('Guas.db')
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
        cont=re.sub(r'\n{2}',"\n",cont)
        cont=cont.replace("?","")
        cont=cont.replace("<br>","\n")
        self.txtContent.setPlainText(cont)

    def deleteWaste(self):
        QMessageBox.information(None, "危险！", "当前帖子重复或数据无效，请确认将被删除！")
        row = self.tableGua.currentRow()
        rowid = self.tableGua.item(row, 6).text()
        connection = sqlite3.connect('Guas.db')
        cursor = connection.cursor()
        query='delete from  StockGuas  WHERE rowid = {}  '.format(rowid)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        print("deleting is finished")
        self.loadInfo(self.mode)
        self.tableGua.setCurrentCell(row, 1) 

    def removeRecord(self):
        QMessageBox.information(None, "警告！", "当前帖子将被移除到futures表格！")
        row = self.tableGua.currentRow()
        rowid = self.tableGua.item(row, 6).text()
        connection = sqlite3.connect('Guas.db')
        cursor = connection.cursor()
        query1='insert into futures  select * from  StockGuas  WHERE rowid = {}  '.format(rowid)
        query2='delete from stockGuas where rowid={}  '.format(rowid)
        cursor.execute(query1)
        cursor.execute(query2)
        connection.commit()
        cursor.close()
        connection.close()
        print("deleting is finished")
        self.loadInfo(self.mode)
        self.tableGua.setCurrentCell(row, 1) 

    def refreshMark(self):            
        connection = sqlite3.connect('Guas.db')
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
            html_file_git="E:/git/64gua.github.io/"+os.path.basename(html_file)
            shutil.copy(html_file, html_file_git)
        print(html_file,html_file_git)
        # query='update StockGuas set markdown=1 where rowid={}  '.format(rowid)
            
    def paipan(self):
        gua=sixyao.Zhugua()
        day1=self.txtGuaDate.text()
        namestr=self.txtGuaName.text()
        if day1=="" or namestr=="":
            QMessageBox.information(None, "危险！", "没有卦名和日期，无法排卦！")
            return        
        if '之' in namestr:
            split_string=self.txtGuaName.text().split('之')
            name1 = split_string[0].strip() 
            name2 = split_string[1].strip() 
        else:
            name1=namestr.strip("静卦")
            name2=namestr.strip("静卦")
        gzstring=gua.setDate(day1)
        gua.makeGuaByName(name1,name2)
        #outname,guacont=gua.displayDoubleGuaText()
        outGuaName,guacont=gua.displayDoubleGuaText()
        self.txtContent.append(guacont)

    def refreshText(self):
        self.txtGuaName.clear()
        self.txtStockCode.clear()
        self.txtStockName.clear()
        self.txtGuaDate.clear()
        self.txtContent.clear()
        self.txtSubject.clear()
        self.label_pic.clear()
        self.insert_mode=True
        self.btn_save_markdown.setText("插入新记录")

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
        newfile_git="E:/git/64gua.github.io/images/"+os.path.basename(newfile)
        print("save jpg as :", newfile)
        if newfile:
            src="temp100.jpg"
            shutil.copy(src, newfile)
            shutil.copy(newfile,newfile_git)
            print(newfile,newfile_git)
        mdlink="images/"+os.path.basename(newfile)
        self.txtContent.append( f'![]({mdlink})')
        
    
    def delete_useless_image(self):
        basedir="c:/stock6yao/"
        gitdir="E:/git/64gua.github.io/"
        QMessageBox.information(None, "警告", self.current_image+"此图片即将删除，需要删除？") 
        print(basedir+self.current_image)
        os.remove(basedir+self.current_image)
        os.remove(gitdir+self.current_image)
        print(f"image in both folders: {self.current_image} has been Deleted! ")
    
    def renewStockName(self):   #可以同时搜索股票和ETF
        code=self.txtStockCode.text()
        name=akPlot.findname_stock(code)
        self.txtStockName.setText(name)

    def renewStockCode(self):  #可以同时搜索股票和ETF
        name=self.txtStockName.text()
        code=akPlot.findcode_stock(name)
        code=code.replace("sh","").replace("sz","")
        self.txtStockCode.setText(code)

    def generatePics(self):
        xsize=self.tableGua.rowCount() 
        mddir="../images/"
        #ysize=self.tableGua.columnCount()
        #self.drawType="D"
        for x in range(0,xsize):
            rowid = self.tableGua.item(x, 6).text()
            postTitle=self.tableGua.item(x,0).text()
            rawStock=self.tableGua.item(x,2).text()
            guaContent=self.tableGua.items[x,5].text()
            stockCode,stockName=akPlot.extractStockName(rawStock)
            if stockCode=="NULL" or stockName=="NULL":
                stockCode,stockName=akPlot.extractStockName(postTitle)
            stockDate=self.tableGua.item(x,1).text()
            scr=akPlot.drawDailyLine(stockCode,stockDate)
            #pixmap=QPixmap(imgfile)
            filename=secNum+"_"+originDay+"_D.jpg"
            newfile=mddir+filename
            shutil.copy(src, newfile)
            mdlink="images/"+os.path.basename(newfile)
            newguaContent=guaContent+f'![]({mdlink})'
            connection = sqlite3.connect('Guas.db')
            cursor = connection.cursor()
            query='UPDATE StockGuas  SET  guaContent ="{}" WHERE rowid = {}  '.format(newguaContent, rowid)
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
        print("batch saving images is OK")
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("金融易经案例库")
    window.show()
    sys.exit(app.exec_())