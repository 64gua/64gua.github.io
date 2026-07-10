#deepseek 支持
from aip import AipOcr
import re
from typing import Dict, Optional
import os
import csv
import pandas as pd
from pathlib import Path

# 在文件顶部定义常量
STOCK_CSV_FILE = "stock_and_etf.csv"
   
# def load_stock_mapping(csv_file: str = STOCK_CSV_FILE) -> dict:    

    # """
    # 加载股票映射表
    # 返回: {名称: 代码} 的字典
    # """
    # df = pd.read_csv(csv_file)
    
    # # 去除可能的空格，并过滤掉空值
    # df['code'] = df['code'].astype(str).str.strip()
    # df['name'] = df['name'].astype(str).str.strip()
    # # 过滤掉空名称或空代码
    # df = df[(df['name'] != '') & (df['name'] != 'nan') & (df['code'] != '') & (df['code'] != 'nan')]
    # # 构建映射：名称 -> 代码
    # name_to_code = dict(zip(df['name'], df['code']))
    
    # # 添加别名映射（可以扩展）
    # alias_map = {
    #     '上证': 'sh000001',
    #     '大盘': 'sh000001',
    #     '上证指数': 'sh000001',
    #     '深证': '399001',
    #     '深成指': '399001',
    #     '深圳成指': '399001',
    #     '创业板': '399006',
    #     '科创50': '000688',
    # }
    
    # # 合并映射（别名优先）
    # for alias, code in alias_map.items():
    #     name_to_code[alias] = code
    
    # return name_to_code


