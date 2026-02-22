label splashscreen:
    # MOKOt
    scene start_splash 
    $ renpy.pause(1.5)
    show text "{=typewr}{color=#909090}{size=65}NECO Game Stydio{/size}{/color}{/}" with Dissolve(1.5)
    $ renpy.pause(3)
    hide text with dissolve 
    $ renpy.pause(0.56)
    
    jump chapt0_splashscr

    return

# стиль строк к главам
#Первая

screen chapter01_splashscr():
    zorder 100
    modal False
    
    vbox:
        align (0.5, 0.5)
        text "Глава 01. Сон Страны Грёз":
            size 36 
            color "#ff0000"
            bold True
            align (0.5, 0.5)

#Вторая

screen chapter2_splashscr():
    zorder 100
    modal False
    
    vbox:
        align (0.5, 0.5)
        text "Глава 02. Граница Между Сном и Явью":
            size 36
            color "#ff0000"
            bold True
            align (0.5, 0.5)

#третья
    
screen chapter3_splashscr():
    zorder 100
    modal False
    
    vbox:
        align (0.5, 0.5)
        text "Глава 03. Иллюзорная Бесконечная Ночь и Фантастическая Женщина":
            size 36
            color "#ff0000"
            bold True
            align (0.5, 0.5)

#Четвертая

screen chapter4_splashscr():
    zorder 100
    modal False
    
    vbox:
        align (0.5, 0.5)
        text "Глава 04. Иллюзорный Город Куклы":
            size 36
            color "#ff0000"
            bold True
            align (0.5, 0.5)


# стиль строк к эпиграфам


screen chapt_splashscr(line):
    zorder 100
    modal False
    frame:
        background None
        xalign 0.5
        yalign 0.5
        text line:
            size 28
            color "#7fbdbf"
            italic True
            text_align 0.5


# стиль строк к эпиграфам доп.

screen chapt_splashscr_01(line):
    zorder 100
    modal False
    frame:
        background None
        xalign 0.5
        yalign 0.5
        text line:
            size 28
            color "#d16f6a"
            italic True
            text_align 0.5


# эпиграф заставки игры
# text_font = "GOST_A.ttf"

label chapt0_splashscr:
    show screen chapt_splashscr("{font=fonts/CeltesSP2.otf}{size=65}Привет, путник!{/size}{/font}")
    with dissolve
    pause 4.0
    hide screen chapt_splashscr
    with dissolve

    show screen chapt_splashscr("{font=fonts/CeltesSP2.otf}{size=60}Ты забрёл в мои туманные сны, где звёзды шепчут древние тайны.{/size}{/font}")
    with dissolve
    pause 4.0
    hide screen chapt_splashscr
    with dissolve

    show screen chapt_splashscr("{font=fonts/CeltesSP2.otf}{size=65}Расскажи, что привело тебя к Ведьме измерений?{/size}{/font}")
    with dissolve
    pause 4.0
    hide screen chapt_splashscr
    with dissolve

    show screen chapt_splashscr("{font=fonts/CeltesSP2.otf}{size=65}Может, вместе мы разгадаем загадки, скрытые в алых снах.{/size}{/font}")
    with dissolve
    pause 4.0 # Дольше на последней строке
    hide screen chapt_splashscr
    with dissolve
    
    return

# главы
# Первая глава

label chapter_01_splashscr:
    show screen chapter01_splashscr
    with dissolve
    pause 2.0
    hide screen chapter01_splashscr
    with dissolve
    return
    
#label chapt
#Вторая глава
    
label chapter_02_splashscr:
    show screen chapter2_splashscr
    with dissolve
    pause 2.0
    hide screen chapter2_splashscr
    with dissolve
    return

#Третья глава

label chapter_03_splashscr:
    show screen chapter3_splashscr
    with dissolve
    pause 2.0
    hide screen chapter3_splashscr
    with dissolve
    return

#Четвертая глава

label chapter_04_splashscr:
    show screen chapter4_splashscr
    with dissolve
    pause 2.0
    hide screen chapter4_splashscr
    with dissolve
    return


# Эпиграфы

# Эпиграф первой главы

label chapt_01_splashscr:
    show screen chapt_splashscr_01("Ведьма снов и туманных дождей с черных скал. ")
    with dissolve
    pause 5.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Ведьма измерений. Гуляющая сама по себе по фракталу древа миров.\n Мечтающая когда-нибудь приблизиться к Грани и обрести своё собственное Имя. ")
    with dissolve
    pause 10.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("И собирающая интересные истории. ")
    with dissolve
    pause 4.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Обожающая в жару нагишом купаться в ледяных ручьях,\n спать под открытым звездным небом и любоваться им.")
    with dissolve
    pause 6.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Она любит зиму и восхищается ветром.")
    with dissolve
    pause 4.0
    hide screen chapt_splashscr_01
    with dissolve


    return

#Эпиграф первой главы доп.

label chapt_01_1_splashscr:

    show screen chapt_splashscr_01("Кругом-кругом всё кружит карусель,\n Кругом-кругом всё быстрей\n Ты без забот приди на наш фестиваль,")
    with dissolve
    pause 8.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Кругом-кругом с ними кружись\n Давай-давай, ведь уже все собрались\n Кругом-кругом кружатся все,\n В страну фантазий тут все собрались.")
    with dissolve
    pause 8.0
    hide screen chapt_splashscr_01
    with dissolve

    return

#Эпиграф первой главы доп.

label chapt_01_2_splashscr:

    show screen chapt_splashscr_01("Когда вечности суть я познала сама,\n Я тебя здесь уже найти не смогла,\n В тумане снов своих плывёт\n Ярких звёзд водоворот.\n Сон единый я создам, о цветах в серебряной ночи,\n Как тени этого яркого мира засыпают вечным сном.")
    with dissolve
    pause 10.0
    hide screen chapt_splashscr_01
    with dissolve

    return

# Эпиграф второй главы

label chapt_02_splashscr:
    show screen chapt_splashscr("А на утро выпал снег.\n В моем саду уж не цветет сирен\n В иллюзиях и в мечтаний\n Девочка бродит одна по миру снегов и льда.")
    with dissolve
    pause 8.0
    hide screen chapt_splashscr
    with dissolve

    return

#Эпиграф третьей главы

label chapt_03_splashscr:
     
    show screen chapt_splashscr("В одиночестве она всегда,\n В тумане снов своих плывет.\n И девочки мечта уходит вдаль,\n В веках живя в симметрии грез.")
    with dissolve
    pause 8.0
    hide screen chapt_splashscr
    with dissolve

    return

#Эпиграф четвертой главы

label chapt_04_splashscr:
    show screen chapt_splashscr("Круг единый создав, будут сотни в нём цветов.\n Кружится, кружится платья воздушный подол.\n В такт движениям танца он плавно парит над цветами.\n Цветочный фестиваль иллюзорного мира.")
    with dissolve
    pause 8.0
    hide screen chapt_splashscr
    with dissolve

    return