# 数据爬取
import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    print(f"正在抓取页面: {url}")
    try:
        # 增加 timeout 防止程序无响应，增加 headers 模拟浏览器
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status() # 检查请求是否成功
        # 自动识别网页编码，避免强制 GBK 导致 UTF-8 网页出现“骞/鏈”乱码
        resp.encoding = resp.apparent_encoding
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')

        tr_list = soup.find_all('tr')
        dates, conditions, temp = [], [], []
        # 检查是否获取到数据行
        if len(tr_list) <= 1:
            print(f"警告: 页面 {url} 未找到数据行。")
            return pd.DataFrame()

        for data in tr_list[1:]:
            sub_data = data.text.split()
            if len(sub_data) < 4:
                continue
            
            # 清洗数据：去除多余的字符和空格
            date_str = sub_data[0].replace('/', '').strip()
            # 拼接天气状况和气温，并去除多余的斜杠
            condition_str = ''.join(sub_data[1:3]).replace('/', '').strip()
            temp_str = ''.join(sub_data[3:6]).replace('/', '').strip()
            
            dates.append(date_str)
            conditions.append(condition_str)
            temp.append(temp_str)
        
        _data = pd.DataFrame()
        _data['日期'] = dates
        _data['天气状况'] = conditions
        _data['气温'] = temp
        
        print(f"成功获取 {len(_data)} 条数据。")
        return _data
    except Exception as e:
        print(f"抓取 {url} 时出错: {e}")
        return pd.DataFrame()

# 定义要抓取的月份列表
months = [
    '202305', '202306', '202307', '202308', '202309', '202310',
    '202311', '202312', '202401', '202402', '202403', '202404',
    '202405', '202406', '202407', '202408', '202409', '202410',
    '202411', '202412', '202501', '202502', '202503', '202504',
    '202505', '202506', '202507', '202508', '202509', '202510',
    '202511', '202512', '202601', '202602'
]

all_data = []
for month in months:
    url = f'https://www.tianqihoubao.com/lishi/nanjing/month/{month}.html'
    df = get_data(url)
    if not df.empty:
        all_data.append(df)
    time.sleep(1)

if all_data:
    data = pd.concat(all_data).reset_index(drop=True)
    filename = '南京2023年5月到2026年2月天气情况.csv'
    
   
    def save_file(df, name):
        try:
            df.to_csv(name, index=False, encoding='gb18030', errors='replace')
            print(f"\n成功！所有数据已保存至: {name}")
            return True
        except PermissionError:
            print(f"\n[错误] 无法保存到 {name}，文件可能正在被 Excel 打开。")
            return False
        except Exception as e:
            print(f"\n[错误] 保存文件时发生未知错误: {e}")
            return False


    if not save_file(data, filename):
        new_name = f"南京天气数据_{int(time.time())}.csv"
        print(f"请关闭 Excel 窗口后重试。为了防止数据丢失，我正尝试存为新文件: {new_name}")
        save_file(data, new_name)
else:
    print("\n未能抓取到任何数据。")
