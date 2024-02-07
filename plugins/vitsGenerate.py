# -*- coding: utf-8 -*-
import json
import os
import subprocess
from asyncio import sleep

import httpx
import requests

from plugins.RandomStr import random_str
from vits.MoeGoe import vG


async def edgetts(data):
    speaker=data.get("speaker")
    text=data.get("text")
    #os.system("where python")
    p = random_str() + ".mp3"
    prf = "data/voices/" + p
    command = f"edge-tts --voice {speaker} --text {text} --write-media {prf}"
    os.system(command)
    return prf
async def sovits(data):
    url = "http://127.0.0.1:9082/synthesize"  # 后端服务的地址
    params = data  # 请求参数
    async with httpx.AsyncClient(timeout=200) as client:
        r=await client.post(url, json=json.dumps(params))
        p = "data/voices/" + random_str() + '.wav'
        print("sovits语音合成路径：" + p)
        with open(p, "wb") as f:
            f.write(r.content)
        return p
async def taffySayTest(data,url,proxy=None):
    if url=='':
        url = "http://localhost:9080/synthesize"  # 后端服务的地址
        async with httpx.AsyncClient(timeout=200) as client:
            r = await client.post(url, json=json.dumps(data))
            p = "data/voices/" + random_str() + '.wav'
            print("bert_vits语音合成路径：" + p)
            with open(p, "wb") as f:
                f.write(r.content)
            return p
    else:
        if str(url).endswith("/synthesize"):
            pass
        elif str(url).endswith("/"):
            url+="synthesize"
        else:
            url+="/synthesize"
        '''proxies = {
            "http://": proxy,
            "https://": proxy
        }'''
        # 请求参数

        async with httpx.AsyncClient(timeout=200) as client:
            r=await client.post(url, json=json.dumps(data))
            p="data/voices/"+random_str()+'.wav'
            print("bert_vits语音合成路径："+p)
            with open(p, "wb") as f:
                f.write(r.content)
            return p
async def outVits(data):
    speaker = data.get("speaker")
    text = data.get("text")
    # os.system("where python")
    p = random_str() + ".mp3"
    p = "data/voices/" + p
    url="https://api.lolimi.cn/API/yyhc/y.php?msg="+text+"&speaker="+speaker+"&Length=1&noisew=0.8&sdp=0.4&noise=0.6&type=json"
    async with httpx.AsyncClient(timeout=200) as client:
        r = await client.post(url, json=json.dumps(data))
        newUrl=r.json().get("music")
        print("outvits语音合成路径：" + p)
        r1=requests.get(newUrl)
        with open(p, "wb") as f:
            f.write(r1.content)
        return p
async def voiceGenerate(data):
    # 向本地 API 发送 POST 请求
    if "MoeGoe.py" in os.listdir():
        from MoeGoe import voiceGenerate as vg
        # 解析请求中的参数
        text = data['text']
        out = data["out"]

        try:
            speaker = data['speaker']
            modelSelect = data['modelSelect']
        except:
            speaker = 2
            modelSelect = ['voiceModel/nene/1374_epochsm.pth', 'voiceModel/nene/config.json']

            # with open('config/settings.yaml', 'r', encoding='utf-8') as f:
            # result = yaml.load(f.read(), Loader=yaml.FullLoader)
            # speaker = result.get("vits").get("speaker")
            # modelSelect = result.get("vits").get("modelSelect")
        # 调用 voiceG() 函数
        if modelSelect[0].endswith("I.pth"):
            text = text.replace("[JA]", "").replace("[ZH]", "")
        await vg(tex=text, out=out, speakerID=speaker, modelSelect=modelSelect)
        print("语音生成完成")
        # 将生成的音频返回给客户端
        return out

    else:
        print("start voice generate")

        text = data['text']
        out = data["out"]
        try:
            speaker = data['speaker']
            modelSelect = data['modelSelect']
        except Exception as e:
            speaker = 2
            modelSelect = ['vits/voiceModel/nene/1374_epochsm.pth', 'vits/voiceModel/nene/config.json']
            print(e)
            # with open('config/settings.yaml', 'r', encoding='utf-8') as f:
            # result = yaml.load(f.read(), Loader=yaml.FullLoader)
            # speaker = result.get("vits").get("speaker")
            # modelSelect = result.get("vits").get("modelSelect")
        # 调用 voiceG() 函数
        if modelSelect[0].endswith("I.pth"):
            text = text.replace("[JA]", "").replace("[ZH]", "")
        # print("get")
        await vG(tex=text, out=out, speakerID=speaker, modelSelect=modelSelect)
        print("语音生成完成")
        return out
