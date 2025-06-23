import requests
from bs4 import BeautifulSoup
import os
import json
import re
import time

# 从articles.json加载文章数据
try:
    with open('articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
except FileNotFoundError:
    print("错误: articles.json 文件未找到。")
    exit()
except json.JSONDecodeError:
    print("错误: articles.json 文件格式不正确。")
    exit()

# 确保 'page' 文件夹存在
output_dir = 'page'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历所有文章
for article in articles:
    url = article.get('href')
    if not url:
        continue

    # 从URL中提取文章ID
    match = re.search(r'(\d+)\.html$', url)
    if not match:
        continue
    
    page_id = match.group(1)
    file_path = os.path.join(output_dir, f'{page_id}.html')

    # 如果文件已存在，则跳过
    if os.path.exists(file_path):
        print(f"文件 {file_path} 已存在，跳过。")
        continue

    try:
        # 发送HTTP请求获取页面内容
        print(f"正在抓取: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # 如果请求失败则抛出异常

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找具有指定class的元素
        header_element = soup.find(class_="entry-header")
        content_element = soup.find(class_="entry-content u-text-format u-clearfix")

        if header_element and content_element:
            # 将找到的元素的HTML内容保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(header_element.prettify())
                f.write(content_element.prettify())
            print(f"成功将内容保存到 {file_path}")
        else:
            if not header_element:
                print(f"在 {url} 中未找到 class='entry-header' 的元素。")
            if not content_element:
                print(f"在 {url} 中未找到 class='entry-content u-text-format u-clearfix' 的元素。")
        
        # 增加延迟以避免对服务器造成过大压力
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"请求URL时出错 ({url}): {e}")
    except Exception as e:
        print(f"处理 {url} 时发生错误: {e}")

print("所有文章处理完成。") 