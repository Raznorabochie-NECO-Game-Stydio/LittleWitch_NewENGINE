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


#дополнительные вектора перемещения
transform moveout_left_bottom:
    ease 5.0  xpos -500 ypos 1200

transform movein_left_bottom_01:
    xalign -0.5
    yalign 1.5
    ease 5.0 xalign 0.5 yalign 0.7

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

# ════════════════════════════════════════════════════════════════════
#  СИСТЕМА СОСТАВНОГО ПЕРСОНАЖА «МАЛЕНЬКАЯ ВЕДЬМА» (SLW)
# ────────────────────────────────────────────────────────────────────
#  Идея: персонаж собирается из множества PNG-слоёв (тело, глаза, рот,
#  брови, веснушки, плач, волосы, шляпа, бельё, одежда, перчатки, сапоги,
#  коса). Какие именно картинки рисовать — определяется текущим
#  состоянием store.slw (объект SLWState) и текущей силой ветра wind_01.
#
#  Слои собираются в Composite на холсте CANVAS, а итог отдаётся через
#  DynamicDisplayable build_slw — поэтому достаточно изменить slw.xxx,
#  и на следующем кадре отрисовка обновится.
# ════════════════════════════════════════════════════════════════════
init python:

    import random

    # Размер «холста», на котором собирается персонаж.
    # Все PNG-слои должны быть нарисованы в этом же размере и УЖЕ
    # выровнены друг под друга (поэтому везде позиция (0, 0)).

    CANVAS = (1500, 2130)

    # ════════════════════════════════════════════════════════════════
    # 1. ТЕЛА
    # ────────────────────────────────────────────────────────────────
    # Словарь: "имя позы/ракурса тела" -> "путь к PNG".
    # Это базовый слой. Какое тело показать — определяется slw.body.
    # Если slw.body указывает на несуществующий ключ — берётся "default".
    # ════════════════════════════════════════════════════════════════

    SLW_BODIES = {
        "bodu_01_left":            "images/sprites/SLW/SWN/bodu/SLW_01_01_bodu_base_left.png",
        "bodu_01_left_down":       "images/sprites/SLW/SWN/bodu/SLW_01_01_bodu_base_left_down.png",
        "bodu_01_left_slant":      "images/sprites/SLW/SWN/bodu/SLW_01_01_bodu_base_left_slant.png",
        "bodu_02_left":            "images/sprites/SLW/SWN/bodu/SLW_01_02_bodu_base_left.png",
        "bodu_02_left_slant":      "images/sprites/SLW/SWN/bodu/SLW_01_02_bodu_base_left_slant.png",
        "bodu_02_default":         "images/sprites/SLW/SWN/bodu/SLW_01_02_bodu_default.png",
        "bodu_02_left_down":       "images/sprites/SLW/SWN/bodu/SLW_01_02_bodu_left_down.png",
        "bodu_03_default":         "images/sprites/SLW/SWN/bodu/SLW_01_03_bodu_base_default.png",
        "bodu_03_left_down":       "images/sprites/SLW/SWN/bodu/SLW_01_03_bodu_base_left_down.png",
        "bodu_03_full_face":       "images/sprites/SLW/SWN/bodu/SLW_01_03_bodu_full_face.png",
        "bodu_03_left_down_slant": "images/sprites/SLW/SWN/bodu/SLW_01_03_bodu_left_down_slant.png",
        "bodu_04_default":         "images/sprites/SLW/SWN/bodu/SLW_01_04_bodu_default.png",
        "bodu_04_left_down":       "images/sprites/SLW/SWN/bodu/SLW_01_04_bodu_base_left_down.png",
        "bodu_04_full_face":       "images/sprites/SLW/SWN/bodu/SLW_01_04_bodu_full_face.png",
        "bodu_04_full_face_slant": "images/sprites/SLW/SWN/bodu/SLW_01_04_bodu_full_face_slant.png",
        "bodu_05_default":         "images/sprites/SLW/SWN/bodu/SLW_01_05_bodu_default.png",
        "bodu_05_full_face":       "images/sprites/SLW/SWN/bodu/SLW_01_05_bodu_full_face.png",
        "bodu_05_full_face_slant": "images/sprites/SLW/SWN/bodu/SLW_01_05_bodu_full_face_slant.png",
        "bodu_05_left":            "images/sprites/SLW/SWN/bodu/SLW_01_05_bodu_left.png",
        "bodu_05_left_down":       "images/sprites/SLW/SWN/bodu/SLW_01_05_bodu_left_down.png",
        "bodu_06_default":         "images/sprites/SLW/SWN/bodu/SLW_01_06_bodu_default.png",
        "bodu_06_left":            "images/sprites/SLW/SWN/bodu/SLW_01_06_bodu_left.png",
        "bodu_06_left_down":       "images/sprites/SLW/SWN/bodu/SLW_01_06_bodu_left_down.png",
        "bodu_06_left_slant":      "images/sprites/SLW/SWN/bodu/SLW_01_06_bodu_left_slant.png",
        "bodu_07_default":         "images/sprites/SLW/SWN/bodu/SLW_01_07_bodu_default.png",
        "bodu_08_default":         "images/sprites/SLW/SWN/bodu/SLW_01_08_bodu_default.png",
        "bodu_08_left":            "images/sprites/SLW/SWN/bodu/SLW_01_08_bodu_left.png",
        "bodu_08_left_down":       "images/sprites/SLW/SWN/bodu/SLW_01_08_bodu_left_down.png",
        "bodu_08_left_slant":      "images/sprites/SLW/SWN/bodu/SLW_01_08_bodu_left_slant.png",
        "bodu_09_default":         "images/sprites/SLW/SWN/bodu/SLW_01_09_bodu_default.png",
        "bodu_09_left":            "images/sprites/SLW/SWN/bodu/SLW_01_09_bodu_left.png",
        "bodu_09_left_down":       "images/sprites/SLW/SWN/bodu/SLW_01_09_bodu_left_down.png",
        "bodu_09_left_slant":      "images/sprites/SLW/SWN/bodu/SLW_01_09_bodu_left_slant.png",
        "bodu_12_base":            "images/sprites/SLW/SWN/bodu/SLW_01_12_bodu_base.png",
        "bodu_13_base":            "images/sprites/SLW/SWN/bodu/SLW_01_13_bodu_base.png",
        # Запасной вариант на случай некорректного значения slw.body.
        "default":                 "images/sprites/SLW/SWN/bodu/SLW_01_01_bodu_base_default.png",
    }

    # ════════════════════════════════════════════════════════════════
    # 2. ШАБЛОН СЛОЁВ ДЛЯ ВСЕХ ТЕЛ (база, набор «по умолчанию»).
    # ────────────────────────────────────────────────────────────────
    # Структура: { "слот": { "имя_варианта": "путь_к_PNG" } }.
    # Это базовый набор «лица + одежды», применяемый ко ВСЕМ телам.
    # В SLW_OVERRIDES отдельные слоты можно переопределить под конкретное тело.
    #
    # В слоте "eyes" есть служебные ключи:
    #   blink_open  / blink_half / blink_closed
    # Это три кадра моргания, их использует анимация в build_eyes_blink.
    # ════════════════════════════════════════════════════════════════
    SLW_FACE_TEMPLATE = {

        # ── ГЛАЗА ── варианты выражений + 3 кадра моргания (внизу словаря)

        "eyes": {
            'eyes_norm_01':               "images/sprites/SLW/SWN/s1/eyes/ese_base_01_01.png",
            'eyes_norm_02':               "images/sprites/SLW/SWN/s1/eyes/ese_base_01_02.png",
            'eyes_norm_03':               "images/sprites/SLW/SWN/s1/eyes/ese_base_01_03.png",
            'eyes_norm_04':               "images/sprites/SLW/SWN/s1/eyes/ese_base_01_02.png",
            'eyes_norm_05':               "images/sprites/SLW/SWN/s1/eyes/ese_base_01_03.png",
            'eyes_norm_blindfold_01':     "images/sprites/SLW/SWN/s1/eyes/ese_base_02_01.png",
            'eyes_norm_blindfold_02':     "images/sprites/SLW/SWN/s1/eyes/ese_base_02_02.png",
            'eyes_norm_blindfold_03':     "images/sprites/SLW/SWN/s1/eyes/ese_base_02_03.png",
            'eyes_norm_blindfold_04':     "images/sprites/SLW/SWN/s1/eyes/ese_base_02_04.png",
            'eyes_left_norm_01':          "images/sprites/SLW/SWN/s1/eyes/ese_base_03_01.png",
            'eyes_right_norm_01':         "images/sprites/SLW/SWN/s1/eyes/ese_base_06_01.png",
            'eyes_left_norm_he_winks_01': "images/sprites/SLW/SWN/s1/eyes/ese_base_04_01.png",
            'eyes_right_norm_he_winks_01':"images/sprites/SLW/SWN/s1/eyes/ese_base_05_01.png",
            'eyes_norm_cray_01':          "images/sprites/SLW/SWN/s1/eyes/ese_base_cray_01_01.png",
            'eyes_norm_horror_01':        "images/sprites/SLW/SWN/s1/eyes/ese_base_horror_01_01.png",
            'eyes_norm_horror_02':        "images/sprites/SLW/SWN/s1/eyes/ese_base_horror_01_02.png",
            'eyes_norm_prizes_01':        "images/sprites/SLW/SWN/s1/eyes/ese_base_prizes_01_01.png",
            'eyes_norm_prizes_02':        "images/sprites/SLW/SWN/s1/eyes/ese_base_prizes_02_01.png",
            # Кадры моргания — используются, когда slw.eyes == "blink".
            "blink_open":          "images/sprites/SLW/SWN/s1/eyes/ese_base_01_01.png",
            "blink_half":          "images/sprites/SLW/SWN/s1/eyes/ese_base_01_02.png",
            "blink_closed":        "images/sprites/SLW/SWN/s1/eyes/ese_base_01_03.png",
        },

        # ── РОТ ── варианты эмоций + 'default' (резервный, если ключ не найден)

        "mouth": {
            'norm_smail_01':        "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_01.png",
            'norm_smail_02':        "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_11.png",
            'norm_smail_03':        "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_06.png",
            'norm_conversation_01': "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_02.png",
            'norm_conversation_02': "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_03.png",
            'norm_conversation_03': "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_07.png",
            'norm_conversation_04': "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_16.png",
            'norm_surprised_01':    "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_04.png",
            'norm_surprised_02':    "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_08.png",
            'norm_surprised_03':    "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_12.png",
            'norm_surprised_04':    "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_14.png",
            'norm_sour_01':         "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_10.png",
            'norm_sour_02':         "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_13.png",
            'norm_sour_03':         "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_15.png",
            'norm_audacious_01':    "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_05.png",
            'norm_language_01':     "images/sprites/SLW/SWN/s1/mouth/mouth_base_01_09.png",
            'default':              "images/sprites/SLW/SWN/s1/mouth/mouth_base_smail_01_01.png",
        },

        # ── БРОВИ ── варианты + 'default'.
        # ВАЖНО: тот же набор используется ДВА раза:
        #   1) слот "brov"  — основной (под волосами, непрозрачный).
        #   2) слот "brov2" — поверх волос, с alpha=0.8 (см. build_slw),
        #      причём он берёт значение ИЗ slw.brov (одна переменная).

        "brov": {
            'brov_surprised_01':   "images/sprites/SLW/SWN/s1/brov/brov_base_01_02.png",
            'brov_gloomy_01':      "images/sprites/SLW/SWN/s1/brov/brov_base_01_03.png",
            'brov_irritations_01': "images/sprites/SLW/SWN/s1/brov/brov_base_01_04.png",
            'brov_sad_01':         "images/sprites/SLW/SWN/s1/brov/brov_base_01_05.png",
            'brov_angry_01':       "images/sprites/SLW/SWN/s1/brov/brov_base_01_06.png",
            'brov_angry_02':       "images/sprites/SLW/SWN/s1/brov/brov_base_01_07.png",
            'brov_angry_03':       "images/sprites/SLW/SWN/s1/brov/brov_base_01_08.png",
            'brov_angry_04':       "images/sprites/SLW/SWN/s1/brov/brov_base_01_09.png",
            'brov_angry_05':       "images/sprites/SLW/SWN/s1/brov/brov_base_01_10.png",
            'brov_angry_06':       "images/sprites/SLW/SWN/s1/brov/brov_base_01_11.png",
            'default':             "images/sprites/SLW/SWN/s1/brov/brov_base_01_01.png",
        },


        # ── ВЕСНУШКИ ── косметическое наложение на лицо.
        "freckles": {
            'norm_01':         "images/sprites/SLW/SWN/s1/freckles/freckles_base_01_02.png",
            'norm_02':         "images/sprites/SLW/SWN/s1/freckles/freckles_base_01_03.png",
            'norm_03':         "images/sprites/SLW/SWN/s1/freckles/freckles_base_01_04.png",
            'norm_04':         "images/sprites/SLW/SWN/s1/freckles/freckles_base_01_05.png",
            'norm_05':         "images/sprites/SLW/SWN/s1/freckles/freckles_base_01_06.png",
            'norm_06':         "images/sprites/SLW/SWN/s1/freckles/freckles_base_01_09.png",
            'norm_hatching_01':"images/sprites/SLW/SWN/s1/freckles/freckles_base_01_07.png",
            'norm_blush_01':   "images/sprites/SLW/SWN/s1/freckles/freckles_base_01_08.png",
            'default':         "images/sprites/SLW/SWN/s1/freckles/freckles_base_01_01.png",

        },

        # ── ПЛАЧ ── слёзы (наложение поверх лица)
        "cry": {
            'cry_01': "images/sprites/SLW/SWN/s1/cry/cry_base_01_02.png",
            'cry_02': "images/sprites/SLW/SWN/s1/cry/cry_base_01_03.png",
            'cry_03': "images/sprites/SLW/SWN/s1/cry/cry_base_01_04.png",
            'cry_04': "images/sprites/SLW/SWN/s1/cry/cry_base_01_05.png",
            'default':"images/sprites/SLW/SWN/s1/cry/cry_base_01_01.png",
        
        },

        # ── ВОЛОСЫ ── три кадра (h1, h2, h3) для анимации развевания.
        # Используются функцией build_hair. h1 — статичный кадр без ветра.

        "hair": {

            'h1': "images/sprites/SLW/SWN/hair/S_01/SLW_01_01_hair_01_01.png",
            'h2': "images/sprites/SLW/SWN/hair/S_01/SLW_01_01_hair_01_02.png",
            'h3': "images/sprites/SLW/SWN/hair/S_01/SLW_01_01_hair_01_03.png",

        },

        # ── ШЛЯПА (задняя часть) ── рисуется ПОД волосами (в начале стопки).
        # Значение берётся из slw.hat. Одна переменная управляет ОБОИМИ
        # слоями шляпы (задним и передним).

        "hat":{

            "hat_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_hat_down_01.png",
            "hat_02": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_hat_down_02.png",


        },

        # ── ШЛЯПА (передняя часть) ── рисуется ПОВЕРХ волос.
        # КЛЮЧИ совпадают с "hat" — но картинки ДРУГИЕ (передние спрайты).
        # В build_slw слот "hat_front" специально читает значение из slw.hat,
        # а картинку — отсюда. Так обе части шляпы синхронны.

        "hat_front": {
            "hat_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_hat_top_01.png",
            "hat_02": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_hat_top_02.png",
        },

        # ── ТРУСИКИ ── нижнее бельё (первый слой одежды).

        "panties": {
            "panties_white": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_panties_white_01.png",
            "panties_black": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_panties_black_01.png",

        },

        # ── ПАНТАЛОНЫ ── поверх трусиков.

        "pantaloons": {
            "pantaloons_long": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_pantaloons_01.png",
            "pantaloons_short": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_pantaloons_02.png",

        },

        # ── ТОП ── верхнее бельё / майка.

        "top": {

            "top_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_01.png",
            "top_02": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_02.png",
            "top_white": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_03.png",
            "top_black": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_04.png",

        },

        # ── ОДЕЖДА ── поверх белья (ночная рубашка / платье и т.п.).

        "clothes": {
            "nightie_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_nightie_01.png",
            "dresses_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_dresses_01.png",
        },

        #упраж
        "exercise": {
            "exercise_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_exercise_01.png",

        },

        #Карсет
        "carset": {
            "Carset_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_Carset_01.png",

        },

        # ── ПЕРЧАТКА ЛЕВАЯ ── разделена на левую/правую, чтобы можно было
        # надеть только одну (например, лишь левую при определённом сюжете).

        "gloves_left":{
            "gloves_left_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_left_gloves_01.png",

        },

        # ── ПЕРЧАТКА ПРАВАЯ ──
        "gloves_right": {
            "gloves_right_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_right_gloves_01.png",

        },

        # ── САПОГ ЛЕВЫЙ ── аналогично перчаткам — раздельно.
        "boots_left": {
            "boots_left_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_left_boot_01.png",

        },

        # ── САПОГ ПРАВЫЙ ──
        # ВНИМАНИЕ: в имени файла "righ_boot" (без 't') — это уже путь
        # к реальному файлу на диске. Проверь, что файл назван именно так.

        "boots_right": {
            "boots_right_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_righ_boot_01.png",

        },

        # ── КОСА ── 4 кадра (k1..k4) для анимации развевания на ветру.
        # Используется в build_kassa. Без ветра показывается k1.

        "kassa": {
            "k1": "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_01.png",
            "k2": "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_02.png",
            "k3": "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_03.png",
            "k4": "images/sprites/SLW/SWN/kassa/SLW_01_01_kassa_04.png",
        },
    }

    # ════════════════════════════════════════════════════════════════
    # 3. ПЕРЕОПРЕДЕЛЕНИЯ для конкретных тел
    # ────────────────────────────────────────────────────────────────
    # Когда конкретное тело (например, "bodu_01_left") требует ИНЫЕ
    # картинки лица/одежды (другой ракурс глаз, другая коса волос и т.д.),
    # для него прописывается «дельта»: какие слоты и какие ключи заменить.
    #
    # Логика слияния (_slw_merge ниже):
    #   - берётся SLW_FACE_TEMPLATE как основа
    #   - сверху накладывается соответствующий блок из SLW_OVERRIDES
    #   - совпадающие ключи перезаписываются, остальные остаются
    # ════════════════════════════════════════════════════════════════

    SLW_OVERRIDES = {

    # ────────────────────────────────────────────────────────────
    # ТЕЛО "bodu_01_left" — использует набор лица S2 (другой ракурс
    # глаз/рта/бровей), волосы S_02, тот же набор одежды.
    # ────────────────────────────────────────────────────────────   
        "bodu_01_left": {
            # Глаза S2 — другой набор PNG, но ключи такие же, как в шаблоне,
            # чтобы остальной код мог обращаться по тем же именам.
            "eyes": {
            'eyes_norm_01':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_01.png",
            'eyes_norm_02':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_02.png",
            'eyes_norm_03':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_03.png",
            'eyes_norm_04':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_05.png",
            'eyes_norm_05':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_15.png",
            'eyes_norm_blindfold_01':     "images/sprites/SLW/SWN/s2/eyes/ese_base_02_08.png",
            'eyes_norm_blindfold_02':     "images/sprites/SLW/SWN/s2/eyes/ese_base_02_12.png",
            'eyes_norm_blindfold_03':     "images/sprites/SLW/SWN/s2/eyes/ese_base_02_03.png",
            'eyes_norm_blindfold_04':     "images/sprites/SLW/SWN/s2/eyes/ese_base_02_14.png",
            'eyes_left_norm_01':          "images/sprites/SLW/SWN/s2/eyes/ese_base_02_10.png",
            'eyes_right_norm_01':         "images/sprites/SLW/SWN/s2/eyes/ese_base_02_07.png",
            'eyes_left_norm_he_winks_01': "images/sprites/SLW/SWN/s2/eyes/ese_base_02_13.png",
            'eyes_right_norm_he_winks_01':"images/sprites/SLW/SWN/s2/eyes/ese_base_02_09.png",
            'eyes_norm_cray_01':          "images/sprites/SLW/SWN/s2/eyes/ese_base_02_11.png",
            'eyes_norm_horror_01':        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_04.png",
            'eyes_norm_horror_02':        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_06.png",
            'eyes_norm_prizes_01':        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_16.png",
            'eyes_norm_prizes_02':        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_17.png",
            # Кадры моргания для этого ракурса.
            "blink_open":          "images/sprites/SLW/SWN/s2/eyes/ese_base_02_01.png",
            "blink_half":          "images/sprites/SLW/SWN/s2/eyes/ese_base_02_02.png",
            "blink_closed":        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_03.png",
        },

        # Рот S2.
        "mouth": {
            'norm_smail_01':        "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_12.png",
            'norm_smail_02':        "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_07.png",
            'norm_smail_03':        "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_09.png",
            'norm_smail_04':        "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_10.png",
            'norm_conversation_01': "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_05.png",
            'norm_conversation_02': "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_03.png",
            'norm_conversation_03': "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_04.png",
            'norm_conversation_04': "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_05.png",
            'norm_surprised_01':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_02.png",
            'norm_surprised_02':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_03.png",
            'norm_surprised_03':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_04.png",
            'norm_surprised_04':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_02.png",
            'norm_sour_01':         "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_08.png",
            'norm_sour_02':         "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_11.png",
            'norm_sour_03':         "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_13.png",
            'norm_audacious_01':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_06.png",
            'norm_language_01':     "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_14.png",
            'default':              "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_01.png",
        },

        # Брови S2.
        "brov": {
            'brov_surprised_01':   "images/sprites/SLW/SWN/s2/brov/brov_base_02_02.png",
            'brov_gloomy_01':      "images/sprites/SLW/SWN/s2/brov/brov_base_02_03.png",
            'brov_irritations_01': "images/sprites/SLW/SWN/s2/brov/brov_base_02_04.png",
            'brov_sad_01':         "images/sprites/SLW/SWN/s2/brov/brov_base_02_05.png",
            'brov_angry_01':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_06.png",
            'brov_angry_02':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_07.png",
            'brov_angry_03':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_08.png",
            'brov_angry_04':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_09.png",
            'brov_angry_05':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_10.png",
            'brov_angry_06':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_10.png",
            'default':             "images/sprites/SLW/SWN/s2/brov/brov_base_02_01.png",
        },

        # Веснушки S2.
        "freckles": {
            'norm_01':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_02.png",
            'norm_02':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_03.png",
            'norm_03':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_04.png",
            'norm_04':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_05.png",
            'norm_05':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_06.png",
            'norm_06':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_09.png",
            'norm_hatching_01':"images/sprites/SLW/SWN/s2/freckles/freckles_base_02_07.png",
            'norm_blush_01':   "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_08.png",
            'default':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_01.png",

        },

        # Плач S2.
        "cry": {
            'cry_01': "images/sprites/SLW/SWN/s2/cry/cry_base_02_02.png",
            'cry_02': "images/sprites/SLW/SWN/s2/cry/cry_base_02_03.png",
            'cry_03': "images/sprites/SLW/SWN/s2/cry/cry_base_02_01.png",
            'cry_04': "images/sprites/SLW/SWN/s2/cry/cry_base_02_01.png",
            'default':"images/sprites/SLW/SWN/s2/cry/cry_base_02_01.png",
        
        },

        # Волосы S_02 — другой набор кадров.
        "hair": {

            'h1': "images/sprites/SLW/SWN/hair/S_02/SLW_01_01_hair_02_01.png",
            'h2': "images/sprites/SLW/SWN/hair/S_02/SLW_01_01_hair_02_02.png",
            'h3': "images/sprites/SLW/SWN/hair/S_02/SLW_01_01_hair_02_03.png",

        },

        # Одежда — дублирует базу. Это сделано «на всякий случай»,
        # чтобы при необходимости легко поменять только под это тело,
        # ничего не трогая в общем шаблоне.

        #трусики
        "panties": {
            "panties_white": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_panties_white_01.png",
            "panties_black": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_panties_black_01.png",

        },

        #панталоны
        "pantaloons": {
            "pantaloons_long": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_pantaloons_01.png",
            "pantaloons_short": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_pantaloons_02.png",

        },
        
        #топ
        "top": {

            "top_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_01.png",
            "top_02": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_02.png",
            "top_white": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_03.png",
            "top_black": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_04.png",

        },

        #одежда

        "clothes": {
            "nightie_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_nightie_01.png",
            "dresses_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_dresses_02.png",
        },

        #упраж
        "exercise": {
            "exercise_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_exercise_01.png",

        },

        #Карсет
        "carset": {
            "Carset_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_Carset_01.png",

        },

        #перчатки левая
        "gloves_left":{
            "gloves_left_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_left_gloves_01.png",

        },

        #перчатка правая
        "gloves_right": {
            "gloves_right_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_right_gloves_01.png",

        },

        #сапог левый
        "boots_left": {
            "boots_left_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_left_boot_01.png",

        },

        #сапог правый
        "boots_right": {
            "boots_right_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_righ_boot_01.png",

        },


        },

        # ────────────────────────────────────────────────────────────
        # ТЕЛО "bodu_01_left_down" — отличается ТОЛЬКО волосами (S_04).
        # Остальное наследуется из SLW_FACE_TEMPLATE без изменений.
        # ────────────────────────────────────────────────────────────

        "bodu_01_left_down": {

        #глаза
        "eyes": {
            'eyes_norm_01':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_01.png",
            'eyes_norm_02':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_02.png",
            'eyes_norm_03':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_03.png",
            'eyes_norm_04':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_05.png",
            'eyes_norm_05':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_15.png",
            'eyes_norm_blindfold_01':     "images/sprites/SLW/SWN/s4/eyes/ese_base_02_08.png",
            'eyes_norm_blindfold_02':     "images/sprites/SLW/SWN/s4/eyes/ese_base_02_12.png",
            'eyes_norm_blindfold_03':     "images/sprites/SLW/SWN/s4/eyes/ese_base_02_03.png",
            'eyes_norm_blindfold_04':     "images/sprites/SLW/SWN/s4/eyes/ese_base_02_14.png",
            'eyes_left_norm_01':          "images/sprites/SLW/SWN/s4/eyes/ese_base_02_10.png",
            'eyes_right_norm_01':         "images/sprites/SLW/SWN/s4/eyes/ese_base_02_07.png",
            'eyes_left_norm_he_winks_01': "images/sprites/SLW/SWN/s4/eyes/ese_base_02_13.png",
            'eyes_right_norm_he_winks_01':"images/sprites/SLW/SWN/s4/eyes/ese_base_02_09.png",
            'eyes_norm_cray_01':          "images/sprites/SLW/SWN/s4/eyes/ese_base_02_11.png",
            'eyes_norm_horror_01':        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_04.png",
            'eyes_norm_horror_02':        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_06.png",
            'eyes_norm_prizes_01':        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_16.png",
            'eyes_norm_prizes_02':        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_17.png",
            # кадры моргания
            "blink_open":          "images/sprites/SLW/SWN/s4/eyes/ese_base_02_01.png",
            "blink_half":          "images/sprites/SLW/SWN/s4/eyes/ese_base_02_02.png",
            "blink_closed":        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_03.png",
        },

        #рот
        "mouth": {
            'norm_smail_01':        "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_12.png",
            'norm_smail_02':        "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_07.png",
            'norm_smail_03':        "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_09.png",
            'norm_smail_04':        "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_10.png",
            'norm_conversation_01': "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_05.png",
            'norm_conversation_02': "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_03.png",
            'norm_conversation_03': "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_04.png",
            'norm_conversation_04': "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_05.png",
            'norm_surprised_01':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_02.png",
            'norm_surprised_02':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_03.png",
            'norm_surprised_03':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_04.png",
            'norm_surprised_04':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_02.png",
            'norm_sour_01':         "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_08.png",
            'norm_sour_02':         "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_11.png",
            'norm_sour_03':         "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_13.png",
            'norm_audacious_01':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_06.png",
            'norm_language_01':     "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_14.png",
            'default':              "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_01.png",
        },

        #бров
        "brov": {
            'brov_surprised_01':   "images/sprites/SLW/SWN/s4/brov/brov_base_02_02.png",
            'brov_gloomy_01':      "images/sprites/SLW/SWN/s4/brov/brov_base_02_03.png",
            'brov_irritations_01': "images/sprites/SLW/SWN/s4/brov/brov_base_02_04.png",
            'brov_sad_01':         "images/sprites/SLW/SWN/s4/brov/brov_base_02_05.png",
            'brov_angry_01':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_06.png",
            'brov_angry_02':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_07.png",
            'brov_angry_03':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_08.png",
            'brov_angry_04':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_09.png",
            'brov_angry_05':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_10.png",
            'brov_angry_06':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_10.png",
            'default':             "images/sprites/SLW/SWN/s4/brov/brov_base_02_01.png",
        },

        # Веснушки
        "freckles": {
            'norm_01':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_02.png",
            'norm_02':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_03.png",
            'norm_03':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_04.png",
            'norm_04':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_05.png",
            'norm_05':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_06.png",
            'norm_06':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_09.png",
            'norm_hatching_01':"images/sprites/SLW/SWN/s4/freckles/freckles_base_02_07.png",
            'norm_blush_01':   "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_08.png",
            'default':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_01.png",

        },

        # Плач
        "cry": {
            'cry_01': "images/sprites/SLW/SWN/s4/cry/cry_base_02_02.png",
            'cry_02': "images/sprites/SLW/SWN/s4/cry/cry_base_02_03.png",
            'cry_03': "images/sprites/SLW/SWN/s4/cry/cry_base_02_01.png",
            'cry_04': "images/sprites/SLW/SWN/s4/cry/cry_base_02_01.png",
            'default':"images/sprites/SLW/SWN/s4/cry/cry_base_02_01.png",
        
        },

        #трусики
        "panties": {
            "panties_white": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_panties_white_01.png",
            "panties_black": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_panties_black_01.png",

        },

        #панталоны
        "pantaloons": {
            "pantaloons_long": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_pantaloons_01.png",
            "pantaloons_short": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_pantaloons_02.png",

        },
        
        #топ
        "top": {

            "top_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_01.png",
            "top_02": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_02.png",
            "top_white": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_03.png",
            "top_black": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_04.png",

        },

        #одежда
        "clothes": {
            "nightie_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_nightie_01.png",
            "dresses_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_dresses_03.png",
        },

        #упраж
        "exercise": {
            "exercise_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_exercise_01.png",

        },

        #Карсет
        "carset": {
            "Carset_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_Carset_01.png",

        },


        #перчатки левая
        "gloves_left":{
            "gloves_left_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_left_gloves_01.png",

        },

        #перчатка правая
        "gloves_right": {
            "gloves_right_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_right_gloves_01.png",

        },

        #сапог левый
        "boots_left": {
            "boots_left_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_left_boot_01.png",

        },

        #сапог правый
        "boots_right": {
            "boots_right_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_righ_boot_01.png",

        },

        #Волосы
        "hair": {

            'h1': "images/sprites/SLW/SWN/hair/S_07/SLW_01_01_hair_02_01.png",
            'h2': "images/sprites/SLW/SWN/hair/S_07/SLW_01_01_hair_02_02.png",
            'h3': "images/sprites/SLW/SWN/hair/S_07/SLW_01_01_hair_02_03.png",

        },

        },

        # ────────────────────────────────────────────────────────────
        # ТЕЛО "bodu_01_left_slant" — наклонённый ракурс.
        # Использует набор лица S3 (s3/eyes, s3/mouth, s3/brov, ...),
        # волосы S_04 и стандартную одежду.
        # Структура полностью аналогична блоку bodu_01_left.
        # ────────────────────────────────────────────────────────────

        "bodu_01_left_slant": {
        
        #глаза
        "eyes": {
            'eyes_norm_01':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_01.png",
            'eyes_norm_02':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_02.png",
            'eyes_norm_03':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_03.png",
            'eyes_norm_04':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_02.png",
            'eyes_norm_05':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_03.png",
            'eyes_norm_blindfold_01':     "images/sprites/SLW/SWN/s3/eyes/ese_base_02_01.png",
            'eyes_norm_blindfold_02':     "images/sprites/SLW/SWN/s3/eyes/ese_base_02_02.png",
            'eyes_norm_blindfold_03':     "images/sprites/SLW/SWN/s3/eyes/ese_base_02_03.png",
            'eyes_norm_blindfold_04':     "images/sprites/SLW/SWN/s3/eyes/ese_base_02_04.png",
            'eyes_left_norm_01':          "images/sprites/SLW/SWN/s3/eyes/ese_base_03_01.png",
            'eyes_right_norm_01':         "images/sprites/SLW/SWN/s3/eyes/ese_base_06_01.png",
            'eyes_left_norm_he_winks_01': "images/sprites/SLW/SWN/s3/eyes/ese_base_04_01.png",
            'eyes_right_norm_he_winks_01':"images/sprites/SLW/SWN/s3/eyes/ese_base_05_01.png",
            'eyes_norm_cray_01':          "images/sprites/SLW/SWN/s3/eyes/ese_base_cray_01_01.png",
            'eyes_norm_horror_01':        "images/sprites/SLW/SWN/s3/eyes/ese_base_horror_01_01.png",
            'eyes_norm_horror_02':        "images/sprites/SLW/SWN/s3/eyes/ese_base_horror_01_02.png",
            'eyes_norm_prizes_01':        "images/sprites/SLW/SWN/s3/eyes/ese_base_prizes_01_01.png",
            'eyes_norm_prizes_02':        "images/sprites/SLW/SWN/s3/eyes/ese_base_prizes_02_01.png",
            # кадры моргания
            "blink_open":          "images/sprites/SLW/SWN/s3/eyes/ese_base_01_01.png",
            "blink_half":          "images/sprites/SLW/SWN/s3/eyes/ese_base_01_02.png",
            "blink_closed":        "images/sprites/SLW/SWN/s3/eyes/ese_base_01_03.png",
        },

        #рот
        "mouth": {
            'norm_smail_01':        "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_01.png",
            'norm_smail_02':        "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_11.png",
            'norm_smail_03':        "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_06.png",
            'norm_conversation_01': "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_02.png",
            'norm_conversation_02': "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_03.png",
            'norm_conversation_03': "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_07.png",
            'norm_conversation_04': "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_16.png",
            'norm_surprised_01':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_04.png",
            'norm_surprised_02':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_08.png",
            'norm_surprised_03':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_12.png",
            'norm_surprised_04':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_14.png",
            'norm_sour_01':         "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_10.png",
            'norm_sour_02':         "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_13.png",
            'norm_sour_03':         "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_15.png",
            'norm_audacious_01':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_05.png",
            'norm_language_01':     "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_09.png",
            'default':              "images/sprites/SLW/SWN/s3/mouth/mouth_base_smail_01_01.png",
        },

        #бров
        "brov": {
            'brov_surprised_01':   "images/sprites/SLW/SWN/s3/brov/brov_base_01_02.png",
            'brov_gloomy_01':      "images/sprites/SLW/SWN/s3/brov/brov_base_01_03.png",
            'brov_irritations_01': "images/sprites/SLW/SWN/s3/brov/brov_base_01_04.png",
            'brov_sad_01':         "images/sprites/SLW/SWN/s3/brov/brov_base_01_05.png",
            'brov_angry_01':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_06.png",
            'brov_angry_02':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_07.png",
            'brov_angry_03':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_08.png",
            'brov_angry_04':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_09.png",
            'brov_angry_05':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_10.png",
            'brov_angry_06':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_11.png",
            'default':             "images/sprites/SLW/SWN/s3/brov/brov_base_01_01.png",
        },


        # Веснушки
        "freckles": {
            'norm_01':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_02.png",
            'norm_02':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_03.png",
            'norm_03':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_04.png",
            'norm_04':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_05.png",
            'norm_05':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_06.png",
            'norm_06':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_09.png",
            'norm_hatching_01':"images/sprites/SLW/SWN/s3/freckles/freckles_base_01_07.png",
            'norm_blush_01':   "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_08.png",
            'default':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_01.png",

        },

        # Плач
        "cry": {
            'cry_01': "images/sprites/SLW/SWN/s3/cry/cry_base_01_02.png",
            'cry_02': "images/sprites/SLW/SWN/s3/cry/cry_base_01_03.png",
            'cry_03': "images/sprites/SLW/SWN/s3/cry/cry_base_01_04.png",
            'cry_04': "images/sprites/SLW/SWN/s3/cry/cry_base_01_05.png",
            'default':"images/sprites/SLW/SWN/s3/cry/cry_base_01_01.png",
        
        },

        #Волосы
        "hair": {

            'h1': "images/sprites/SLW/SWN/hair/S_06/SLW_01_01_hair_01_01.png",
            'h2': "images/sprites/SLW/SWN/hair/S_06/SLW_01_01_hair_01_02.png",
            'h3': "images/sprites/SLW/SWN/hair/S_06/SLW_01_01_hair_01_03.png",

        },

        #шляпа (задняя часть — под волосами)
        "hat":{

            "hat_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_hat_down_01.png",
            "hat_02": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_hat_down_02.png",


        },

        #шляпа (передняя часть — поверх волос, ДРУГИЕ спрайты)
        "hat_front": {
            "hat_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_hat_top_01.png",
            "hat_02": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_hat_top_02.png",
        },

        #трусики
        "panties": {
            "panties_white": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_panties_white_01.png",
            "panties_black": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_panties_black_01.png",

        },

        #панталоны
        "pantaloons": {
            "pantaloons_long": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_pantaloons_01.png",
            "pantaloons_short": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_pantaloons_02.png",

        },

        #топ
        "top": {

            "top_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_01.png",
            "top_02": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_02.png",
            "top_white": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_03.png",
            "top_black": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_top_04.png",

        },

        #одежда
        "clothes": {
            "nightie_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_nightie_01.png",
            "dresses_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_dresses_01.png",
        },

        #упраж
        "exercise": {
            "exercise_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_exercise_01.png",

        },

        #Карсет
        "carset": {
            "Carset_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_Carset_01.png",

        },

        #перчатки левая
        "gloves_left":{
            "gloves_left_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_left_gloves_01.png",

        },

        #перчатка правая
        "gloves_right": {
            "gloves_right_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_right_gloves_01.png",

        },

        #сапог левый
        "boots_left": {
            "boots_left_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_left_boot_01.png",

        },

        #сапог правый
        "boots_right": {
            "boots_right_01": "images/sprites/SLW/SWN/clothes/S01-02/SLW_01_01_bodu_base_default_righ_boot_01.png",

            },

        },

        # ────────────────────────────────────────────────────────────
        # ТЕЛО "bodu_02_left" — левый ракурс.
        # Использует набор лица S2
        # волосы S_04 стандартную одежды -----.
        # Структура полностью аналогична блоку bodu_01_left.
        # ────────────────────────────────────────────────────────────

        "bodu_02_left": {
            # Глаза S2 — другой набор PNG, но ключи такие же, как в шаблоне,
            # чтобы остальной код мог обращаться по тем же именам.
            "eyes": {
            'eyes_norm_01':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_01.png",
            'eyes_norm_02':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_02.png",
            'eyes_norm_03':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_03.png",
            'eyes_norm_04':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_05.png",
            'eyes_norm_05':               "images/sprites/SLW/SWN/s2/eyes/ese_base_02_15.png",
            'eyes_norm_blindfold_01':     "images/sprites/SLW/SWN/s2/eyes/ese_base_02_08.png",
            'eyes_norm_blindfold_02':     "images/sprites/SLW/SWN/s2/eyes/ese_base_02_12.png",
            'eyes_norm_blindfold_03':     "images/sprites/SLW/SWN/s2/eyes/ese_base_02_03.png",
            'eyes_norm_blindfold_04':     "images/sprites/SLW/SWN/s2/eyes/ese_base_02_14.png",
            'eyes_left_norm_01':          "images/sprites/SLW/SWN/s2/eyes/ese_base_02_10.png",
            'eyes_right_norm_01':         "images/sprites/SLW/SWN/s2/eyes/ese_base_02_07.png",
            'eyes_left_norm_he_winks_01': "images/sprites/SLW/SWN/s2/eyes/ese_base_02_13.png",
            'eyes_right_norm_he_winks_01':"images/sprites/SLW/SWN/s2/eyes/ese_base_02_09.png",
            'eyes_norm_cray_01':          "images/sprites/SLW/SWN/s2/eyes/ese_base_02_11.png",
            'eyes_norm_horror_01':        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_04.png",
            'eyes_norm_horror_02':        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_06.png",
            'eyes_norm_prizes_01':        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_16.png",
            'eyes_norm_prizes_02':        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_17.png",
            # Кадры моргания для этого ракурса.
            "blink_open":          "images/sprites/SLW/SWN/s2/eyes/ese_base_02_01.png",
            "blink_half":          "images/sprites/SLW/SWN/s2/eyes/ese_base_02_02.png",
            "blink_closed":        "images/sprites/SLW/SWN/s2/eyes/ese_base_02_03.png",
        },

        # Рот S2.
        "mouth": {
            'norm_smail_01':        "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_12.png",
            'norm_smail_02':        "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_07.png",
            'norm_smail_03':        "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_09.png",
            'norm_smail_04':        "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_10.png",
            'norm_conversation_01': "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_05.png",
            'norm_conversation_02': "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_03.png",
            'norm_conversation_03': "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_04.png",
            'norm_conversation_04': "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_05.png",
            'norm_surprised_01':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_02.png",
            'norm_surprised_02':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_03.png",
            'norm_surprised_03':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_04.png",
            'norm_surprised_04':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_02.png",
            'norm_sour_01':         "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_08.png",
            'norm_sour_02':         "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_11.png",
            'norm_sour_03':         "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_13.png",
            'norm_audacious_01':    "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_06.png",
            'norm_language_01':     "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_14.png",
            'default':              "images/sprites/SLW/SWN/s2/mouth/mouth_base_02_01.png",
        },

        # Брови S2.
        "brov": {
            'brov_surprised_01':   "images/sprites/SLW/SWN/s2/brov/brov_base_02_02.png",
            'brov_gloomy_01':      "images/sprites/SLW/SWN/s2/brov/brov_base_02_03.png",
            'brov_irritations_01': "images/sprites/SLW/SWN/s2/brov/brov_base_02_04.png",
            'brov_sad_01':         "images/sprites/SLW/SWN/s2/brov/brov_base_02_05.png",
            'brov_angry_01':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_06.png",
            'brov_angry_02':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_07.png",
            'brov_angry_03':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_08.png",
            'brov_angry_04':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_09.png",
            'brov_angry_05':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_10.png",
            'brov_angry_06':       "images/sprites/SLW/SWN/s2/brov/brov_base_02_10.png",
            'default':             "images/sprites/SLW/SWN/s2/brov/brov_base_02_01.png",
        },

        # Веснушки S2.
        "freckles": {
            'norm_01':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_02.png",
            'norm_02':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_03.png",
            'norm_03':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_04.png",
            'norm_04':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_05.png",
            'norm_05':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_06.png",
            'norm_06':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_09.png",
            'norm_hatching_01':"images/sprites/SLW/SWN/s2/freckles/freckles_base_02_07.png",
            'norm_blush_01':   "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_08.png",
            'default':         "images/sprites/SLW/SWN/s2/freckles/freckles_base_02_01.png",

        },

        # Плач S2.
        "cry": {
            'cry_01': "images/sprites/SLW/SWN/s2/cry/cry_base_02_02.png",
            'cry_02': "images/sprites/SLW/SWN/s2/cry/cry_base_02_03.png",
            'cry_03': "images/sprites/SLW/SWN/s2/cry/cry_base_02_01.png",
            'cry_04': "images/sprites/SLW/SWN/s2/cry/cry_base_02_01.png",
            'default':"images/sprites/SLW/SWN/s2/cry/cry_base_02_01.png",
        
        },

        # Волосы S_02 — другой набор кадров.
        "hair": {

            'h1': "images/sprites/SLW/SWN/hair/S_02/SLW_01_01_hair_02_01.png",
            'h2': "images/sprites/SLW/SWN/hair/S_02/SLW_01_01_hair_02_02.png",
            'h3': "images/sprites/SLW/SWN/hair/S_02/SLW_01_01_hair_02_03.png",

        },

        # Одежда

        
        
        },

        # ────────────────────────────────────────────────────────────
        # ТЕЛО "bodu_02_left_slant" — наклонённый ракурс.
        # Использует набор лица S3 (s3/eyes, s3/mouth, s3/brov, ...),
        # волосы S_04 и стандартную одежду.
        # Структура полностью аналогична блоку bodu_01_left.
        # ────────────────────────────────────────────────────────────

        "bodu_02_left_slant": {
            #глаза
        "eyes": {
            'eyes_norm_01':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_01.png",
            'eyes_norm_02':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_02.png",
            'eyes_norm_03':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_03.png",
            'eyes_norm_04':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_02.png",
            'eyes_norm_05':               "images/sprites/SLW/SWN/s3/eyes/ese_base_01_03.png",
            'eyes_norm_blindfold_01':     "images/sprites/SLW/SWN/s3/eyes/ese_base_02_01.png",
            'eyes_norm_blindfold_02':     "images/sprites/SLW/SWN/s3/eyes/ese_base_02_02.png",
            'eyes_norm_blindfold_03':     "images/sprites/SLW/SWN/s3/eyes/ese_base_02_03.png",
            'eyes_norm_blindfold_04':     "images/sprites/SLW/SWN/s3/eyes/ese_base_02_04.png",
            'eyes_left_norm_01':          "images/sprites/SLW/SWN/s3/eyes/ese_base_03_01.png",
            'eyes_right_norm_01':         "images/sprites/SLW/SWN/s3/eyes/ese_base_06_01.png",
            'eyes_left_norm_he_winks_01': "images/sprites/SLW/SWN/s3/eyes/ese_base_04_01.png",
            'eyes_right_norm_he_winks_01':"images/sprites/SLW/SWN/s3/eyes/ese_base_05_01.png",
            'eyes_norm_cray_01':          "images/sprites/SLW/SWN/s3/eyes/ese_base_cray_01_01.png",
            'eyes_norm_horror_01':        "images/sprites/SLW/SWN/s3/eyes/ese_base_horror_01_01.png",
            'eyes_norm_horror_02':        "images/sprites/SLW/SWN/s3/eyes/ese_base_horror_01_02.png",
            'eyes_norm_prizes_01':        "images/sprites/SLW/SWN/s3/eyes/ese_base_prizes_01_01.png",
            'eyes_norm_prizes_02':        "images/sprites/SLW/SWN/s3/eyes/ese_base_prizes_02_01.png",
            # кадры моргания
            "blink_open":          "images/sprites/SLW/SWN/s3/eyes/ese_base_01_01.png",
            "blink_half":          "images/sprites/SLW/SWN/s3/eyes/ese_base_01_02.png",
            "blink_closed":        "images/sprites/SLW/SWN/s3/eyes/ese_base_01_03.png",
        },

        #рот
        "mouth": {
            'norm_smail_01':        "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_01.png",
            'norm_smail_02':        "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_11.png",
            'norm_smail_03':        "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_06.png",
            'norm_conversation_01': "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_02.png",
            'norm_conversation_02': "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_03.png",
            'norm_conversation_03': "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_07.png",
            'norm_conversation_04': "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_16.png",
            'norm_surprised_01':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_04.png",
            'norm_surprised_02':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_08.png",
            'norm_surprised_03':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_12.png",
            'norm_surprised_04':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_14.png",
            'norm_sour_01':         "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_10.png",
            'norm_sour_02':         "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_13.png",
            'norm_sour_03':         "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_15.png",
            'norm_audacious_01':    "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_05.png",
            'norm_language_01':     "images/sprites/SLW/SWN/s3/mouth/mouth_base_01_09.png",
            'default':              "images/sprites/SLW/SWN/s3/mouth/mouth_base_smail_01_01.png",
        },

        #бров
        "brov": {
            'brov_surprised_01':   "images/sprites/SLW/SWN/s3/brov/brov_base_01_02.png",
            'brov_gloomy_01':      "images/sprites/SLW/SWN/s3/brov/brov_base_01_03.png",
            'brov_irritations_01': "images/sprites/SLW/SWN/s3/brov/brov_base_01_04.png",
            'brov_sad_01':         "images/sprites/SLW/SWN/s3/brov/brov_base_01_05.png",
            'brov_angry_01':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_06.png",
            'brov_angry_02':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_07.png",
            'brov_angry_03':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_08.png",
            'brov_angry_04':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_09.png",
            'brov_angry_05':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_10.png",
            'brov_angry_06':       "images/sprites/SLW/SWN/s3/brov/brov_base_01_11.png",
            'default':             "images/sprites/SLW/SWN/s3/brov/brov_base_01_01.png",
        },


        # Веснушки
        "freckles": {
            'norm_01':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_02.png",
            'norm_02':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_03.png",
            'norm_03':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_04.png",
            'norm_04':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_05.png",
            'norm_05':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_06.png",
            'norm_06':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_09.png",
            'norm_hatching_01':"images/sprites/SLW/SWN/s3/freckles/freckles_base_01_07.png",
            'norm_blush_01':   "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_08.png",
            'default':         "images/sprites/SLW/SWN/s3/freckles/freckles_base_01_01.png",

        },

        # Плач
        "cry": {
            'cry_01': "images/sprites/SLW/SWN/s3/cry/cry_base_01_02.png",
            'cry_02': "images/sprites/SLW/SWN/s3/cry/cry_base_01_03.png",
            'cry_03': "images/sprites/SLW/SWN/s3/cry/cry_base_01_04.png",
            'cry_04': "images/sprites/SLW/SWN/s3/cry/cry_base_01_05.png",
            'default':"images/sprites/SLW/SWN/s3/cry/cry_base_01_01.png",
        
        },

        #Волосы
        "hair": {

            'h1': "images/sprites/SLW/SWN/hair/S_06/SLW_01_01_hair_01_01.png",
            'h2': "images/sprites/SLW/SWN/hair/S_06/SLW_01_01_hair_01_02.png",
            'h3': "images/sprites/SLW/SWN/hair/S_06/SLW_01_01_hair_01_03.png",

        },


        },
        # ────────────────────────────────────────────────────────────
        # ТЕЛО "bodu_02_default"
        # Использует стандартный набор лица,
        # волосы стандартны.
        # ────────────────────────────────────────────────────────────

        "bodu_02_default":{


            #одежда

        },

        # ────────────────────────────────────────────────────────────
        # ТЕЛО "bodu_02_left_down" — отличается ТОЛЬКО волосами (S_04).
        # Остальное наследуется из SLW_FACE_TEMPLATE без изменений.
        # ────────────────────────────────────────────────────────────

        "bodu_02_left_down": {
            #глаза
        "eyes": {
            'eyes_norm_01':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_01.png",
            'eyes_norm_02':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_02.png",
            'eyes_norm_03':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_03.png",
            'eyes_norm_04':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_05.png",
            'eyes_norm_05':               "images/sprites/SLW/SWN/s4/eyes/ese_base_02_15.png",
            'eyes_norm_blindfold_01':     "images/sprites/SLW/SWN/s4/eyes/ese_base_02_08.png",
            'eyes_norm_blindfold_02':     "images/sprites/SLW/SWN/s4/eyes/ese_base_02_12.png",
            'eyes_norm_blindfold_03':     "images/sprites/SLW/SWN/s4/eyes/ese_base_02_03.png",
            'eyes_norm_blindfold_04':     "images/sprites/SLW/SWN/s4/eyes/ese_base_02_14.png",
            'eyes_left_norm_01':          "images/sprites/SLW/SWN/s4/eyes/ese_base_02_10.png",
            'eyes_right_norm_01':         "images/sprites/SLW/SWN/s4/eyes/ese_base_02_07.png",
            'eyes_left_norm_he_winks_01': "images/sprites/SLW/SWN/s4/eyes/ese_base_02_13.png",
            'eyes_right_norm_he_winks_01':"images/sprites/SLW/SWN/s4/eyes/ese_base_02_09.png",
            'eyes_norm_cray_01':          "images/sprites/SLW/SWN/s4/eyes/ese_base_02_11.png",
            'eyes_norm_horror_01':        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_04.png",
            'eyes_norm_horror_02':        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_06.png",
            'eyes_norm_prizes_01':        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_16.png",
            'eyes_norm_prizes_02':        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_17.png",
            # кадры моргания
            "blink_open":          "images/sprites/SLW/SWN/s4/eyes/ese_base_02_01.png",
            "blink_half":          "images/sprites/SLW/SWN/s4/eyes/ese_base_02_02.png",
            "blink_closed":        "images/sprites/SLW/SWN/s4/eyes/ese_base_02_03.png",
        },

        #рот
        "mouth": {
            'norm_smail_01':        "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_12.png",
            'norm_smail_02':        "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_07.png",
            'norm_smail_03':        "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_09.png",
            'norm_smail_04':        "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_10.png",
            'norm_conversation_01': "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_05.png",
            'norm_conversation_02': "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_03.png",
            'norm_conversation_03': "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_04.png",
            'norm_conversation_04': "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_05.png",
            'norm_surprised_01':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_02.png",
            'norm_surprised_02':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_03.png",
            'norm_surprised_03':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_04.png",
            'norm_surprised_04':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_02.png",
            'norm_sour_01':         "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_08.png",
            'norm_sour_02':         "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_11.png",
            'norm_sour_03':         "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_13.png",
            'norm_audacious_01':    "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_06.png",
            'norm_language_01':     "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_14.png",
            'default':              "images/sprites/SLW/SWN/s4/mouth/mouth_base_02_01.png",
        },

        #бров
        "brov": {
            'brov_surprised_01':   "images/sprites/SLW/SWN/s4/brov/brov_base_02_02.png",
            'brov_gloomy_01':      "images/sprites/SLW/SWN/s4/brov/brov_base_02_03.png",
            'brov_irritations_01': "images/sprites/SLW/SWN/s4/brov/brov_base_02_04.png",
            'brov_sad_01':         "images/sprites/SLW/SWN/s4/brov/brov_base_02_05.png",
            'brov_angry_01':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_06.png",
            'brov_angry_02':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_07.png",
            'brov_angry_03':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_08.png",
            'brov_angry_04':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_09.png",
            'brov_angry_05':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_10.png",
            'brov_angry_06':       "images/sprites/SLW/SWN/s4/brov/brov_base_02_10.png",
            'default':             "images/sprites/SLW/SWN/s4/brov/brov_base_02_01.png",
        },

        # Веснушки
        "freckles": {
            'norm_01':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_02.png",
            'norm_02':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_03.png",
            'norm_03':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_04.png",
            'norm_04':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_05.png",
            'norm_05':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_06.png",
            'norm_06':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_09.png",
            'norm_hatching_01':"images/sprites/SLW/SWN/s4/freckles/freckles_base_02_07.png",
            'norm_blush_01':   "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_08.png",
            'default':         "images/sprites/SLW/SWN/s4/freckles/freckles_base_02_01.png",

        },

        # Плач
        "cry": {
            'cry_01': "images/sprites/SLW/SWN/s4/cry/cry_base_02_02.png",
            'cry_02': "images/sprites/SLW/SWN/s4/cry/cry_base_02_03.png",
            'cry_03': "images/sprites/SLW/SWN/s4/cry/cry_base_02_01.png",
            'cry_04': "images/sprites/SLW/SWN/s4/cry/cry_base_02_01.png",
            'default':"images/sprites/SLW/SWN/s4/cry/cry_base_02_01.png",
        
        },

        #Волосы
        "hair": {

            'h1': "images/sprites/SLW/SWN/hair/S_07/SLW_01_01_hair_02_01.png",
            'h2': "images/sprites/SLW/SWN/hair/S_07/SLW_01_01_hair_02_02.png",
            'h3': "images/sprites/SLW/SWN/hair/S_07/SLW_01_01_hair_02_03.png",

        },



        },

        # ────────────────────────────────────────────────────────────
        # ТЕЛО "bodu_03_default" — использует набор лица S2 (другой ракурс
        # глаз/рта/бровей), волосы S_02, тот же набор одежды.
        # ────────────────────────────────────────────────────────────  

        "bodu_03_default": {


        # ── КОСА ── 4 кадра (k1..k4) для анимации развевания на ветру.
        # Используется в build_kassa. Без ветра показывается k1.

        "kassa": {
            "k1": "images/sprites/SLW/SWN/kassa/s1/SLW_01_01_kassa_01.png",
            "k2": "images/sprites/SLW/SWN/kassa/s1/SLW_01_01_kassa_02.png",
            "k3": "images/sprites/SLW/SWN/kassa/s1/SLW_01_01_kassa_03.png",
            "k4": "images/sprites/SLW/SWN/kassa/s1/SLW_01_01_kassa_04.png",
        },



        },


        "bodu_05_full_face": {
            "eyes": {
                "eyes_norm_01":        "images/sprites/SLW/SWN/eyes/05_ff_norm_01.png",
                "eyes_norm_horror_01": "images/sprites/SLW/SWN/eyes/05_ff_horror_01.png",
                "blink_open":          "images/sprites/SLW/SWN/eyes/05_ff_blink_01.png",
                "blink_half":          "images/sprites/SLW/SWN/eyes/05_ff_blink_02.png",
                "blink_closed":        "images/sprites/SLW/SWN/eyes/05_ff_blink_03.png",
            },
        },
    }

    # ════════════════════════════════════════════════════════════════
    #  СБОРКА ИТОГОВОЙ ТАБЛИЦЫ SLW (тело -> полный набор слоёв)
    # ════════════════════════════════════════════════════════════════

    def _slw_merge(base, override):

        # Сливает базовый шаблон (SLW_FACE_TEMPLATE) с переопределениями
        # для конкретного тела (запись из SLW_OVERRIDES).
        #
        # Логика «глубокого» слияния по слотам:
        #   1) копируем КАЖДЫЙ слот базы в новый словарь (dict(keys) —
        #      делаем КОПИЮ, чтобы не портить общий шаблон при .update);
        #   2) поверх накладываем переопределения: совпадающие ключи
        #      внутри слота перезаписываются, новые — добавляются.

        result = {}
        for slot, keys in base.items():
            result[slot] = dict(keys)                   # копия словаря слота
        for slot, keys in (override or {}).items():     
            result.setdefault(slot, {})                 # если слота не было — создаём
            result[slot].update(keys)                   # накладываем дельту
        return result

    # Строим финальную таблицу: для каждого тела — готовый набор слоёв
    # (лицо + одежда из шаблона/оверрайдов) ПЛЮС путь к самому телу.

    SLW = {}
    for body_key, body_path in SLW_BODIES.items():
        face = _slw_merge(SLW_FACE_TEMPLATE, SLW_OVERRIDES.get(body_key))
        face["body"] = body_path                                            # добавляем слой "body"
        SLW[body_key] = face

    # ────────────────────────────────────────────────────────────────
    # ПОРЯДОК СЛОЁВ (снизу вверх — кто раньше в списке, тот ниже).
    #   hat        — задняя часть шляпы (под всем)
    #   kassa      — коса (за телом)
    #   body       — само тело
    #   brov       — брови (основные, под волосами)
    #   freckles   — веснушки
    #   eyes       — глаза
    #   cry        — слёзы
    #   mouth      — рот
    #   hair       — волосы (перекрывают часть лица/плеч)
    #   brov2      — брови ВТОРОЙ раз, полупрозрачно ПОВЕРХ волос
    #                (чтобы бровь читалась сквозь чёлку)
    #   hat_front  — передняя часть шляпы (поверх волос)
    #   далее одежда: обувь -> бельё -> панталоны -> топ -> платье -> перчатки
    # ────────────────────────────────────────────────────────────────

    SLW_LAYER_ORDER = ["hat", "kassa", "body", "brov", "freckles", "eyes", "cry", "mouth", "hair", "brov2", "hat_front", "boots_left", "boots_right", "panties", "pantaloons", "top", "gloves_left", "gloves_right", "clothes", "exercise", "carset"]

    # ════════════════════════════════════════════════════════════════
    # 4. СОСТОЯНИЕ ПЕРСОНАЖА
    # ────────────────────────────────────────────────────────────────
    # Объект хранит, что СЕЙЧАС надето/показано. Каждое поле — это либо:
    #   None        — слой не рисуется,
    #   "no"        — служебное значение «принудительно не рисовать»,
    #   "ключ"      — имя варианта из соответствующего слота в SLW.
    # Особый случай: eyes == "blink" включает анимацию моргания.
    # ════════════════════════════════════════════════════════════════

    class SLWState(object):
        def __init__(self):
            self.body       = None #"default" поза тела (ключ из SLW_BODIES)
            self.eyes       = None #"eyes_norm_01"   # или "blink" для анимации моргания выражение глаз ИЛИ "blink" (анимация)
            self.freckles   = None # веснушки
            self.cry        = None # слёзы
            self.mouth      = None # рот
            self.brov       = None # брови (управляет и brov, и brov2)
            self.hair       = None   # ← добавь (если ещё нет) волосы (анимируются на ветру)
            self.hat        = None   # ← добавь: одна переменная для обоих слоёв шляпы шляпа (одна переменная на обе части)
            # --- одежда ---
            self.boots_left    = None
            self.boots_right   = None
            self.panties       = None
            self.pantaloons    = None
            self.top           = None
            self.clothes       = None # платье / ночнушка
            self.exercise      = None
            self.carset        = None
            self.gloves_left   = None
            self.gloves_right  = None

    # ПРИМЕЧАНИЕ: убери дубликат self.clothes из верхней части —
    # он был объявлен дважды (см. прошлую правку).

    # Создаём глобальный объект состояния один раз (переживает rollback,
    # т.к. лежит в store). hasattr защищает от пересоздания при reload.
            

    if not hasattr(store, "slw"):
        store.slw = SLWState()

    # Сила ветра, влияет на скорость анимации косы и волос:
    #   0 — нет ветра (статичный кадр), 1 — слабый, 2 — средний, 3 — сильный.

    # wind_01: 0 нет ветра, 1 слабый, 2 средний, 3 сильный
    if not hasattr(store, "wind_01"):
        store.wind_01 = 0

    #
    # =====================================================
    # 5. АНИМАЦИЯ КОСЫ (как Displayable, кадрами)
    #    Скорость зависит от wind_01.
    #────────────────────────────────────────────────────────────────
    # Покадровая анимация. Последовательность кадров «туда-сюда»:
    # k1 → k2 → k3 → k4 → k2 → (цикл). Скорость зависит от ветра.
    # ════════════════════════════════════════════════════════════════

    _KASSA_FRAMES = ["k1", "k2", "k3", "k4", "k2"]

    def build_kassa(st, at):

        # st — время (в секундах) с момента старта этого Displayable.

        wind = getattr(store, "wind_01", 0)
        if wind <= 0:
            # без ветра — статичный первый кадр
            # Нет ветра — показываем статичный первый кадр и не перерисовываем
            # (второй элемент кортежа 0 = «не планировать следующий кадр»).
            kassa = SLW.get(store.slw.body, SLW["default"]).get("kassa", {})
            path = kassa.get("k1")
            if path is None:
                return Null(), 0 # нет картинки — пустышка
            return Composite(CANVAS, (0, 0), path), 0

        # скорость кадра по силе ветра
        # Время показа одного кадра в зависимости от силы ветра
        # (чем сильнее ветер — тем быстрее смена кадров).
        frame_time = {1: 0.5, 2: 0.35, 3: 0.2}.get(wind, 0.5)

        kassa = SLW.get(store.slw.body, SLW["default"]).get("kassa", {})
        # Номер текущего кадра: сколько «слотов времени» прошло, по кругу.
        idx = int(st / frame_time) % len(_KASSA_FRAMES)
        path = kassa.get(_KASSA_FRAMES[idx])

        if path is None:
            return Null(), 0

        d = Composite(CANVAS, (0, 0), path)
        # перерисовать к следующему кадру
        # Второй элемент — через сколько секунд перерисовать (до след. кадра).
        return d, frame_time - (st % frame_time)

    # ════════════════════════════════════════════════════════════════
    # 5b. АНИМАЦИЯ ВОЛОС (синхронно с косой)
    # ────────────────────────────────────────────────────────────────
    # Та же логика, что у косы, но кадры h1..h3 и цикл h1→h2→h3→h2.
    # Используется ТА ЖЕ формула frame_time, чтобы волосы и коса
    # колыхались в одном ритме.
    # ════════════════════════════════════════════════════════════════

    _HAIR_FRAMES = ["h1", "h2", "h3", "h2"]

    def build_hair(st, at):
        wind = getattr(store, "wind_01", 0)

        hair = SLW.get(store.slw.body, SLW["default"]).get("hair", {})

        if wind <= 0:
            # без ветра — статичный первый кадр
            # Без ветра — статичный кадр h1.
            path = hair.get("h1")
            if path is None:
                return Null(), 0
            return Composite(CANVAS, (0, 0), path), 0

        # та же скорость, что у косы — для синхрона
        frame_time = {1: 0.5, 2: 0.35, 3: 0.2}.get(wind, 0.5)

        idx = int(st / frame_time) % len(_HAIR_FRAMES)
        path = hair.get(_HAIR_FRAMES[idx])

        if path is None:
            return Null(), 0

        d = Composite(CANVAS, (0, 0), path)
        return d, frame_time - (st % frame_time)

    # ════════════════════════════════════════════════════════════════
    # 7. ГЛАВНЫЙ СТРОИТЕЛЬ ПЕРСОНАЖА
    # ────────────────────────────────────────────────────────────────
    # Проходит по SLW_LAYER_ORDER и для каждого слота добавляет в список
    # `layers` пару [(позиция), картинка_или_Displayable]. Затем собирает
    # всё в один Composite. Возвращает (Composite, 0) — статичная сборка,
    # а анимации внутри (kassa/hair/eyes) перерисовывают себя сами.
    # ════════════════════════════════════════════════════════════════

    def build_slw(st, at):
        s = store.slw  # текущее состояние
        data = SLW.get(s.body, SLW["default"]) # набор файлов для этого тела

        layers = []
        for slot in SLW_LAYER_ORDER:

            # ── ТЕЛО ── всегда рисуем (путь лежит в data["body"]).

            if slot == "body":
                layers += [(0, 0), data["body"]]
                continue

            # ── ТЕЛО ── всегда рисуем (путь лежит в data["body"]).

            if slot == "kassa":
                # анимированная коса как вложенный DynamicDisplayable
                layers += [(0, 0), slw_kassa_displayable]   # переиспользуем
                continue

            # ── ГЛАЗА (режим моргания) ── если slw.eyes == "blink",
            # вставляем анимацию моргания вместо статичной картинки.
            # ВНИМАНИЕ: если eyes НЕ "blink", этот if ничего не делает,
            # и слот глаз обработается ниже общим кодом (статичный спрайт).

            if slot == "eyes":
                key = getattr(s, "eyes", None)
                if key == "blink":
                    layers += [(0, 0), slw_eyes_blink_displayable]
       
                    continue

            # ── ВОЛОСЫ ── вставляем анимированный Displayable.

            if slot == "hair":
                # анимированные волосы (синхронно с косой)
                layers += [(0, 0), slw_hair_displayable]
                continue

            # ── БРОВИ ВТОРОЙ РАЗ (поверх волос, полупрозрачно) ──
            # Берём значение из slw.brov (не из отдельной переменной),
            # картинку — из набора "brov", и накрываем Transform(alpha=0.8).

            if slot == "brov2":
                # ВТОРОЙ слой бровей = то же значение, что и основной brov
                key = getattr(s, "brov", None)
                if key is None or key == "no":
                    continue
                # картинку берём из словаря "brov" (тот же набор)
                slot_dict = data.get("brov", {})
                if key in slot_dict:
                    path = slot_dict[key]
                else:
                    path = slot_dict.get("default")
                if path:
                    layers += [(0, 0), Transform(path, alpha=0.8)]
                continue

            # ── ПЕРЕДНЯЯ ЧАСТЬ ШЛЯПЫ (поверх волос) ──
            # Управляется тем же slw.hat, что и задняя часть, но картинки
            # берутся из отдельного набора "hat_front".

            if slot == "hat_front":                      # ← НОВОЕ
                key = getattr(s, "hat", None)
                if key is None or key == "no":
                    continue
                slot_dict = data.get("hat_front", {})
                if key in slot_dict:
                    path = slot_dict[key]
                else:
                    path = slot_dict.get("default")
                if path:
                    layers += [(0, 0), path]
                continue

            # ── ОБЩИЙ СЛУЧАЙ (все остальные слоты) ──
            # Достаём имя варианта из состояния по имени слота.

            key = getattr(s, slot, None)
            if key is None:                 # слой не задан — пропускаем
                continue
            if key == "no":                 # ← служебное: не рисовать слой принудительно скрыт — пропускаем
                continue

            slot_dict = data.get(slot, {})
            if key in slot_dict:
                path = slot_dict[key]       # нашли точное совпадение
            else:
                path = slot_dict.get("default") # иначе — запасной вариант

            if path:                        # None/пусто — не рисуем пустой путь не добавляем
                layers += [(0, 0), path]

        # Собираем все слои в один холст. 0 = не перерисовывать автоматически
        # (внутренние анимированные слои сами просят перерисовку).

        return Composite(CANVAS, *layers), 0


    # ════════════════════════════════════════════════════════════════
    #  ЖИВОЕ МОРГАНИЕ
    # ────────────────────────────────────────────────────────────────
    #  Логика:
    #   - персонаж держит глаза открытыми случайное время;
    #   - затем проигрывается моргание: half → closed → half → open;
    #   - иногда (12%) делает «двойное» моргание (короткая пауза и ещё раз);
    #   - состояние хранится в ГЛОБАЛЬНОМ словаре _blink (одно на всех),
    #     потому что DynamicDisplayable может вызываться в разных контекстах,
    #     и локальное состояние «сбрасывалось» бы.
    # ════════════════════════════════════════════════════════════════
    # ==========================================================
    # Живое моргание Маленькой Ведьмы
    # - случайная пауза между морганиями
    # - редкое двойное моргание
    # - сброс при смене положения головы
    # ==========================================================
    
    import time

    # start — время начала текущего моргания (None = глаза открыты);
    # next  — момент времени, когда нужно начать следующее моргание.

    # Глобальное состояние моргания (НЕ в blink_state, а снаружи —
    # одно на всех, не зависит от контекста рендера)
    _blink = {"start": None, "next": None}

    def build_eyes_blink(st, at):
        # Берём кадры моргания для текущего тела.
        eyes = SLW.get(store.slw.body, SLW["default"]).get("eyes", {})
        e_open   = eyes.get("blink_open")
        e_half   = eyes.get("blink_half")
        e_closed = eyes.get("blink_closed")

        # Длительности фаз (в секундах):
        HALF   = 0.15                   # полуприкрытые
        CLOSED = 0.25                   # полностью закрытые
        DUR    = HALF + CLOSED + HALF   # полная длительность моргания

        now = time.time()   # абсолютное время — не зависит от контекста! АБСОЛЮТНОЕ время — не зависит от st (контекста)

        b = _blink

        # первичная инициализация
        # Первый запуск: назначаем время первого моргания.
        if b["next"] is None:
            b["next"] = now + random.uniform(2.0, 4.0)

        # === ГЛАЗА ОТКРЫТЫ ===
        if b["start"] is None:
            if now >= b["next"]:
                b["start"] = now # пора моргнуть — стартуем
            else:
                # ещё рано: показываем открытые глаза,
                # перепроверяем через 0.05 с.
                return _slw_eyes_render(e_open), 0.05

        # === ИДЁТ МОРГАНИЕ === t — сколько прошло с начала.
        t = now - b["start"]

        if t < HALF:
            return _slw_eyes_render(e_half), 0.02    # прикрываются
        elif t < HALF + CLOSED:
            return _slw_eyes_render(e_closed), 0.02  # закрыты
        elif t < DUR:
            return _slw_eyes_render(e_half), 0.02    # открываются
        else:
            # моргание завершено Моргание завершено — сбрасываем и планируем следующее.
            b["start"] = None
            if random.random() < 0.12:
                # 12% шанс на «двойное» моргание — короткая пауза.
                b["next"] = now + random.uniform(0.15, 0.3)   # двойное
            else:
                # обычная пауза до следующего моргания.
                b["next"] = now + random.uniform(3.0, 6.0)
            return _slw_eyes_render(e_open), 0.02


    def _slw_eyes_render(path):
        # Вспомогательная: оборачивает путь в Composite на холсте.
        # Если кадра нет (None) — возвращает пустышку Null().
        if path is None:
            return Null()
        return Composite(CANVAS, (0, 0), path)

    # ════════════════════════════════════════════════════════════════
    #  РЕГИСТРАЦИЯ DYNAMIC-DISPLAYABLE-ОВ
    # ────────────────────────────────────────────────────────────────
    #  DynamicDisplayable(func) каждый кадр вызывает func(st, at) и
    #  показывает то, что она вернёт. Так анимации «живут» сами.
    # ════════════════════════════════════════════════════════════════
    # БЕЗ blink_state — теперь состояние глобальное
    slw_eyes_blink_displayable = DynamicDisplayable(build_eyes_blink)   # моргание

    slw_kassa_displayable = DynamicDisplayable(build_kassa)             # коса

    slw_hair_displayable = DynamicDisplayable(build_hair)               # волосы


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
    def make_fly_swarm(
        count=38,              # сколько всего светлячков на экране
        start_spread=5.0,     # насколько растянуть их появление по времени
        border=550             # зона появления за пределами экрана
    ):
        flies = []

        for i in range(count):
            flies.append(
                SnowBlossom(
                    FlyParticle(),
                    count=1,

                    border=border,

                    # движение чуть разное у каждого
                    xspeed=(random.uniform(-70, -25), random.uniform(-60, -30)),
                    yspeed=(random.uniform(-120, -50), random.uniform(-100, -60)),

                    # каждый появляется в разный момент
                    start=random.uniform(0.0, start_spread),

                    # False — не заполнять экран сразу
                    fast=True
                )
            )

        return Fixed(*flies)
