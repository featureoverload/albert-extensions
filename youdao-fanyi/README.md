# 有道翻译插件



## 资料

开发本插件时写的博客：

- [编写 Albert 翻译插件 :link:](https://blog.csdn.net/qq_29757283/article/details/94874750)

- [编写 Albert 翻译插件之功能升级 :link:](https://blog.csdn.net/qq_29757283/article/details/95018343)



## 安装

插件安装：

```shell
$ wget https://raw.githubusercontent.com/RDpWTeHM/albert-extensions/master/youdao-fanyi/youdao_translate.py
$ cp youdao_translate.py \
~/.local/share/albert/org.albert.extension.python/modules/

```

插件所需环境配置：

```shell
$ pip3 install --user requests
$ vim ~/.profile
...

export YOUDAO_APPID=387da...yourappid
export YOUDAO_APPKEY=QDl0k5...yourappkey

:wq
$
```

> 其中，有道的 APP ID 和 Key 需要自己“免费”注册申请。

为了使修改过的 `$HOME/.profile` 生效，**在桌面上 电源位置 > 用户 > “注销”；注销之后重新登录**。



启用插件：

alert tray-icon > settings > Extensions > Python > Translate World > ✅ 勾选上。

![enable有道翻译插件](res/enable_youdao-fanyi.gif)



## 使用

输入 'tr ' （含有空格）作为触发，然后输入查询单词（有补全提示，依赖 ubuntu 内置单词字典），再然后输入 '|z' 翻译到中文（`|` 代表管道的含义，`z` 是触发“翻译到中文”，即将 `|` 管道前的单词通过管道进行下一步处理——翻译）。

使用图示：

![](res/usage_youdao_translate.gif)