class YijingLocalParser:
    """
    本地解析易经卦象OCR文本，无需API
    """
    # ========== 类常量：所有实例共享 ==========
    STOCK_CSV_FILE = "stock_and_etf.csv"
    
    # 六十四卦映射（类变量，只加载一次）
    HEXAGRAM_MAP = {
        '乾为天': '乾', '坤为地': '坤', '水雷屯': '屯', '山水蒙': '蒙',
        '水天需': '需', '天水讼': '讼', '地水师': '师', '水地比': '比',
        '风天小畜': '小畜', '天泽履': '履', '地天泰': '泰', '天地否': '否',
        '天火同人': '同人', '火天大有': '大有', '地山谦': '谦', '雷地豫': '豫',
        '泽雷随': '随', '山风蛊': '蛊', '地泽临': '临', '风地观': '观',
        '火雷噬嗑': '噬嗑', '山火贲': '贲', '山地剥': '剥', '地雷复': '复',
        '天雷无妄': '无妄', '山天大畜': '大畜', '山雷颐': '颐', '泽风大过': '大过',
        '坎为水': '坎', '离为火': '离', '泽山咸': '咸', '雷风恒': '恒',
        '天山遁': '遁', '雷天大壮': '大壮', '火地晋': '晋', '地火明夷': '明夷',
        '风火家人': '家人', '火泽睽': '睽', '水山蹇': '蹇', '雷水解': '解',
        '山泽损': '损', '风雷益': '益', '泽天夬': '夬', '天风姤': '姤',
        '泽地萃': '萃', '地风升': '升', '泽水困': '困', '水风井': '井',
        '泽火革': '革', '火风鼎': '鼎', '震为雷': '震', '艮为山': '艮',
        '风山渐': '渐', '雷泽归妹': '归妹', '雷火丰': '丰', '火山旅': '旅',
        '巽为风': '巽', '兑为泽': '兑', '风水涣': '涣', '水泽节': '节',
        '风泽中孚': '中孚', '雷山小过': '小过', '水火既济': '既济', '火水未济': '未济'
    }
    
    # 全名列表（按长度排序，优先匹配长的）
    FULL_NAMES = sorted(HEXAGRAM_MAP.keys(), key=len, reverse=True)
    
    # 简称列表
    SHORT_NAMES = list(HEXAGRAM_MAP.values())

    # ========== 股票映射缓存（懒加载） ==========
    _stock_mapping: Optional[Dict[str, str]] = None   # code -> name
    _name_to_code: Optional[Dict[str, str]] = None    # name -> code

    def __init__(self, csv_file: str = STOCK_CSV_FILE):
        """
        初始化解析器
        
        Args:
            csv_file: 股票CSV文件路径
        """
        self.csv_file = csv_file
        self._ensure_stock_loaded()
    
    @classmethod
    def _ensure_stock_loaded(cls) -> None:
        """确保股票映射已加载（只加载一次）"""
        if cls._stock_mapping is None:
            print("📂 首次加载股票映射...")  # 调试用
            cls._load_stock_mapping()
    
    @classmethod
    def _load_stock_mapping(cls) -> None:
        """
        加载CSV文件，构建两个映射字典
        1. _stock_mapping: code -> name
        2. _name_to_code: name -> code
        """
        try:
            df = pd.read_csv(cls.STOCK_CSV_FILE, dtype=str)
        except FileNotFoundError:
            print(f"错误：找不到文件 {cls.STOCK_CSV_FILE}")
            cls._stock_mapping = {}
            cls._name_to_code = {}
            return
        except Exception as e:
            print(f"读取CSV文件出错：{e}")
            cls._stock_mapping = {}
            cls._name_to_code = {}
            return
        # 清理数据，保留前导零
        df['code'] = df['code'].astype(str).str.strip()
        df['name'] = df['name'].astype(str).str.strip()
        df = df.dropna(subset=['code', 'name'])
        df = df[df['code'] != '']
        df = df[df['name'] != '']
        
        # 构建两个映射
        cls._stock_mapping = dict(zip(df['code'], df['name']))
        cls._name_to_code = dict(zip(df['name'], df['code']))
        
        # 添加别名映射
        alias_map = {
            '上证': 'sh000001',
            '大盘': 'sh000001',
            '上证指数': 'sh000001',
            '深证': '399001',
            '深成指': '399001',
            '深圳成指': '399001',
            '创业板': '399006',
            '科创50': '000688',
        }
        
        # 别名也加入 name_to_code
        for alias, code in alias_map.items():
            cls._name_to_code[alias] = code
            if code not in cls._stock_mapping:
                cls._stock_mapping[code] = alias

    @classmethod
    def load_stock_mapping(cls) -> Dict[str, str]:
        """
        返回 name -> code 的映射字典（兼容原有接口）
        """
        cls._ensure_stock_loaded()
        return cls._name_to_code or {}
    
    def _extract_hexagram(self, text):
        """
        提取卦象，返回简称格式：
        - 有变卦（找到2个不同卦名）：简称之简称 (如：履之无妄)
        - 无变卦（只找到1个卦名）：简称静卦 (如：履静卦)
        """
        # 在全文中搜索所有出现的全名
        found_full_names = []
        for full_name in self.FULL_NAMES:
            if full_name in text:
                found_full_names.append(full_name)
        
        # 去重（保留顺序）
        seen = set()
        found_full_names = [x for x in found_full_names if not (x in seen or seen.add(x))]
        
        # 如果找到2个及以上不同的全名 → 有变卦
        if len(found_full_names) >= 2:
            # 根据在文本中出现的位置排序，确定本卦和变卦
            found_with_pos = []
            for full_name in found_full_names:
                pos = text.find(full_name)
                found_with_pos.append((pos, full_name))
            
            # 按位置排序（先出现的在前面）
            found_with_pos.sort(key=lambda x: x[0])
            
            # 第一个是本卦，第二个是变卦
            main_full = found_with_pos[0][1]
            change_full = found_with_pos[1][1]
            
            main_short = self.HEXAGRAM_MAP[main_full]
            change_short = self.HEXAGRAM_MAP[change_full]
            return f"{main_short}之{change_short}"
        
        # 如果只找到1个全名 → 静卦
        elif len(found_full_names) == 1:
            short = self.HEXAGRAM_MAP[found_full_names[0]]
            return f"{short}静卦"    
        return "未知卦"   

    def _extract_user(self, text) :
            # 模式可扩展：直接添加新用户即可
            patterns = {
                "金玉堂": r"金玉堂",
                "九戒": r"(?:用户9854|九戒)",
                "纪辰": r"详细资料",
                "天同": r"天同",
                "JUED": r"三七笔记",
                "风生水起":r"用户5P",
                "家艺":"家艺"
                # 未来扩展示例：
                # "张三": r"张三|用户1234",
                # "李四": r"李四|管理员",
            }
            
            for user, pattern in patterns.items():
                if re.search(pattern, text):
                    return user
            
            return "未知用户"
        
    def _extract_stock_from_topic(self, text) :
        """
        Returns:
            (code, name) 如果找到，返回(代码, 名称)；否则返回(None, None)
        """
        # 确保已加载
        code="未知代号"
        name="未知名字"
        self._ensure_stock_loaded()
        
        if not self._stock_mapping:
            return code, name
        
        # 1. 优先匹配6位数字的股票代码
        code_pattern = r'\b(\d{6})\b'
        found_codes = re.findall(code_pattern, text)
        
        for code in found_codes:
            # 精确匹配原始代码
            if code in self._stock_mapping:
                return code, self._stock_mapping[code]
            
            # 去掉前导零匹配（处理CSV中代码被转成数字的情况）
            stripped = str(int(code))
            for stock_code, stock_name in self._stock_mapping.items():
                if stock_code.lstrip('0') == stripped:
                    return stock_code, stock_name
        
        # 2. 如果没找到代码，匹配股票名称（处理全半角）
        full_to_half = str.maketrans(
            'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ',
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        )
        normalized_text = text.translate(full_to_half)
        for name, code in self._name_to_code.items():
            if name and name != '':
                normalized_name = name.translate(full_to_half)
                escaped_name = re.escape(normalized_name)
                if re.search(escaped_name, normalized_text, re.IGNORECASE):
                    return code, name       
        return code, name
    
    def _extract_time_and_date(self, text) :
        datestr="未知日期"
        timestr="未知时间"
        # 1. 提取日期
        date_match = re.search(r'(\d{4})[-年/.](\d{1,2})[-月/.](\d{1,2})', text)
        datestr = f"{date_match.group(1)}-{date_match.group(2).zfill(2)}-{date_match.group(3).zfill(2)}"
        
        # 2. 提取时间
        time_match = re.search(
            r'(\d{4})[-年/.](\d{1,2})[-月/.](\d{1,2})[日]?\s*(\d{1,2})[时:：](\d{2})[分]?', 
            text
        )    
        if time_match:
            hour = int(time_match.group(4))
            minute = int(time_match.group(5))
            if 0 <= hour < 24 and 0 <= minute < 60:
                timestr = f"{hour:02d}:{minute:02d}"
        return datestr,timestr
    
    def parse(self, ocr_text: str) -> Dict[str, str]:
            result = {
                "date": "",
                "time": "",
                "hexagram": "",
                "topic": "",
                "stock_code": "",  
                "stock_name": "",   
                "user":""
            }

            # 1. 提取日期
            datestr,timestr=self. _extract_time_and_date(ocr_text)
            result['date']=datestr
            result['time']=timestr
            # 3. 提取卦象
            hexagram_result = self._extract_hexagram(ocr_text)
            if hexagram_result:
                result["hexagram"] = hexagram_result               
            # 4. 提取主题
            topic_patterns = [
                r'(?:占问|事项|主题|占事|问事|标题)\s*[:：]?\s*\n?\s*([^\n]+)',
                r'\([男女]?占\)\s*([^\n]+)',
                r'(?:^|\n)(?:占问|事项|主题|占事|问事|标题)\s*\n\s*([^\n]+)',
            ]
            for pattern in topic_patterns:
                topic_match = re.search(pattern, ocr_text, re.MULTILINE)
                if topic_match:
                    result["topic"] = topic_match.group(1).strip()
                    break
            # 去除主题中的所有逗号（全角和半角）
            if result["topic"]:
                result["topic"] = result["topic"].replace('，', '').replace(',', '')

            # 5. 从主题中提取股票信息
            if result["topic"]:
                stock_code,stock_name = self._extract_stock_from_topic(result["topic"])         
                result["stock_code"] = stock_code
                result["stock_name"] = stock_name
            # 6. 提取用户名
            result["user"]=self._extract_user(ocr_text)
            
            return result
      