init python:
    import random

    class FlyParticle(renpy.Displayable):
        def __init__(self, **kwargs):
            super(FlyParticle, self).__init__(**kwargs)

            # 4 варианта, но уже как displayable, а не строки
            self.variants = [
                renpy.displayable("fly1"),
                renpy.displayable("fly2"),
                renpy.displayable("fly3"),
                renpy.displayable("fly4"),
            ]

            self.anim_phase_offset = random.uniform(0.0, 1000.0)
            self.switch_phase_offset = random.uniform(0.0, 1000.0)

            self.current = random.randrange(4)

            self.last_switch = None
            self.switch_time = random.uniform(1.5, 6.0)

        def copy(self):
            return FlyParticle()

        def render(self, width, height, st, at):
            st_anim = st + self.anim_phase_offset
            st_switch = st + self.switch_phase_offset

            if self.last_switch is None:
                self.last_switch = st_switch

            if st_switch - self.last_switch >= self.switch_time:
                choices = [i for i in range(4) if i != self.current]
                self.current = random.choice(choices)

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

# белой вспышки экрана:
image white_01 = Solid("#ffffff")

transform screen_flash:
    alpha 0.0
    linear 0.1 alpha 0.8
    linear 0.3 alpha 0.0

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
    "images/BG/0014.jpg" with dissA
    pause 3.0
    
    "images/BG/0015.jpg" with dissA
    pause 3.0
    
    "images/BG/0016.jpg" with dissA
    pause 3.0
    
    "images/BG/0014a.jpg" with dissA
    pause 3.0

    "images/BG/0014c.jpg" with dissA
    pause 3.0

    "images/BG/0014b.jpg" with dissA
    pause 3.0

    "images/BG/0014d.jpg" with dissA
    pause 3.0
    
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
image bg0036a = "images/BG/0035a.jpg"
image bg0036b = "images/BG/0035b.jpg"
image bg0036c = "images/BG/0035c.jpg"
image bg0036d = "images/BG/0035d.jpg"
image bg0036e = "images/BG/0035e.jpg"
image bg0036f = "images/BG/0035f.jpg"
image bg0036g = "images/BG/0035g.jpg"
image bg0036h = "images/BG/0035h.jpg"
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
    zoom 1.7
    
