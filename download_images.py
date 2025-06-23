import os
import re
import requests
import sys
from urllib.parse import urlparse

# --- 配置 ---
# 请在这里修改包含HTML文件的目录和网站基本URL
PAGE_DIRECTORY = 'page'
BASE_URL = 'https://aqitanai.chat'
# --- 配置结束 ---

def process_html_file(html_file_path, base_url):
    """
    下载HTML文件中的图片，并将文件中的URL替换为本地路径。
    """
    if not html_file_path or not os.path.exists(html_file_path):
        print(f"错误: 找不到HTML文件 '{html_file_path}'")
        return

    if not base_url:
        print("错误: 未提供基本URL。")
        return

    print(f"正在处理文件: {html_file_path}")

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"读取文件时出错 {html_file_path}: {e}")
        return

    # 正则表达式查找src, data-src, 和 srcset 属性中的URL
    # (?:...) 是一个非捕获组
    regex = r'(src|data-src|srcset)\s*=\s*["\']([^"\']+)["\']'
    matches = re.findall(regex, html_content)

    urls_to_download = set()
    for _, url_group in matches:
        # 处理srcset, 其中可能包含多个URL和宽度描述符
        parts = [p.strip().split()[0] for p in url_group.split(',')]
        for url in parts:
            if url:
                full_url = url
                if url.startswith("//"):
                    full_url = "https:" + url
                
                # 只处理属于目标网站的URL
                if base_url in full_url:
                    urls_to_download.add(full_url)

    # 下载图片
    for url in urls_to_download:
        try:
            parsed_url = urlparse(url)
            local_path = parsed_url.path.lstrip('/')
            
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                print(f"正在创建目录: {local_dir}")
                os.makedirs(local_dir, exist_ok=True)
            
            if not os.path.exists(local_path):
                print(f"正在下载 {url} 到 {local_path}")
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                print(f"文件已存在: {local_path}. 跳过下载。")

        except requests.exceptions.RequestException as e:
            print(f"下载失败 {url}: {e}")
        except Exception as e:
            print(f"处理时发生错误 {url}: {e}")

    # 在HTML内容中替换URL
    print("正在HTML文件中替换URL...")
    modified_html_content = html_content
    # 替换 http://, https://, 和 // 开头的URL
    base_domain = urlparse(base_url).netloc
    modified_html_content = re.sub(r'https?://' + re.escape(base_domain), '', modified_html_content)
    modified_html_content = re.sub(r'//' + re.escape(base_domain), '', modified_html_content)

    # 移除路径开头的斜杠，确保是相对路径
    modified_html_content = re.sub(r'(src|data-src|srcset)=["\']' + re.escape('/'), r'\1="', modified_html_content)


    try:
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(modified_html_content)
        print(f"成功更新文件: {html_file_path}")
    except Exception as e:
        print(f"写入文件时出错 {html_file_path}: {e}")
    
    print("处理完成。")


if __name__ == "__main__":
    if not os.path.isdir(PAGE_DIRECTORY):
        print(f"错误: 目录 '{PAGE_DIRECTORY}' 不存在。")
    else:
        print(f"开始处理目录 '{PAGE_DIRECTORY}' 下的所有HTML文件...")
        for filename in os.listdir(PAGE_DIRECTORY):
            if filename.lower().endswith('.html'):
                file_path = os.path.join(PAGE_DIRECTORY, filename)
                process_html_file(file_path, BASE_URL)
        print("所有HTML文件处理完毕。") 