# ════════════════════════════════════════════════════════════════════
#  ВИТРИНА СПРАЙТА «МАЛЕНЬКАЯ ВЕДЬМА» (SLW VIEWER)
# ────────────────────────────────────────────────────────────────────
#  Интерактивный тестер: перебираешь кнопками любые слоты и сразу
#  видишь результат. Запуск:  jump slw_viewer   (или call slw_viewer)
# ════════════════════════════════════════════════════════════════════

init python:

    # ── Списки доступных вариантов для каждого слота ──────────────
    # Первый элемент во всех списках — None (слой выключен).
    # Где уместно — добавлен "no" (принудительно скрыть).

    SLW_VIEW = {

        "body": [
            "default",
            "bodu_01_left", "bodu_01_left_down", "bodu_01_left_slant",
            "bodu_02_left", "bodu_02_left_slant", "bodu_02_default", "bodu_02_left_down",
            "bodu_03_default", "bodu_03_left_down", "bodu_03_full_face", "bodu_03_left_down_slant",
            "bodu_04_default", "bodu_04_left_down", "bodu_04_full_face", "bodu_04_full_face_slant",
            "bodu_05_default", "bodu_05_full_face", "bodu_05_full_face_slant", "bodu_05_left", "bodu_05_left_down",
            "bodu_06_default", "bodu_06_left", "bodu_06_left_down", "bodu_06_left_slant",
            "bodu_07_default",
            "bodu_08_default", "bodu_08_left", "bodu_08_left_down", "bodu_08_left_slant",
            "bodu_09_default", "bodu_09_left", "bodu_09_left_down", "bodu_09_left_slant",
            "bodu_12_base", "bodu_13_base",
        ],

        "eyes": [
            None, "blink",
            "eyes_norm_01", "eyes_norm_02", "eyes_norm_03", "eyes_norm_04", "eyes_norm_05",
            "eyes_norm_blindfold_01", "eyes_norm_blindfold_02",
            "eyes_norm_blindfold_03", "eyes_norm_blindfold_04",
            "eyes_left_norm_01", "eyes_right_norm_01",
            "eyes_left_norm_he_winks_01", "eyes_right_norm_he_winks_01",
            "eyes_norm_cray_01",
            "eyes_norm_horror_01", "eyes_norm_horror_02",
            "eyes_norm_prizes_01", "eyes_norm_prizes_02",
        ],

        "mouth": [
            None,
            "norm_smail_01", "norm_smail_02", "norm_smail_03", "norm_smail_04",
            "norm_conversation_01", "norm_conversation_02",
            "norm_conversation_03", "norm_conversation_04",
            "norm_surprised_01", "norm_surprised_02",
            "norm_surprised_03", "norm_surprised_04",
            "norm_sour_01", "norm_sour_02", "norm_sour_03",
            "norm_audacious_01", "norm_language_01",
            "default",
        ],

        "brov": [
            None,
            "brov_surprised_01", "brov_gloomy_01", "brov_irritations_01", "brov_sad_01",
            "brov_angry_01", "brov_angry_02", "brov_angry_03",
            "brov_angry_04", "brov_angry_05", "brov_angry_06",
            "default",
        ],

        "freckles": [
            None,
            "norm_01", "norm_02", "norm_03", "norm_04", "norm_05", "norm_06",
            "norm_hatching_01", "norm_blush_01", "default",
        ],

        "cry": [
            None, "cry_01", "cry_02", "cry_03", "cry_04", "default",
        ],

        "hat": [
            None, "hat_01", "hat_02",
        ],

        "panties": [
            None, "no", "panties_white", "panties_black",
        ],

        "pantaloons": [
            None, "pantaloons_long", "pantaloons_short",
        ],

        "top": [
            None, "top_01", "top_02", "top_white", "top_black",
        ],

        "clothes": [
            None, "nightie_01", "dresses_01",
        ],

        "exercise": [
            None, "exercise_01",
        ],

        "carset": [
            None, "Carset_01",
        ],

        "gloves_left": [
            None, "gloves_left_01",
        ],

        "gloves_right": [
            None, "gloves_right_01",
        ],

        "boots_left": [
            None, "boots_left_01",
        ],

        "boots_right": [
            None, "boots_right_01",
        ],
    }

    # Порядок слотов в меню витрины (как их показывать сверху вниз).
    SLW_VIEW_ORDER = [
        "body", "eyes", "mouth", "brov", "freckles", "cry",
        "hat", "boots_left", "boots_right",
        "panties", "pantaloons", "top",
        "clothes", "exercise", "carset",
        "gloves_left", "gloves_right",
    ]

    # ── Переключение значения слота вперёд/назад ───────────────────
    def slw_cycle(slot, step):
        options = SLW_VIEW.get(slot, [None])
        cur = getattr(store.slw, slot, None)
        try:
            idx = options.index(cur)
        except ValueError:
            idx = 0
        idx = (idx + step) % len(options)
        setattr(store.slw, slot, options[idx])
        renpy.restart_interaction()

    # Текстовое представление текущего значения (для подписи).
    def slw_label(slot):
        cur = getattr(store.slw, slot, None)
        if cur is None:
            return "—"
        return str(cur)

    # Циклический перебор силы ветра 0..3.
    def slw_cycle_wind(step):
        store.wind_01 = (getattr(store, "wind_01", 0) + step) % 4
        renpy.restart_interaction()