image bg0064:
    "images/BG/0058b.png"
    alpha 0.4
    xzoom 2.5
    yzoom 2.0
    
image bg0065:
    "images/BG/0058a.jpg"
    xzoom 2.5
    yzoom 2.0

image bg0066 = "images/BG/0059.jpg"
image bg0066a = "images/BG/0059a.jpg"
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
image bg0096a:
    contains:
        parallel:
            "images/BG/0069.jpg" with dissA
            pause 2.0

            "images/BG/0071.jpg" with dissA
            pause 2.0

            "images/BG/0072.jpg" with dissA
            pause 2.0

            "images/BG/0073.jpg" with dissA

    contains:
        parallel:
            "images/sprites/SLW/LW_slip_01.png"
            pos (0, 400)

image bg0097:
    contains:
        "images/BG/0071.jpg"
    contains:
        "images/sprites/SLW/LW_slip_01.png"
        pos (0, 400)
        
image bg0098:
    contains:
        "images/BG/0072.jpg"
    contains:
        "images/sprites/SLW/LW_slip_01.png"
        pos (0, 400)

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
#  Маленькая Ведьма
# ===================================================
# ИСПРАВЛЕНО:
#   - убрано дублирование group brov
#   - brov_norm_01 оставлен в одной группе (непрозрачный вариант)
#   - атрибут SH помечен default
# ════════════════════════════════════════════════════════════════════
#  РЕГИСТРАЦИЯ ИЗОБРАЖЕНИЯ ПЕРСОНАЖА
# ────────────────────────────────────────────────────────────────────
#  build_slw собирает все слои в Composite. Теперь его можно
#  показывать как обычный спрайт: show little_witch
# ════════════════════════════════════════════════════════════════════


