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

init python:

    class LayoutElementParams:
        """
        Параметры элемента лица для конкретного положения головы.
        
        offset           — (dx, dy) смещение от BASE
        rotate           — поворот элемента (float или None)
        anchor           — точка привязки поворота (ax, ay) или None
        transform_anchor — компенсировать ли сдвиг при повороте (bool)
        
        Используется в LAYOUTS как замена простого tuple offset_*.
        
        Приоритет параметров итогового Transform:
            1. FaceEntry.rotate / anchor (индивидуальный для файла)
            2. LayoutElementParams.rotate / anchor (для позиции головы)
            Если у FaceEntry есть rotate — LayoutElementParams.rotate
            игнорируется (файл уже имеет свой поворот).
        """

        def __init__(
            self,
            offset           = (0, 0),
            rotate           = None,
            anchor           = None,
            transform_anchor = True
        ):
            self.offset           = offset
            self.rotate           = rotate
            self.anchor           = anchor
            self.transform_anchor = transform_anchor

        def merge_with_entry(self, entry):
            """
            Объединить параметры layout с параметрами FaceEntry.
            
            Правило слияния:
            - offset:   складываются (layout + entry)
            - rotate:   приоритет у FaceEntry, если у него есть rotate
                        иначе берём rotate из layout
            - anchor:   приоритет у FaceEntry, если у него есть anchor
                        иначе берём anchor из layout
            - transform_anchor: приоритет у FaceEntry
            
            Возвращает dict параметров для Transform().
            """
            kwargs = dict(entry.transform)

            # --- rotate ---
            # FaceEntry.rotate перекрывает layout rotate
            final_rotate = entry.rotate \
                if entry.rotate is not None \
                else self.rotate

            # --- anchor ---
            final_anchor = entry.anchor \
                if entry.anchor is not None \
                else self.anchor

            # --- transform_anchor ---
            # Если у entry явно задан anchor — берём его transform_anchor
            # Иначе берём из layout
            if entry.anchor is not None:
                final_transform_anchor = entry.transform_anchor
            else:
                final_transform_anchor = self.transform_anchor

            # Записываем в kwargs
            if final_rotate is not None:
                kwargs['rotate'] = final_rotate

                if final_anchor is not None:
                    kwargs['anchor']           = final_anchor
                    kwargs['transform_anchor'] = final_transform_anchor
                else:
                    # По умолчанию центр
                    kwargs['anchor']           = (0.5, 0.5)
                    kwargs['transform_anchor'] = final_transform_anchor

            elif final_anchor is not None:
                kwargs['anchor'] = final_anchor

            return kwargs

        def __repr__(self):
            return (
                "LayoutElementParams("
                "offset={}, "
                "rotate={}, "
                "anchor={}, "
                "transform_anchor={}"
                ")"
            ).format(
                self.offset,
                self.rotate,
                self.anchor,
                self.transform_anchor
            )

    class FaceEntry:
        """
        Описание одного файла элемента лица.
        
        path             — путь к файлу (обязательно)
        offset           — (dx, dy) индивидуальное смещение
                        добавляется ПОВЕРХ смещения из LAYOUTS
        transform        — dict с параметрами Transform
                        (zoom, xzoom, alpha ...)
        rotate           — угол поворота в градусах (float)
                        None = без поворота
        anchor           — точка привязки поворота (ax, ay)
                        значения 0.0-1.0 (относительно размера изображения)
                        или пиксели (int)
                        None = (0.5, 0.5) центр
        transform_anchor — bool: смещать ли позицию при повороте
                        True  = изображение вращается вокруг anchor,
                                позиция на холсте НЕ меняется
                        False = изображение вращается вокруг anchor,
                                но позиция на холсте сдвигается
        """

        def __init__(
            self,
            path,
            offset           = (0, 0),
            transform        = None,
            rotate           = None,
            anchor           = None,
            transform_anchor = True
        ):
            self.path             = path
            self.offset           = offset
            self.transform        = transform or {}
            self.rotate           = rotate
            self.anchor           = anchor
            self.transform_anchor = transform_anchor

        def build_transform(self):
            """
            Собрать итоговый словарь параметров для Transform().
            
            Приоритет:
                1. Явные rotate / anchor / transform_anchor
                2. Дополнительные параметры из self.transform
                (zoom, xzoom, alpha и т.д.)
            
            Параметры из self.transform НЕ перезаписывают
            rotate / anchor / transform_anchor если они заданы явно.
            """
            # Начинаем с копии доп. параметров
            kwargs = dict(self.transform)

            # Поворот
            if self.rotate is not None:
                kwargs['rotate'] = self.rotate

                # Якорь для поворота
                if self.anchor is not None:
                    kwargs['anchor']           = self.anchor
                    kwargs['transform_anchor'] = self.transform_anchor
                else:
                    # По умолчанию — центр изображения
                    kwargs['anchor']           = (0.5, 0.5)
                    kwargs['transform_anchor'] = self.transform_anchor

            elif self.anchor is not None:
                # Якорь без поворота (для позиционирования)
                kwargs['anchor'] = self.anchor

            return kwargs

        def get_absolute_anchor_offset(self, img_w, img_h):
            """
            Вычислить сдвиг позиции из-за якоря в пикселях.
            
            Нужно если transform_anchor=False —
            тогда Ren'Py не компенсирует сдвиг якоря автоматически,
            и мы делаем это вручную.
            
            img_w, img_h — размер изображения в пикселях
            
            Возвращает (dx, dy) — поправку к позиции на холсте.
            """
            if self.anchor is None:
                return (0, 0)

            ax, ay = self.anchor

            # Если якорь задан в долях (0.0-1.0)
            if isinstance(ax, float):
                ox = int(ax * img_w)
            else:
                ox = ax

            if isinstance(ay, float):
                oy = int(ay * img_h)
            else:
                oy = ay

            return (ox, oy)

        def __repr__(self):
            return (
                "FaceEntry("
                "path={!r}, "
                "offset={}, "
                "rotate={}, "
                "anchor={}, "
                "transform_anchor={}, "
                "transform={}"
                ")"
            ).format(
                self.path,
                self.offset,
                self.rotate,
                self.anchor,
                self.transform_anchor,
                self.transform
            )


    class HeadLayout:

        # ===================================================
        # НАБОРЫ ФАЙЛОВ для элементов лица
        # set_01 — для default и left_slant
        # set_02 — для left, left_down, left_top, right и т.д.

        # FACE_SETS — наборы файлов
        # Каждый элемент — FaceEntry(path, offset, transform)
        #
        # offset    — (dx, dy) сдвиг конкретно этого файла
        # transform — параметры Transform только для него
        # 
        # ===================================================

        FACE_SETS = {

            'set_01': {
                # Глаза
                'eyes': {
                    'eyes_norm_01':               "images/sprites/SLW/SWN/s1/ese_base_01_01.png",
                    'eyes_norm_02':               "images/sprites/SLW/SWN/s1/ese_base_01_02.png",
                    'eyes_norm_03':               "images/sprites/SLW/SWN/s1/ese_base_01_03.png",
                    'eyes_norm_blindfold_01':     "images/sprites/SLW/SWN/s1/ese_base_02_01.png",
                    'eyes_norm_blindfold_02':     "images/sprites/SLW/SWN/s1/ese_base_02_02.png",
                    'eyes_norm_blindfold_03':     "images/sprites/SLW/SWN/s1/ese_base_02_03.png",
                    'eyes_norm_blindfold_04':     "images/sprites/SLW/SWN/s1/ese_base_02_04.png",
                    'eyes_left_norm_01':          "images/sprites/SLW/SWN/s1/ese_base_03_01.png",
                    'eyes_right_norm_01':         "images/sprites/SLW/SWN/s1/ese_base_06_01.png",
                    'eyes_left_norm_he_winks_01': "images/sprites/SLW/SWN/s1/ese_base_04_01.png",
                    'eyes_right_norm_he_winks_01':"images/sprites/SLW/SWN/s1/ese_base_05_01.png",
                    'eyes_norm_cray_01':          "images/sprites/SLW/SWN/s1/ese_base_cray_01_01.png",
                    'eyes_norm_horror_01':        "images/sprites/SLW/SWN/s1/ese_base_horror_01_01.png",
                    'eyes_norm_horror_02':        "images/sprites/SLW/SWN/s1/ese_base_horror_01_02.png",
                    'eyes_norm_prizes_01':        "images/sprites/SLW/SWN/s1/ese_base_prizes_01_01.png",
                    # кадры моргания
                    'blink_open':                 FaceEntry("images/sprites/SLW/SWN/s1/ese_base_01_01.png", offset = (0, -230)),
                    'blink_half':                 FaceEntry("images/sprites/SLW/SWN/s1/ese_base_01_02.png", offset = (0, -230)),
                    'blink_closed':               FaceEntry("images/sprites/SLW/SWN/s1/ese_base_01_03.png", offset = (0, -230)),
                },
                # Рот
                'mouth': {
                    'norm_smail_01':        "images/sprites/SLW/SWN/s1/mouth_base_smail_01_01.png",
                    'norm_smail_02':        "images/sprites/SLW/SWN/s1/mouth_base_smail_01_11.png",
                    'norm_smail_03':        "images/sprites/SLW/SWN/s1/mouth_base_smail_01_06.png",
                    'norm_conversation_01': "images/sprites/SLW/SWN/s1/mouth_base_smail_01_02.png",
                    'norm_conversation_02': "images/sprites/SLW/SWN/s1/mouth_base_smail_01_03.png",
                    'norm_conversation_03': "images/sprites/SLW/SWN/s1/mouth_base_smail_01_07.png",
                    'norm_conversation_04': "images/sprites/SLW/SWN/s1/mouth_base_smail_01_16.png",
                    'norm_surprised_01':    "images/sprites/SLW/SWN/s1/mouth_base_smail_01_04.png",
                    'norm_surprised_02':    "images/sprites/SLW/SWN/s1/mouth_base_smail_01_08.png",
                    'norm_surprised_03':    "images/sprites/SLW/SWN/s1/mouth_base_smail_01_12.png",
                    'norm_surprised_04':    "images/sprites/SLW/SWN/s1/mouth_base_smail_01_14.png",
                    'norm_sour_01':         "images/sprites/SLW/SWN/s1/mouth_base_smail_01_10.png",
                    'norm_sour_02':         "images/sprites/SLW/SWN/s1/mouth_base_smail_01_13.png",
                    'norm_sour_03':         "images/sprites/SLW/SWN/s1/mouth_base_smail_01_15.png",
                    'norm_audacious_01':    "images/sprites/SLW/SWN/s1/mouth_base_smail_01_05.png",
                    'norm_language_01':     "images/sprites/SLW/SWN/s1/mouth_base_smail_01_09.png",
                    'default':              "images/sprites/SLW/SWN/s1/mouth_base_01_01.png",
                },
                # Брови
                'brov': {
                    'brov_surprised_01':   "images/sprites/SLW/SWN/s1/brov_base_01_02.png",
                    'brov_gloomy_01':      "images/sprites/SLW/SWN/s1/brov_base_01_03.png",
                    'brov_irritations_01': "images/sprites/SLW/SWN/s1/brov_base_01_04.png",
                    'brov_sad_01':         "images/sprites/SLW/SWN/s1/brov_base_01_05.png",
                    'brov_angry_01':       "images/sprites/SLW/SWN/s1/brov_base_01_06.png",
                    'brov_angry_02':       "images/sprites/SLW/SWN/s1/brov_base_01_07.png",
                    'brov_angry_03':       "images/sprites/SLW/SWN/s1/brov_base_01_08.png",
                    'brov_angry_04':       "images/sprites/SLW/SWN/s1/brov_base_01_09.png",
                    'brov_angry_05':       "images/sprites/SLW/SWN/s1/brov_base_01_10.png",
                    'brov_angry_06':       "images/sprites/SLW/SWN/s1/brov_base_01_11.png",
                    'default':             "images/sprites/SLW/SWN/s1/brov_base_01_01.png",
                },
                # Веснушки
                'freckles': {
                    'norm_01':         "images/sprites/SLW/SWN/s1/freckles_base_01_02.png",
                    'norm_02':         "images/sprites/SLW/SWN/s1/freckles_base_01_03.png",
                    'norm_03':         "images/sprites/SLW/SWN/s1/freckles_base_01_04.png",
                    'norm_04':         "images/sprites/SLW/SWN/s1/freckles_base_01_05.png",
                    'norm_05':         "images/sprites/SLW/SWN/s1/freckles_base_01_06.png",
                    'norm_hatching_01':"images/sprites/SLW/SWN/s1/freckles_base_01_07.png",
                    'norm_blush_01':   "images/sprites/SLW/SWN/s1/freckles_base_01_08.png",
                    'default':         "images/sprites/SLW/SWN/s1/freckles_base_01_01.png",
                },
                # Плач
                'cry': {
                    'cry_01': "images/sprites/SLW/SWN/s1/cry_base_01_02.png",
                    'cry_02': "images/sprites/SLW/SWN/s1/cry_base_01_03.png",
                    'cry_03': "images/sprites/SLW/SWN/s1/cry_base_01_04.png",
                    'cry_04': "images/sprites/SLW/SWN/s1/cry_base_01_05.png",
                    'default':"images/sprites/SLW/SWN/s1/cry_base_01_01.png",
                },
            },

            # -----------------------------------------------
            # set_02 — для left, left_down, left_top,
            #          right, right_down, right_top
            # -----------------------------------------------

            'set_02': {
                'eyes': {
                    'eyes_norm_01':               "images/sprites/SLW/SWN/ese_base_01_01.png",
                    'eyes_norm_02':               "images/sprites/SLW/SWN/ese_base_01_02.png",
                    'eyes_norm_03':               "images/sprites/SLW/SWN/ese_base_01_03.png",
                    'eyes_norm_blindfold_01':     "images/sprites/SLW/SWN/ese_base_02_01.png",
                    'eyes_norm_blindfold_02':     "images/sprites/SLW/SWN/ese_base_02_02.png",
                    'eyes_norm_blindfold_03':     "images/sprites/SLW/SWN/ese_base_02_03.png",
                    'eyes_norm_blindfold_04':     "images/sprites/SLW/SWN/ese_base_02_04.png",
                    'eyes_left_norm_01':          "images/sprites/SLW/SWN/ese_base_03_01.png",
                    'eyes_right_norm_01':         "images/sprites/SLW/SWN/ese_base_06_01.png",
                    'eyes_left_norm_he_winks_01': "images/sprites/SLW/SWN/ese_base_04_01.png",
                    'eyes_right_norm_he_winks_01':"images/sprites/SLW/SWN/ese_base_05_01.png",
                    'eyes_norm_cray_01':          "images/sprites/SLW/SWN/ese_base_cray_01_01.png",
                    'eyes_norm_horror_01':        "images/sprites/SLW/SWN/ese_base_horror_01_01.png",
                    'eyes_norm_horror_02':        "images/sprites/SLW/SWN/ese_base_horror_01_02.png",
                    'eyes_norm_prizes_01':        "images/sprites/SLW/SWN/ese_base_prizes_01_01.png",
                    'blink_open':                 "images/sprites/SLW/SWN/ese_base_01_01.png",
                    'blink_half':                 "images/sprites/SLW/SWN/ese_base_01_02.png",
                    'blink_closed':               "images/sprites/SLW/SWN/ese_base_01_03.png",
                },
                'mouth': {
                    'norm_smail_01':        "images/sprites/SLW/SWN/mouth_base_smail_01_01.png",
                    'norm_smail_02':        "images/sprites/SLW/SWN/mouth_base_smail_01_11.png",
                    'norm_smail_03':        "images/sprites/SLW/SWN/mouth_base_smail_01_06.png",
                    'norm_conversation_01': "images/sprites/SLW/SWN/mouth_base_smail_01_02.png",
                    'norm_conversation_02': "images/sprites/SLW/SWN/mouth_base_smail_01_03.png",
                    'norm_conversation_03': "images/sprites/SLW/SWN/mouth_base_smail_01_07.png",
                    'norm_conversation_04': "images/sprites/SLW/SWN/mouth_base_smail_01_16.png",
                    'norm_surprised_01':    "images/sprites/SLW/SWN/mouth_base_smail_01_04.png",
                    'norm_surprised_02':    "images/sprites/SLW/SWN/mouth_base_smail_01_08.png",
                    'norm_surprised_03':    "images/sprites/SLW/SWN/mouth_base_smail_01_12.png",
                    'norm_surprised_04':    "images/sprites/SLW/SWN/mouth_base_smail_01_14.png",
                    'norm_sour_01':         "images/sprites/SLW/SWN/mouth_base_smail_01_10.png",
                    'norm_sour_02':         "images/sprites/SLW/SWN/mouth_base_smail_01_13.png",
                    'norm_sour_03':         "images/sprites/SLW/SWN/mouth_base_smail_01_15.png",
                    'norm_audacious_01':    "images/sprites/SLW/SWN/mouth_base_smail_01_05.png",
                    'norm_language_01':     "images/sprites/SLW/SWN/mouth_base_smail_01_09.png",
                    'default':              "images/sprites/SLW/SWN/mouth_base_01_01.png",
                },
                'brov': {
                    'brov_surprised_01':   "images/sprites/SLW/SWN/brov_base_01_02.png",
                    'brov_gloomy_01':      "images/sprites/SLW/SWN/brov_base_01_03.png",
                    'brov_irritations_01': "images/sprites/SLW/SWN/brov_base_01_04.png",
                    'brov_sad_01':         "images/sprites/SLW/SWN/brov_base_01_05.png",
                    'brov_angry_01':       "images/sprites/SLW/SWN/brov_base_01_06.png",
                    'brov_angry_02':       "images/sprites/SLW/SWN/brov_base_01_07.png",
                    'brov_angry_03':       "images/sprites/SLW/SWN/brov_base_01_08.png",
                    'brov_angry_04':       "images/sprites/SLW/SWN/brov_base_01_09.png",
                    'brov_angry_05':       "images/sprites/SLW/SWN/brov_base_01_10.png",
                    'brov_angry_06':       "images/sprites/SLW/SWN/brov_base_01_11.png",
                    'default':             "images/sprites/SLW/SWN/brov_base_01_01.png",
                },
                'freckles': {
                    'norm_01':          "images/sprites/SLW/SWN/freckles_base_01_02.png",
                    'norm_02':          "images/sprites/SLW/SWN/freckles_base_01_03.png",
                    'norm_03':          "images/sprites/SLW/SWN/freckles_base_01_04.png",
                    'norm_04':          "images/sprites/SLW/SWN/freckles_base_01_05.png",
                    'norm_05':          "images/sprites/SLW/SWN/freckles_base_01_06.png",
                    'norm_hatching_01': "images/sprites/SLW/SWN/freckles_base_01_07.png",
                    'norm_blush_01':    "images/sprites/SLW/SWN/freckles_base_01_08.png",
                    'default':          "images/sprites/SLW/SWN/freckles_base_01_01.png",
                },
                'cry': {
                    'cry_01': "images/sprites/SLW/SWN/cry_base_01_02.png",
                    'cry_02': "images/sprites/SLW/SWN/cry_base_01_03.png",
                    'cry_03': "images/sprites/SLW/SWN/cry_base_01_04.png",
                    'cry_04': "images/sprites/SLW/SWN/cry_base_01_05.png",
                    'default':"images/sprites/SLW/SWN/cry_base_01_01.png",
                },
            },
        }

        # ===================================================
        # Какой набор файлов использовать для каждой позиции
        # ===================================================

        HEAD_TO_SET = {
            'default':    'set_01',   # прямо — набор 01
            'left_slant': 'set_01',   # наклон — набор 01
            'left':       'set_02',   # влево   — набор 02
            'left_down':  'set_02',
            'left_top':   'set_02',
            'right':      'set_02',
            'right_down': 'set_02',
            'right_top':  'set_02',
        }

        # 
        """
        Таблица смещений элементов лица для каждого положения головы.
        
        Структура каждой записи:
        {
            'face_pos':  (x, y),      # позиция основы лица
            'face_zoom': float,       # масштаб лица
            'face_rotate': float,     # поворот лица (градусы)
            'face_xzoom': float,      # зеркало по X (1 или -1)
            'neck_pos':  (x, y),      # позиция шеи (None если нет)
            'neck_img':  str,         # файл шеи
            'neck_xzoom': float,      # зеркало шеи
            'face_img':  str,         # файл лица
            'canvas':    (w, h),      # размер холста
            
            # смещения элементов лица относительно базовых координат
            'offset_eyes':     (dx, dy),
            'offset_mouth':    (dx, dy),
            'offset_brov':     (dx, dy),
            'offset_freckles': (dx, dy),
            'offset_cry':      (dx, dy),
        }
        """

        # Базовые координаты элементов (для позиции 'default' / 'left')
        #===================================================
        # Базовые координаты элементов лица
        # ===================================================
        BASE = {
            'eyes':     (1655, 620),
            'mouth':    (1950, 980),
            'brov':     (1650, 530),
            'freckles': (1750, 810),
            'cry':      (1730, 750),
        }

        # Таблица: положение головы -> параметры
        #===================================================
        # Параметры головы для каждой позиции
        # ===================================================
        LAYOUTS = {

            'left': {
                'canvas':       (4500, 6200),
                'neck_img':     "images/sprites/SLW/SWN/neck_01.png",
                'neck_pos':     (1800, 940),
                'neck_xzoom':   1,
                'face_img':     "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
                'face_pos':     (1255, 35),
                'face_zoom':    0.93,
                'face_rotate':  0,
                'face_xzoom':   1,
                # смещения элементов лица от BASE
                'offset_eyes':     (0,    0),
                'offset_mouth':    (0,    0),
                'offset_brov':     (0,    0),
                'offset_freckles': (0,    0),
                'offset_cry':      (0,    0),
            },
            # -----------------------------------------------
            # Влево наклон — голова повёрнута -10°
            # Элементы лица тоже поворачиваются вместе с головой
            # -----------------------------------------------

            'left_slant': {
                'canvas':       (4500, 6200),
                'neck_img':     None,
                'neck_pos':     None,
                'neck_xzoom':   1,
                'face_img':     "images/sprites/SLW/SWN/SLW_01_01_feis_01.png",
                'face_pos':     (1330, 40),
                'face_zoom':    1.0,
                'face_rotate':  -10,
                'face_xzoom':   1,
                # голова наклонена — элементы тоже смещаются
                'offset_eyes': LayoutElementParams(
                    offset           = (-60, -30),
                    rotate           = -4,           # вместе с головой
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_mouth': LayoutElementParams(
                    offset           = (-150, -20),
                    rotate           = -10,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_brov': LayoutElementParams(
                    offset           = (-180, -30),
                    rotate           = -10,
                    anchor           = (0.5, 1.0),    # от нижнего края бровей
                    transform_anchor = True
                ),
                'offset_freckles': LayoutElementParams(
                    offset           = (-150, -25),
                    rotate           = -10,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_cry': LayoutElementParams(
                    offset           = (-150, -20),
                    rotate           = -10,
                    anchor           = (0.5, 0.0),    # слёзы текут от верха
                    transform_anchor = True
                ),
            },

            # -----------------------------------------------
            # Влево вниз — голова повёрнута -15°
            # -----------------------------------------------

            'left_down': {
                'canvas':       (4500, 6200),
                'neck_img':     "images/sprites/SLW/SWN/neck_01.png",
                'neck_pos':     (1790, 940),
                'neck_xzoom':   1,
                'face_img':     "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
                'face_pos':     (1160, 80),
                'face_zoom':    0.93,
                'face_rotate':  -15,
                'face_xzoom':   1,
                'offset_eyes': LayoutElementParams(
                    offset           = (-370, -20),
                    rotate           = -15,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_mouth': LayoutElementParams(
                    offset           = (-370, -10),
                    rotate           = -15,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_brov': LayoutElementParams(
                    offset           = (-370, -20),
                    rotate           = -15,
                    anchor           = (0.5, 1.0),
                    transform_anchor = True
                ),
                'offset_freckles': LayoutElementParams(
                    offset           = (-370, -15),
                    rotate           = -15,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_cry': LayoutElementParams(
                    offset           = (-370, -10),
                    rotate           = -15,
                    anchor           = (0.5, 0.0),
                    transform_anchor = True
                ),
            },

            # -----------------------------------------------
            # Влево вверх — голова повёрнута +10°
            # -----------------------------------------------

            'left_top': {
                'canvas':       (4500, 6200),
                'neck_img':     "images/sprites/SLW/SWN/neck_01.png",
                'neck_pos':     (1800, 940),
                'neck_xzoom':   1,
                'face_img':     "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
                'face_pos':     (1325, 80),
                'face_zoom':    0.93,
                'face_rotate':  10,
                'face_xzoom':   1,
                'offset_eyes': LayoutElementParams(
                    offset           = (-220, -20),
                    rotate           = 10,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_mouth': LayoutElementParams(
                    offset           = (-220, -10),
                    rotate           = 10,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_brov': LayoutElementParams(
                    offset           = (-220, -20),
                    rotate           = 10,
                    anchor           = (0.5, 1.0),
                    transform_anchor = True
                ),
                'offset_freckles': LayoutElementParams(
                    offset           = (-220, -15),
                    rotate           = 10,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_cry': LayoutElementParams(
                    offset           = (-220, -10),
                    rotate           = 10,
                    anchor           = (0.5, 0.0),
                    transform_anchor = True
                ),
            },

            # -----------------------------------------------
            # Вправо
            # -----------------------------------------------

            'right': {
                'canvas':       (4500, 6200),
                'neck_img':     "images/sprites/SLW/SWN/neck_02.png",
                'neck_pos':     (1770, 940),
                'neck_xzoom':   -1,
                'face_img':     "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
                'face_pos':     (1270, 80),
                'face_zoom':    0.93,
                'face_rotate':  0,
                'face_xzoom':   -1,
                'offset_eyes':     (0,    0),
                'offset_mouth':    (0,    0),
                'offset_brov':     (0,    0),
                'offset_freckles': (0,    0),
                'offset_cry':      (0,    0),
            },

            # -----------------------------------------------
            # Вправо вниз — голова повёрнута +15°
            # -----------------------------------------------

            'right_down': {
                'canvas':       (4500, 6200),
                'neck_img':     "images/sprites/SLW/SWN/neck_02.png",
                'neck_pos':     (1800, 940),
                'neck_xzoom':   -1,
                'face_img':     "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
                'face_pos':     (1370, 80),
                'face_zoom':    0.93,
                'face_rotate':  15,
                'face_xzoom':   -1,
                'offset_eyes': LayoutElementParams(
                    offset           = (-280, -20),
                    rotate           = 15,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_mouth': LayoutElementParams(
                    offset           = (-280, -10),
                    rotate           = 15,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_brov': LayoutElementParams(
                    offset           = (-280, -20),
                    rotate           = 15,
                    anchor           = (0.5, 1.0),
                    transform_anchor = True
                ),
                'offset_freckles': LayoutElementParams(
                    offset           = (-280, -15),
                    rotate           = 15,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_cry': LayoutElementParams(
                    offset           = (-280, -10),
                    rotate           = 15,
                    anchor           = (0.5, 0.0),
                    transform_anchor = True
                ),
            },

            # -----------------------------------------------
            # Вправо вверх — голова повёрнута -10°
            # -----------------------------------------------

            'right_top': {
                'canvas':       (4500, 6200),
                'neck_img':     "images/sprites/SLW/SWN/neck_02.png",
                'neck_pos':     (1800, 940),
                'neck_xzoom':   -1,
                'face_img':     "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
                'face_pos':     (1240, 80),
                'face_zoom':    0.93,
                'face_rotate':  -10,
                'face_xzoom':   -1,
                'offset_eyes': LayoutElementParams(
                    offset           = (-380, -20),
                    rotate           = -10,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_mouth': LayoutElementParams(
                    offset           = (-380, -10),
                    rotate           = -10,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_brov': LayoutElementParams(
                    offset           = (-380, -20),
                    rotate           = -10,
                    anchor           = (0.5, 1.0),
                    transform_anchor = True
                ),
                'offset_freckles': LayoutElementParams(
                    offset           = (-380, -15),
                    rotate           = -10,
                    anchor           = (0.5, 0.5),
                    transform_anchor = True
                ),
                'offset_cry': LayoutElementParams(
                    offset           = (-380, -10),
                    rotate           = -10,
                    anchor           = (0.5, 0.0),
                    transform_anchor = True
                ),
            },

            # -----------------------------------------------
            # Default — прямо вперёд
            # -----------------------------------------------

            # default — прямо вперёд
            'default': {
                'canvas':       (4500, 6200),
                'neck_img':     None,
                'neck_pos':     None,
                'neck_xzoom':   1,
                'face_img':     "images/sprites/SLW/SWN/SLW_01_01_feis_01.png",
                'face_pos':     (1385, 35),
                'face_zoom':    1.0,
                'face_rotate':  0,
                'face_xzoom':   1,
                'offset_eyes':     LayoutElementParams(
                    offset = (0, 0),
                    rotate = 5,
                    anchor = (0.5, 0.5),
                    transform_anchor = True
                    ),
                'offset_mouth':    LayoutElementParams(offset = (0, 0)),
                'offset_brov':     LayoutElementParams(offset = (0, 0)),
                'offset_freckles': LayoutElementParams(offset = (0, 0)),
                'offset_cry':      LayoutElementParams(offset = (0, 0)),
            },
        }


        @staticmethod
        def get_layout(head_pos):
            """Вернуть словарь параметров для позиции головы."""
            return HeadLayout.LAYOUTS.get(
                head_pos,
                HeadLayout.LAYOUTS['default']
            )

        @staticmethod
        def get_element_params(head_pos, element):
            """
            Вернуть LayoutElementParams для элемента.
            Если не найден — вернуть пустой LayoutElementParams.
            """
            layout = HeadLayout.get_layout(head_pos)
            key    = 'offset_' + element
            params = layout.get(key)

            # Поддержка старого формата tuple (на случай если где-то осталось)
            if isinstance(params, tuple):
                return LayoutElementParams(offset=params)

            # Если не задан совсем
            if params is None:
                return LayoutElementParams()

            return params

        @staticmethod
        def get_set(head_pos):
            """
            Вернуть словарь файлов (FACE_SETS[...])
            для текущего положения головы.
            """
            set_name = HeadLayout.HEAD_TO_SET.get(head_pos, 'set_01')
            return HeadLayout.FACE_SETS[set_name]

        @staticmethod
        def get_entry(head_pos, element, variant):
            """
            Вернуть FaceEntry для элемента и варианта.
            Если вариант не найден — вернуть 'default'.
            Если 'default' тоже нет — вернуть None.

            Поддерживает старый формат, когда в FACE_SETS лежит строка.
            """
            face_set     = HeadLayout.get_set(head_pos)
            element_dict = face_set.get(element, {})
            entry        = element_dict.get(variant)

            if entry is None:
                entry = element_dict.get('default')

            if entry is None:
                return None

            if isinstance(entry, FaceEntry):
                return entry

            if isinstance(entry, str):
                return FaceEntry(entry)

            return None

        @staticmethod
        def get_file(head_pos, element, variant):
            """
            Получить путь к файлу элемента лица.
            
            head_pos — положение головы ('left', 'right', 'default' ...)
            element  — 'eyes' / 'mouth' / 'brov' / 'freckles' / 'cry'
            variant  — вариант элемента ('eyes_norm_01', 'norm_smail_01' ...)
                    если вариант не найден — берём 'default'
            """
            face_set = HeadLayout.get_set(head_pos)
            element_dict = face_set.get(element, {})
            # Если вариант не найден — пробуем 'default'
            return element_dict.get(variant, element_dict.get('default', None))

        @staticmethod
        def face_pos(head_pos, element, entry=None):
            """
            Вернуть абсолютную позицию элемента лица
            с учётом BASE + offset для текущего положения головы.
            
            element — 'eyes', 'mouth', 'brov', 'freckles', 'cry'

            Вернуть абсолютную позицию (x, y) элемента лица.
            BASE + offset для текущего положения головы.
            Вернуть итоговую позицию (x, y) элемента лица.
            
            Итог = BASE[element] 
                + LAYOUTS offset (общий для всех файлов данной позиции)
                + FaceEntry.offset (индивидуальный для конкретного файла)
            
            entry — FaceEntry (если уже получен, чтобы не искать дважды)
            """
            layout_params = HeadLayout.get_element_params(head_pos, element)
            bx, by        = HeadLayout.BASE[element]
            dx, dy        = layout_params.offset
            # Индивидуальное смещение из FaceEntry
            ex, ey = (0, 0)
            if entry is not None:
                ex, ey = entry.offset

            return (bx + dx + ex, by + dy + ey)

        @staticmethod
        def get(head_pos, key, fallback=None):
            """
            Получить любой параметр layout по ключу.
            Получить параметр для текущего положения головы.
            head_pos — значение переменной head_LW_01
            key      — ключ из LAYOUTS (например 'offset_eyes')
            fallback — значение по умолчанию если позиция неизвестна
            """
            layout = HeadLayout.get_layout(head_pos)
            return layout.get(key, fallback)

    # =======================================================
    # DynamicDisplayable — строители
    # =======================================================

    def build_head(st, at):
        """
        Строит Composite головы.
        Автоматически читает head_LW_01 из store.
        """
        pos = renpy.store.head_LW_01
        L   = HeadLayout.get_layout(pos)

        layers = []

        # Шея
        if L['neck_img'] is not None:
            layers.append(L['neck_pos'])
            layers.append(
                Transform(
                    L['neck_img'],
                    xzoom  = L['neck_xzoom'],
                    anchor = (0.5, 0.5)
                )
            )

        # Лицо
        layers.append(L['face_pos'])
        has_rotate = (L['face_rotate'] != 0)
        layers.append(
            Transform(
                L['face_img'],
                zoom             = L['face_zoom'],
                rotate           = L['face_rotate'],
                xzoom            = L['face_xzoom'],
                anchor           = (0.5, 1.0) if has_rotate else (0.5, 0.5),
                transform_anchor = has_rotate
            )
        )
        # redraw=0 — перестраивать при каждом кадре
        # (смена head_LW_01 подхватится автоматически)
        return Composite(L['canvas'], *layers), 0

   
       
    # -------------------------------------------------------
    # Универсальный строитель элемента лица
    # -------------------------------------------------------

    def make_head_composite():
        """
        Строит Composite для текущего положения головы.
        Вызывается через ConditionSwitch (см. ниже).
        Используется как callable в Function().

        Фабрика строителей для DynamicDisplayable.
        
        element — 'eyes' / 'mouth' / 'brov' / 'freckles' / 'cry'
        
        Возвращаемая функция:
            st, at       — стандартные аргументы DynamicDisplayable
            variant      — ключ варианта ('eyes_norm_01', 'norm_smail_01' ...)
            extra_kwargs — доп. параметры для Transform (dict или None)
        """
        pos   = head_LW_01 if 'head_LW_01' in dir() else 'default'
        L     = HeadLayout.LAYOUTS.get(pos, HeadLayout.LAYOUTS['default'])

        layers = []

        # Шея (если есть)
        if L['neck_img'] is not None:
            layers.append(L['neck_pos'])
            neck_t = Transform(
                L['neck_img'],
                xzoom=L['neck_xzoom'],
                anchor=(0.5, 0.5)
            )
            layers.append(neck_t)

        # Лицо
        layers.append(L['face_pos'])
        face_t = Transform(
            L['face_img'],
            zoom       = L['face_zoom'],
            rotate     = L['face_rotate'],
            xzoom      = L['face_xzoom'],
            anchor     = (0.5, 1.0),
            transform_anchor = (L['face_rotate'] != 0)
        )
        layers.append(face_t)

        return Composite(L['canvas'], *layers)

