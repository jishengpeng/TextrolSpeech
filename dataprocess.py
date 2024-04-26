import os
import subprocess
import pyworld as pw
import librosa
import matplotlib.pyplot as plt
import numpy as np
from textgrid import TextGrid
import pandas as pd

### This script is recovered based on the chat history. If the threshold in the high and low does not match the result, Please recalculate the related label again and give feedback in the Github issue.



###  pitch [136.57698522,196.09780757]   < low, normal, > high
def gets_mean_pitch(wav_path):

    # x, fs = sf.read(wav_path)
    x, fs = librosa.load(wav_path)
    # print("*****",fs)
    x = x.astype(np.double)
    # _f0_h, t_h = pw.harvest(x, fs)   #0.005s
    _f0_h, t_h = pw.dio(x, fs)

    #得到基频
    f0_h = pw.stonemask(x, _f0_h, t_h, fs)
    data = f0_h
    mask = (data != 0)
    # 计算每段非零的平均值 
    segments = np.split(data, np.where(np.diff(mask))[0]+1)
    non_zero_num,value = 0 ,0
    for seg in segments:
        if len(seg)<=0 or seg[0]==0:
            continue
        non_zero_num += len(seg)
        value += seg.sum()
    if non_zero_num==0:
      return 0,False
    return value/non_zero_num,True

### energy [0.03331899,0.05054203]  < 0.03331899 low, normal, > 0.05054203 high
def get_energy(wav_path):
    y, sr = librosa.load(wav_path)
    energy = librosa.feature.rms(y=y)
    energy = energy.mean()
    return energy

###tempo [0.252,0.38645446]  该值表示平均每个单词的发音时间，< 0.252 high, normal, > 0.38645446 low
def extract_tempo(textgrid_fp):
    itvs = TextGrid.fromFile(textgrid_fp)[0]
    num =0
    dur =0
    for i in range(len(itvs)):
        if itvs[i].mark == '':
            continue
        num += 1
        dur += itvs[i].maxTime - itvs[i].minTime
    # if num==0:
    #     continue
    tempo = dur /num


