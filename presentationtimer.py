#!/usr/bin/python3
import tkinter as tk
import tkinter.font as tkFont
import math
import time
from configparser import ConfigParser
import sys
import re

# ## variable dicts ##
config = {}

# ## default values ##
# ### fons ###
config['fontfamily_title'] = ''
config['fontfamily_counter'] = ''
config['fontfamily_allocation'] = ''

# ### color ###
config['color_default_bg'] = '#000'
config['color_default_fg'] = '#FFF'
config['color_currenttitle_bg'] = None
config['color_currenttitle_fg'] = None
config['color_nexttitle_bg'] = None
config['color_nexttitle_fg'] = None
config['color_nextheader_bg'] = None
config['color_nextheader_fg'] = None
config['color_allocation_bg'] = None
config['color_allocationmain_fg'] = '#EFA'
config['color_allocationplus_fg'] = None
config['color_allocationsub_fg'] = '#AEF'
config['color_counter_bg'] = None
config['color_borderline'] = '#888'

# ### size ###
# #### スクリーン全体の高さに対する、タイトル文字列の比率
config['ratio_title_height'] = 0.1
# #### タイトル文字列に対する、上下のパディング高さの比率
config['ratio_title_padding'] = 0.3
# #### カウンター＋割当て時間のエリアの高さの、スクリーン全体の高さから上下のタイトル文字列分を引いた残りに対する比率
config['ratio_counterarea_height'] = 0.6
# #### カウンターと割当て時間の文字列の比率(カウンター側
config['ratio_counter_height'] = 10 / 16
# #### カウンターのラベルの文字サイズ(カウンター本体に対する比率)
config['ratio_counter_label'] = 0.4
# #### 割当て時間のフォントの、カウンターのフォントに対する比率
config['ratio_allocation_fontsize'] = 0.4
# #### 割当て時間の文字列に対する、上下のパディング高さの比率
config['ratio_allocation_padding'] = 0.2

# ### strings ###
# #### 次の発表タイトルに対するラベル
config['next_header'] = "Next >>>"
# #### カウンターのラベル(発表)
config['label_allocationmain'] = "発表"
# #### カウンターのラベル(質疑)
config['label_allocationsub'] = "質疑"
# #### カウンターのラベル(のこり)
config['counter_label_remaining'] = "のこり"

# ### logo ###
# #### logo 表示位置(左上基準) ####
config['logo_position'] = '1x1'
# #### ロゴの背景色 ####
config['color_logo_bg'] = None