init python:

    # -------------------------------------------------------

    def build_face_element(st, at, element, image_path,
                        base_x, base_y, extra_transform=None):
        """
        Универсальный строитель для элементов лица.
        
        element       — 'eyes'/'mouth'/'brov'/'freckles'/'cry'
        image_path    — путь к файлу (строка)
        base_x, base_y — базовые координаты из BASE
        extra_transform — доп. параметры Transform (dict) или None
        """
        pos     = renpy.store.head_LW_01
        abs_pos = HeadLayout.face_pos(pos, element)

        t_kwargs = {}
        if extra_transform:
            t_kwargs.update(extra_transform)

        layers = [abs_pos, Transform(image_path, **t_kwargs)]
        canvas = HeadLayout.get(pos, 'canvas', (4500, 6200))

        return Composite(canvas, *layers), 0

    # -------------------------------------------------------
    # Фабрики для каждого элемента
    # Используем замыкания, чтобы не дублировать код
    # -------------------------------------------------------
    # -------------------------------------------------------
    # Универсальная фабрика строителей элементов лица
    # С поддержкой FaceEntry (offset + transform)
    # -------------------------------------------------------



    def _make_element_builder(element):
        """
        Фабрика строителей для DynamicDisplayable.
        
        element — 'eyes' / 'mouth' / 'brov' / 'freckles' / 'cry'
        
        Возвращаемая функция:
            st, at       — стандартные аргументы DynamicDisplayable
            variant      — ключ варианта ('eyes_norm_01', 'norm_smail_01' ...)
            extra_kwargs — доп. параметры для Transform (dict или None)

        Фабрика строителей для DynamicDisplayable.
        
        Возвращаемая функция:
            st, at   — стандартные аргументы DynamicDisplayable
            variant  — ключ варианта ('eyes_norm_01', 'norm_smail_01' ...)
        
        Логика:
            1. Читаем head_LW_01 из store
            2. Находим FaceEntry через HeadLayout.get_entry()
            3. Считаем итоговую позицию:
            BASE + layout_offset + entry.offset
            4. Строим Transform с параметрами из entry.transform
            5. Возвращаем Composite
        """
        def builder(st, at, variant):
            pos           = renpy.store.head_LW_01
            entry         = HeadLayout.get_entry(pos, element, variant)

            if entry is None:
                return Null(), 0

            canvas        = HeadLayout.get(pos, 'canvas', (4500, 6200))
            ax, ay        = HeadLayout.face_pos(pos, element, entry)
            layout_params = HeadLayout.get_element_params(pos, element)
            t_kwargs      = layout_params.merge_with_entry(entry)

            d = Composite(
                canvas,
                (ax, ay),
                Transform(entry.path, **t_kwargs)
            )
            return d, 0

        return builder

    _build_eyes     = _make_element_builder('eyes')
    _build_mouth    = _make_element_builder('mouth')
    _build_brov     = _make_element_builder('brov')
    _build_freckles = _make_element_builder('freckles')
    _build_cry      = _make_element_builder('cry')

    # -------------------------------------------------------
    # Строитель моргания
    # -------------------------------------------------------

    def build_eyes_blink(st, at):
        """
        Анимация моргания.
        Кадры берутся из набора текущей позиции головы.
        """
        pos    = renpy.store.head_LW_01
        canvas = HeadLayout.get(pos, 'canvas', (4500, 6200))

        e_open   = HeadLayout.get_entry(pos, 'eyes', 'blink_open')
        e_half   = HeadLayout.get_entry(pos, 'eyes', 'blink_half')
        e_closed = HeadLayout.get_entry(pos, 'eyes', 'blink_closed')

        cycle = 3.0
        t     = st % cycle

        if t < 1.0:
            entry  = e_open
            redraw = 1.0 - t
        elif t < 1.25:
            entry  = e_half
            redraw = 1.25 - t
        elif t < 1.5:
            entry  = e_closed
            redraw = 1.5 - t
        elif t < 1.75:
            entry  = e_half
            redraw = 1.75 - t
        else:
            entry  = e_open
            redraw = cycle - t

        if entry is None:
            return Null(), redraw

        ax, ay        = HeadLayout.face_pos(pos, 'eyes', entry)
        layout_params = HeadLayout.get_element_params(pos, 'eyes')
        t_kwargs      = layout_params.merge_with_entry(entry)

        d = Composite(
            canvas,
            (ax, ay),
            Transform(entry.path, **t_kwargs)
        )
        return d, redraw


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
image bg0004:
    "images/BG/0004a01.jpg"
    pause 0.5
    "images/BG/0004a02.jpg"
    pause 0.5
    "images/BG/0004a03.jpg"
    pause 0.5
    "images/BG/0004a04.jpg"
    pause 0.5
    "images/BG/0004a05.jpg"
    pause 0.5
    "images/BG/0004a06.jpg"
    pause 0.5
    "images/BG/0004a07.jpg"
    pause 0.5
    "images/BG/0004a08.jpg"
    pause 0.5
    "images/BG/0004a09.jpg"
    pause 0.5
    "images/BG/0004a10.jpg"
    pause 0.5
    "images/BG/0004a11.jpg"
    pause 0.5
    "images/BG/0004a12.jpg"
    pause 0.5
    "images/BG/0004a13.jpg"
    pause 0.5
    "images/BG/0004a14.jpg"
    pause 0.5
    "images/BG/0004a15.jpg"
    pause 0.5
    "images/BG/0004a16.jpg"
    pause 0.5
    "images/BG/0004a17.jpg"
    pause 0.5
    "images/BG/0004a18.jpg"
    pause 0.5
    "images/BG/0004a19.jpg"
    pause 0.5
    "images/BG/0004a20.jpg"
    pause 0.5
    "images/BG/0004a21.jpg"
    pause 0.5
    "images/BG/0004a22.jpg"
    pause 0.5
    "images/BG/0004a23.jpg"
    pause 0.5
    repeat
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
        (4500, 6000),
        (1000, 630),
        Transform("images/sprites/SLW/SWN/SLW_01_01_kassa_01.png", zoom=0.75)
    )
    pause 0.5
    Composite(
        (4500, 6000),
        (1150, 600),
        Transform("images/sprites/SLW/SWN/SLW_01_01_kassa_02.png", zoom=0.75)
    )
    pause 0.5
    Composite(
        (4500, 6000),
        (1300, 580),
        Transform("images/sprites/SLW/SWN/SLW_01_01_kassa_03.png", zoom=0.75)
    )
    pause 0.5
    Composite(
        (4500, 6000),
        (1500, 670),
        Transform("images/sprites/SLW/SWN/SLW_01_01_kassa_04.png", zoom=0.75)
    )
    pause 0.5
    Composite(
        (4500, 6000),
        (1150, 600),
        Transform("images/sprites/SLW/SWN/SLW_01_01_kassa_02.png", zoom=0.75)
    )
    pause 0.5
    repeat