image little_witch = DynamicDisplayable(build_slw)

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

# норм

image LW_Color_Nor_a_01 = "images/sprites/SLW/LW_Norma_a_01.png"
image LW_Color_Nor_a_02 = "images/sprites/SLW/LW_Norma_a_07.png"
image LW_Color_Nor_a_03 = "images/sprites/SLW/LW_Norma_a_10.png"
image LW_Color_Nor_a_04 = "images/sprites/SLW/LW_Norma_a_13.png"

image LW_Color_NormaBust_a_01 = "images/sprites/SLW/LW_Norma_a_26.png"
image LW_Color_NormaBust_a_02 = "images/sprites/SLW/LW_Norma_a_27.png"
    
image LW_Color_nf_01 = "images/sprites/SLW/LW_Norma02.png"
image LW_Color_nf_02 = "images/sprites/SLW/LW_Norma03.png"

#наклон стеснительно-заигрующе
image LW_Color_Nak_a_04 = "images/sprites/SLW/LW_Nak_a_04.png" 

#наклон гловы
image LW_Color_Nak_a_01 = "images/sprites/SLW/LW_Nak_a_01.png"
image LW_Color_Nak_a_02 = "images/sprites/SLW/LW_Nak_a_02.png"
image LW_Color_Nak_a_03 = "images/sprites/SLW/LW_Nak_a_03.png"