class Window:
    @classmethod
    def initialize(cls, sample, geometry):
        # ## root window ##
        cls.root = tk.Tk()

        cls.root.config(bg=config['color_default_bg'])
        # ## screen size ##
        if not geometry:
            print("fullscreen")
            cls.root.attributes("-fullscreen", True)
            _scrn_width = cls.root.winfo_screenwidth()
            _scrn_height = cls.root.winfo_screenheight()
            cls.root.geometry("%dx%d" % (_scrn_width, _scrn_height))
        else:
            cls.root.geometry(geometry)
            (_scrn_width, _scrn_height) = map(int, geometry.split('x'))

        # ## title text restriction ##
        _ttltxt_maxheight = math.floor(_scrn_height * config['ratio_title_height'])
        _ttltxt_maxwidth = _scrn_width - math.floor(_ttltxt_maxheight * config['ratio_title_padding'] * 2)

        # ## calcurate title font size ##
        _size_list = list(range(120, 36, -12))
        _size_list.extend(range(36, 10, -4))

        for _size in _size_list:
            cls.font_title = tkFont.Font(family=config['fontfamily_title'], size=_size)
            if _ttltxt_maxheight < cls.font_title.metrics("linespace"):
                continue
            if _ttltxt_maxwidth < cls.font_title.measure(config['next_header'] + sample):
                continue

            break

        # ## counter text restriction ##
        _cntrtxt_maxheight = math.floor((_scrn_height - 2 * _ttltxt_maxheight) *
                                        config['ratio_counterarea_height'] *
                                        config['ratio_counter_height'])

        # ## calcurate counter font size ##
        _size_list = range(300, 36, -12)

        for _size in _size_list:
            cls.font_counter = tkFont.Font(family=config['fontfamily_counter'], size=_size)

            if _cntrtxt_maxheight < cls.font_counter.metrics("linespace"):
                continue

            cls.font_allocation = tkFont.Font(family=config['fontfamily_allocation'],
                                              size=math.floor(_size * config['ratio_allocation_fontsize']))
            cls.font_remaining = tkFont.Font(family=config['fontfamily_counter'],
                                             size=math.floor(_size * config['ratio_counter_label']))
            break

        # ## widgets ##
        # ## current title ##
        cls.txt_current = tk.StringVar()
        cls.lbl_current = tk.Label(cls.root,
                                   textvariable=cls.txt_current, font=cls.font_title,
                                   fg=config['color_currenttitle_fg'], bg=config['color_currenttitle_bg'],
                                   pady=_ttltxt_maxheight*config['ratio_title_padding'])
        cls.lbl_current.pack()

        # ## border between current title and counter ##
        cls.lbl_upperline = tk.Label(cls.root, text='', font=('', 1), border=0,
                                     highlightthickness=0, bg=config['color_borderline'])
        cls.lbl_upperline.pack(fill=tk.X)

        # ## spacer ##
        cls.lbl_upperspacer = tk.Label(cls.root, text='', font=('', 1), border=0,
                                       highlightthickness=0, bg=config['color_default_bg'])
        cls.lbl_upperspacer.pack(expand=True, fill=tk.BOTH)

        # ## counter ##
        # ### counter title ###
        cls.frm_counter = tk.Frame(cls.root, bg=config['color_default_bg'])
        cls.frm_remaining = tk.Frame(cls.frm_counter, bg=config['color_default_bg'])
        cls.txt_remaining_title = tk.StringVar()
        cls.lbl_remaining_title = tk.Label(cls.frm_remaining,
                                           textvariable=cls.txt_remaining_title, font=cls.font_remaining,
                                           fg=config['color_allocationmain_fg'], bg=config['color_counter_bg'])
        cls.lbl_remaining_title.pack()
        cls.lbl_remaining_remaining = tk.Label(cls.frm_remaining,
                                               text=config['counter_label_remaining'], font=cls.font_remaining,
                                               fg=config['color_allocationmain_fg'], bg=config['color_counter_bg'])
        cls.lbl_remaining_remaining.pack()
        cls.frm_remaining.pack(expand=True, side=tk.LEFT)
        # ### counter ###
        cls.txt_counter = tk.StringVar()
        cls.lbl_counter = tk.Label(cls.frm_counter,
                                   textvariable=cls.txt_counter, font=cls.font_counter,
                                   fg=config['color_allocationmain_fg'], bg=config['color_counter_bg'],
                                   padx=cls.font_remaining.metrics("linespace") / 2)
        cls.lbl_counter.pack(expand=True, side=tk.LEFT)
        cls.frm_counter.pack()

        # ## allocation time ##
        cls.frm_allocation = tk.Frame(cls.root, bg=config['color_allocation_bg'])
        _alctlbl_paddingheight = cls.font_allocation.metrics("linespace") * config['ratio_allocation_padding']

        cls.txt_alct_main = tk.StringVar()
        cls.lbl_alct_main = tk.Label(cls.frm_allocation,
                                     textvariable=cls.txt_alct_main, font=cls.font_allocation,
                                     fg=config['color_allocationmain_fg'], bg=config['color_allocation_bg'],
                                     pady=_alctlbl_paddingheight)
        cls.lbl_alct_main.pack(side=tk.LEFT)

        cls.lbl_alct_plus = tk.Label(cls.frm_allocation,
                                     text=' + ', font=cls.font_allocation,
                                     fg=config['color_allocationplus_fg'], bg=config['color_allocation_bg'],
                                     pady=_alctlbl_paddingheight)
        cls.lbl_alct_plus.pack(side=tk.LEFT)

        cls.txt_alct_sub = tk.StringVar()
        cls.lbl_alct_sub = tk.Label(cls.frm_allocation,
                                    textvariable=cls.txt_alct_sub, font=cls.font_allocation,
                                    fg=config['color_allocationsub_fg'], bg=config['color_allocation_bg'],
                                    pady=_alctlbl_paddingheight)
        cls.lbl_alct_sub.pack(side=tk.LEFT)

        cls.frm_allocation.pack(expand=True, fill=tk.Y)

        # ## spacer ##
        cls.lbl_lowerspacer = tk.Label(cls.root, text='', font=('', 1), border=0,
                                       highlightthickness=0, bg=config['color_default_bg'])
        cls.lbl_lowerspacer.pack(expand=True, fill=tk.BOTH)

        # ## border between current title and counter ##
        cls.lbl_lowerline = tk.Label(cls.root, text='', font=('', 1), border=0,
                                     highlightthickness=0, bg=config['color_borderline'])
        cls.lbl_lowerline.pack(fill=tk.X)

        # ## next title ##
        cls.frm_nexttitle = tk.Frame(cls.root, bg=config['color_nexttitle_bg'])

        cls.lbl_nextheader = tk.Label(cls.frm_nexttitle, text=config['next_header'], font=cls.font_title,
                                      fg=config['color_nextheader_fg'], bg=config['color_nextheader_bg'],
                                      padx=_ttltxt_maxheight*config['ratio_title_padding'],
                                      pady=_ttltxt_maxheight*config['ratio_title_padding'])
        cls.lbl_nextheader.pack(side=tk.LEFT)

        cls.txt_next = tk.StringVar()
        cls.lbl_next = tk.Label(cls.frm_nexttitle, textvariable=cls.txt_next, font=cls.font_title,
                                fg=config['color_nexttitle_fg'], bg=config['color_nexttitle_bg'],
                                pady=_ttltxt_maxheight*config['ratio_title_padding'])
        cls.lbl_next.pack(side=tk.LEFT)

        cls.frm_nexttitle.pack(fill=tk.X)

        if 'logo_file' in config:
            cls.image = tk.PhotoImage(file=config['logo_file'])
            cls.lbl_logo = tk.Label(cls.root, image=cls.image, bg=config['color_logo_bg'])
            (x, y) = map(int, config['logo_position'].split('x'))
            cls.lbl_logo.place(x=x, y=y)

        # ## event handlers ##
        cls.lbl_current.bind("<Button-1>", cls._click_current)
        cls.lbl_current.bind("<Double-Button-1>", cls._doubleclick_current)

        cls.lbl_next.bind("<Button-1>", lambda e: Presentation.goNext())

    @classmethod
    def _click_current(cls, event):
        cls.presentation.start_and_stop()

    @classmethod
    def _doubleclick_current(cls, event):
        cls.presentation.reset()

    @classmethod
    def setPresentation(cls, presentation):
        cls.presentation = presentation

    @classmethod
    def count(cls):
        if cls.presentation.update():
            cls.root.after(1000, cls.count)

    @classmethod
    def makeCounterAllocationMain(cls, counter_label):
        cls.lbl_counter.config(fg=config['color_allocationmain_fg'])
        cls.lbl_remaining_remaining.config(fg=config['color_allocationmain_fg'])
        cls.lbl_remaining_title.config(fg=config['color_allocationmain_fg'])
        cls.txt_remaining_title.set(counter_label)

    @classmethod
    def makeCounterAllocationSub(cls, counter_label):
        cls.lbl_counter.config(fg=config['color_allocationsub_fg'])
        cls.lbl_remaining_remaining.config(fg=config['color_allocationsub_fg'])
        cls.lbl_remaining_title.config(fg=config['color_allocationsub_fg'])
        cls.txt_remaining_title.set(counter_label)

    @classmethod
    def setCurrentTitle(cls, title):
        cls.txt_current.set(title)

    @classmethod
    def setNextTitle(cls, title):
        cls.txt_next.set(title)

    @classmethod
    def setAllocationMain(cls, time):
        cls.txt_alct_main.set(time)

    @classmethod
    def setAllocationSub(cls, time):
        if time:
            cls.txt_alct_sub.set(time)
            cls.lbl_alct_plus.pack(side=tk.LEFT)
            cls.lbl_alct_sub.pack(side=tk.LEFT)
        else:
            cls.lbl_alct_plus.pack_forget()
            cls.lbl_alct_sub.pack_forget()

    @classmethod
    def setCounter(cls, m, s):
        cls.txt_counter.set("%02d:%02d" % (m, s))