# Вариант 2 — средний ветер
image SLW_kassa_wind_02:
    contains:
        # Покадровая анимация кадров
        Composite(
            (4500, 6000),
            (2000, 630),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_01.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (4500, 6000),
            (2150, 600),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_02.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (4500, 6000),
            (2300, 580),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_03.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (4500, 6000),
            (2500, 670),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_04.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (4500, 6000),
            (2150, 600),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_02.png",
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
            (4500, 6000),
            (2000, 630),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_01.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (4500, 6000),
            (2150, 600),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_02.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (4500, 6000),
            (2300, 580),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_03.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (4500, 6000),
            (2500, 670),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_04.png",
                zoom=0.75
            )
        )
        pause 0.5
        Composite(
            (4500, 6000),
            (2150, 600),
            Transform(
                "images/sprites/SLW/SWN/SLW_01_01_kassa_02.png",
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
        (4500, 6000),
        (1000, 600),
        Transform("images/sprites/SLW/SWN/SLW_01_01_kassa_01.png", zoom=0.75)
    )

# Выбор анимации косы с учётом ветра
image SLW_kassa_01 = ConditionSwitch(
    "wind_01 == 1", "SLW_kassa_wind_01",
    "wind_01 == 2", "SLW_kassa_wind_02",
    "wind_01 == 3", "SLW_kassa_wind_03",
    "True",         "SLW_kassa_still"
)

# ===================================================
# ГОЛОВА
# ===================================================

image LWS_head = DynamicDisplayable(build_head)

#image LWS_head = ConditionSwitch(

#    "head_LW_01 == 'left'",
#    Composite(
#        (4500, 6200),
#        (1800, 940), "images/sprites/SLW/SWN/neck_01.png",
#        (1530, 140),
#        Transform(
#            "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
#            zoom=0.93
#        )
#    ),

#    "head_LW_01 == 'left_slant'",
#    Composite(
#        (4500, 6200),
#        (1330, 40),
#        Transform(
#            "images/sprites/SLW/SWN/SLW_01_01_feis_01.png",
#            rotate=-10,
#            anchor=(0.5, 1.0),
#            transform_anchor=True
#        )
#    ),

#    "head_LW_01 == 'left_down'",
#    Composite(
#        (4500, 6200),
#        (1800, 940), "images/sprites/SLW/SWN/neck_01.png",
#        (1160, 80),
#        Transform(
#            "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
#            zoom=0.93,
#            rotate=-15,
#            anchor=(0.5, 1.0),
#            transform_anchor=True
#        )
#    ),

#    "head_LW_01 == 'left_top'",
#    Composite(
#        (4500, 6200),
#        (1800, 940), "images/sprites/SLW/SWN/neck_01.png",
#        (1325, 80),
#        Transform(
#            "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
#            zoom=0.93,
#            rotate=10,
#            anchor=(0.5, 1.0),
#            transform_anchor=True
#        )
#    ),

#    "head_LW_01 == 'right'",
#    Composite(
#        (4500, 6200),
#        (1760, 940), 
#        Transform(
#            "images/sprites/SLW/SWN/neck_02.png",
#            xzoom=-1,
#            anchor=(0.5, 0.5)
#        ),
#        (1560, 140),
#        Transform(
#            "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
#            zoom=0.93,
#            xzoom=-1,
#            anchor=(0.5, 0.5)
#        )
#    ),

#    "head_LW_01 == 'right_down'",
#    Composite(
#        (4500, 6200),
#        (1800, 940), 
#        Transform(
#            "images/sprites/SLW/SWN/neck_02.png",
#            xzoom=-1,
#            anchor=(0.5, 0.5)
#        ),
#        (1370, 80),
#        Transform(
#            "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
#            zoom=0.93,
#            rotate=15,
#            xzoom=-1,
#            anchor=(0.5, 1.0),
#            transform_anchor=True
#        )
#    ),

#    "head_LW_01 == 'right_top'",
#    Composite(
#        (4500, 6200),
#        (1800, 940), 
#        Transform(
#            "images/sprites/SLW/SWN/neck_02.png",
#            xzoom=-1,
#            anchor=(0.5, 0.5)
#        ),
#        (1240, 80),
#        Transform(
#            "images/sprites/SLW/SWN/SLW_01_02_feis_01.png",
#            zoom=0.93,
#            rotate=-10,
#            xzoom=-1,
#            anchor=(0.5, 1.0),
#            transform_anchor=True
#        )
#    ),

#    "True",
#    Composite(
#        (4500, 6200),
#        (1590, 160),
#        "images/sprites/SLW/SWN/SLW_01_01_feis_01.png"
#    )
#)

# ===================================================
# ВОЛОСЫ
# ===================================================

# Медленный ветер
image SLW_hair_wind_slow:
    Composite(
        (4500, 6000),
        (1327, 58), "images/sprites/SLW/SWN/SLW_01_01_hair_01_01.png"
    )
    pause 0.5
    Composite(
        (4500, 6000),
        (1332, 46), "images/sprites/SLW/SWN/SLW_01_01_hair_01_02.png"
    )
    pause 0.5
    Composite(
        (4500, 6000),
        (1318, 58), "images/sprites/SLW/SWN/SLW_01_01_hair_01_03.png"
    )
    pause 0.5
    Composite(
        (4500, 6000),
        (1332, 46), "images/sprites/SLW/SWN/SLW_01_01_hair_01_02.png"
    )
    pause 0.5
    repeat

# Быстрый ветер
image SLW_hair_wind_fast:
    Composite(
        (4500, 6000),
        (1327, 58), "images/sprites/SLW/SWN/SLW_01_01_hair_01_01.png"
    )
    pause 0.2
    Composite(
        (4500, 6000),
        (1332, 46), "images/sprites/SLW/SWN/SLW_01_01_hair_01_02.png"
    )
    pause 0.2
    Composite(
        (4500, 6000),
        (1318, 58), "images/sprites/SLW/SWN/SLW_01_01_hair_01_03.png"
    )
    pause 0.2
    Composite(
        (4500, 6000),
        (1332, 46), "images/sprites/SLW/SWN/SLW_01_01_hair_01_02.png"
    )
    pause 0.2
    repeat

# Статичные волосы
image SLW_hair_static:
    Composite(
        (4500, 6000),
        (1327, 58), "images/sprites/SLW/SWN/SLW_01_01_hair_01_01.png"
    )

# Выбор волос через ConditionSwitch
image SLW_hair_01 = ConditionSwitch(
    "wind_01 == 1",              "SLW_hair_wind_slow",
    "wind_01 == 2 or wind_01 == 3", "SLW_hair_wind_fast",
    "True",                      "SLW_hair_static"
)

# ===================================================
# ГЛАЗА
# ===================================================

image SLW_eyes_blink_01 = DynamicDisplayable(build_eyes_blink)

image SLW_eyes_01 = ConditionSwitch(

    "eyes_LW_01 == 'eyes_norm_01'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_01'),

    "eyes_LW_01 == 'eyes_norm_02'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_02'),

    "eyes_LW_01 == 'eyes_norm_03'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_03'),

    "eyes_LW_01 == 'eyes_norm_blindfold_01'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_blindfold_01'),

    "eyes_LW_01 == 'eyes_norm_blindfold_02'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_blindfold_02'),

    "eyes_LW_01 == 'eyes_norm_blindfold_03'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_blindfold_03'),

    "eyes_LW_01 == 'eyes_norm_blindfold_04'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_blindfold_04'),

    "eyes_LW_01 == 'eyes_left_norm_01'",
    DynamicDisplayable(_build_eyes, 'eyes_left_norm_01'),

    "eyes_LW_01 == 'eyes_right_norm_01'",
    DynamicDisplayable(_build_eyes, 'eyes_right_norm_01'),

    "eyes_LW_01 == 'eyes_left_norm_he_winks_01'",
    DynamicDisplayable(_build_eyes, 'eyes_left_norm_he_winks_01'),

    "eyes_LW_01 == 'eyes_right_norm_he_winks_01'",
    DynamicDisplayable(_build_eyes, 'eyes_right_norm_he_winks_01'),

    "eyes_LW_01 == 'eyes_norm_cray_01'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_cray_01'),

    "eyes_LW_01 == 'eyes_norm_horror_01'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_horror_01'),

    "eyes_LW_01 == 'eyes_norm_horror_02'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_horror_02'),

    "eyes_LW_01 == 'eyes_norm_prizes_01'",
    DynamicDisplayable(_build_eyes, 'eyes_norm_prizes_01'),

    "True",
    DynamicDisplayable(build_eyes_blink)
)

# Анимация моргания (базовая)
#image SLW_eyes_blink_01:
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_01_01.png"
#    )
#    pause 1.0
#    choice:
#        Composite(
#            (4500, 6200),
#           (1655, 620), "images/sprites/SLW/SWN/ese_base_01_01.png"
#        )
#        pause 1.0
#    choice:
#        Composite(
#            (4500, 6200),
#            (1655, 620), "images/sprites/SLW/SWN/ese_base_01_02.png"
#        )
#        pause 0.25
#       Composite(
#            (4500, 6200),
#           (1655, 620), "images/sprites/SLW/SWN/ese_base_01_03.png"
#        )
#        pause 0.25
#        Composite(
#            (4500, 6200),
#            (1655, 620), "images/sprites/SLW/SWN/ese_base_01_02.png"
#        )
#        pause 0.5
#    repeat

# Выбор варианта глаз
# ИСПРАВЛЕНО: "Trye" -> "True"
#image SLW_eyes_01 = ConditionSwitch(

#    "eyes_LW_01 == 'eyes_norm_01'",
#   Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_01_01.png"
#    ),

#    "eyes_LW_01 == 'eyes_norm_02'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_01_02.png"
#    ),

#    "eyes_LW_01 == 'eyes_norm_03'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_01_03.png"
#    ),

#    "eyes_LW_01 == 'eyes_norm_blindfold_01'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_02_01.png"
#    ),

#    "eyes_LW_01 == 'eyes_norm_blindfold_02'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_02_02.png"
#    ),

#    "eyes_LW_01 == 'eyes_norm_blindfold_03'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_02_03.png"
#    ),
#
#    "eyes_LW_01 == 'eyes_norm_blindfold_04'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_02_04.png"
#    ),
#
#    "eyes_LW_01 == 'eyes_left_norm_01'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_03_01.png"
#    ),
#
#    "eyes_LW_01 == 'eyes_right_norm_01'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_06_01.png"
#    ),
#
#    "eyes_LW_01 == 'eyes_left_norm_he_winks_01'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_04_01.png"
#    ),
#
#    "eyes_LW_01 == 'eyes_right_norm_he_winks_01'",
#    Composite(
#        (4500, 6200),
#        (1655, 600), "images/sprites/SLW/SWN/ese_base_05_01.png"
#    ),

#    "eyes_LW_01 == 'eyes_norm_cray_01'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_cray_01_01.png"
#    ),
#
#    "eyes_LW_01 == 'eyes_norm_horror_01'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_horror_01_01.png"
#    ),
#
#    "eyes_LW_01 == 'eyes_norm_horror_02'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_horror_01_02.png"
#    ),
#
#    "eyes_LW_01 == 'eyes_norm_prizes_01'",
#    Composite(
#        (4500, 6200),
#        (1655, 620), "images/sprites/SLW/SWN/ese_base_prizes_01_01.png"
#    ),

#    "True", "SLW_eyes_blink_01"   # ИСПРАВЛЕНО: было "Trye"
#)

# ===================================================
# ПЛАЧ
# ===================================================

image SLW_cry_01 = ConditionSwitch(

    "cry_LW_01 == 'no'", Null(),

    "cry_LW_01 == 'cry_01'", 
    Composite(
        (4500, 6200),
        (1680, 750), "images/sprites/SLW/SWN/cry_base_01_02.png"
    ),

    "cry_LW_01 == 'cry_02'", 
    Composite(
        (4500, 6200),
        (1730, 750), "images/sprites/SLW/SWN/cry_base_01_03.png"
    ),

    "cry_LW_01 == 'cry_03'", 
    Composite(
        (4500, 6200),
        (1730, 750), "images/sprites/SLW/SWN/cry_base_01_04.png"
    ),

    "cry_LW_01 == 'cry_04'", 
    Composite(
        (4500, 6200),
        (1730, 750), "images/sprites/SLW/SWN/cry_base_01_05.png"
    ),

    "True", 
    Composite(
        (4500, 6200),
        (1730, 750), "images/sprites/SLW/SWN/cry_base_01_01.png"
    )
)

# ===================================================
# ВЕСНУШКИ
# ===================================================

# ИСПРАВЛЕНО: "Trye" -> "True"
image SLW_freckles_01 = ConditionSwitch(

    "freckles_LW_01 == 'no'", Null(),

    "freckles_LW_01 == 'norm_01'",
    Composite(
        (4500, 6200),
        (1750, 810), "images/sprites/SLW/SWN/freckles_base_01_02.png"
    ),

    "freckles_LW_01 == 'norm_02'",
    Composite(
        (4500, 6200),
        (1750, 810), "images/sprites/SLW/SWN/freckles_base_01_03.png"
    ),

    "freckles_LW_01 == 'norm_03'",
    Composite(
        (4500, 6200),
        (1750, 810), "images/sprites/SLW/SWN/freckles_base_01_04.png"
    ),

    "freckles_LW_01 == 'norm_04'",
    Composite(
        (4500, 6200),
        (1750, 810), "images/sprites/SLW/SWN/freckles_base_01_05.png"
    ),

    "freckles_LW_01 == 'norm_05'",
    Composite(
        (4500, 6200),
        (1750, 810), "images/sprites/SLW/SWN/freckles_base_01_06.png"
    ),

    "freckles_LW_01 == 'norm_hatching_01'",
    Composite(
        (4500, 6200),
        (1750, 810), "images/sprites/SLW/SWN/freckles_base_01_07.png"
    ),

    "freckles_LW_01 == 'norm_blush_01'",
    Composite(
        (4500, 6200),
        (1150, 810), "images/sprites/SLW/SWN/freckles_base_01_08.png"
    ),

    "True",                         # ИСПРАВЛЕНО: было "Trye"
    Composite(
        (4500, 6200),
        (1750, 810), "images/sprites/SLW/SWN/freckles_base_01_01.png"
    )
)

# ===================================================
# РОТ
# ===================================================

image SLW_mouth_01 = ConditionSwitch(

    "mouth_LW_01 == 'norm_smail_01'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_01.png"
    ),

    "mouth_LW_01 == 'norm_smail_02'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_11.png"
    ),

    "mouth_LW_01 == 'norm_smail_03'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_06.png"
    ),

    "mouth_LW_01 == 'norm_conversation_01'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_02.png"
    ),

    "mouth_LW_01 == 'norm_conversation_02'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_03.png"
    ),

    "mouth_LW_01 == 'norm_conversation_03'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_07.png"
    ),

    "mouth_LW_01 == 'norm_conversation_04'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_16.png"
    ),

    "mouth_LW_01 == 'norm_surprised_01'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_04.png"
    ),

    "mouth_LW_01 == 'norm_surprised_02'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_08.png"
    ),

    "mouth_LW_01 == 'norm_surprised_03'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_12.png"
    ),

    "mouth_LW_01 == 'norm_surprised_04'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_14.png"
    ),

    "mouth_LW_01 == 'norm_sour_01'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_10.png"
    ),

    "mouth_LW_01 == 'norm_sour_02'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_13.png"
    ),

    "mouth_LW_01 == 'norm_sour_03'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_15.png"
    ),

    "mouth_LW_01 == 'norm_audacious_01'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_05.png"
    ),

    "mouth_LW_01 == 'norm_language_01'",
    Composite(
        (4500, 6200),
        (1950, 980), "images/sprites/SLW/SWN/mouth_base_smail_01_09.png"
    ),

    "True",
    Composite(
        (4500, 6200),
        (1970, 980), "images/sprites/SLW/SWN/mouth_base_01_01.png"
    )
)