#2/3 наклон
image LW_Color_Nak_a_05 = "images/sprites/SLW/LW_Nak_a_05.png"
image LW_Color_Nak_a_06 = "images/sprites/SLW/LW_Nak_a_06.png"  
image LW_Color_Nak_a_07 = "images/sprites/SLW/LW_Nak_a_07.png"

#наклон стеснительно-заигрующе
image WL_Color_Nak_a_04 = "images/sprites/SLW/LW_Nak_a_04.png"
 
#доволная
image LW_Color_Nak_a_08 = "images/sprites/SLW/LW_Nak_a_08.png"
    
#глаза закрыты
image LW_Color_NorEyesOff_a_01 = "images/sprites/SLW/LW_Norma_a_02.png"
image LW_Color_NorEyesOff_a_02 = "images/sprites/SLW/LW_Norma_a_05.png"
  
#Разговор глаза закрыты
image LW_Color_NorRazEyesOff_a_01 = "images/sprites/SLW/LW_Norma_a_03.png"
image LW_Color_NorRazEyesOff_a_02 = "images/sprites/SLW/LW_Norma_a_04.png"
    
#удивленно напугана
image LW_Color_NorHorror_a_01 = "images/sprites/SLW/LW_Norma_a_06.png"
image LW_Color_NorHorror_a_02 = "images/sprites/SLW/LW_Norma_a_25.png"
    
