# THIS_PATH is defined in chess_displayable.rpy
# define THIS_PATH = '00-chess-engine/'
# MOKOt

init python:
    # for importing libraries
    import_dir = os.path.join(renpy.config.gamedir, THIS_PATH, 'python-packages')
    # to prevent STOCKFISH_ENGINE from getting stored and pickled
    global_objects = {}

#шейдеры
#define config.default_textshader = True
#$ renpy.register_text_shader()

#=================================================
#задаем дополнителные звуковые каналы
#=================================================
#renpy.music.register_channel ("nature", "sound", loop=True)
#renpy.music.register_channel ("natu", "sound", loop=True)
#renpy.music.register_channel ("natu_fon", "sound", loop=True)


init python:
    renpy.music.register_channel("nature", "sound", loop=True)
    renpy.music.register_channel("natu", "sound", loop=True)
    renpy.music.register_channel("natu_fon", "sound", loop=True)


# MOKOt
#==============================================
#генератор случайных чисел
#==============================================

#$ ran_dig = renpy.random.choice([1,6])
$ gtm = 0
$ player_guess = 0
#$ mci = 0

#===============================================   
#Генерат позиции(Де)
#===============================================
# MOKOt

init python:
    from random import uniform
    import math
    #Это даст нам корды и границы безопасной зоны
    def get_coords():
        nx, ny = uniform(0, 1920), uniform(0, 1080)
        xf = uniform(min(nx, -ny), max(nx, -ny))
        yf = uniform(min(-nx, ny), max(-nx, ny))
        return int(xf), int(yf)
        
    #Это докидывает конфиг для движения
    def create_mover():
        x = 960
        y = 540
        target_x = 960
        target_y = 540
        start_x = 960
        start_y = 540
        progress = 1.0
        duration = 1.0
        start_time = 0
        #ТРОГАТЬ ТУТА
        speed = 400
        #ЭТО СКОРОСТЬ
        
        #А это само двигло
        def move_func(trans, st, at):
            nonlocal x, y, target_x, target_y, start_x, start_y, progress, duration, start_time
            
            if progress >= 1.0:
                start_x, start_y = x, y
                target_x, target_y = get_coords()
                
                dx = target_x - start_x
                dy = target_y - start_y
                distance = math.sqrt(dx*dx + dy*dy)
                duration = max(0.5, distance / speed)
                progress = 0
                start_time = st
                
            elapsed = st - start_time
            progress = min(1.0, elapsed / duration)
            
            if progress < 1.0:
                x = start_x + (target_x - start_x) * progress
                y = start_y + (target_y - start_y) * progress
            else:
                x, y = target_x, target_y
            
            trans.pos = (int(x), int(y))
            return 0
        
        return move_func
        
#это чтоб оно шароёбилось
transform smooth_random_move:
    function create_mover()
#Это тестовое, пока оставлю
#transform test_transform():
#        pos (0, 0)


#===================================================
# mci(MENU CHOICE ID)
#===================================================
# MOKOt

init python:
    import rgen
    mci = rgen.rgen()

python:
    import rgen
    
    class AutoMCI:
        def __init__(self):
            self.current = None
        
        def __call__(self):
            self.current = rgen.rgen()
            return self.current
    
    mci = AutoMCI()

#python:
#    import rgen

#define mci = rgen.rgen()
#$ mci = rgen.rgen()
#define Cha_01 = mci



#=============================================================
#карты таро
#=============================================================
# MOKOt

screen my_text_screen(line):
    frame:
        #Вот это твоё положение и размер рамки
        xalign 0.6
        yalign 0.1
        xsize 1200
        
        # Укажи путь к фону
        background im.FactorScale("images/my_frame_bg.png", 1.7) 
        
        # Добавь отступы, чтобы текст не прилипал к краям картинки
        padding (20, 20) 
        
        text line:
            size 35 
            italic False
            #bold True
            #text_align 0.5

#======================================================================
#святлечки
#======================================================================

init python:
    import random

    class FlyParticle(renpy.Displayable):
        def __init__(self, **kwargs):
            super(FlyParticle, self).__init__(**kwargs)

            # 4 варианта (каждый — 2 кадра)
            self.variants = ["fly1", "fly2", "fly3", "fly4"]

            # 1) рассинхрон фазы анимации (кадры внутри filmstrip)
            self.anim_phase_offset = random.uniform(0.0, 1000.0)

            # 2) рассинхрон именно переключения "картинок" (fly01..fly04)
            self.switch_phase_offset = random.uniform(0.0, 1000.0)

            # 3) начальная картинка тоже случайная
            self.current = random.randrange(4)

            self.last_switch = None
            self.switch_time = random.uniform(1.5, 6.0)

        def copy(self):
            # SnowBlossom делает копии частиц через copy()
            return FlyParticle()

        def render(self, width, height, st, at):
            # время для фазы анимации (чтобы кадры не совпадали)
            st_anim = st + self.anim_phase_offset

            # время для логики смены вариантов (чтобы смены не совпадали)
            st_switch = st + self.switch_phase_offset

            if self.last_switch is None:
                self.last_switch = st_switch

            # случайная смена варианта, без повтора подряд
            if st_switch - self.last_switch >= self.switch_time:
                choices = [i for i in range(4) if i != self.current]
                self.current = random.choice(choices)

                # следующее переключение в другое случайное время
                self.switch_time = random.uniform(1.5, 6.0)
                self.last_switch = st_switch

            cr = renpy.render(self.variants[self.current], width, height, st_anim, at)

            r = renpy.Render(cr.width, cr.height)
            r.blit(cr, (0, 0))

            renpy.redraw(self, 0.1)
            return r

        def visit(self):
            return self.variants

###########################################################################

#===========================================================
#старшие арканы
#===========================================================

init python:
    letters = [
        "A","B","C","D","E","F","G","H","I","J","K",
        "L","M","N","O","P","R","S","T","U","V","Y"
    ]

    SAT_cards = {
        f"SAT_{i+1:02}": f"images/major_arcana/card_{letters[i]}.png"
        for i in range(len(letters))
    }

#==============================================================
#младщие арканы
#==============================================================

image MAT_01 = im.FactorScale("images/minor_arcana/01.png", 2.9)
image MAT_02 = im.FactorScale("images/minor_arcana/02.png", 2.9)
image MAT_03 = im.FactorScale("images/minor_arcana/03.png", 2.9)
image MAT_04 = im.FactorScale("images/minor_arcana/04.png", 2.9)
image MAT_05 = im.FactorScale("images/minor_arcana/05.png", 2.9)
image MAT_06 = im.FactorScale("images/minor_arcana/06.png", 2.9)
image MAT_07 = im.FactorScale("images/minor_arcana/07.png", 2.9)
image MAT_08 = im.FactorScale("images/minor_arcana/08.png", 2.9)
image MAT_09 = im.FactorScale("images/minor_arcana/09.png", 2.9)
image MAT_10 = im.FactorScale("images/minor_arcana/10.png", 2.9)
image MAT_11 = im.FactorScale("images/minor_arcana/11.png", 2.9)
image MAT_12 = im.FactorScale("images/minor_arcana/12.png", 2.9)
image MAT_13 = im.FactorScale("images/minor_arcana/13.png", 2.9)
image MAT_14 = im.FactorScale("images/minor_arcana/14.png", 2.9)
image MAT_15 = im.FactorScale("images/minor_arcana/15.png", 2.9)
image MAT_16 = im.FactorScale("images/minor_arcana/16.png", 2.9)
image MAT_17 = im.FactorScale("images/minor_arcana/17.png", 2.9)
image MAT_18 = im.FactorScale("images/minor_arcana/18.png", 2.9)
image MAT_19 = im.FactorScale("images/minor_arcana/19.png", 2.9)
image MAT_20 = im.FactorScale("images/minor_arcana/20.png", 2.9)
image MAT_21 = im.FactorScale("images/minor_arcana/21.png", 2.9)
image MAT_22 = im.FactorScale("images/minor_arcana/22.png", 2.9)
image MAT_23 = im.FactorScale("images/minor_arcana/23.png", 2.9)
image MAT_24 = im.FactorScale("images/minor_arcana/24.png", 2.9)
image MAT_25 = im.FactorScale("images/minor_arcana/25.png", 2.9)
image MAT_26 = im.FactorScale("images/minor_arcana/26.png", 2.9)
image MAT_27 = im.FactorScale("images/minor_arcana/27.png", 2.9)
image MAT_28 = im.FactorScale("images/minor_arcana/28.png", 2.9)
image MAT_29 = im.FactorScale("images/minor_arcana/29.png", 2.9)
image MAT_30 = im.FactorScale("images/minor_arcana/30.png", 2.9)
image MAT_31 = im.FactorScale("images/minor_arcana/31.png", 2.9)
image MAT_32 = im.FactorScale("images/minor_arcana/32.png", 2.9)
image MAT_33 = im.FactorScale("images/minor_arcana/33.png", 2.9)
image MAT_34 = im.FactorScale("images/minor_arcana/34.png", 2.9)
image MAT_35 = im.FactorScale("images/minor_arcana/35.png", 2.9)
image MAT_36 = im.FactorScale("images/minor_arcana/36.png", 2.9)
image MAT_37 = im.FactorScale("images/minor_arcana/37.png", 2.9)
image MAT_38 = im.FactorScale("images/minor_arcana/38.png", 2.9)
image MAT_39 = im.FactorScale("images/minor_arcana/39.png", 2.9)
image MAT_40 = im.FactorScale("images/minor_arcana/40.png", 2.9)

########################################################################################
#ПЕРЕМЕННЫЕ


