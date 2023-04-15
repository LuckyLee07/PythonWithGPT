#!/bin/bash

sub_file_cn=cn.srt
sub_file_en=en.srt
infile=input_video.mp4


subvf_en="subtitles=${sub_file_cn}:force_style='FontName=方正黑体简体,Fontsize=11,BorderStyle=1,Outline=1,Shadow=0,PrimaryColour=&HFFFFFF&,OutlineColour=&H5A6A83&,Spacing=1.5,Alignment=2,MarginL=5,MarginR=5,MarginV=05'"
subvf_cn="subtitles=${sub_file_en}:force_style='FontName=TimesNewRoman,Fontsize=13,BorderStyle=1,Outline=1,Shadow=0,PrimaryColour=&HFFFFFF&,OutlineColour=&H853F1B&,Spacing=0.5,Alignment=2,MarginL=5,MarginR=5,MarginV=18'"

#ffplay -i "${infile}" -vf "${subvf_cn}","${subvf_en}",scale=1280:720
ffmpeg -i "${infile}" -vf ${subvf_cn},${subvf_en} out.mp4