#разговор
image LW_Color_NorRaz_a_01 = "images/sprites/SLW/LW_Norma_a_08.png"
image LW_Color_NorRaz_a_02 = "images/sprites/SLW/LW_Norma_a_21.png"
image LW_Color_NorRaz_a_03 = "images/sprites/SLW/LW_Norma_a_23.png"
    
#Язык
image LW_Color_NorLeng_a_01 = "images/sprites/SLW/LW_Norma_a_09.png"
    
#Удивлена
image LW_Color_NorUdivlena_a_01 = "images/sprites/SLW/LW_Norma_a_11.png"
    
#стеснается
image LW_Color_NorShyUdivlena_a_01 = "images/sprites/SLW/LW_Norma_a_12.png"
image LW_Color_NorShy_a_01 = "images/sprites/SLW/LW_Norma_a_14.png"
image LW_Color_NorShy_a_02 = "images/sprites/SLW/LW_Norma_a_19.png"
image LW_Color_NorShy_a_03 = "images/sprites/SLW/LW_Norma_a_20.png"
image LW_Color_NorShyEyesOff_a_01 = "images/sprites/SLW/LW_Norma_a_17.png"
image LW_Color_NorShyRaz_a_01 = "images/sprites/SLW/LW_Norma_a_15.png"
image LW_Color_NorShyRaz_a_02 = "images/sprites/SLW/LW_Norma_a_22.png"
image LW_Color_NorShyRaz_a_03 = "images/sprites/SLW/LW_Norma_a_24.png"
image LW_Color_NorShyRazEyesOff_a_01 = "images/sprites/SLW/LW_Norma_a_18.png"
image LW_Color_NorShyHorror_a_01 = "images/sprites/SLW/LW_Norma_a_16.png"
    
