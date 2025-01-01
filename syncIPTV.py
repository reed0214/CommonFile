import os
import requests


def download_and_save(link_dict, base_save_directory):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_save_directory = os.path.join(script_dir, base_save_directory)
    print(f"file download dir: {base_save_directory}")
    # 确保基础保存目录存在
    if not os.path.exists(base_save_directory):
        os.makedirs(base_save_directory)

    for directory, url in link_dict.items():
        try:
            print(f"now download {directory}")
            # 创建子目录
            save_directory = os.path.join(base_save_directory, directory)
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            # 从URL中提取文件名
            file_name = os.path.basename(url)
            if not file_name:
                file_name = "downloaded_content.txt"  # 如果URL没有文件名，使用默认名称

            # 文件保存的完整路径
            file_path = os.path.join(save_directory, file_name)

            # 发送HTTP请求获取内容
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功

            print(f"download complete {url}")
            # 如果文件已存在，则删除旧文件
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")

            print(f"deal content to {file_path}")
            headStr = '#EXTM3U x-tvg-url="https://live.fanmingming.cn/e.xml","https://epg.112114.xyz/pp.xml","http://epg.51zmt.top:8000/e.xml", "https://e.erw.cc/e.xml","http://epg.aptvapp.com/xml","https://epg.pw/xmltv/epg_CN.xml","https://epg.pw/xmltv/epg_HK.xml","https://epg.pw/xmltv/epg_TW.xml"'
            # 处理文件内容
            content = response.text

            # 替换第一行内容为 '12345'
            lines = content.splitlines()
            if lines:
                lines[0] = headStr
                content = '\n'.join(lines)

            # 替换所有 'https://live.fanmingming.com' 为 'https://live.fanmingming.cn'
            content = content.replace(
                'https://live.fanmingming.com', 'https://live.fanmingming.cn')

            # 保存内容到文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f"Downloaded and saved: {file_path}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")
        except OSError as e:
            print(f"Failed to delete or save file {file_path}: {e}")


# 示例链接字典，key为目录名，value为链接
link_dict = {
    "kimwang1978": "https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/refs/heads/main/merged_output.m3u",
    "guovin": "https://raw.githubusercontent.com/Guovin/iptv-api/refs/heads/gd/output/result.m3u",
    "yuanzl77": "https://raw.githubusercontent.com/yuanzl77/IPTV/refs/heads/main/live.m3u"
}

# 基础保存目录
base_save_directory = "m3u_file"

# 下载并保存文件
download_and_save(link_dict, base_save_directory)