class Presentation:
    _current = None
    _presentations = []

    @classmethod
    def setCurrent(cls, pos):
        cls._current = cls._presentations[pos]
        cls._current.setup()

    @classmethod
    def setNext(cls, pos):
        if pos < len(cls._presentations):
            cls._next = pos
            cls._presentations[pos].setupNext()
        else:
            Window.setNextTitle('')

    @classmethod
    def goNext(cls):
        cls.setCurrent(cls._next)
        cls.setNext(cls._next + 1)

    @classmethod
    def append(cls, title, min_main, min_sub, rings, alct_main_label, alct_sub_label):
        cls._presentations.append(cls(title, min_main, min_sub, rings, alct_main_label, alct_sub_label))

    def __init__(self, title, min_main, min_sub, rings, alct_main_label, alct_sub_label):
        self.title = title
        self.min_main = min_main
        self.min_sub = min_sub
        self.rings = rings
        self.alct_main_label = alct_main_label
        self.alct_sub_label = alct_sub_label
        self.reset()

    def reset(self):
        self.allocation = 'main'
        self.start_time = None
        self._counter = None
        self._stop_time = None
        if self.rings:
            self.ringtimes = sorted(self.rings.keys())
            self.ringtime = self.ringtimes.pop()
        else:
            self.ringtime = None
        self.seconds = self.min_main * 60
        if Presentation._current is self:
            self.update()

        return(self)

    def setup(self):
        Window.setAllocationMain("%dmin" % self.min_main)
        if self.min_sub:
            Window.setAllocationSub("%dmin" % self.min_sub)
        else:
            Window.setAllocationSub(None)
        Window.setPresentation(self)
        Window.setCurrentTitle(self.title)
        self.update()
        return(self)

    def setupNext(self):
        Window.setNextTitle(self.title)
        return(self)

    def start_and_stop(self):
        if self._counter == 'start':
            self._counter = 'stop'
            self._stop_time = time.time()
            return(self)

        if self._counter == 'stop':
            self.seconds += time.time() - self._stop_time
        else:  # e.g. self._counter is None
            self.start_time = time.time()

        self._counter = 'start'

        Window.count()
        return(self)

    def update(self):
        if self._counter == 'stop':
            return(False)

        if self.start_time is None:
            remaining = self.seconds
            Window.makeCounterAllocationMain(self.alct_main_label)
        else:
            remaining = math.ceil(self.seconds - (time.time() - self.start_time))

        if self.ringtime is not None and self.ringtime == remaining:
            for i in range(self.rings[remaining]):
                Window.root.bell()
                print("ring, at %d (%d/%d):" % (remaining, i+1, self.rings[remaining]))
                time.sleep(0.2)
            if self.ringtimes:
                self.ringtime = self.ringtimes.pop()
            else:
                self.ringtime = None

        if remaining < 0:
            if self.allocation == 'sub':
                return(False)

            # switch counter from main allocation time to sub
            self.allocation = 'sub'
            remaining = self.min_sub * 60
            self.seconds += remaining
            Window.makeCounterAllocationSub(self.alct_sub_label)

        m = math.floor(remaining / 60)
        s = remaining % 60

        Window.setCounter(m, s)

        return(self._counter == "start")