#====================================================
#БРОВИ
#====================================================

image SLW_brov_01 = ConditionSwitch(

    "brov_LW_01 == 'brov_surprised_01'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_02.png"
            ),

    "brov_LW_01 == 'brov_gloomy_01'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_03.png"
            ),

    "brov_LW_01 == 'brov_irritations_01'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_04.png"
            ),

    "brov_LW_01 == 'brov_sad_01'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_05.png"
            ),

    "brov_LW_01 == 'brov_angry_01'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_06.png"
            ),

    "brov_LW_01 == 'brov_angry_02'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_07.png"
            ),

    "brov_LW_01 == 'brov_angry_03'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_08.png"
            ),

    "brov_LW_01 == 'brov_angry_04'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_09.png"
            ),

    "brov_LW_01 == 'brov_angry_05'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_10.png"
            ),

    "brov_LW_01 == 'brov_angry_06'", Composite(
                (4500, 6200),
                (1650, 530), "images/sprites/SLW/SWN/brov_base_01_11.png"
            ),

    "True", Composite(
                (4500, 6200),
                (1665, 550), "images/sprites/SLW/SWN/brov_base_01_01.png"
            )
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

    # заглушка
    attribute SH:# default:
        Composite(
            (2500, 6200),
            (1556, 130), "images/sprites/SLW/SWN/SLW_H.png"
        )

    # Тело
    group bodu_01:
        attribute bodu_norm_01_nude default:
            Composite(
                (5500, 6200),
                (1000, 1000), "images/sprites/SLW/SWN/SLW_01_02_bodu_base.png"
            )

    # Голова
    attribute head default:
        "LWS_head"
   
    attribute brov_01:# default:
        # Брови (одна группа, один вариант по умолчанию)
        # ИСПРАВЛЕНО: была дублирующая group brov с im.Alpha
        "SLW_brov_01"

    attribute eyes_01 default:
        # Глаза
        "SLW_eyes_01"

    attribute cry_01:# default:
        #плач
        "SLW_cry_01"
 
    attribute freckles_01:# default:
        # Веснушки
        "SLW_freckles_01"

    attribute mouth_01:# default:
        # Рот
        "SLW_mouth_01"

    
    attribute hair_01:# default:
        # Волосы
        "SLW_hair_01"

    attribute brov_alpha_01:# default:
        #брови альфа канал.
        Transform("SLW_brov_01", alpha=0.7)

    group censorship:
        # Цензура (не default — показывается только явным вызовом)
        attribute censorship_01:
            Composite(
                (3500, 6000),
                (-390, 80), "images/sprites/SLW/SWN/censorship_01_01_base.png"
            )


