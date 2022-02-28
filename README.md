# Image-Viewer-by-python_kivy
一个轻量级看图小程序，简单高效，没有广告。使用Python+kivy完成。图片保存目录需要满足一定结构，配合Python爬虫一同使用效果更佳。

## 说明

1. `run-on-Android-Pydroid.py`可以直接在安卓的Pydroid中运行
2. `source.py`文件是可以打包成Android App的源码，与可以直接在Pydroid中运行的代码有所不同
3. `msyh.ttc`是微软雅黑字体文件，在程序中需要用到，请将其与py文件放在同一目录下
4. 使用`buildozer`打包时记得添加包含文件`.ttc`、需要的库`natsort`
