
#2024-11-29 给数据库增加干支字段，亥月酉日
import sqlite3
import re
import datetime, sxtwl
import sixyao
tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
dicXunKong={"戌亥": ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉'],
            "申酉":['甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未'],
            "午未": ['甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳'],
            "辰巳":['甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯'],
            "寅卯": ['甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑'],
            "子丑":['甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥']  
              }

def gangzhibystr (datestring="2023-02-04"):
    d=datetime.datetime.strptime(datestring, "%Y-%m-%d")
    cdate = sxtwl.fromSolar(d.year, d.month, d.day)
    #return [ tiangan[cdate.getYearGZ().tg] + dizhi[cdate.getYearGZ().dz],
    #           tiangan[cdate.getMonthGZ().tg] + dizhi[cdate.getMonthGZ().dz],
    #           tiangan[cdate.getDayGZ().tg] + dizhi[cdate.getDayGZ().dz] ] 
    gangzhi_month_day=tiangan[cdate.getMonthGZ().tg]+dizhi[cdate.getMonthGZ().dz]+"月"+tiangan[cdate.getDayGZ().tg]+dizhi[cdate.getDayGZ().dz]+"日"
    return gangzhi_month_day
                    
def xunkong_count(datestring):
    d=datetime.datetime.strptime(datestring, "%Y-%m-%d")
    cdate = sxtwl.fromSolar(d.year, d.month, d.day)
    #return [ tiangan[cdate.getYearGZ().tg] + dizhi[cdate.getYearGZ().dz],
    #           tiangan[cdate.getMonthGZ().tg] + dizhi[cdate.getMonthGZ().dz],
    #           tiangan[cdate.getDayGZ().tg] + dizhi[cdate.getDayGZ().dz] ] 
    gangzhi_of_day=tiangan[cdate.getDayGZ().tg] + dizhi[cdate.getDayGZ().dz]
    print(gangzhi_of_day)
    for key, values in dicXunKong.items():
        if gangzhi_of_day in values:
            return key
     
def add_gangzhi():
    conn = sqlite3.connect('C:/stock6yao/Guas.db')
    #conn = sqlite3.connect('C:/stock6yao/Guas_back.db')
    cursor = conn.cursor()
    #cursor.execute("ALTER TABLE student ADD COLUMN year INTEGER")
    cursor.execute("SELECT rowid, guaDate, gangZhi, guaName FROM stockGuas")
    rows = cursor.fetchall()
    i=0
    for row in rows:
        rowid = row[0]
        gua_date_string = row[1]
        gangzhi=row[2]
        guaname=row[3]
        # if gua_date_string!="NULL" and "-" in gua_date_string and  gangzhi==None:
        if gua_date_string!="NULL" and "-" in gua_date_string and  gangzhi==None:
        # if gangzhi==None:
            i=i+1
            print(rowid, gua_date_string,gangzhi,guaname, i)
            gangzhi = gangzhibystr(gua_date_string)   
            print(rowid, gua_date_string,gangzhi,guaname, i)
            cursor.execute("UPDATE stockGuas SET gangZhi = ? WHERE rowid = ?", (gangzhi, rowid))
            conn.commit()  
            print(i," is OK!")    
    conn.close()

def add_xunkong():
    conn = sqlite3.connect('C:/stock6yao/Guas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, guaDate,gangZhi, xunKong FROM stockGuas")
    rows = cursor.fetchall()
    i=0
    for row in rows:
        rowid = row[0]
        gua_date_string = row[1]
        gangzhi=row[2]
        xunkong_text=row[3]
        pattern=r'^\d{4}-\d{2}-\d{2}$'
        # print(rowid, gua_date_string,gangzhi,xunkong_text, i)
        if gangzhi!="NULL" and re.match(pattern,gua_date_string) and  xunkong_text==None:
            i=i+1
            xunkongstr = xunkong_count(gua_date_string)
            print(rowid, gua_date_string, xunkongstr, i)
            cursor.execute("UPDATE stockGuas SET xunKong = ? WHERE rowid = ?", (xunkongstr, rowid))
            conn.commit()
            print(i,"is ok!")
    conn.close()


def add_gong():
    conn = sqlite3.connect('C:/stock6yao/Guas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, guaDate, guaName,gong FROM stockGuas")
    rows = cursor.fetchall()
    i=0
    for row in rows:
        rowid = row[0]
        gua_date_string = row[1]
        guaname=row[2]
        gong=row[3]
        if gua_date_string!="NULL" and "-" in gua_date_string and  gong==None:
            i=i+1
            gong=sixyao.countGongByName(guaname)
            print(rowid, gua_date_string,gong, i)
            cursor.execute("UPDATE stockGuas SET gong = ? WHERE rowid = ?", (gong, rowid))
            conn.commit()  
            print(i," is OK!")    
    conn.close()

def add_xunkong():
    conn = sqlite3.connect('C:/stock6yao/Guas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, guaDate,gangZhi, xunKong FROM stockGuas")
    rows = cursor.fetchall()
    i=0
    for row in rows:
        rowid = row[0]
        gua_date_string = row[1]
        gangzhi=row[2]
        xunkong_text=row[3]
        pattern=r'^\d{4}-\d{2}-\d{2}$'
        # print(rowid, gua_date_string,gangzhi,xunkong_text, i)
        if gangzhi!="NULL" and re.match(pattern,gua_date_string) and  xunkong_text==None:
            i=i+1
            xunkongstr = xunkong_count(gua_date_string)
            print(rowid, gua_date_string, xunkongstr, i)
            cursor.execute("UPDATE stockGuas SET xunKong = ? WHERE rowid = ?", (xunkongstr, rowid))
            conn.commit()
            print(i,"is ok!")
    conn.close()



if __name__ == "__main__": 
    gangzhi=gangzhibystr("2026-01-23")
    print(gangzhi)
    add_gangzhi()
    add_xunkong()
    # gong1=sixyao.countGongByName("旅之丰")
    add_gong()
    print("everything is OK!!!")
    
    #2024-11-29 经数据库增加干支字段，亥月酉日
    