#    always:
#        Composite(
#            (949, 1900),
#            (560,337), im.FactorScale("images/sprites/SLW/SWN/SLW_01_01_kassa_01.png", 0.50, 0.50),
#            (0, 330), "images/sprites/SLW/SWN/SLW_01_01_bodu_base.png", 
#            (323, 9), "images/sprites/SLW/SWN/SLW_01_01_feis_01.png"
#        )
        
#    attribute censorship:

#        Composite(
#            (949, 1900),
#            (0, 330), "images/sprites/SLW/SWN/censorship_01_01_base.png"
#        )

#    group eye:
        
#        attribute eye_norm default:

#            Composite(
#                (949, 1900),
#                (365, 210), "images/sprites/SLW/SWN/SLW_01_01_eyes_norm_01.png"  
#            )
              

#    group mouth:

#        attribute mouth_norm default:

#            Composite(
#                (949, 1900),
#                (460, 345), "images/sprites/SLW/SWN/SLW_01_01_mouth_norm_01.png" 
#           )


#    group eyebrows:

#        attribute eyebrows_norm default:

#            Composite(
#                (949, 1900),
#                (385, 165), "images/sprites/SLW/SWN/SLW_01_01_eyebrows_norm_01.png"
#           )   

    #attribute fece default:
        #im.FactorScale("images/sprites/SLW/SWN/SLW_01_01_feis_01.png", 0.5, 0.5)

    #if angry:
        #""
    #else:
        #""

    #group costume :

        #attribute 01:

        #attribute 02:

        #attribute 03:
    # attribute gloves