# Основная переменная, суть которой подсчет очков выбора игрока между действиями выбора, 
# влияющая на то какая концовка послесловия будет продемонстрированная игроку по окончанию игры.
define ppoints = 0
define PP = 0

# Переменная нужная для того чтобы определит, сказал ли персонаж свое имя или нет.
define DollCam = False

# Переменная определяет имеется у игрока доступ в данную комнату или нет.
define WCRoom = False
define WCRoom_01 = False
define WCC = False

# Переменная, которая меняется при посещении комнате, и впоследствии определяет, какая сцена будет показана игроку.
define Wite = False

#Переменные для доступа на скрытый этаж, и скрытую историю.
define enigma_01 = False
define enigma_02 = False

#перемноживания матриц
$ brightness_opacity = brightness * opacity
$ fraktal_04_opacity = fraktal_04 * opacity
$ fraktal_01_fraktal_03 = fraktal_01 * fraktal_03


#переменная для определения лестничных клеток

define hallway_001 = False
define hallway_002 = False
define hallway_003 = False
define hallway_004 = False
define hallway_005 = False
define hallway_006 = False
define hallway_007 = False
define hallway_008 = False
define hallway_009 = False
define hallway_010 = False
define hallway_011 = False

# Переменные от 00 до ХХ служащие для определения посещения комнат.
define Room_01 = False
define Room_02 = False
define Room_03 = False
define Room_04 = False
define Room_05 = False
define Room_06 = False
define Room_07 = False
define Room_08 = False
define Room_09 = False
define Room_10 = False
define Room_11 = False
define Room_12 = False
define Room_13 = False
define Room_14 = False
define Room_15 = False
define Room_16 = False
define Room_17 = False
define Room_18 = False
define Room_19 = False
define Room_20 = False
define Room_21 = False
define Room_22 = False
define Room_23 = False
define Room_24 = False
define Room_25 = False
define Room_26 = False
define Room_27 = False
define Room_28 = False
define Room_29 = False
define Room_30 = False
define Room_31 = False
define Room_32 = False
define Room_33 = False
define Room_34 = False
define Room_35 = False
define Room_36 = False
define Room_37 = False
define Room_38 = False
define Room_39 = False
define Room_40 = False

#Переменная необхадимая чтобы сделат бесконечную череду комнат
define Room_infiniti = 0

# переменные необходимые как метки для определения посещения разных купе в вагона
define KupeRoom01 = False
define KupeRoom02 = False
define KupeRoom03 = False
define KupeRoom04 = False
define KupeRoom05 = False

# Переменная нужная для определения того был ли прочитан журнал лежащий в почтовом ящике.
define Jurnal = False
define Key = False
define Key_01 = False
define Key_02 = False
define Key_03 = False
define Key_04 = False
define Key_05 = False
define Key_06 = False

#дополнительные переменные в квартирах

#фомка

define fomka = False
define fomka_endurance = 0

#Квартира 002 вариант 01 этаж 02

define hallway_prihojay_002_01 = 0
define hallway_prihojay_002_02 = False
define F_room_002_01_01 = 0
define F_room_002_02_01 = 0
define F_room_002_03_01 = 0
define F_room_002_04_01 = 0
define F_room_002_kitchen_01 = 0
define F_room_002_Windows_01 = 0
define F_room_002_WC_01 = False
define F_room_002_bathroom_01 = False

# квартира 002 вариант 02 этаж 02

define Box_002_02_01 = False
define F_Room_002_01 = 0
define cards_Key = False

#Квартира 003 этаж 02

define Key_flat_01 = False

# Переменная необхадимая чтобы определит пошла ли МВ по следам, или рещила сночала осмотрет осталные этожи.
define traces_01 = False

#переменная нужная для определения если ГГ побывала в дополнительном блоке четвертой главы
define Under_01 = False

# Переменная необходимая для определения того что МВ взяла пульт от телевизора
define remote_controller = False
define Batter_01 = False

#переменная необходимая для определения быль ли просмотрен определенный телевизор
define TV_01 = False


#квартира 036
define Key_shees_enigma_01 = False

$ brightness_opacity = brightness * opacity
$ fraktal_04_opacity = fraktal_04 * opacity
$ fraktal_01_fraktal_03 = fraktal_01 * fraktal_03

#############################################################################
#ПЕРСОНАЖИ
#NVL

define nn = Character(None, 
                    what_size = 45, 
                    what_font ="fonts/GOST_A.ttf", 
                    color="#c8ffc8", 
                    kind=nvl
                    )

#=================================================================
#СЮЖЕТНЫЕ
#=================================================================

#image='Little_witch'
define LW = Character('Маленькая ведьма', 
        color="#6f0ead",
        outlines = [ (2, "#000000") ],
        what_size = 35,
        what_color = "#541f82", 
        what_outlines = [ (2, "#000000") ],
        ctc = anim.Filmstrip(im.FactorScale("images/Ani/LIFE_01.png", 0.15), 
                            (127, 130), 
                            (4, 1), 
                            .50, 
                            xpos=1700, 
                            ypos=950, 
                            xanchor=0, 
                            yanchor=0
                            ),
        ctc_position = "fixed"
        )

define HM = Character('Хранительница Миров', 
        color="#aaaa00",
        outlines = [ (2, "#000000") ],
        what_size = 35,
        what_color = "#aaaa98",
        what_outlines = [ (2, "#000000") ],
        ctc = anim.Filmstrip(im.FactorScale("images/Ani/LIFE_02.png", 0.3),
                            (168, 110),
                            (5, 1),
                            .50,
                            xpos=1700,
                            ypos=950,
                            xanchor=0,
                            yanchor=0
                            ),
        ctc_position = "fixed"
        )

define GO = Character('Голос Океана', 
        color="#063271", 
        outlines = [ (2, "#000000") ],
        what_size = 35,
        what_color = "#009fe6",
        what_outlines = [ (2, "#000000") ]
        )

define FN = Character('Неизвестные', 
        color="#440047", 
        outlines = [ (2, "#000000") ],
        what_size = 35,
        what_color = "#6A0026",
        what_outlines = [ (2, "#000000") ]
        )

define Doll = Character('Кукла', 
        color="#9A5D9D",
        outlines = [ (2, "#000000")],
        what_size = 35,
        what_color = "#7D0F80",
        what_outlines = [ (2, "#000000")]
        )

define Cam = Character('Кампанелла', 
        color="#9A5D9D",
        outlines = [ (2, "#000000")],
        what_size = 35,
        what_color = "#7D0F80",
        what_outlines = [ (2, "#000000")]
        )

define Ananim = Character('???', 
        color="#009fe6",
        outlines = [(2, "#000000")],
        what_size = 35,
        what_color = "#440047",
        what_outlines = [(2, "#000000")]
        )

define Shu = Character('Мара', 
        color="#7A0026",
        outlines = [(2, "#000000")],
        what_size = 35,
        what_color = "#EC008C",
        what_outlines = [(2, "#000000")]
        )

define men = Character('Байкер', 
        color="#363636",
        what_size = 35,
        what_color = "#A1A1A1",
        what_outlines = [(2, "#000000")]
        )

define monster = Character('Монстр', 
        color="#063271", 
        outlines = [ (2, "#000000") ],
        what_size = 35,
        what_color = "#009fe6",
        what_outlines = [ (2, "#000000") ]
        )

define FC = Character('Фосфорная Кошка', 
        color="#8560a8", 
        outlines = [ (2, "#000000") ],
        what_size = 35,
        what_color = "#5674b9",
        what_outlines = [ (2, "#000000") ]
        )

define CO = Character('Корабль-оболочка', 
        color="#51e9e4",
        outlines = [(2, "#000000")],
        what_size = 35,
        what_color = "#e4e951",
        what_outlines = [ (2, "#000000") ]
        )

define CC = Character('Син-Син', 
        color="#6836A1",
        outlines = [(2, "#000000")],
        what_size = 35,
        what_color = "#A1368E",
        what_outlines =[(2, "#000000")]
        )

define ZBE = Character('Звездочет', 
        color="#E5CC2A",
        outlines = [(2, "#000000")],
        what_size = 35,
        what_color = "#B9FAA5",
        what_outlines =[(2, "#000000")]
        )

define LO = Character('Лохматый', 
        color="#2ACDE5",
        outlines = [(2, "#000000")],
        what_size = 35,
        what_color = "#37646B",
        what_outlines =[(2, "#000000")]
        )

#=========================================================================
# основной стиль текста
#=========================================================================

define e = Character(None, 
                        what_size = 35, 
                        what_font = "fonts/segoescript.ttf", 
                        what_outlines = [(3, "#0008", 2, 2), (3, "#0068b3", 0, 0)], 
                        what_layout = "subtitle", 
                        window_background="#00000000",what_xalign = 0.5, 
                        what_text_align = 0.5, cps = 25, 
                        window_xfill = False, 
                        window_xalign = 0.5
                        )

#define en = Character(None, kind=nvl)

#===========================================================================
#ШРИФТЫ(Задам стилем ибо могу)
#===========================================================================
#СТИЛЬ - Чепятная машинка(typewriter)

style typewr is text:
    size 30
    color "#ffffff"
    font "fonts/DS-Moster.ttf"

#===============================================================================
#ФОНЫ
#===============================================================================

#===============================================================================
#ПОНГ
#===============================================================================

image bg pong field = "images/pong/pong_field.png"

################################################################################

#===============================================================================
#СТАРТОВЫЙ СПЛЭШ
#===============================================================================