def baiduOCR(picfile):
    APP_ID='30244035'
    API_KEY='hZU6fDI7MP6iG5bFaXtIGcsk'
    SECRET_KEY = 'QGChDbrUKMwxMONN1tWnm24a6ZKz91We'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    print("clinet connection is OK!")
    with open(picfile, 'rb') as i:
        img = i.read()
    message = client.basicGeneral(img)
    # 提取所有文字并合并
    words = [item.get('words') for item in message.get('words_result', [])]
    result_text = '\n'.join(words)
    print(result_text)
    return result_text

def process_all_images( image_folder,  output_csv, columns: list = None):
    # 默认全部列
    if columns is None:
        columns = ['图片文件', '卦象', '日期', '股票代码', '主题']
    
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    # 获取所有图片文件
    image_files = []
    for file in os.listdir(image_folder):
        if os.path.splitext(file)[1].lower() in image_extensions:
            image_files.append(file)
    
    if not image_files:
        print(f"在 {image_folder} 中未找到图片文件")
        return
    
    image_files.sort()
    print(f"找到 {len(image_files)} 张图片，开始处理...")
    
    parser = YijingLocalParser()
    results = []
    
    for idx, image_file in enumerate(image_files, 1):
        image_path = os.path.join(image_folder, image_file)
        print(f"\n[{idx}/{len(image_files)}] 处理: {image_file}")
        
        try:
            ocr_result = baiduOCR(image_path)
            result = parser.parse(ocr_result)
            print(result)
            combined_topic = f"{result['topic']}-{result['user']}-{result['time']}"
         
            row = {
                '图片文件': image_file,
                '卦象': result['hexagram'] or '未识别',
                '日期': result['date'] or '未识别',
                '股票代码': result.get('stock_code', '') or '未识别',
                '主题': combined_topic,
            }
            
            results.append(row)
            print(f"  ✅ 卦象: {result['hexagram']}, 主题: {result['topic']}")
            
        except Exception as e:
            print(f"  ❌ 处理失败: {e}")
            results.append({col: '识别失败' for col in columns})
    
    # 只保留指定的列
    filtered_results = [{col: row.get(col, '') for col in columns} for row in results]
    
    # 写入CSV
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(filtered_results)
    
    success_count = sum(1 for r in results if r.get('卦象', '') not in ['识别失败', '未识别'])
    print(f"\n✅ 处理完成！共处理 {len(results)} 张图片")
    print(f"📊 结果已保存到: {output_csv}")
    print(f"📈 成功识别: {success_count}/{len(results)} 张")

def clear_first_column(csv_name):
# 读取文件
    csv_clean=csv_name
    df = pd.read_csv(csv_name)
    # 删除第一列
    df = df.drop(df.columns[0], axis=1)
    # 另存文件
    p = Path(csv_name)
    new_csv = str(p.with_name(f"{p.stem}_clean{p.suffix}"))
    df.to_csv(new_csv, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    # 批量识别指定文件夹
    image_folder = "C:/Users/1/Desktop/wechatImage/0706"
    output_csv = image_folder+"/result_first.csv"
    # process_all_images(image_folder, output_csv)
    clear_first_column(output_csv)
    print("OK!.......")
    # #单独识别某个图
    # image="testimg/jued1.jpg"
    # ocr_result=baiduOCR(image)
    # parser = YijingLocalParser()
    # print(ocr_result)
    # result = parser.parse(ocr_result)
    # print(f"📅 日期: {result['date']}")
    # print(f"🕐 时间: {result['time']}")
    # print(f"☯ 卦象: {result['hexagram']}")
    # print(f"📝 主题: {result['topic']}")
    # print(f"📝 股票代码: {result['stock_code']}")
    # print(f"📝 股票名: {result['stock_name']}")
    # print(f"📝 用户: {result['user']}")