# спит
image LW_sl_01 = "images/sprites/SLW/LW_slip_01.png"
    
# C
    
image LW_Color_Norm_c_01 = anim.SMAnimation("ax",
    anim.State ("ax", "images/sprites/SLW/LW_Norma_c_01.png"),
    anim.Edge ("ax", 1.0, "ax", prob=7),
    anim.Edge ("ax", 0.25, "bx"),
    anim.State ("bx", "images/sprites/SLW/LW_Norma_c_02.png"),
    anim.Edge ("bx", 0.25, "cx"),
    anim.State ("cx", "images/sprites/SLW/LW_Norma_c_03.png"),
    anim.Edge ("cx", 0.25, "dx"),
    anim.State ("dx", "images/sprites/SLW/LW_Norma_c_02.png"),
    anim.Edge ("dx", 0.5, "ax")
    ) 



image LW_Color_Nor_c_02 = "images/sprites/SLW/LW_Norma_c_01.png"
image LW_Color_Nor_c_03 = "images/sprites/SLW/LW_Norma_c_02.png"
image LW_Color_Nor_c_04 = "images/sprites/SLW/LW_Norma_c_03.png"
image LW_Color_Nor_c_06 = "images/sprites/SLW/LW_Norma_c_04.png"
    
#наклон головы
image LW_Color_Nor_c_17 = "images/sprites/SLW/LW_Norma_c_16.png"
image LW_Color_Nor_c_18 = "images/sprites/SLW/LW_Norma_c_17.png"
image LW_Color_Nor_c_19 = "images/sprites/SLW/LW_Norma_c_18.png"
image LW_Color_Nor_c_22 = "images/sprites/SLW/LW_Norma_c_21.png"
    
# показывает Язык
image LW_Color_Nor_c_07 = "images/sprites/SLW/LW_Norma_c_06.png"
    
#подозрительная
image LW_Color_Nor_c_08 = "images/sprites/SLW/LW_Norma_c_07.png"
    
# Разговор 
image LW_Color_Nor_c_09 = "images/sprites/SLW/LW_Norma_c_08.png"
    
#закрытие глаза разговор, 
image LW_Color_Nor_c_10 = "images/sprites/SLW/LW_Norma_c_09.png"
image LW_Color_Nor_c_14 = "images/sprites/SLW/LW_Norma_c_13.png"
image LW_Color_Nor_c_15 = "images/sprites/SLW/LW_Norma_c_14.png"
    
#удивленная подозрительная
image LW_Color_Nor_c_11 = "images/sprites/SLW/LW_Norma_c_10.png"

#Хорор удивленная
image LW_Color_Nor_c_12 = "images/sprites/SLW/LW_Norma_c_11.png"
    
# кислая
image LW_Color_Nor_c_13 = "images/sprites/SLW/LW_Norma_c_12.png"
    
# кислая, глаза закрыти
image LW_Color_Nor_c_16 = "images/sprites/SLW/LW_Norma_c_15.png"
    
# поза 02
image LW_Color_Nor_c_05 = "images/sprites/SLW/LW_Norma_c_05.png"
    
#наклон стеснительно-заигрующе
image LW_Color_Nor_c_20 = "images/sprites/SLW/LW_Norma_c_19.png"
image LW_Color_Nor_c_21 = "images/sprites/SLW/LW_Norma_c_20.png"
    
# спина спрайты
image LW_Spin_c_01 = "images/sprites/SLW/LW_Spin_c_01.png"
image LW_Spin_a_01 = "images/sprites/SLW/LW_Spin_a_01.png"
image LW_Spin_c_02 = "images/sprites/SLW/LW_Spin_c_02.png"
      
#image LW_NorBust_c_01 = im.FactorScale("images/sprites/SLW/LW_Norma_c_05.png", 0.15, 0.15)
    
#N обнаженная
image LW_NFM_01:
    "images/sprites/SLW/LW_Nude_Full_01.png"
    zoom 0.2
#im.FactorScale("images/sprites/SLW/LW_Nude_Full_01.png", 0.2, 0.2)
image LW_slip_01 = "images/sprites/SLW/LW_slip_01.png"