# в полный рост
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
    
#наклон гловы
image LW_NakBust_a_01 = im.FactorScale("images/sprites/SLW/LW_Nak_a_01.png", 0.15, 0.15)
image LW_NakBust_a_02 = im.FactorScale("images/sprites/SLW/LW_Nak_a_02.png", 0.15, 0.15)
image LW_NakBust_a_03 = im.FactorScale("images/sprites/SLW/LW_Nak_a_03.png", 0.15, 0.15)
    
#2/3
image LW_NakBust_a_07 = im.FactorScale("images/sprites/SLW/LW_Nak_a_07.png", 0.15, 0.15)
    
#2/3 наклон
image LW_NakBust_a_05 = im.FactorScale("images/sprites/SLW/LW_Nak_a_05.png", 0.15, 0.15)
image LW_NakBust_a_06 = im.FactorScale("images/sprites/SLW/LW_Nak_a_06.png", 0.15, 0.15)
    
#наклон стеснительно-заигрующе
image LW_NakBust_a_04 = im.FactorScale("images/sprites/SLW/LW_Nak_a_04.png", 0.15, 0.15) 
    
#доволная
image LW_NakBust_a_08 = im.FactorScale("images/sprites/SLW/LW_Nak_a_08.png", 0.15, 0.15)
    