image start_splash = Transform(
    Composite(
        (1920, 1080),
        (0, 0), Solid("#000000"),
        (0, 0), im.Alpha("gui/start_splash/splash_wallp.jpg", 0.347)
    ),
    matrixcolor=BrightnessMatrix(-0.09)
)

#================================================================================
#СЮЖЕТНЫЕ
#================================================================================

image bg0000 = "images/texture/Blek.jpg"
image bg0000a = "images/BG/0000a.jpg"
image bg0000b = "images/BG/0000b.jpg"
image bg0000c = "images/texture/Withe.jpg"
image bg0001 = "images/BG/0001.jpg"
image bg0002 = "images/BG/0002.jpg"
image bg0003 = "images/BG/0003.jpg"
#Movie(play="images/BG/0001/generated_video_00.mp4")
image bg0004:
    Movie(play="images/BG/0001/generated_video_00.WEBM")
    zoom 3.0
    #repeat
image bg0005:
    "images/BG/0005a.jpg" with dissolve
    pause 0.5
    "images/BG/0005b.jpg" with dissolve
    pause 1.5
    repeat
image bg0006 = "images/BG/0006.jpg"
image bg0007 = "images/BG/0007.jpg"
image bg0008 = "images/BG/0008.jpg"
image a0008:
    "images/BG/0008.jpg"
    matrixcolor InvertMatrix(1.0)

image bg0009 = "images/BG/0009.jpg"
image bg0010 = "images/BG/0010.jpg"
image bg0011 = "images/BG/0011.jpg"
image bg0012 = "images/BG/0012.jpg"
image bg0012a = "images/BG/0012a.jpg"
image bg0013 = "images/BG/0013.jpg"
image bg0014:
    "images/BG/0014.jpg"
    pause 3.0
    
    "images/BG/0015.jpg" with dissA
    pause 3.0
    
    "images/BG/0016.jpg" with dissA
    pause 3.0
    
    "images/BG/0014.jpg" with dissA
    
    repeat
image bg0015 = "images/BG/0014.jpg"
image bg0016 = "images/BG/0015.jpg"
image bg0017 = "images/BG/0016.jpg"
image bg0018 = "images/BG/0017.jpg"
image bg0019 = "images/BG/0018.jpg"
image bg0020 = "images/BG/0019.jpg"
image bg0021 = "images/BG/0020.jpg"
image bg0022 = "images/BG/0021.jpg"
image bg0023 = "images/BG/0022.jpg"
image bg0024 = "images/BG/0023.jpg"
image bg0025 = "images/BG/0024.jpg"
image bg0026 = "images/BG/0025.jpg"
image bg0027 = "images/BG/0026.jpg"
image bg0028 = "images/BG/0027.jpg"
image bg0029 = "images/BG/0028.jpg"
image bg0030 = "images/BG/0029.jpg"
image bg0031 = "images/BG/0030.jpg"
image bg0032 = "images/BG/0031.jpg"
image bg0033 = "images/BG/0032.jpg"
image bg0034:
    contains:
        "images/BG/0033.jpg"
        
    contains:
        "images/BG/0033b.png"
        alpha 0.4

    contains:
        "images/BG/0033a.png"
        alpha 0.6

    contains:
        "images/BG/0033c.png"
        matrixcolor color_01

image bg0036 = "images/BG/0035.jpg"
image bg0037 = "images/BG/0036.jpg"
image bg0038 = "images/BG/0037.jpg"
image bg0039 = "images/BG/0038.jpg"
image bg0040 = "images/BG/0039.jpg"
image a0041:
    "images/BG/0038a.jpg"
    contains:
        "Logo/Alaya_IU.png"
        alpha 0.5

image bg0041:
    contains:
        "images/BG/0038a.jpg"
        parallel:
            matrixcolor BrightnessMatrix(-0.5)
            easein 1.5 matrixcolor BrightnessMatrix(-0.35)
            pause 0.7
            easeout 1.5 matrixcolor BrightnessMatrix(-0.5)
            repeat
    contains:
        "Logo/Alaya_IU.png"
        parallel:
            alpha 0.2
            ease 1.5 alpha 0.4
            pause 0.7
            ease 1.5 alpha 0.2
            repeat
        parallel:
            matrixcolor BrightnessMatrix(-0.65)
            easein 1.5 matrixcolor BrightnessMatrix(-0.45)
            pause 0.7
            easeout 1.5 matrixcolor BrightnessMatrix(-0.65)
            repeat
    
image bg0042 = "images/BG/0038a.jpg"
image bg0043 = "images/BG/0039a.jpg"
image bg0044:
    contains:
        "images/BG/0040c.jpg" with dissolve
        easeout 1.5 matrixcolor BrightnessMatrix(-0.60)
        "images/BG/0040b.jpg" with dissolve
        easeout 1.5 matrixcolor BrightnessMatrix(-0.44)
        "images/BG/0040a.jpg" with dissolve
        easeout 1.5 matrixcolor BrightnessMatrix(-0.22)
        "images/BG/0040b.jpg" with dissolve
        easeout 1.5 matrixcolor BrightnessMatrix(-0.44)
        repeat

    contains:
        "Logo/Alaya_IU_01.png" with dissolve
        alpha 0.5
        easeout 1.5 matrixcolor BrightnessMatrix(-0.40)
        easeout 1.5 matrixcolor BrightnessMatrix(-0.30)
        easeout 1.5 matrixcolor BrightnessMatrix(-0.20)
        easeout 1.5 matrixcolor BrightnessMatrix(-0.30)
        repeat
image bg0045 =  "images/BG/0040c.jpg"
image bg0046:
    contains:
        "images/BG/0039a.jpg" with dissolve
    contains:
        "Logo/Alaya_IU.png"
        alpha 0.35
    matrixcolor BrightnessMatrix(-0.80)
    easeout 1.85 matrixcolor BrightnessMatrix(-0.45)
    easeout 1.65 matrixcolor BrightnessMatrix(-0.70)
    easeout 1.85 matrixcolor BrightnessMatrix(-0.80)
    repeat
    
image bg0047 = "images/BG/0041.jpg"
image bg0048 = "images/BG/0042.jpg"
image bg0049 = "images/BG/0043.jpg"
image bg0050 = "images/BG/0044.jpg"
image bg0051 = "images/BG/0045.jpg"
image bg0052 = "images/BG/0046.jpg"
image bg0053 = "images/BG/0047.jpg"
image bg0054 = "images/BG/0048.jpg"
image bg0055 = "images/BG/0049.jpg"
image bg0056 = "images/BG/0050.jpg"
image bg0057 = "images/BG/0051.jpg"
image bg0058 = "images/BG/0052.jpg"
image bg0059 = "images/BG/0053.jpg"
image bg0060 = "images/BG/0054.jpg"
image bg0061 = "images/BG/0055.jpg"
image bg0062 = "images/BG/0056.jpg"
image bg0063:
    "images/BG/0057.jpg"
    zoom 1.27
    
image bg0064:
    "images/BG/0058b.png"
    alpha 0.6
    xzoom 1.5
    yzoom 1.0
    
image bg0065:
    "images/BG/0058a.jpg"
    xzoom 1.8
    yzoom 2.0

image bg0066 = "images/BG/0059.jpg"
image bg0067:
    "images/BG/0057.jpg"
    zoom 1.1
image bg0068 = "images/BG/0060.jpg"
image bg0069 = "images/BG/0061.jpg"
image bg0070 = "images/BG/0062.jpg"
image bg0071 = "images/BG/0063.jpg"
image bg0072 = "images/BG/0064.jpg"
image bg0073 = "images/BG/0065.jpg"
image bg0074 = "images/BG/0066.jpg"
image bg0075 = "images/BG/0067.jpg"
image bg0076 = "images/BG/0068.jpg"
image bg0077 = "images/BG/0069.jpg"
image bg0078 = "images/BG/0070.jpg"
image bg0079 = "images/BG/0071.jpg"
image bg0080 = "images/BG/0072.jpg"
image bg0081 = "images/BG/0073.jpg"
image bg0082 = "images/BG/0074.jpg"
image bg0083 = "images/BG/0075.jpg"
image bg0084 = "images/BG/0076.jpg"
image bg0085 = "images/BG/0077.jpg"
image bg0086 = "images/BG/0078.jpg"
image bg0087 = "images/BG/0079.jpg"
image bg0089 = "images/BG/0080.jpg"
image bg0090 = "images/BG/0081.jpg"
image bg0091 = "images/BG/0082.jpg"
image bg0092 = "images/BG/0083.jpg"
image bg0093 = "images/BG/0084.jpg"
image bg0094 = "images/BG/0085.jpg"
image bg0095 = "images/BG/0086.jpg"
image bg0096 = "images/BG/0087.jpg"
image bg0097:
    "images/BG/0071.jpg"
    contains:
        "images/sprites/SLW/LW_slip_01.png"
        pos (-60, 150)
        
image bg0098:
    "images/BG/0072.jpg",
    contains:
        "images/sprites/SLW/LW_slip_01.png"
        pos (- 60, 150)

image bg0099 = "images/BG/0088.jpg"
image bg0100 = "images/BG/0089.jpg"
image bg0101 = "images/BG/0090.jpg"
image bg0102 = "images/BG/0091.jpg"
image bg0103 = "images/BG/0092.jpg"
image bg0104 = "images/BG/0093.jpg"
image bg0105 = "images/BG/0094.jpg"
image bg0106 = "images/BG/0095.jpg"
image bg0107 = "images/BG/0096.jpg"
image bg0108 = "images/BG/0097.jpg"
image bg0109 = "images/BG/0098.jpg"
#image F_masked = im.AlphaMask("Mask.png", "pod.png")

#=================================================================
# текстуры
#=================================================================

