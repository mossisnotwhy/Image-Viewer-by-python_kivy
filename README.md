# Image-Viewer-by-python_kivy
一个轻量级看图小程序，简单高效，没有广告。使用Python+kivy完成。图片保存目录需要满足一定结构，配合Python爬虫一同使用效果更佳。

## 根目录文件说明

1. `run-on-Android-Pydroid.py`文件：可以直接在安卓的Pydroid APP中运行
2. `msyh.ttc`文件：微软雅黑字体，在程序中需要用到，请将其与py文件放在同一目录下再运行

## v1.0目录文件说明

该目录为版本v1.0的文件目录，包括：
1. `main.py`文件：用于打包成Android`.apk`安装包的源码，与直接在Pydroid中运行的代码有所不同
2. `buildozer.spec`文件：我在使用`buildozer`打包时的配置文件
3. `requirements.txt`文件：需要用到的Python库
4. `msyh.ttc`文件：微软雅黑字体，打包时需与`mian.py`文件放在同一目录下
