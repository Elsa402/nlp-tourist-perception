import requests
import os
import time

# === Step 1: 替换为你的 DeepL API Key ===
DEEPL_API_KEY = '我的DeeL API key'  # <<< 替换这里

# === Step 2: 文件路径设置 ===
input_file = '/Users/elsa/Desktop/爬虫学习/0721学习/翻译失败汇总_副本1.txt'
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'translated_output_副本1.txt')

# === Step 3: 翻译函数（使用 DeepL） ===
def deepl_translate(text, target_lang='ZH'):
    url = 'https://api-free.deepl.com/v2/translate'
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'target_lang': target_lang
    }
    try:
        response = requests.post(url, data=params)
        result = response.json()
        if 'translations' in result:
            return result['translations'][0]['text']
        else:
            print("翻译失败:", result)
            return text
    except Exception as e:
        print("请求出错:", e)
        return text

# === Step 4: 逐行读取 + 翻译 + 写出 ===
with open(input_file, 'r', encoding='utf-8') as fin:
    lines = fin.readlines()

total_lines = len(lines)
with open(output_file, 'w', encoding='utf-8') as fout:
    for idx, line in enumerate(lines):
        parts = line.strip().split(',', 2)
        if len(parts) == 3:
            row, col, text = parts
            if text.strip():
                translated = deepl_translate(text)
                time.sleep(0.5)
            else:
                translated = ''
            fout.write(f"{row},{col},{translated}\n")
        else:
            fout.write(line)
        fout.flush()  # 立即刷新到文件
        os.fsync(fout.fileno())  # 强制写入磁盘

        # 显示进度条
        progress = (idx + 1) / total_lines * 100
        print(f"\r翻译进度：{progress:.2f}%", end='')

print(f"\n✅ 翻译完成，文件已保存到：{output_file}")