image LW_NorBust_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_01.png", 0.15, 0.15)
image LW_NorBust_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_07.png", 0.15, 0.15)
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
    
image LW_NormaBust_a_01 = im.FactorScale("images/sprites/SLW/LW_Norma_a_26.png", 0.27, 0.27)
image LW_NormaBust_a_02 = im.FactorScale("images/sprites/SLW/LW_Norma_a_27.png", 0.2, 0.2)
    
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
define screen_left_01 = Position(xpos=200, ypos=1050)
define screen_left_02 = Position(xpos=200, ypos=900)
define screen_left_03 = Position(xpos=270, ypos=1150)
define screen_center_01  = Position(xpos=700, ypos=1050)
define screen_center_02  = Position(xpos=700, ypos=900)
define screen_center_03  = Position(xpos=400, ypos=100)
define screen_right_01 = Position(xpos=1100, ypos=1050)
define screen_right_02 = Position(xpos=1100, ypos=900)

# переменные для Маленькой Ведьмы на ближный средний и дальный план
default LW_short_range = FactorZoom(0.53, 0.53, 0.0, opaque = False)
default LW_medium_range = FactorZoom(0.30, 0.30, 0.0, opaque = False)
default LW_long_range = FactorZoom(0.15, 0.15, 0.0, opaque = False)

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
define loposC = Position(xpos = 760, ypos = 145, xanchor = 0.5, yanchor = 0.5)
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
