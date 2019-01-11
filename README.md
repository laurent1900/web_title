# web_title

动态爬取网站名称，Python2+selenium+phantomjs。支持单个域名查询和从文件导入,支持多进程。

依赖库：

selenium==2.48.0

argparse

multiprocessing

安装方法：

1、在官网下载phantomjs，这里面分别提供了Windows、Mac、以及Linux 的安装包，根据自己的需要下载即可。下载完成后，将其解压到容易找到的文件夹中，打开并找到bin文件夹里的 phantomjs.exe，点击运行，出现如下界面，说明安装成功，可以使用了。

2、添加路径。将bin目录下的phantomjs.exe（这里用Windows举例）的路径添加到系统变量Path中

3、pip install selenium==2.48.0

4、pip install argparse

使用方法:

--host  指定域名

python web_title.py --host www.a.com

--file 从文件导入域名

将域名一行一个存入文件中并保存，运行下列命令：

python web_title.py --file hosts.txt

--threads 指定线程数，默认为5个线程

python web_title.py --file hosts.txt --threads 5
