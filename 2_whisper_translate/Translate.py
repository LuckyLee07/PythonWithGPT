# -*- coding: UTF-8 -*-
import re
import os
import time
import html
import pytube
import random
import shutil
import subprocess
from urllib import parse
import requests

GOOGLE_TRANSLATE_URL = 'http://translate.google.com/m?q=%s&tl=%s&sl=%s'


# 1、使用ffmpeg将视频转换成F16形式的音频
def mp4_to_wav_ffmpeg(mp4_path, wav_dir):
    dir_, file = os.path.split(mp4_path)
    wav_path = os.path.join(wav_dir, file.replace('.mp4', '.wav'))
    if os.path.exists(wav_path): os.remove(wav_path)

    cmd = ['ffmpeg', '-i', mp4_path, '-ar', '16000', '-ac', '2', '-c:a', 'pcm_s16le', wav_path]
    result = subprocess.run(cmd, shell=False)
    print(f"Command1=====>>>: {' '.join(result.args)}")


# 2、使用编译好的Whisper将音频转换成文字
def wav_to_text_whisper(wav_path, text_dir):
    #whisper_bin = f'{whisper}/main'
    cmd = ['./main', '-f', wav_path, '-m', model_bin, '-otxt']
    result = subprocess.run(cmd, shell=False)
    print(f"Command2=====>>>: {' '.join(result.args)}")

    text_path = wav_path + '.txt'
    if os.path.exists(text_path): #移动字幕到其他目录下
        new_text_path = text_path.replace('.wav', '')
        if os.path.exists(new_text_path): 
            os.remove(new_text_path)
        os.rename(text_path, new_text_path)
        
        dir_, file = os.path.split(new_text_path)
        dst_path = os.path.join(text_dir, file)
        if os.path.exists(dst_path): os.remove(dst_path)
        shutil.move(new_text_path, text_dir) #先删除目标文件再移动


# 3、调用Google翻译将文字翻译成中文或其他语言
def translate_google(text, to_language="auto", text_language="auto"):
    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text,to_language,text_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        raise Exception("error->", text)

    return html.unescape(result[0])


def file_translate_google(filepath):
    can_trans_flag = False
    orgin_text, trans_text = '',''
    with open(filepath, 'r') as reader:
        all_lines = reader.read().split('\n')
        trans_line_count = 0
        for index, line in enumerate(all_lines, 1):
            orgin_text = orgin_text + line +'\n'
            trans_line_count = trans_line_count + 1

            if trans_line_count >= 20:
                if line.strip().endswith(('.','!','?')):
                    can_trans_flag = True
                    trans_line_count = 0
            
            if can_trans_flag or (orgin_text and index==len(all_lines)):
                time.sleep(random.random() * 0.5)
                print(index, '+++++++++++++++++++++++++++++++++++++++++++++++')
                result = translate_google(orgin_text, "zh-CN", "en")
                print(result, '\n')

                result = result.replace('​', '')
                trans_text = trans_text + result + '\n'

                orgin_text = ''
                can_trans_flag = False

    if filepath.find('_en.') == -1:
        path_newfile = filepath.replace('.', '_cn.');
    else:
        path_newfile = filepath.replace('_en.', '_cn.');
    with open(path_newfile, 'w', encoding='utf-8') as wtf:
        wtf.write(trans_text); wtf.flush()

    return path_newfile


# 4、将中/英文字转换成视频字幕srt格式
def text_to_srt_by_regex(filepath):
    text_subtitles = []
    re_gex = re.compile(r'\[([.:\d]+)[->\s]+([.:\d]+)\]\s+(.+)')
    with open(filepath, 'r', encoding='utf-8') as reader:
        content = reader.read()
        results = re_gex.findall(content)
        for index, result in enumerate(results,1):
            s_time = result[0].replace('.',',')
            e_time = result[1].replace('.',',')

            subtitle = '%d\n%s --> %s\n%s\n'%(index, s_time, e_time, result[2])
            text_subtitles.append(subtitle)

    fpath, fext_ = os.path.splitext(filepath)
    with open(f'{fpath}.srt', 'w', encoding='utf-8') as wtf:
        for title in text_subtitles:
            wtf.write(title + '\n')


# 5、使用ffmpeg将中/英字幕合并到视频中
def srt_combin_mp4_ffmpeg(mp4_path, esrt_path, csrt_path):
    subvf_zh=f"subtitles={csrt_path}:force_style='FontName=方正黑体简体,Fontsize=11,BorderStyle=1,Outline=1,Shadow=0,PrimaryColour=&HFFFFFF&,OutlineColour=&H5A6A83&,Spacing=1.5,Alignment=2,MarginL=5,MarginR=5,MarginV=05'"
    subvf_en=f"subtitles={esrt_path}:force_style='FontName=TimesNewRoman,Fontsize=13,BorderStyle=1,Outline=1,Shadow=0,PrimaryColour=&HFFFFFF&,OutlineColour=&H853F1B&,Spacing=0.5,Alignment=2,MarginL=5,MarginR=5,MarginV=18'"

    print(f"Command=====>>>:", csrt_path)
    print(f"Command=====>>>:", esrt_path)
    output_path = mp4_path.replace('.', '_n.')
    if os.path.exists(output_path):
        os.remove(output_path)

    cmd = ['ffmpeg', '-i', mp4_path, '-vf', f"{subvf_zh},{subvf_en}", output_path]
    result = subprocess.run(cmd, shell=False)


# 0、下载YouTube视频
def video_download_pytube(video_list):
    for index, video_url in enumerate(video_list):
        # 1、创建YouTube对象
        youtube = pytube.YouTube(video_url)
        
        # 2、获取视频流(可选视频质量)
        #stream = yt.streams.filter(res='720p').first()
        stream = youtube.streams.get_highest_resolution()
                
        # 3、开始下载视频
        print('Downloding Video =====>>>', youtube.title)
        stream.download(output_path="load_mp4")


def main_generate_srt(video_name):
    mp4_path = f'data_mp4/{video_name}.mp4'
    wav_path = f'data_wavs/{video_name}.wav'
    mp4_to_wav_ffmpeg(mp4_path, 'data_wavs')
    wav_to_text_whisper(wav_path, 'data_text')
    
    text_path = f'data_text/{video_name}.txt'
    text_path1 = f'data_text/{video_name}_cn.txt'
    file_translate_google(text_path)
    
    text_to_srt_by_regex(text_path)
    text_to_srt_by_regex(text_path1)
    
    e_srt_path = text_path.replace('.txt', '.srt')
    c_srt_path = text_path1.replace('.txt', '.srt')
    srt_combin_mp4_ffmpeg(mp4_path, e_srt_path, c_srt_path)



base_path = f'/Users/lizi/Desktop/GithubWorks'
model_bin = f'{base_path}/_models_/ggml-tiny.en.bin'
model_bin = f'{base_path}/_models_/ggml-small.en.bin'

video_lists = ['https://www.youtube.com/watch?v=JxIZbV_XjAs']

if __name__ == '__main__':
    
    #video_download_pytube(video_lists)

    file_name = 'Introducing the GAME ENGINE series'
    main_generate_srt(file_name)

    #print(translate("你吃饭了么?", "en","zh-CN")) #汉语转英语
    #print(translate("你吃饭了么？", "ja","zh-CN")) #汉语转日语
    #print(translate("about your situation", "zh-CN","en")) #英语转汉语

