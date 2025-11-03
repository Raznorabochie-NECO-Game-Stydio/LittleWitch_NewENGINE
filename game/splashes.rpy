label splashscreen:
    scene black 
    $ renpy.pause(2)
    show text "NECO Game Stydio" with dissolve 
    $ renpy.pause(3)
    hide text with dissolve 
    $ renpy.pause(1)

# стиль строк к главам

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

screen chapter2_splashscr():
    zorder 100
    modal False
    
    vbox:
        align (0.5, 0.5)
        text "Глава 2. Граница Между Сном и Явью":
            size 36
            color "#ff0000"
            bold True
            align (0.5, 0.5)
    
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


# стиль строк к эпиграфам

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

            
label chapt0_splashscr:
    show screen chapt_splashscr("Привет, путник! Ты забрёл в мои туманные сны, ")
    with dissolve
    pause 4.0
    hide screen chapt_splashscr
    with dissolve

    show screen chapt_splashscr("где звёзды шепчут древние тайны.")
    with dissolve
    pause 4.0
    hide screen chapt_splashscr
    with dissolve

    show screen chapt_splashscr(" Расскажи, что привело тебя к Ведьме измерений?")
    with dissolve
    pause 4.0
    hide screen chapt_splashscr
    with dissolve


    show screen chapt_splashscr(" Может, вместе мы разгадаем загадки, скрытые в алых снах.")
    with dissolve
    pause 4.0 # Дольше на последней строке
    hide screen chapt_splashscr
    with dissolve

    
    return

# главы

label chapter_01_splashscr:
    show screen chapter01_splashscr
    with dissolve
    pause 2.0
    hide screen chapter01_splashscr
    with dissolve
    return
    
#label chapt
    
label chapter2_splashscr:
    show screen chapter2_splashscr
    with dissolve
    pause 2.0
    hide screen chapter2_splashscr
    with dissolve
    return

label chapter3_splashscr:
    show screen chapter3_splashscr
    with dissolve
    pause 2.0
    hide screen chapter3_splashscr
    with dissolve
    return


label chapter4_splashscr:
    show screen chapter3_splashscr
    with dissolve
    pause 2.0
    hide screen chapter3_splashscr
    with dissolve
    return


# Эпиграфы


label chapt_01_splashscr:
    show screen chapt_splashscr_01("Ведьма снов и туманных дождей с черных скал. ")
    with dissolve
    pause 5.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Ведьма измерений. Гуляющая сама по себе по фракталу древа миров. Мечтающая когда-нибудь приблизиться к Грани и обрести своё собственное Имя. ")
    with dissolve
    pause 10.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("И собирающая интересные истории. ")
    with dissolve
    pause 4.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Обожающая в жару нагишом купаться в ледяных ручьях, спать под открытым звездным небом и любоваться им.")
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

label chapt_01_1_splashscr:

    show screen chapt_splashscr_01("Кругом-кругом всё кружит карусель,")
    with dissolve
    pause 5.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Кругом-кругом всё быстрей.")
    with dissolve
    pause 5.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Ты без забот приди на наш фестиваль,")
    with dissolve
    pause 5.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Кругом-кругом с ними кружись")
    with dissolve
    pause 5.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Давай-давай, ведь уже все собрались")
    with dissolve
    pause 5.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("Кругом-кругом кружатся все,")
    with dissolve
    pause 5.0
    hide screen chapt_splashscr_01
    with dissolve

    show screen chapt_splashscr_01("В страну фантазий тут все собрались.")
    with dissolve
    pause 5.0
    hide screen chapt_splashscr_01
    with dissolve


    return


label chapt2_splashscr:
    show screen chapt_splashscr
    with dissolve
    pause 2.0
    hide screen chapt_splashscr
    with dissolve
    return

label chapt3_splashscr:
     
    show screen chapt_splashscr("В одиночестве она всегда,")
    with dissolve
    pause 2.0
    hide screen chapt_splashscr
    with dissolve

    show screen chapt_splashscr("В тумане снов своих плывет.")
    with dissolve
    pause 2.0
    hide screen chapt_splashscr
    with dissolve

    show screen chapt_splashscr("И девочки мечта уходит вдаль,")
    with dissolve
    pause 2.0
    hide screen chapt_splashscr
    with dissolve

    show screen chapt_splashscr("В веках живя в симметрии грез.")
    with dissolve
    pause 3.0  # Дольше на последней строке
    hide screen chapt_splashscr
    with dissolve
    
    return

label chapt4_splashscr:
    show screen chapt_splashscr
    with dissolve
    pause 2.0
    hide screen chapt_splashscr
    with dissolve
    return