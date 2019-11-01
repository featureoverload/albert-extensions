# 搜索 Markdown 文档内容插件



## 安装

插件安装：

```shell
$ wget https://raw.githubusercontent.com/RDpWTeHM/albert-extensions/master/search-in-markdown/search_markdown.py
$ cp search_markdown.py \
~/.local/share/albert/org.albert.extension.python/modules/

```

插件所需环境配置：

```shell
$ mkdir -p ~/.config/albert/org.albert.extension.python
$ vim ~/.config/albert/org.albert.extension.python/search_markdown.json
{"markdown_files_directory": "/<path>/<to>/<markdown-files-folder>", "trigger_len": 3}
~
~
~
:wq
$
```

> 其中：
>
> - markdown_files_directory 用来放你想要搜索的 markdown 文档路径
> - trigger_len 指定了在 albert 搜索框输入多长的字符开始触发搜索



启用插件：

alert tray-icon > settings > Extensions > Python > **Search in Markdowns** > ✅ 勾选上。



## 使用

输入 'smd ' （含有空格）作为触发，然后输入搜索关键字




