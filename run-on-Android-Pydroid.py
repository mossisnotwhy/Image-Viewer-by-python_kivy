import os

from kivy.config import Config

Config.set('kivy', 'default_font', ['msyh', 'msyh.ttc'])

from kivy import require
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from natsort import natsorted,ns

require('1.11.1')


class Homepage(FloatLayout):
    def __init__(self):
        super(Homepage, self).__init__()
        self.cols = 3
        self.rows = 3
        self.homepage_button = Button(text='选择目录',
                                      font_size=72,
                                      size_hint=(.5, .25),
                                      pos_hint={'center_x': .5, 'center_y': .5},
                                      on_press=self.choose_img)
        self.add_widget(self.homepage_button)

    def choose_img(self, *args):
        self.file_chooser = FileChooserListView(path='/storage/emulated/0',
                                                size_hint=(1, .9),
                                                pos_hint={'top': 1})
        self.chooes_file_button = Button(text='确定',
                                         size_hint=(.8, .05),
                                         pos_hint={'center_x': .5, 'y': .025},
                                         on_press=self.get_img)
        self.clear_widgets()
        self.add_widget(self.file_chooser)
        self.add_widget(self.chooes_file_button)

    def get_img(self, *args):
        self.cur_img_path = self.file_chooser.selection[0]
        self.cur_atlas_path = os.path.split(self.cur_img_path)[0]
        # 生成图集列表，并取得当前图集的下标
        self.build_atlas_list()
        self.cur_atlas_index = self.atlas_list.index(self.cur_atlas_path)
        # 生成图片列表，并取得当前图片的下标
        self.build_img_list()
        self.cur_img_index = self.img_list.index(self.cur_img_path)
        self.print_img()

    def build_img_list(self, *args):
        # 生成当前图集下的图片列表并排序
        self.img_name_list = os.listdir(self.cur_atlas_path)
        self.img_name_list = natsorted(self.img_name_list,alg=ns.PATH)
        self.img_list = [os.path.join(self.cur_atlas_path, img_name) for img_name in self.img_name_list]
        # 生成当前图集名称，保留前16个字符
        self.atlas_name = os.path.split(self.cur_atlas_path)[1]
        self.atlas_name = self.atlas_name[:20] + '...' if len(self.atlas_name) > 20 else self.atlas_name

    def build_atlas_list(self, *args):
        # 获取图集列表
        self.atlas_list_path = os.path.split(self.cur_atlas_path)[0]
        self.atlas_keyword=os.path.split(self.atlas_list_path)[1]
        self.atlas_name_list = os.listdir(self.atlas_list_path)
        self.atlas_name_list = natsorted(self.atlas_name_list,alg=ns.PATH)
        self.atlas_list = [os.path.join(self.atlas_list_path, atlas_name) for atlas_name in self.atlas_name_list]

    def print_img(self):
        self.img_index_label = Label(text=f'{self.cur_img_index + 1}/{len(self.img_list)}',
                                     size_hint=(.2, .05),
                                     pos_hint={'center_x': .5, 'top': .975})
        self.atlas_info_label = Label(text=f'{self.atlas_name}({self.cur_atlas_index + 1}/{len(self.atlas_list)})',
                                      size_hint=(.2, .05),
                                      pos_hint={'center_x': .5, 'y': .075})
        self.atlas_keyword_label=Label(text=f'{self.atlas_keyword}',
                                       size_hint=(.2, .05),
                                       pos_hint={'center_x': .5, 'y': .125})
        self.back_button = Button(text='返回',
                                  size_hint=(.15, .05),
                                  pos_hint={'y': .025, 'x': .025},
                                  on_press=self.choose_img)
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
        self.img = Image(source=self.cur_img_path,
                         allow_stretch=True,
                         size_hint=(1, .9),
                         pos_hint={'top': 1},
                         on_touch_down=self.next_img)
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
        if self.cur_img_index > 0:
            self.cur_img_index -= 1
        self.cur_img_path = self.img_list[self.cur_img_index]
        self.print_img()

    def next_img(self, *args):
        if self.cur_img_index < len(self.img_list) - 1:
            self.cur_img_index += 1
        self.cur_img_path = self.img_list[self.cur_img_index]
        self.print_img()

    def last_atlas(self, *args):
        if self.cur_atlas_index > 0:
            self.cur_atlas_index -= 1
        self.cur_atlas_path = self.atlas_list[self.cur_atlas_index]
        self.build_img_list()
        self.cur_img_index=0
        self.cur_img_path = self.img_list[self.cur_img_index]
        self.print_img()

    def next_atlas(self, *args):
        if self.cur_atlas_index < len(self.atlas_list) - 1:
            self.cur_atlas_index += 1
        self.cur_atlas_path = self.atlas_list[self.cur_atlas_index]
        self.build_img_list()
        self.cur_img_index=0
        self.cur_img_path = self.img_list[self.cur_img_index]
        self.print_img()


class TestApp(App):
    def build(self):
        return Homepage()


if __name__ == '__main__':
    TestApp().run()