#region бумага
image peper_01:
    contains:
        Solid("#000000")

    contains:
        "images/texture/peper_02.jpg"
        alpha 0.347
        matrixcolor SepiaMatrix()
        
    contains:
        "images/texture/the_letters_03.jpg"
        alpha 0.3

    matrixcolor BrightnessMatrix(-0.09)

image peper_02:
    contains:
        Solid("#000000")

    contains:
        "images/texture/peper_05.jpg"
        alpha 0.347
        matrixcolor SepiaMatrix()
        
    contains:
        "images/texture/the_letters_03.jpg"
        alpha 0.3 

    matrixcolor BrightnessMatrix(-0.09)


image peper_03:
    contains:
        Solid("#000000")

    contains:
        "images/texture/peper_06.jpg"
        alpha 0.347
        matrixcolor SepiaMatrix()
        
    contains:
        "images/texture/the_letters_03.jpg"
        alpha 0.3 

    matrixcolor BrightnessMatrix(-0.09)
#endregion Region name

#================================================================================
#цветочные
#================================================================================

image floralt_01 = Composite(
        (1920, 1080),
        (0, 0), Solid("#000000"),
        (0, 0), im.Alpha("images/texture/floral_texture_01.jpg", 0.9),
        (0, 0), im.Sepia(im.Alpha("images/texture/muar_01.png", 0.3))
    )
    
#==================================================================================   
#концовки
#==================================================================================

image DEnd:
    contains:
        "images/END/END_00.jpg"
        matrixcolor SepiaMatrix()
    contains:
        "images/END/END_02.jpg"
        alpha 0.7
    contains:
        "images/END/END_01.jpg"
        alpha 0.347
        
    matrixcolor BrightnessMatrix(-0.09)


####################################################################################
#СПРАЙТЫ
#МАЛЕНЬКАЯ ВЕДЬМА
#составные спрайты

# ===================================================
# АНИМИРОВАННАЯ КОСА
# ===================================================

# Вариант 1 — слабый ветер
image SLW_kassa_wind_01:
    Composite(
        (5000, 6800),
        (1000, 630),
        "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_01.png"
    )
    pause 0.5
    Composite(
        (5000, 6800),
        (1150, 600),
        "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_02.png"
    )
    pause 0.5
    Composite(
        (5000, 6800),
        (1300, 580),
        "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_03.png"
    )
    pause 0.5
    Composite(
        (5000, 6800),
        (1500, 670),
        "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_04.png"
    )
    pause 0.5
    Composite(
        (5000, 6800),
        (1150, 600),
        "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_02.png"
    )
    pause 0.5
    repeat

# Вариант 2 — средний ветер
image SLW_kassa_wind_02:
    contains:
        # Покадровая анимация кадров
        Composite(
            (5000, 6800),
            (2000, 630),
            "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_01.png"
        )
        pause 0.5
        Composite(
            (5000, 6800),
            (2150, 600),
            "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_02.png"
        )
        pause 0.5
        Composite(
            (5000, 6800),
            (2300, 580),
            "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_03.png"
        )
        pause 0.5
        Composite(
            (5000, 6800),
            (2500, 670),
            "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_04.png",
        )
        pause 0.5
        Composite(
            (5000, 6800),
            (2150, 600),
            "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_02.png"
        )
        pause 0.5
        repeat

    # Качание всей анимации
    rotate_pad False
    xanchor 0.5
    yanchor 0.0
    block:
        ease 0.5 rotate 7
        easeout 1.5 rotate -3
        repeat

