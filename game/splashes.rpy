label splashscreen:
    scene black 
    $ renpy.pause(1)
    show text "NECO Game Stydio" with dissolve 
    $ renpy.pause(2)
    hide text with dissolve 
    $ renpy.pause(1)
    return

screen chapter1_splashscr():
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
            
label chapt0_splashscr:
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

label chapter1_splashscr:
    show screen chapter1_splashscr
    with dissolve
    pause 2.0
    hide screen chapter1_splashscr
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