#Дракон
image DRC:
    "images/CG/Drakon.png"
    alpha 0.85
    zoom 1.02




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
image Cainic:
    "images/logo/Cainic.png"
    zoom 2.5
image Mil_01:
    "images/logo/Milnii_01.png"
    alpha 0.9
    zoom 1.6

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

image fog_01:
    parallel:
        "images/Logo/fog_01.png" with dissolve
        pause 1.0
        "images/Logo/fog_02.png" with dissolve
        pause 1.0
        "images/Logo/fog_03.png" with dissolve
        pause 1.0
        "images/Logo/fog_04.png" with dissolve
        pause 1.0
        "images/Logo/fog_05.png" with dissolve
        pause 1.0
        "images/Logo/fog_06.png" with dissolve
        pause 1.0
        "images/Logo/fog_07.png" with dissolve
        pause 1.0
        "images/Logo/fog_08.png" with dissolve
        pause 1.0
        "images/Logo/fog_09.png" with dissolve
        pause 1.0
        "images/Logo/fog_11.png" with dissolve
        pause 1.0
        "images/Logo/fog_12.png" with dissolve
        pause 1.0
        "images/Logo/fog_13.png" with dissolve
        pause 1.0
        "images/Logo/fog_14.png" with dissolve
        pause 1.0
        "images/Logo/fog_13.png" with dissolve
        pause 1.0
        "images/Logo/fog_12.png" with dissolve
        pause 1.0
        "images/Logo/fog_11.png" with dissolve
        pause 1.0
        "images/Logo/fog_10.png" with dissolve
        pause 1.0
        "images/Logo/fog_09.png" with dissolve
        pause 1.0
        "images/Logo/fog_08.png" with dissolve
        pause 1.0
        "images/Logo/fog_07.png" with dissolve
        pause 1.0
        "images/Logo/fog_06.png" with dissolve
        pause 1.0
        "images/Logo/fog_05.png" with dissolve
        pause 1.0
        "images/Logo/fog_04.png" with dissolve
        pause 1.0
        "images/Logo/fog_03.png" with dissolve
        pause 1.0
        "images/Logo/fog_02.png" with dissolve
        pause 1.0
        repeat
    parallel:
        alpha 0.7
        ease 0.5 alpha 0.85
        pause 25.0
        ease 0.5 alpha 0.7
        repeat
    parallel:
        matrixcolor BrightnessMatrix(-0.75)
        easein 0.5 matrixcolor BrightnessMatrix(-0.65)
        pause 25.0
        easeout 0.5 matrixcolor BrightnessMatrix(-0.75)
        repeat

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
# анимации природных явлений и прочих эффектов

#анимировать яркость:
transform flash:
    matrixcolor BrightnessMatrix(0.0)
    linear 0.2 matrixcolor BrightnessMatrix(1.0)
    linear 0.2 matrixcolor BrightnessMatrix(0.0)

#Если хочешь, чтобы персонаж мигнул несколько раз:
transform double_flash:
    matrixcolor BrightnessMatrix(0.0)
    linear 0.1 matrixcolor BrightnessMatrix(0.6)
    linear 0.1 matrixcolor BrightnessMatrix(0.0)
    linear 0.1 matrixcolor BrightnessMatrix(0.6)
    linear 0.1 matrixcolor BrightnessMatrix(0.0)

#персонаж получает урон: красная вспышка.
transform damage_flash:
    matrixcolor TintMatrix("#ffffff")
    linear 0.08 matrixcolor TintMatrix("#ff4444")
    linear 0.12 matrixcolor TintMatrix("#ffffff")

#вспышка с яркостью:
transform hit_flash:
    matrixcolor BrightnessMatrix(0.0)
    linear 0.08 matrixcolor BrightnessMatrix(0.8)
    linear 0.15 matrixcolor BrightnessMatrix(0.0)

#для воспоминания
transform memory_effect:
    matrixcolor SepiaMatrix() * BrightnessMatrix(0.1)

#ночной сцены
transform night_effect:
    matrixcolor TintMatrix("#8888cc") * BrightnessMatrix(-0.3)

#Уменьшить контраст:
transform low_contrast:
    matrixcolor ContrastMatrix(0.5)

#контраст
transform high_contrast:
    matrixcolor ContrastMatrix(1.5)

#яркость
transform dark:
    matrixcolor BrightnessMatrix(-0.4)

#хоррора
transform horror_effect:
    matrixcolor SaturationMatrix(0.2) * ContrastMatrix(1.8) * BrightnessMatrix(-0.2)

#насыщенность
transform grayscale:
    matrixcolor SaturationMatrix(0.0)

#Сильно насыщенные цвета:
transform oversaturated:
    matrixcolor SaturationMatrix(2.0)

# психоделический эффект:
transform hue_shift:
    matrixcolor HueMatrix(0)
    linear 1.0 matrixcolor HueMatrix(90)
    linear 1.0 matrixcolor HueMatrix(180)
    linear 1.0 matrixcolor HueMatrix(360)
    repeat

#Анимация резкой инверсии:
transform invert_flash:
    matrixcolor InvertMatrix(0.0)
    linear 0.1 matrixcolor InvertMatrix(1.0)
    linear 0.1 matrixcolor InvertMatrix(0.0)

# сделать персонажа красноватым:
transform red_tint:
    matrixcolor TintMatrix("#ff9999")

#Синий оттенок:
transform blue_tint:
    matrixcolor TintMatrix("#9999ff")

#Зелёный оттенок:
transform green_tint:
    matrixcolor TintMatrix("#99ff99")

#прозрачность
transform half_visible:
    matrixcolor OpacityMatrix(0.5)

#сделать персонажа темнее и чёрно-белым:
transform dark_gray:
    matrixcolor BrightnessMatrix(-0.3) * SaturationMatrix(0.0)

#Красный тёмный эффект:
transform dark_red:
    matrixcolor BrightnessMatrix(-0.2) * TintMatrix("#ff7777")

#Сепия + затемнение:
transform dark_sepia:
    matrixcolor SepiaMatrix() * BrightnessMatrix(-0.2)

#Возврат к обычному виду
transform normal_color:
    matrixcolor IdentityMatrix()

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


image fly1_1 = Transform("images/ani/fly01.png", crop=(0, 0, 20, 20))
image fly1_2 = Transform("images/ani/fly01.png", crop=(20, 0, 20, 20))

image fly2_1 = Transform("images/ani/fly02.png", crop=(0, 0, 20, 20))
image fly2_2 = Transform("images/ani/fly02.png", crop=(20, 0, 20, 20))

image fly3_1 = Transform("images/ani/fly03.png", crop=(0, 0, 20, 20))
image fly3_2 = Transform("images/ani/fly03.png", crop=(20, 0, 20, 20))

image fly4_1 = Transform("images/ani/fly04.png", crop=(0, 0, 20, 20))
image fly4_2 = Transform("images/ani/fly04.png", crop=(20, 0, 20, 20))

image fly1:
    subpixel True
    "fly1_1"
    pause 0.50
    "fly1_2"
    pause 0.50
    repeat

image fly2:
    subpixel True
    "fly2_1"
    pause 0.50
    "fly2_2"
    pause 0.50
    repeat

image fly3:
    subpixel True
    "fly3_1"
    pause 0.50
    "fly3_2"
    pause 0.50
    repeat

image fly4:
    subpixel True
    "fly4_1"
    pause 0.50
    "fly4_2"
    pause 0.50
    repeat

image fly = make_fly_swarm(
    count=38,
    start_spread=5.0,
    border=550
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
    
image starA:
    "images/Ani/5a.png"
    pause 2.0

    "images/Ani/5b.png"
    pause 2.0

    "images/Ani/5c.png"
    pause 2.0

    "images/Ani/5d.png"
    pause 2.0

    "images/Ani/5e.png"
    pause 2.0

    "images/Ani/5f.png"
    pause 2.0

    "images/Ani/5h.png"
    pause 2.0

    repeat

# = Animation(
#    "images/Ani/5a.png", 2.0, 
#    "images/Ani/5b.png", 2.0, 
#    "images/Ani/5c.png", 2.0, 
#    "images/Ani/5d.png", 2.0,
#    "images/Ani/5e.png", 2.0,
#    "images/Ani/5f.png", 2.0, 
#    "images/Ani/5h.png", 2.0
#    )
   
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
define screen_right_03_long = Position(xpos=1500, ypos=50)
define screen_right_03_long_may = Position(xpos=1500, ypos=90)
define screen_left_02 = Position(xpos=100, ypos=500)
define screen_left_03 = Position(xpos=470, ypos=1690)
define screen_Center_02 = Position(xpos=600, ypos=500)  

# переменные для Маленькой Ведьмы на ближный средний и дальный план
define LW_short_range = FactorZoom(1.5, 1.5, 0.0, opaque = False)
define LW_medium_range = FactorZoom(1.0, 1.0, 0.0, opaque = False)
define LW_long_range = FactorZoom(0.5, 0.5, 0.0, opaque = False)

#Для маленькой ведьмы для ч/б спрайтов

define screen_center_short = Position(xpos=950, ypos=2850)
define screen_center_long = Position(xpos=950, ypos=1050)

# переменные для Маленькой Ведьмы на ближный средний и дальный план для других спрайтов
transform LW_short_range_01:
    zoom 1.5

transform LW_medium_range_01:
    zoom 1.0

transform LW_long_range_01:
    zoom 0.5

# переменные для Маленькой Ведьмы для эмодзи

define emo_LW_medium = FactorZoom(1.8, 1.8, 0.0, opaque = False)

#==============================================================================================    
# параметрыческие функции
#==============================================================================================

define loposL = Position(xpos = 170, ypos = 50, xanchor = 0, yanchor = 0)
define loposLD = Position(xpos = 170, ypos = -50, xanchor = 0, yanchor = 0)
define loposLZ = Position(xpos = 190, ypos = 30, xanchor = 0, yanchor = 0)
define loposLX = Position(xpos = 450, ypos = 550, xanchor = 0.5, yanchor = 0.5)
define loposLX_01 = Position(xpos = 350, ypos = 610, xanchor = 0.5, yanchor = 0.5)
define loposR = Position(xpos = 720, ypos = 10, xanchor = 0, yanchor = 0)
define loposRC = Position(xpos = 700, ypos =120, xanchor = 0, yanchor = 0)
define loposRG = Position(xpos = 660, ypos = 10, xanchor = 0, yanchor = 0)
define loposC_LM_long = Position(xpos = 1000, ypos = 145, xanchor = 0.5, yanchor = 0.5)
define loposC_LM_medium = Position(xpos = 1100, ypos = 145, xanchor = 0.5, yanchor = 0.5)
define loposCFull = Position(xpos = 1000, ypos = 100, xanchor = 0.5, yanchor = 0.5)
define loposCA = Position(xpos = 465, ypos = 25, xanchor = 0, yanchor = 0)
define lopoA = Position(xpos = 115, ypos = 370, xanchor = 0, yanchor = 0)
define lopoB = Position(xpos = 145, ypos = 240, xanchor = 0, yanchor = 0)
define lopoC = Position(xpos = 145, ypos = 120, xanchor = 0, yanchor = 0)
define razgavor = FactorZoom(1.0, 1.01, 0.0, opaque = False)
define xijena = FactorZoom(0.0, 0.5, 0.0, opaque = False)
define levelUp = FactorZoom(0.2, 1.0, 1.0, opaque = False)
define posA = Position(xpos = 0.45, ypos = 0.30, xanchor = 0, yanchor = 0)
define lopoD = Position(xpos = 165, ypos = 0, xanchor = 0, yanchor = 0)
define lopoE = Position(xpos = 165, ypos = -180, xanchor = 0, yanchor = 0)
define lopoLeft = Position(xpos = 0, ypos = 180, xanchor = 0, yanchor = 0)
define lopoRight = Position(xpos = 709, ypos = 180, xanchor = 0, yanchor = 0)
define lopo = Position(xpos = 279, ypos = 110, xanchor = 0, yanchor = 0)
define pos_Cainic = Position(xpos = 780, ypos = 770, xanchor = 0.5, yanchor = 0.5)
define pos_cen = Position(xpos = 750, ypos = 360, xanchor = 0.5, yanchor = 0.5)
define zoom_starA = FactorZoom(2.8, 2.0, 0.0, opaque = False)
define zoom_starA_01 = FactorZoom(1.8, 1.5, 0.0, opaque = False)


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