# Вариант 3 — сильный ветер
# ИСПРАВЛЕНО: убран некорректный parallel внутри image ATL
# Используем простое чередование кадров с разными позициями
# Отдельные кадры кассы
# Финальная сборка с rotate отдельно
image SLW_kassa_wind_03:
    contains:
        # Покадровая анимация кадров
        Composite(
            (5000, 6800),
            (2000, 630),
            Transform(
                "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_01.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (5000, 6800),
            (2150, 600),
            Transform(
                "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_02.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (5000, 6800),
            (2300, 580),
            Transform(
                "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_03.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (5000, 6800),
            (2500, 670),
            Transform(
                "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_04.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (5000, 6800),
            (2150, 600),
            Transform(
                "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_02.png",
                zoom=0.75
            )
        )
        pause 0.5
        repeat

    # Качание всей анимации
    rotate_pad False
    xanchor 0.5
    yanchor 0.0
    block:
        ease 0.2 rotate 15
        easeout 0.8 rotate 3
        ease 0.4 rotate 8
        easeout 1.5 rotate -4
        repeat

# Статичная коса (без ветра)
image SLW_kassa_still:
    Composite(
        (5000, 6800),
        (2500, 600),
        "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_01.png"
    )

# Выбор анимации косы с учётом ветра
image SLW_kassa_01 = ConditionSwitch(
    "wind_01 == 1", "SLW_kassa_wind_01",
    "wind_01 == 2", "SLW_kassa_wind_02",
    "wind_01 == 3", "SLW_kassa_wind_03",
    "True",         "SLW_kassa_still"
)

# ===================================================
# LAYEREDIMAGE — Маленькая Ведьма
# ===================================================
# ИСПРАВЛЕНО:
#   - убрано дублирование group brov
#   - brov_norm_01 оставлен в одной группе (непрозрачный вариант)
#   - атрибут SH помечен default

layeredimage Little_witch:

    always:
        Null()

    # Коса
    attribute kassa_01 default:
        "SLW_kassa_01"


# цветные спрайты

# в полный рост
# Основной спрайт с анимацией моргания

image LW_Norma_Color_01 = anim. SMAnimation("ax",
    anim.State ("ax", "images/sprites/SLW/LW_Norma01.png"),
    anim.Edge ("ax", 1.0, "ax", prob=7),
    anim.Edge ("ax", 0.25, "bx"),
    anim.State ("bx","images/sprites/SLW/LW_Norma02.png"),
    anim.Edge ("bx", 0.25, "cx"),
    anim.State ("cx", "images/sprites/SLW/LW_Norma03.png"),
    anim.Edge ("cx", 0.25, "dx"),
    anim.State ("dx", "images/sprites/SLW/LW_Norma02.png"),
    anim.Edge ("dx", 0.5, "ax")
    ) 

image LW_Color_Nor_a_01 = "images/sprites/SLW/LW_Norma_a_01.png"
image LW_Color_Nor_a_02 = "images/sprites/SLW/LW_Norma_a_07.png"

image LW_Color_NormaBust_a_01 = "images/sprites/SLW/LW_Norma_a_26.png"
image LW_Color_NormaBust_a_02 = "images/sprites/SLW/LW_Norma_a_27.png"
    

#наклон стеснительно-заигрующе
image LW_Color_Nak_a_04 = "images/sprites/SLW/LW_Nak_a_04.png" 

#наклон гловы
image LW_Color_Nak_a_01 = "images/sprites/SLW/LW_Nak_a_01.png"
image LW_Color_Nak_a_02 = "images/sprites/SLW/LW_Nak_a_02.png"
image LW_NakBust_a_03 = im.FactorScale("images/sprites/SLW/LW_Nak_a_03.png", 0.15, 0.15)

#2/3 наклон
image LW_Color_Nak_a_05 = "images/sprites/SLW/LW_Nak_a_05.png"
image LW_Color_Nak_a_06 = "images/sprites/SLW/LW_Nak_a_06.png"  

#2/3
image LW_Color_Nak_a_07 = "images/sprites/SLW/LW_Nak_a_07.png"
  
#доволная
image LW_Color_Nak_a_08 = "images/sprites/SLW/LW_Nak_a_08.png"
    

image LW_NormFull_01 = anim. SMAnimation("ax",
    anim.State ("ax", im.FactorScale("images/sprites/SLW/LW_Norma01.png", 0.1, 0.1)),
    anim.Edge ("ax", 1.0, "ax", prob=7),
    anim.Edge ("ax", 0.25, "bx"),
    anim.State ("bx", im.FactorScale("images/sprites/SLW/LW_Norma02.png", 0.1, 0.1)),
    anim.Edge ("bx", 0.25, "cx"),
    anim.State ("cx", im.FactorScale("images/sprites/SLW/LW_Norma03.png", 0.1, 0.1)),
    anim.Edge ("cx", 0.25, "dx"),
    anim.State ("dx", im.FactorScale("images/sprites/SLW/LW_Norma02.png", 0.1, 0.1)),
    anim.Edge ("dx", 0.5, "ax")
    ) 
    
image LW_nf_01 = im.FactorScale("images/sprites/SLW/LW_Norma02.png", 0.1, 0.1)
image LW_nf_02 = im.FactorScale("images/sprites/SLW/LW_Norma03.png", 0.1, 0.1)
    
#наклон гловы
image LW_NakFull_a_01 = im.FactorScale("images/sprites/SLW/LW_Nak_a_01.png", 0.1, 0.1)
image LW_NakFull_a_02 = im.FactorScale("images/sprites/SLW/LW_Nak_a_02.png", 0.1, 0.1)
image LW_NakFull_a_03 = im.FactorScale("images/sprites/SLW/LW_Nak_a_03.png", 0.1, 0.1)
    
#2/3
image WL_NakFull_a_07 = im.FactorScale("images/sprites/SLW/LW_Nak_a_07.png", 0.1, 0.1)
    
#2/3 наклон
image WL_NakFull_a_05 = im.FactorScale("images/sprites/SLW/LW_Nak_a_05.png", 0.1, 0.1)
image WL_NakFull_a_06 = im.FactorScale("images/sprites/SLW/LW_Nak_a_06.png", 0.1, 0.1)
    
#наклон стеснительно-заигрующе
image WL_NakFull_a_04 = im.FactorScale("images/sprites/SLW/LW_Nak_a_04.png", 0.1, 0.1) 
    
#доволная
image WL_NakFull_a_08 = im.FactorScale("images/sprites/SLW/LW_Nak_a_08.png", 0.1, 0.1)
    
image LW_NorFull_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_01.png", 0.1, 0.1)
image LW_NorFull_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_07.png", 0.1, 0.1)
image LW_NorFull_a_03 = im.FactorScale("images/sprites/SLW/LW_Norma_a_10.png", 0.1, 0.1)
image LW_NorFull_a_04 = im.FactorScale("images/sprites/SLW/LW_Norma_a_13.png", 0.1, 0.1)
    
#глаза закрыты
image LW_NorFullEyesOff_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_02.png", 0.1, 0.1)
image LW_NorFullEyesOff_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_05.png", 0.1, 0.1)
    
#Разговор глаза закрыты
image LW_NorFullRazEyesOff_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_03.png", 0.1, 0.1)
image LW_NorFullRazEyesOff_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_04.png", 0.1, 0.1)
    
#удивленно напугана
image LW_NorFullHorror_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_06.png", 0.1, 0.1)
image LW_NorFullHorror_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_25.png", 0.1, 0.1)
    
#разговор
image LW_NorFullRaz_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_08.png", 0.1, 0.1)
image LW_NorFullRaz_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_21.png", 0.1, 0.1)
image LW_NorFullRaz_a_03 = im.FactorScale("images/sprites/SLW/LW_Norma_a_23.png", 0.1, 0.1)
    
#Язык
image LW_NorFullLeng_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_09.png", 0.1, 0.1)
    
#Удивлена
image LW_NorFullUdivlena_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_11.png", 0.1, 0.1)
    
#стеснается
image LW_NorFullShyUdivlena_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_12.png", 0.1, 0.1)
image LW_NorFullShy_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_14.png", 0.1, 0.1)
image LW_NorFullShy_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_19.png", 0.1, 0.1)
image LW_NorFullShy_a_03 = im.FactorScale("images/sprites/SLW/LW_Norma_a_20.png", 0.1, 0.1)
image LW_NorFullShyEyesOff_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_17.png", 0.1, 0.1)
image LW_NorFullShyRaz_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_15.png", 0.1, 0.1)
image LW_NorFullShyRaz_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_22.png", 0.1, 0.1)
image LW_NorFullShyRaz_a_03 = im.FactorScale("images/sprites/SLW/LW_Norma_a_24.png", 0.1, 0.1)
image LW_NorFullShyRazEyesOff_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_18.png", 0.1, 0.1)
image LW_NorFullShyHorror_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_16.png", 0.1, 0.1)
    
# спит
image LW_sl_01 = "images/sprites/SLW/LW_slip_01.png"
    
# C
    
image LW_NormFull_c_01 = anim.SMAnimation("ax",
    anim.State ("ax", im.FactorScale("images/sprites/SLW/LW_Norma_c_01.png", 0.1, 0.1)),
    anim.Edge ("ax", 1.0, "ax", prob=7),
    anim.Edge ("ax", 0.25, "bx"),
    anim.State ("bx", im.FactorScale("images/sprites/SLW/LW_Norma_c_02.png", 0.1, 0.1)),
    anim.Edge ("bx", 0.25, "cx"),
    anim.State ("cx", im.FactorScale("images/sprites/SLW/LW_Norma_c_03.png", 0.1, 0.1)),
    anim.Edge ("cx", 0.25, "dx"),
    anim.State ("dx", im.FactorScale("images/sprites/SLW/LW_Norma_c_02.png", 0.1, 0.1)),
    anim.Edge ("dx", 0.5, "ax")
    ) 



image LW_NorFull_c_02 = im.FactorScale("images/sprites/SLW/LW_Norma_c_01.png", 0.1, 0.1)
image LW_NorFull_c_03 = im.FactorScale("images/sprites/SLW/LW_Norma_c_02.png", 0.1, 0.1)
image LW_NorFull_c_04 = im.FactorScale("images/sprites/SLW/LW_Norma_c_03.png", 0.1, 0.1)
image LW_NorFull_c_06 = im.FactorScale("images/sprites/SLW/LW_Norma_c_04.png", 0.1, 0.1)
    
#наклон головы
image LW_NorFull_c_17 = im.FactorScale("images/sprites/SLW/LW_Norma_c_16.png", 0.1, 0.1)
image LW_NorFull_c_18 = im.FactorScale("images/sprites/SLW/LW_Norma_c_17.png", 0.1, 0.1)
image LW_NorFull_c_19 = im.FactorScale("images/sprites/SLW/LW_Norma_c_18.png", 0.1, 0.1)
    
# показывает Язык
image LW_NorFull_c_07 = im.FactorScale("images/sprites/SLW/LW_Norma_c_06.png", 0.1, 0.1)
    
#подозрительная
image LW_NorFull_c_08 = im.FactorScale("images/sprites/SLW/LW_Norma_c_07.png", 0.1, 0.1)
    
# Разговор 
image LW_NorFull_c_09 = im.FactorScale("images/sprites/SLW/LW_Norma_c_08.png", 0.1, 0.1)
    
#закрытие глаза разговор, 
image LW_NorFull_c_10 = im.FactorScale("images/sprites/SLW/LW_Norma_c_09.png", 0.1, 0.1)
image LW_NorFull_c_14 = im.FactorScale("images/sprites/SLW/LW_Norma_c_13.png", 0.1, 0.1)
image LW_NorFull_c_15 = im.FactorScale("images/sprites/SLW/LW_Norma_c_14.png", 0.1, 0.1)
    
#удивленная подозрительная
image LW_NorFull_c_11 = im.FactorScale("images/sprites/SLW/LW_Norma_c_10.png", 0.1, 0.1)
    
#Хорор удивленная
image LW_NorFull_c_12 = im.FactorScale("images/sprites/SLW/LW_Norma_c_11.png", 0.1, 0.1)
    
# кислая
image LW_NorFull_c_13 = im.FactorScale("images/sprites/SLW/LW_Norma_c_12.png", 0.1, 0.1)
    
# кислая, глаза закрыти
image LW_NorFull_c_16 = im.FactorScale("images/sprites/SLW/LW_Norma_c_15.png", 0.1, 0.1)
    
# поза 02
image LW_NorFull_c_05 = im.FactorScale("images/sprites/SLW/LW_Norma_c_05.png", 0.1, 0.1)
    
#наклон стеснительно-заигрующе
image LW_NorFull_c_20 = im.FactorScale("images/sprites/SLW/LW_Norma_c_19.png", 0.1, 0.1)
image LW_NorFull_c_21 = im.FactorScale("images/sprites/SLW/LW_Norma_c_20.png", 0.1, 0.1)
    
    
# спрайт ближный план
image LW_NormBust_01 = anim. SMAnimation("ax",
    anim.State ("ax", im.FactorScale("images/sprites/SLW/LW_Norma01.png", 0.15, 0.15)),
    anim.Edge ("ax", 1.0, "ax", prob=7),
    anim.Edge ("ax", 0.25, "bx"),
    anim.State ("bx", im.FactorScale("images/sprites/SLW/LW_Norma02.png", 0.15, 0.15)),
    anim.Edge ("bx", 0.25, "cx"),
    anim.State ("cx", im.FactorScale("images/sprites/SLW/LW_Norma03.png", 0.15, 0.15)),
    anim.Edge ("cx", 0.25, "dx"),
    anim.State ("dx", im.FactorScale("images/sprites/SLW/LW_Norma02.png", 0.15, 0.15)),
    anim.Edge ("dx", 0.5, "ax")
    ) 
    
image LW_nb_01 = im.FactorScale("images/sprites/SLW/LW_Norma02.png", 0.15, 0.15)
image LW_nb_02 = im.FactorScale("images/sprites/SLW/LW_Norma03.png", 0.15, 0.15)
    

  

    



image LW_NorBust_a_03 = im.FactorScale("images/sprites/SLW/LW_Norma_a_10.png", 0.15, 0.15)
image LW_NorBust_a_04 = im.FactorScale("images/sprites/SLW/LW_Norma_a_13.png", 0.15, 0.15)
    
#глаза закрыти
image LW_NorBustEyesOff_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_02.png", 0.15, 0.15)
image LW_NorBustEyesOff_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_05.png", 0.15, 0.15)
    
#Разговор глаза закрыти
image LW_NorBustRazEyesOff_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_03.png", 0.15, 0.15)
image LW_NorBustRazEyesOff_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_04.png", 0.15, 0.15)
    
#удивленно напугана
image LW_NorBustHorror_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_06.png", 0.15, 0.15)
image LW_NorBustHorror_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_25.png", 0.15, 0.15)
    
#разговор
image LW_NorBustRaz_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_08.png", 0.15, 0.15)
image LW_NorBustRaz_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_21.png", 0.15, 0.15)
image LW_NorBustRaz_a_03 = im.FactorScale("images/sprites/SLW/LW_Norma_a_23.png", 0.15, 0.15)
    
#Язык
image LW_NorBustLeng_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_09.png", 0.15, 0.15)
    
#Удивлена
image LW_NorBustUdivlena_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_11.png", 0.15, 0.15)
    
#стеснается
image LW_NorBustShyUdivlena_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_12.png", 0.15, 0.15)
image LW_NorBustShy_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_14.png", 0.15, 0.15)
image LW_NorBustShy_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_19.png", 0.15, 0.15)
image LW_NorBustShy_a_03 = im.FactorScale("images/sprites/SLW/LW_Norma_a_20.png", 0.15, 0.15)
image LW_NorBustShyEyesOff_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_17.png", 0.15, 0.15)
image LW_NorBustShyRaz_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_15.png", 0.15, 0.15)
image LW_NorBustShyRaz_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_22.png", 0.15, 0.15)
image LW_NorBustShyRaz_a_03 = im.FactorScale("images/sprites/SLW/LW_Norma_a_24.png", 0.15, 0.15)
image LW_NorBustShyRazEyesOff_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_18.png", 0.15, 0.15)
image LW_NorBustShyHorror_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_16.png", 0.15, 0.15)
    
# C
image LW_NormBust_c_01 = anim.SMAnimation("ax",
    anim.State ("ax", im.FactorScale("images/sprites/SLW/LW_Norma_c_01.png", 0.15, 0.15)),
    anim.Edge ("ax", 1.0, "ax", prob=7),
    anim.Edge ("ax", 0.25, "bx"),
    anim.State ("bx", im.FactorScale("images/sprites/SLW/LW_Norma_c_02.png", 0.15, 0.15)),
    anim.Edge ("bx", 0.25, "cx"),
    anim.State ("cx", im.FactorScale("images/sprites/SLW/LW_Norma_c_03.png", 0.15, 0.15)),
    anim.Edge ("cx", 0.25, "dx"),
    anim.State ("dx", im.FactorScale("images/sprites/SLW/LW_Norma_c_02.png", 0.15, 0.15)),
    anim.Edge ("dx", 0.5, "ax")
    ) 
    
image LW_NorBust_c_02 = im.FactorScale("images/sprites/SLW/LW_Norma_c_01.png", 0.15, 0.15)
image LW_NorBust_c_03 = im.FactorScale("images/sprites/SLW/LW_Norma_c_02.png", 0.15, 0.15)
image LW_NorBust_c_04 = im.FactorScale("images/sprites/SLW/LW_Norma_c_03.png", 0.15, 0.15)
image LW_NorBust_c_06 = im.FactorScale("images/sprites/SLW/LW_Norma_c_04.png", 0.15, 0.15)
    
#наклон головы
image LW_NorBust_c_17 = im.FactorScale("images/sprites/SLW/LW_Norma_c_16.png", 0.15, 0.15)
image LW_NorBust_c_18 = im.FactorScale("images/sprites/SLW/LW_Norma_c_17.png", 0.15, 0.15)
image LW_NorBust_c_19 = im.FactorScale("images/sprites/SLW/LW_Norma_c_18.png", 0.15, 0.15)
image LW_NorBust_c_22 = im.FactorScale("images/sprites/SLW/LW_Norma_c_21.png", 0.15, 0.15)
    
# показывает Язык
image LW_NorBust_c_07 = im.FactorScale("images/sprites/SLW/LW_Norma_c_06.png", 0.15, 0.15)
    
#подозрительная
image LW_NorBust_c_08 = im.FactorScale("images/sprites/SLW/LW_Norma_c_07.png", 0.15, 0.15)
    
# Разговор 
image LW_NorBust_c_09 = im.FactorScale("images/sprites/SLW/LW_Norma_c_08.png", 0.15, 0.15)
    
#закрытие глаза разговор, 
image LW_NorBust_c_10 = im.FactorScale("images/sprites/SLW/LW_Norma_c_09.png", 0.15, 0.15)
image LW_NorBust_c_14 = im.FactorScale("images/sprites/SLW/LW_Norma_c_13.png", 0.15, 0.15)
image LW_NorBust_c_15 = im.FactorScale("images/sprites/SLW/LW_Norma_c_14.png", 0.15, 0.15)
    
#удивленная подозрительная
image LW_NorBust_c_11 = im.FactorScale("images/sprites/SLW/LW_Norma_c_10.png", 0.15, 0.15)
    
#Хорор удивленная
image LW_NorBust_c_12 = im.FactorScale("images/sprites/SLW/LW_Norma_c_11.png", 0.15, 0.15)
    
# кислая
image LW_NorBust_c_13 = im.FactorScale("images/sprites/SLW/LW_Norma_c_12.png", 0.15, 0.15)
    
# кислая, глаза закрыти
image LW_NorBust_c_16 = im.FactorScale("images/sprites/SLW/LW_Norma_c_15.png", 0.15, 0.15)
    
# поза 02
image LW_NorBust_c_05 = im.FactorScale("images/sprites/SLW/LW_Norma_c_05.png", 0.15, 0.15)
    
# спина спрайты
image LW_Spin_c_01 = im.FactorScale("images/sprites/SLW/LW_Spin_c_01.png", 0.1, 0.1)
image LW_Spin_a_01 = "images/sprites/SLW/LW_Spin_a_01.png"
image LW_Spin_c_02 = im.FactorScale("images/sprites/SLW/LW_Spin_c_02.png", 0.21, 0.21)
    

#наклон стеснительно-заигрующе
image LW_NorBust_c_20 = im.FactorScale("images/sprites/SLW/LW_Norma_c_19.png", 0.15, 0.15)
image LW_NorBust_c_21 = im.FactorScale("images/sprites/SLW/LW_Norma_c_20.png", 0.15, 0.15)
    
#image LW_NorBust_c_01 = im.FactorScale("images/sprites/SLW/LW_Norma_c_05.png", 0.15, 0.15)
    
#N обнаженная
image LW_NFM_01 = im.FactorScale("images/sprites/SLW/LW_Nude_Full_01.png", 0.2, 0.2)
image LW_slip_01 = "images/sprites/SLW/LW_slip_01.png"

#Дракон
image DRC = im.FactorScale(im.Alpha("images/CG/Drakon.png", 0.85), 1.3, 1.3)

#Хранительница Миров




# фанерики

#image:
#                "augustina_dress"
#                matrixcolor TintMatrix("#f00")
#                linear 1 matrixcolor TintMatrix("#0f0")
#                linear 1 matrixcolor TintMatrix("#00f")
#                repeat


#########################################################################################
# добавочные изображения

image ZB = "images/SD/ZB.png"
image B = "images/SD/B.png"
image V = "images/SD/V.png"
image N = "images/SD/N.png"
image C = "images/SD/C.png"
image VP = "images/SD/VP.png"
image ZL = "images/SD/ZL.png"
image D = "images/SD/D.png"
image SF = "images/SD/SF.png"
image SHT ="images/SD/SHT.png"
image GI = "images/SD/GI.png"
image SNO = "images/SD/Snow.png"
image TC = "images/SD/TC.png"
image S01 = "images/SD/SS01.png"
image S02 = "images/SD/SS02.png"
image S03 = "images/SD/SS03.png"
image S04 = "images/SD/SS04.png"
image DR = "images/SD/Drim.png"
image ST = "images/SD/ST.png"
image MO = "images/SD/MO.png"
image OB = "images/SD/OB.png"
image GR = "images/SD/GR.png"
image LO = "images/SD/LO.png"
image STAR_S = "images/SD/STAR_IU.png"
image Cainic = im.FactorScale("images/logo/Cainic.png", 1.7, 1.7)
image Mil_01 = im.FactorScale(im.Alpha("images/logo/Milnii_01.png", 0.9), 1.6, 1.6)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   
# Объявляем изображение магического круга.
image magic_circle = "images/BG/magic.png"
    
    # эффекты тумана и освящения
image Alaya_01:
    "images/Logo/Alaya_IU.png"
    alpha 0.5
    
image Alaya_02:
    "images/Logo/Alaya_IU_01.png"
    alpha 0.5
    
image Alaya_03:
    "images/Logo/Alaya_IU_02.png"
    alpha 0.5
    
image Alaya_04:
    "images/Logo/Alaya_IU_03.png"
    alpha 0.5
    
image Alaya_05:
    "images/Logo/Alaya_IU_04.png"
    alpha 0.5
        

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
# анимации природных явлений и прочих эффектов

# Нота
image NA:
    "images/Ani/N01.png"
    ease 0.5
    "images/Ani/N03.png"
    ease 0.5
    "images/Ani/N02.png"
    ease 0.5
    repeat

# дождь

image rain = SnowBlossom(anim.Filmstrip(
    "images/Ani/H2O.png", (20, 20), (2, 1), .25), 
    count=30, border=50, xspeed=(50, 50), yspeed=(400, 400), start=0,  fast=True
    )
    
# Бризги

image sn = SnowBlossom(anim.Filmstrip(
    "images/Ani/BZ.png", (20, 20), (2, 1), .25), 
    count=80, border=10, xspeed=(100, 400), yspeed=(100, 400), start=1,  fast=False
    )
    
# Снег

image snow = SnowBlossom(anim.Filmstrip(
    "images/Ani/snow.png", (20, 20), (4, 1), .25), 
    count=60, border=1, xspeed=(10, 10), yspeed=(10, 100), start=0,  fast=True
    )
    
image pe = SnowBlossom("images/Ani/pepel.png", 
    count=60, border=1, xspeed=(10, 10), yspeed=(10, 100), start=0,  fast=True
    )
    
# светлячки 

image fly1:
    subpixel True
    "images/ani/fly01.png" crop (0, 0, 20, 20) 
    pause 0.50
    "images/ani/fly01.png" crop (20, 0, 20, 20) 
    pause 0.50
    repeat

image fly2:
    subpixel True
    "images/ani/fly02.png" crop (0, 0, 20, 20) 
    pause 0.50
    "images/ani/fly02.png" crop (20, 0, 20, 20) 
    pause 0.50
    repeat

image fly3:
    subpixel True
    "images/ani/fly03.png" crop (0, 0, 20, 20) 
    pause 0.50
    "images/ani/fly03.png" crop (20, 0, 20, 20) 
    pause 0.50
    repeat

image fly4:
    subpixel True
    "images/ani/fly04.png" crop (0, 0, 20, 20) 
    pause 0.50
    "images/ani/fly04.png" crop (20, 0, 20, 20) 
    pause 0.50
    repeat

image fly = SnowBlossom(
    FlyParticle(),
    count=50, border=250, xspeed=(-50, -50), yspeed=(-100, -60), start=45, fast=True
)

#image fly = SnowBlossom(anim.SMAnimation(
#    "rrr",
#    anim.State("rrr", anim.Filmstrip("images/Ani/fly01.png", (20, 20), (2,1), .50)), 
#    anim.State("ggg", anim.Filmstrip("images/ani/fly02.png", (20, 20), (2,1), .50)),
#    anim.State("bbb", anim.Filmstrip("images/ani/fly03.png", (20, 20), (2,1), .50)),
#    anim.State("ccc", anim.Filmstrip("images/ani/fly04.png", (20, 20), (2,1), .50)),
    
#    anim.Edge("rrr", 10.0, "ggg"),
#    anim.Edge("rrr", 10.0, "bbb"),
#    anim.Edge("rrr", 10.0, "ccc"),
    
#    anim.Edge("ggg", 10.0, "rrr"),
#    anim.Edge("ggg", 10.0, "bbb"),
#    anim.Edge("ggg", 10.0, "ccc"),
    
#    anim.Edge("bbb", 10.0, "rrr"),
#    anim.Edge("bbb", 10.0, "ggg"),
#    anim.Edge("bbb", 10.0, "ccc"),
    
#    anim.Edge("ccc", 10.0, "rrr"),
#    anim.Edge("ccc", 10.0, "bbb"),
#    anim.Edge("ccc", 10.0, "ggg")
#    ), 
     
#    count=50, border=50, xspeed=(-20, -20), yspeed=(-30, -30), start=15,  fast=False
#    )
    
image starA = Animation(
    "images/Ani/5a.png", 2.0, 
    "images/Ani/5b.png", 2.0, 
    "images/Ani/5c.png", 2.0, 
    "images/Ani/5d.png", 2.0,
    "images/Ani/5e.png", 2.0,
    "images/Ani/5f.png", 2.0, 
    "images/Ani/5h.png", 2.0
    )
   
image STRA = SnowBlossom(anim.Filmstrip(
    "images/Ani/starr.png",
    (24, 24), (2, 1), .10),
    count=120, border=10, xspeed=(-900, -10), yspeed=(10, 0), start=1,  fast=True
    )
    
image bfly = anim.Filmstrip(
    "images/Ani/bfly.png", 
    (30, 30), (2, 1), 13.0
    )
    
image wfly = anim.Filmstrip(
    "images/Ani/fly02.png",
    (20, 20), (2, 1), 15.0
    )
    
image wit01 = anim.Filmstrip(
    "images/Ani/wit01.png",
    (20, 20), (2, 1), 10.0
    )
    
image per = SnowBlossom(anim.Filmstrip(
    "images/Ani/per.png",
    (40, 40), (4, 1), .15),
    count=40, border=1, xspeed=(-10, -150), yspeed=(-100, -10), start=0,  fast=True
    )
    
image bafly_01:
    parallel:
        "images/Ani/baterfly01.png" crop (0, 0, 50, 50)
        pause 0.28
        "images/Ani/baterfly01.png" crop (50, 0, 50, 50)
        pause 0.28
        "images/Ani/baterfly01.png" crop (100, 0, 50, 50)
        pause 0.28
        "images/Ani/baterfly01.png" crop (150, 0, 50, 50)
        pause 0.28
        repeat

    parallel:
        matrixcolor inverted
        pause 1.0
        matrixcolor fraktal_02
        pause 1.0
        matrixcolor fraktal_01
        pause 1.0
        matrixcolor fraktal_03
        pause 1.0
        repeat
    
image bafly_02:
    parallel:
        "images/Ani/baterfly02.png" crop (0, 0, 66, 55)
        pause 0.35
        "images/Ani/baterfly02.png" crop (0, 0, 66, 55)
        pause 0.35
        "images/Ani/baterfly02.png" crop (0, 0, 66, 55)
        pause 0.35
        "images/Ani/baterfly02.png" crop (0, 0, 66, 55)
        pause 0.35 
        repeat
        
    parallel:
        matrixcolor fraktal_01
        pause 1.0
        matrixcolor fraktal_03
        pause 1.0
        matrixcolor fraktal_02
        pause 1.0
        matrixcolor fraktal_04
        pause 1.0
        repeat
        
image bafly_03:
    parallel:
        "images/Ani/baterfly03.png" crop (0, 0, 66, 55)
        pause 0.30
        "images/Ani/baterfly03.png" crop (0, 0, 66, 55)
        pause 0.30
        "images/Ani/baterfly03.png" crop (0, 0, 66, 55)
        pause 0.30
        "images/Ani/baterfly03.png" crop (0, 0, 66, 55)
        pause 0.30
        repeat
        
    parallel:
        matrixcolor fraktal_04
        pause 1.0
        matrixcolor fraktal_01
        pause 1.0
        matrixcolor fraktal_03
        pause 1.0
        matrixcolor inverted
        pause 1.0
        repeat
        
image bafly_04:
    parallel:
        "images/Ani/baterfly03.png" crop (0, 0, 50, 50)
        pause 0.33
        "images/Ani/baterfly03.png" crop (0, 0, 50, 50)
        pause 0.33
        "images/Ani/baterfly03.png" crop (0, 0, 50, 50)
        pause 0.33
        "images/Ani/baterfly03.png" crop (0, 0, 50, 50)
        pause 0.33
        repeat
        
    parallel:
        matrixcolor brightness
        pause 1.0
        matrixcolor fraktal_04
        pause 1.0
        matrixcolor fraktal_01
        pause 1.0
        matrixcolor opacity
        pause 1.0
        repeat
    
image sb:
    "images/Ani/s01.png"
    pause 1.5
    "images/Ani/s02.png"
    pause 1.5
    "images/Ani/s03.png"
    pause 1.5
    "images/Ani/s04.png"
    pause 1.5
    "images/Ani/s05.png"
    pause 1.5
    "images/Ani/s06.png"
    pause 1.5
    repeat

    
image star_01:
    alpha 0.35
    parallel:
        "images/Ani/star.png" crop (0, 0, 480, 300)
        pause 0.5
        "images/Ani/star.png" crop (480, 0, 480, 300)
        pause 0.5
        "images/Ani/star.png" crop (960, 0, 480, 300)
        pause 0.5
        "images/Ani/star.png" crop (1440, 0, 480, 300)
        pause 0.5
        "images/Ani/star.png" crop (1920, 0, 480, 300)
        pause 0.5
        repeat

    parallel:
        matrixcolor inverted
        pause 1.0
        matrixcolor fra
        pause 1.0
        matrixcolor frac
        pause 1.0
        matrixcolor fra
        pause 1.0
        repeat
    
image dim_animated:
    # Кадр 1
    "images/Ani/dim.png" crop (0, 0, 500, 500)
    pause 0.2
    # Кадр 2
    "images/Ani/dim.png" crop (500, 0, 500, 500)
    pause 0.2
    # Кадр 3
    "images/Ani/dim.png" crop (1000, 0, 500, 500)
    pause 0.2
    # Кадр 4
    "images/Ani/dim.png" crop (1500, 0, 500, 500)
    pause 0.2

    repeat
    
image dimCat:
    # Общая прозрачность для всего образа (75%)
    alpha 0.75

    # ПАРАЛЛЕЛЬ 1: Анимация кадров (нарезка 4x1)
    parallel:
        "images/Ani/dim.png" crop (0, 0, 500, 500)
        pause 0.20
        "images/Ani/dim.png" crop (500, 0, 500, 500)
        pause 0.20
        "images/Ani/dim.png" crop (1000, 0, 500, 500)
        pause 0.20
        "images/Ani/dim.png" crop (1500, 0, 500, 500)
        pause 0.20
        repeat

    # ПАРАЛЛЕЛЬ 2: Цикл смены цветов (матрицы)
    parallel:
        matrixcolor inverted
        pause 1.0
        matrixcolor fra
        pause 1.0
        matrixcolor frac
        pause 1.0
        matrixcolor fra
        pause 1.0
        matrixcolor inverted
        pause 1.0
        repeat
    
image STU = anim.Filmstrip("images/styl/STU.png", (236, 600), (18, 1), .20)
    
#анимация стрелок
image send_left:
    "images/Strit/send_01.png" crop (0, 0, 91, 33)
    pause 0.50
    
image send_right:
    "images/Strit/send_02.png" crop (0, 0, 91, 33)
    pause 0.50

#МУЗЫКА

#ЗВУКИ

#ПЕРЕХОДЫ

##################################################################################################

#=======================================================================
# Анимация на основе состояний-переходов.
#========================================================================
   
image smanim = anim.SMAnimation(
        
    # Имя начального состояния.
    "r",

    # Используемые состояния, и объекты, изображаемые во время
    # этих состояний.
    anim.State("r", "#f00"),
    anim.State("g", "#0f0"),
    anim.State("b", "#00f"),

    # Переходы, описываемые старым состоянием, временем, в течение
    # которого мы находимся в старом состоянии, новым состоянием и 
    # эффектом перехода.
    #
    # dissolve работает только для полностью непрозрачных изображений.
    # Также можно применять move.        
    anim.Edge("r", .5, "g", dissolve),
    anim.Edge("r", .5, "b", dissolve),
 
    anim.Edge("g", .5, "r", dissolve),
    anim.Edge("g", .5, "b", dissolve),

    anim.Edge("b", .5, "r", dissolve),
    anim.Edge("b", .5, "g", dissolve),         
    )

#============================================================================
# Определяем несколько новых эффектов перехода.
#============================================================================

define flashbulb = Fade(0.2, 0.0, 0.8, color='#fff')
define diss = Dissolve (1.5)
define dissA = Dissolve (3.0)
define dissB = Dissolve (10.0)
define tele = MultipleTransition([
    False, dissolve, "#fff", dissolve, 
    False, dissolve, "#fff", dissolve,
    True, dissolve, "#fff", dissolve, True]
    )


#======================================================================================   
# Эффекты перехода с использованием маски (ImageDissolve).
#======================================================================================

define circleirisout = ImageDissolve("data/id_circleiris.png", 1.0, 8)
define circleirisin = ImageDissolve("data/id_circleiris.png", 1.0, 8, reverse=True)
define circlewipe = ImageDissolve("data/id_circlewipe.png", 1.0, 8)
define dream = ImageDissolve("data/id_dream.png", 2.0, 64)
define teleport = ImageDissolve("data/id_teleport.png", 1.0, 0)
define centeriss = ImageDissolve("data/center.png", 2.0, 8)
define downiss = ImageDissolve("data/down.png", 1.0, 8)
define icenteriss = ImageDissolve("data/lcenter.png", 1.0, 8)
define leftiss = ImageDissolve("data/left.png", 1.0, 8)
define rightiss = ImageDissolve("data/right.png", 1.0, 8)
define light2iss = ImageDissolve("data/light2.png", 1.0, 8)
define light3iss = ImageDissolve("data/light3.png", 1.0, 8, reverse=True)
define light4iss = ImageDissolve("data/light4.png", 1.0, 8, reverse=True)
define light6iss = ImageDissolve("data/light6.png", 1.0, 8)
define tcenteriss = ImageDissolve("data/tcenter.png", 1.0, 8)
define tlcenteriss = ImageDissolve("data/tlcenter.png", 1.0, 8)
define upiss = ImageDissolve("data/up.png", 1.0, 8)

#==========================================================================================  
# Эффекты перехода от одного режима к другому
#==========================================================================================
$ config.adv_nvl_transition = dissolve
$ config.nvl_adv_transition = dissolve

#===========================================================================================    
#дополнительные позиции спрайтов
#============================================================================================

#Для маленькой ведьмы
define screen_left_01_short = Position(xpos=0, ypos=0)
define screen_left_02_medium = Position(xpos=200, ypos=0)
define screen_left_03_long = Position(xpos=270, ypos=0)
define screen_center_01_short = Position(xpos=300, ypos=0)
define screen_center_02_medium  = Position(xpos=400, ypos=0)
define screen_center_03_long  = Position(xpos=650, ypos=50)
define screen_right_01_short = Position(xpos=900, ypos=0)
define screen_right_02_medium = Position(xpos=1100, ypos=0)

# переменные для Маленькой Ведьмы на ближный средний и дальный план
define LW_short_range = FactorZoom(1.5, 1.5, 0.0, opaque = False)
define LW_medium_range = FactorZoom(1.0, 1.0, 0.0, opaque = False)
define LW_long_range = FactorZoom(0.5, 0.5, 0.0, opaque = False)

# переменные для Маленькой Ведьмы для эмодзи

define emo_LW_medium = FactorZoom(1.8, 1.8, 0.0, opaque = False)

#==============================================================================================    
# параметрыческие функции
#==============================================================================================

define loposL = Position(xpos = 170, ypos = 50, xanchor = 0, yanchor = 0)
define loposLD = Position(xpos = 170, ypos = -50, xanchor = 0, yanchor = 0)
define loposLZ = Position(xpos = 190, ypos = 30, xanchor = 0, yanchor = 0)
define loposLX = Position(xpos = 120, ypos = 180, xanchor = 0, yanchor = 0)
define loposR = Position(xpos = 720, ypos = 10, xanchor = 0, yanchor = 0)
define loposRC = Position(xpos = 700, ypos =120, xanchor = 0, yanchor = 0)
define loposRG = Position(xpos = 660, ypos = 10, xanchor = 0, yanchor = 0)
define loposC_LM_long = Position(xpos = 1000, ypos = 145, xanchor = 0.5, yanchor = 0.5)
define loposC_LM_medium = Position(xpos = 1100, ypos = 145, xanchor = 0.5, yanchor = 0.5)
define loposCFull = Position(xpos = 700, ypos = 100, xanchor = 0.5, yanchor = 0.5)
define loposCA = Position(xpos = 465, ypos = 25, xanchor = 0, yanchor = 0)
define lopoA = Position(xpos = 115, ypos = 370, xanchor = 0, yanchor = 0)
define lopoB = Position(xpos = 145, ypos = 240, xanchor = 0, yanchor = 0)
define lopoC = Position(xpos = 145, ypos = 120, xanchor = 0, yanchor = 0)
define razgavor = FactorZoom(1.0, 1.01, 0.0, opaque = False)
define xijena = FactorZoom(0.0, 0.7, 0.0, opaque = False)
define levelUp = FactorZoom(0.2, 1.0, 1.0, opaque = False)
define posA = Position(xpos = 0.45, ypos = 0.30, xanchor = 0, yanchor = 0)
define lopoD = Position(xpos = 165, ypos = 0, xanchor = 0, yanchor = 0)
define lopoE = Position(xpos = 165, ypos = -180, xanchor = 0, yanchor = 0)
define lopoLeft = Position(xpos = 0, ypos = 180, xanchor = 0, yanchor = 0)
define lopoRight = Position(xpos = 709, ypos = 180, xanchor = 0, yanchor = 0)
define lopo = Position(xpos = 279, ypos = 110, xanchor = 0, yanchor = 0)
define pos_Cainic = Position(xpos = 512, ypos = 510, xanchor = 0.5, yanchor = 0.5)
define pos_cen = Position(xpos = 750, ypos = 360, xanchor = 0.5, yanchor = 0.5)


define move = MoveTransition(1.5)
define slow_move = MoveTransition(3.0)

#####################################################################################
#Слои
#====================================================================================
init: 
    $ config.layers.insert(1, 'sloi01')
    $ config.layers.insert(2, 'sloi02')
    $ config.layers.insert(3, 'sloi03')
    $ config.layers.insert(4, 'sloi04')
    $ config.layers.insert(5, 'sloi05')
    $ config.layers.insert(6, 'sloi06')

#=====================================================================================
#МАТРИЦЫ
#=====================================================================================

define brightness = Matrix([
    1.0, 0.0, 0.0, 0.1,
    0.0, 1.0, 0.0, 0.1,
    0.0, 0.0, 1.0, 0.1,
    0.0, 0.0, 0.0, 1.0
    ])
    
define opacity = Matrix([
    1.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.5
    ])
    
define inverted = Matrix([
    -1.0, 0.0, 0.0, 1.0,
    0.0, -1.0, 0.0, 1.0,
    0.0, 0.0, -1.0, 1.0,
    0.0, 0.0, 0.0, 1.0
    ])
    
define fraktal_01 = Matrix([
    0.5, 0.0, 0.0, 1.0,
    0.0, 0.5, 0.0, 1.0,
    0.0, 0.0, -1.0, 1.0,
    0.0, 0.0, 0.0, 1.0
    ])
    
define fraktal_02 = Matrix([
    0.5, 0.0, 0.0, 0.5,
    0.0, 0.5, 0.0, 0.5,
    0.0, 0.0, 0.5, 1.0,
    0.0, 0.0, 0.0, 0.5
    ])
    
define fraktal_03 = Matrix([
    0.5, 0.0, 0.0, 0.5,
    0.0, -0.5, 0.0, 0.5,
    0.0, 0.0, -0.5, 1,
    0.0, 0.0, 0.0, 0.5
    ])
    
define fraktal_04 = Matrix([
    1.0, 0.0, 0.0, 0.5,
    0.0, 1.0, 0.0, 0.5,
    0.0, 0.0, 1.0, 0.5,
    0.0, 0.0, 0.0, 1.0
    ])
    
define fraktal_05 = Matrix([
    -1.0, 0.0, 1.0, 0.5,
    0.0, 1.0, 0.0, 1.0,
    -1.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 0.0, -1.0
    ])
    
define fra = Matrix([
    -0.3, 0.0, 0.8, 0.0,
    0.0, 0.3, 0.0, 1.0,
    1.0, 0.0, -0.3, 0.0,
    0.0, 0.0, 0.0, 1.0
    ])
    
define frac = Matrix([
    0.7, 0.0, 0.8, 0.2,
    0.0, -0.6, 0.0, 1.0,
    1.0, 0.0, -0.4, -0.6,
    0.0, 0.0, 0.0, 1.0
    ])
    
define color_01 = Matrix([
    1.0, 0.0, 0.0, 0.1,
    0.0, 1.0, 0.0, 0.1,
    0.0, 0.0, 0.9, 0.1,
    0.0, 0.0, 0.0, 1.0
    ])


####################################################################################
#МЕНЮ ЭКСТРА
# MOKOt

image extra neutral:
    "images/sprites/xtra/001.png"
    pause 0.1
    "images/sprites/xtra/002.png"
    pause 0.1
    "images/sprites/xtra/003.png"
    pause 0.1
    "images/sprites/xtra/004.png"
    pause 0.1
    repeat


#КОНЦОВКИ
