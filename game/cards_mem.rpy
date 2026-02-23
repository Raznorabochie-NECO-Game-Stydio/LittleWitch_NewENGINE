init python:
    # НАСТРОЙКИ ИГРЫ ПО УМОЛЧАНИЮ:

    # набор типов карточек по умолчанию
    all_cards = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'Y']
    # ширина и высота поля
    ww = 3
    hh = 3
    # сколько карточек можно открыть за 1 ход
    max_c = 2
    # размер текста в карточке для текстового режима
    card_size = 48
    # время, выделенное на прохождение
    max_time = 25
    # пауза перед тем, как карточки исчезнут
    wait = 0.5
    # режим карточек с изображениями, а не с иекстом
    img_mode = True

    values_list = []
    temp = []
    # объявляем картинки-карточки
    # должны быть в формате "images/card_*.png"
    # обязательны "card_back.png" и "card_empty.png"
    for fn in renpy.list_files():
        if fn.startswith("images/cardgame/card_") and fn.endswith((".png")):
            name = fn[21:-4]
            renpy.image("card " + name, fn)
            if name != "empty" and name != "back":
                temp.append(str(name))
    # если картинок найдено > 1,
    # то меняем набор типов карточек, но имена файлов
    if len(temp) > 1:
        all_cards = temp
    else:
        # иначе включаем текстовый режим,
        # так как картинок очень мало
        img_mode = False

    # функция инициализации игрового поля
    def cards_init():
        global values_list
        values_list = []
        while len(values_list) + max_c <= ww * hh:
            current_card = renpy.random.choice(all_cards)
            for i in range(0, max_c):
                values_list.append(current_card)
        renpy.random.shuffle(values_list)
        while len(values_list) < ww * hh:
            values_list.append('empty')

# экран игры
screen memo_scr:
    # таймер    
    timer 1.0 action If (memo_timer > 1, SetVariable("memo_timer", memo_timer - 1), Jump("memo_game_lose") ) repeat True
    # поле
    grid ww hh:
        align (.5, .5) # в центре
        for card in cards_list:
            button:
                left_padding 0
                right_padding 0
                top_padding 0
                bottom_padding 0
                background None
                if card["c_value"] == 'empty':
                    if img_mode:
                        add "card empty"
                    else:
                        text " " size card_size
                else:
                    if card["c_chosen"]:
                        if img_mode:
                            add "card " + card["c_value"]
                        else:
                            text card["c_value"] size card_size
                    else:
                        if img_mode:
                            add "card back"
                        else:
                            text "#" size card_size
                # нажатие на кнопку-карточку
                action If ( (card["c_chosen"] or not can_click), None, [SetDict(cards_list[card["c_number"]], "c_chosen", True), Return(card["c_number"]) ] )
    text str(memo_timer) xalign .5 yalign 0.0 size card_size

# сама игра
label memoria_game:
    $ cards_init()
    $ cards_list = []
    python:
        for i in range (0, len(values_list) ):
            if values_list[i] == 'empty':
                cards_list.append ( {"c_number":i, "c_value": values_list[i], "c_chosen":True} )   
            else:
                cards_list.append ( {"c_number":i, "c_value": values_list[i], "c_chosen":False} )   
    $ memo_timer = max_time
    # показать экран с игрой
    show screen memo_scr
    # основной цикл игры
    label memo_game_loop:
        $ can_click = True
        $ turned_cards_numbers = []
        $ turned_cards_values = []
        $ turns_left = max_c
        label turns_loop:
            if turns_left > 0:
                $ result = ui.interact()
                $ memo_timer = memo_timer
                $ turned_cards_numbers.append (cards_list[result]["c_number"])
                $ turned_cards_values.append (cards_list[result]["c_value"])
                $ turns_left -= 1
                jump turns_loop
        # предотвращаем открытие лишних карточек
        $ can_click = False
        if turned_cards_values.count(turned_cards_values[0]) != len(turned_cards_values):
            $ renpy.pause (wait, hard = True)
            python:
                for i in range (0, len(turned_cards_numbers) ):
                    cards_list[turned_cards_numbers[i]]["c_chosen"] = False
        else:
            $ renpy.pause (wait, hard = True)
            python: 
                for i in range (0, len(turned_cards_numbers) ):
                    cards_list[turned_cards_numbers[i]]["c_value"] = 'empty'
                for j in cards_list:
                    if j["c_chosen"] == False:
                        renpy.jump ("memo_game_loop")
                renpy.jump ("memo_game_win")
        jump memo_game_loop

# проигрыш
label memo_game_lose:
    hide screen memo_scr
    $ renpy.pause (0.1, hard = True)
    LW "- Я проиграла..."
    jump memoria_game

# выигрыш
label memo_game_win:
    hide screen memo_scr
    $ renpy.pause (0.1, hard = True)
    LW "- Я победила!"
    $ cards_Key = True
    return

# пример запуска
# label start:
    # scene black
    # $ max_time = 60
    # $ ww, hh = 4, 4
    # call memoria_game
    # return
