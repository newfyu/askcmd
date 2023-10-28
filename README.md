# `askcmd` 使用指南

## 简介

`askcmd` 是一个轻量简便的命令行工具，帮助用户根据自然语言生成或解释命令行命令。使用 OpenAI 的 `gpt-3.5-turbo` 模型来生成或解释用户的查询。

![askcmd](https://github.com/newfyu/askcmd/assets/43229758/fc2ae91b-10bf-4ada-8b6c-58598504f8af)

## 安装

从 GitHub 克隆仓库：

```bash
git clone https://github.com/newfyu/askcmd.git
cd askcmd
python setup.py install
```

## 设置

首次使用以下参数来配置 `askcmd`:
```bash
askcmd --key YOUR_OPENAI_KEY # 首次使用必须设置
askcmd --api-base API_BASE # 可选，设置反向代理地址，如果你的网络无法访问 OpenAI，可尝试设置为比如 "https://api.openai-proxy.com" 等公开的反向代理地址。输入 "none" 移除之前设置的反向代理地址。
askcmd --proxy YOUR_PROXY # 可选，如果你是用自己的本地代理工具，在此处设置代理地址，例如 "http://127.0.0.1:1087"
```


## 使用
```bash
askcmd
```