# ## read config file ##
def _readconfigfile(file):
    configfile = ConfigParser()
    configfile.read(file)
    max_title = ''
    if 'settings' in configfile.sections():
        config.update(dict(configfile['settings']))
        # 数値設定項目(ratio_*)を、str → float 化
        config.update(map(lambda x: (x, float(config[x])),
                          filter(lambda x: x.startswith('ratio'), configfile['settings'].keys())))

    # 値が未設定の色設定項目に対して、デフォルト値を設定
    for c in filter(lambda x: x.startswith("color_") and not config[x], config.keys()):
        if c.endswith("_fg"):
            config[c] = config['color_default_fg']
        elif c.endswith("_bg"):
            config[c] = config['color_default_bg']

    for p in filter(lambda x: x.startswith("Presentation"), configfile.sections()):
        title = configfile[p].get('title')
        main_min = configfile[p].getint('main_minute')
        sub_min = configfile[p].getint('sub_minute')
        alct_main_label = configfile[p].get('label_allocationmain', config['label_allocationmain'])
        alct_sub_label = configfile[p].get('label_allocationsub', config['label_allocationsub'])
        rings = {}
        for r in filter(lambda x: x.startswith("ring_remaining_min."), configfile[p].keys()):
            timing = configfile[p].get(r)
            if not timing.isdecimal():
                continue
            timing = int(timing) * 60
            count = int(r.split('.')[1])
            rings[timing] = count

        Presentation.append(title, main_min, sub_min, rings, alct_main_label, alct_sub_label)
        if len(max_title) < len(title):
            max_title = title

    if re.fullmatch(r"-?[0-9]{1,4}x-?[0-9]{1,4}", config['logo_position']) is None:
        print("logo_position must be like '10x10' format", file=sys.stderr)

    return(max_title)

if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--geometry", metavar='800x600', help="window size")
    parser.add_argument("config", help="config file (ini format)")
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print("%s: error: file `%s' is not found" % (sys.argv[0], args.config))
        exit(1)
    if args.geometry and re.fullmatch(r"[1-9][0-9]{2,3}x[1-9][0-9]{2,3}", args.geometry) is None:
        parser.print_help()
        exit(1)

    max_title = _readconfigfile(args.config)

    Window.initialize(max_title, args.geometry)
    Presentation.setCurrent(0)
    Presentation.setNext(1)

    Window.root.mainloop()
