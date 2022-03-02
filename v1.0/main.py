"""图片浏览App源代码"""
# 设置kivy版本
from kivy import require

require('2.0.0')

# 设置默认字体
from kivy.config import Config

Config.set('kivy', 'default_font', ['msyh', 'msyh.ttc'])

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView

from natsort import ns, natsorted
from filetype import guess

import os


class Homepage(FloatLayout):
    """主页"""

    def __init__(self):
        """初始化初始页面"""
        super(Homepage, self).__init__()
        # 存放浏览文件时的初始目录
        self.start_dir = '/storage'
        self.homepage_button = Button(text='选择目录',
                                      font_size=72,
                                      size_hint=(.5, .25),
                                      pos_hint={'center_x': .5, 'center_y': .5},
                                      on_press=self.sd_or_internal)
        self.add_widget(self.homepage_button)

    def sd_or_internal(self, *args):
        """选择从哪个目录进入"""
        self.clear_widgets()
        self.from_internal_button = Button(text='内部存储',
                                           font_size=72,
                                           size_hint=(.5, .25),
                                           pos_hint={'center_x': .5, 'y': .55},
                                           on_press=self.choose_img_from_internal)
        self.from_external_button = Button(text='外部存储',
                                           font_size=72,
                                           size_hint=(.5, .25),
                                           pos_hint={'center_x': .5, 'y': .2},
                                           on_press=self.choose_img_from_external)
        self.add_widget(self.from_external_button)
        self.add_widget(self.from_internal_button)

    def choose_img_from_external(self, *args):
        """从外部访问时，进入根目录"""
        self.choose_img()

    def choose_img_from_internal(self, *args):
        """
        从内部访问时，进入/storage/emulated/0目录
        （因为Android app无法访问"/storage/emulated"目录，但可以跨过这层目录直接访问"/storage/emulated/0"目录）
        """
        self.start_dir = '/storage/emulated/0'
        self.choose_img()

    def choose_img(self, *args):
        """选择图片文件路径"""
        self.file_chooser = FileChooserListView(path=self.start_dir,
                                                dirselect=True,
                                                size_hint=(1, .9),
                                                pos_hint={'top': 1})
        self.chooes_file_button = Button(text='确定',
                                         size_hint=(.8, .05),
                                         pos_hint={'center_x': .5, 'y': 0.025},
                                         on_press=self.get_img)
        self.clear_widgets()
        self.add_widget(self.file_chooser)
        self.add_widget(self.chooes_file_button)

    def get_img(self, *args):
        """从FileChooser中获取图片文件的地址，并建立相应的图片列表和图集列表"""
        # 获取文件选择器结果
        self.cur_img_path = self.file_chooser.selection[0]
        self.cur_atlas_path = os.path.split(self.cur_img_path)[0]
        # 更新文件选择器的初始目录
        self.start_dir = os.path.split(self.cur_atlas_path)[0]
        # 生成图集列表，并取得当前图集的下标
        self.build_atlas_list()
        self.cur_atlas_index = self.atlas_list.index(self.cur_atlas_path)
        # 生成图片列表，并取得当前图片的下标
        self.build_img_list()
        self.cur_img_index = self.img_list.index(self.cur_img_path)
        # 图集名称
        self.atlas_name=self.atlas_name_list[self.cur_atlas_index]
        self.print_img()

    def build_img_list(self, *args):
        """使用self.cur_img_path和self.cur_atlas_path建立图片列表"""
        # 生成当前图集下的图片列表并排序
        self.img_name_list = os.listdir(self.cur_atlas_path)
        self.img_name_list = natsorted(self.img_name_list, alg=ns.PATH)
        self.img_list = [os.path.join(self.cur_atlas_path, img_name) for img_name in self.img_name_list]

    def build_atlas_list(self, *args):
        """使用self.cur_atlas_path建立图集列表"""
        # 获取图集列表
        self.atlas_list_path = os.path.split(self.cur_atlas_path)[0]
        self.atlas_keyword = os.path.split(self.atlas_list_path)[1]
        self.atlas_name_list = os.listdir(self.atlas_list_path)
        self.atlas_name_list = natsorted(self.atlas_name_list, alg=ns.PATH)
        self.atlas_list = [os.path.join(self.atlas_list_path, atlas_name) for atlas_name in self.atlas_name_list]
        # 生成图集名称列表，保留前20个字符
        for index, atlas_name in enumerate(self.atlas_name_list):
            if len(atlas_name) > 20:
                self.atlas_name_list[index] = atlas_name[:20]

    def print_img(self):
        """输出图片"""
        self.img_index_label = Label(text=f'{self.cur_img_index + 1}/{len(self.img_list)}',
                                     size_hint=(.2, .05),
                                     pos_hint={'center_x': .5, 'top': .975})
        self.atlas_info_label = Label(text=f'{self.atlas_name}({self.cur_atlas_index + 1}/{len(self.atlas_list)})',
                                      size_hint=(.2, .05),
                                      pos_hint={'center_x': .5, 'y': .075})
        self.atlas_keyword_label = Label(text=f'{self.atlas_keyword}',
                                         size_hint=(.2, .05),
                                         pos_hint={'center_x': .5, 'y': .125})
        self.back_button = Button(text='返回',
                                  size_hint=(.15, .05),
                                  pos_hint={'y': .025, 'x': .025},
                                  on_press=self.sd_or_internal)
        self.last_img_button = Button(text='上一张',
                                      size_hint=(.15, .05),
                                      pos_hint={'y': .025, 'x': .225},
                                      on_press=self.last_img)
        self.next_img_button = Button(text='下一张',
                                      size_hint=(.15, .05),
                                      pos_hint={'y': .025, 'x': .425},
                                      on_press=self.next_img)
        self.last_atlas_button = Button(text='上一集',
                                        size_hint=(.15, .05),
                                        pos_hint={'y': .025, 'x': .625},
                                        on_press=self.last_atlas)
        self.next_atlas_button = Button(text='下一集',
                                        size_hint=(.15, .05),
                                        pos_hint={'y': .025, 'x': .825},
                                        on_press=self.next_atlas)
        if os.path.isfile(self.cur_img_path):
            # 如果路径是文件，尝试判断文件类型
            try:
                # 如果文件没有访问权限，则会报错
                ftype = guess(self.cur_img_path)
            except Exception:
                # 出现报错时，输出提示
                self.img = Label(text='当前文件没有访问权限',
                                 font_size=56,
                                 size_hint=(1, .9),
                                 pos_hint={'top': 1})
            else:
                if ftype and ftype.mime.split('/')[0] == 'image':
                    # 如果是图像文件，打开它
                    self.img = Image(source=self.cur_img_path,
                                     allow_stretch=True,
                                     size_hint=(1, .9),
                                     pos_hint={'top': 1},
                                     on_touch_down=self.next_img)
                else:
                    # 如果不是图像文件，输出提示
                    self.img = Label(text='该文件不能以图像形式打开',
                                     font_size=56,
                                     size_hint=(1, .9),
                                     pos_hint={'top': 1})
        else:
            # 如果路径是目录，输出提示
            self.img = Label(text='当前路径为文件夹',
                             font_size=56,
                             size_hint=(1, .9),
                             pos_hint={'top': 1})
        self.clear_widgets()
        self.add_widget(self.img)
        self.add_widget(self.img_index_label)
        self.add_widget(self.atlas_info_label)
        self.add_widget(self.atlas_keyword_label)
        self.add_widget(self.back_button)
        self.add_widget(self.last_img_button)
        self.add_widget(self.next_img_button)
        self.add_widget(self.last_atlas_button)
        self.add_widget(self.next_atlas_button)

    def last_img(self, *args):
        """上一张图片"""
        if self.cur_img_index > 0 and self.img_list:
            self.cur_img_index -= 1
            self.cur_img_path = self.img_list[self.cur_img_index]
        self.print_img()

    def next_img(self, *args):
        """下一张图片"""
        if self.cur_img_index < len(self.img_list) - 1 and self.img_list:
            self.cur_img_index += 1
            self.cur_img_path = self.img_list[self.cur_img_index]
        self.print_img()

    def rebuild_img_list(self, *args):
        """更换图集时重新建立图片列表"""
        last_atlas_path = self.cur_atlas_path
        self.cur_atlas_path = self.atlas_list[self.cur_atlas_index]
        self.atlas_name=self.atlas_name_list[self.cur_atlas_index]
        try:
            # 如果目标目录无访问权限，则会报错
            self.build_img_list()
            # 将图片下标重设为0
            self.cur_img_index = 0
        except Exception:
            # 出错时恢复self.cui_atlas_path，但保持self.cur_atlas_index和self.atlas_name
            self.cur_atlas_path = last_atlas_path
            self.build_img_list()
        if self.img_list:
            # 如果当前图集为空目录，则不更改self.cur_img_path
            self.cur_img_path = self.img_list[self.cur_img_index]

    def last_atlas(self, *args):
        """上一个图集"""
        if self.cur_atlas_index > 0:
            self.cur_atlas_index -= 1
        self.rebuild_img_list()
        self.print_img()

    def next_atlas(self, *args):
        """下一个图集"""
        if self.cur_atlas_index < len(self.atlas_list) - 1:
            self.cur_atlas_index += 1
        self.rebuild_img_list()
        self.print_img()


class TestApp(App):
    """我的应用"""

    def build(self):
        """build方法由run方法调用，需要返回程序的根控件"""
        return Homepage()


if __name__ == '__main__':
    TestApp().run()