# ════════════════════════════════════════════════════════════════════
#  Displayable персонажа (если ещё не объявлен в твоём проекте)
#  Если у тебя УЖЕ есть `image little_witch = DynamicDisplayable(build_slw)`,
#  то этот блок можно удалить, чтобы не дублировать.
# ════════════════════════════════════════════════════════════════════
#image little_witch = DynamicDisplayable(build_slw)


# ════════════════════════════════════════════════════════════════════
#  ЭКРАН ВИТРИНЫ
# ════════════════════════════════════════════════════════════════════
screen slw_viewer_screen():

    # Тёмный фон, чтобы спрайт читался.
    add Solid("#222")

    # Сам персонаж — слева, уменьшенный, чтобы влез на экран.
    # CANVAS = 1500x2130, поэтому масштабируем ~0.4.
    add "little_witch":
        xalign 0.0
        yalign 1.0
        xoffset 40
        zoom 0.4

    # Панель управления справа.
    frame:
        xalign 1.0
        yalign 0.0
        xsize 560
        ysize config.screen_height
        background Solid("#000000cc")
        padding (16, 16)

        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                spacing 6

                text "SLW VIEWER — витрина спрайта" size 26 color "#ffd966"
                null height 4

                # Ветер — отдельной строкой.
                hbox:
                    spacing 6
                    textbutton "<" action Function(slw_cycle_wind, -1) xsize 44
                    frame:
                        xsize 320
                        background Solid("#333")
                        padding (8, 6)
                        text "wind_01: [wind_01]" size 20
                    textbutton ">" action Function(slw_cycle_wind, +1) xsize 44

                null height 6

                # Перебор всех слотов.
                for slot in SLW_VIEW_ORDER:
                    hbox:
                        spacing 6
                        textbutton "<" action Function(slw_cycle, slot, -1) xsize 44
                        frame:
                            xsize 320
                            background Solid("#333")
                            padding (8, 6)
                            vbox:
                                text "[slot]" size 16 color "#9fd3ff"
                                text "[slw_label(slot)]" size 18
                        textbutton ">" action Function(slw_cycle, slot, +1) xsize 44

                null height 10

                # Быстрые пресеты.
                text "Быстрые действия:" size 18 color "#ffd966"

                textbutton "Полный комплект (одетая)":
                    action [
                        SetField(slw, "body", "bodu_03_default"),
                        SetField(slw, "eyes", "blink"),
                        SetField(slw, "mouth", "norm_smail_01"),
                        SetField(slw, "brov", "default"),
                        SetField(slw, "hat", "hat_01"),
                        SetField(slw, "panties", "panties_white"),
                        SetField(slw, "top", "top_01"),
                        SetField(slw, "clothes", "dresses_01"),
                        SetField(slw, "boots_left", "boots_left_01"),
                        SetField(slw, "boots_right", "boots_right_01"),
                        Function(renpy.restart_interaction),
                    ]

                textbutton "Только лицо (всё снять)":
                    action [
                        SetField(slw, "hat", None),
                        SetField(slw, "panties", None),
                        SetField(slw, "pantaloons", None),
                        SetField(slw, "top", None),
                        SetField(slw, "clothes", None),
                        SetField(slw, "exercise", None),
                        SetField(slw, "carset", None),
                        SetField(slw, "gloves_left", None),
                        SetField(slw, "gloves_right", None),
                        SetField(slw, "boots_left", None),
                        SetField(slw, "boots_right", None),
                        Function(renpy.restart_interaction),
                    ]

                textbutton "Сбросить ВСЁ (None)":
                    action [
                        SetField(slw, "eyes", None),
                        SetField(slw, "mouth", None),
                        SetField(slw, "brov", None),
                        SetField(slw, "freckles", None),
                        SetField(slw, "cry", None),
                        SetField(slw, "hat", None),
                        SetField(slw, "panties", None),
                        SetField(slw, "pantaloons", None),
                        SetField(slw, "top", None),
                        SetField(slw, "clothes", None),
                        SetField(slw, "exercise", None),
                        SetField(slw, "carset", None),
                        SetField(slw, "gloves_left", None),
                        SetField(slw, "gloves_right", None),
                        SetField(slw, "boots_left", None),
                        SetField(slw, "boots_right", None),
                        Function(renpy.restart_interaction),
                    ]

                null height 10

                # Проверка lip-sync (заставит рот говорить).
                textbutton "Тест речи (lip-sync)":
                    action Return("talk")

                null height 10

                textbutton "ВЫХОД" action Return("exit") text_color "#ff8888"


# ════════════════════════════════════════════════════════════════════
#  LABEL ЗАПУСКА ВИТРИНЫ
# ════════════════════════════════════════════════════════════════════
label slw_viewer:

    # Подготовим персонажа (если ничего не задано — поставим базовое тело).
    $ if slw.body is None: slw.body = "bodu_03_default"
    $ if slw.eyes is None: slw.eyes = "blink"

    show little_witch

label slw_viewer_loop:

    $ _ret = renpy.call_screen("slw_viewer_screen")

    if _ret == "exit":
        hide little_witch
        return

    if _ret == "talk":
        # Персонаж говорит — проверяем lip-sync.
        # Используем готового персонажа LW, объявленного в init
        # (define LW = LipSyncCharacter("Ведьма", callback=slw_say_callback)).
        LW "Привет! Это проверка движения рта во время речи. Раз, два, три, четыре, пять!"
        jump slw_viewer_loop

    jump slw_viewer_loop