label splashscreen:
    scene black 
    $ renpy.pause(1)
    show text "NECO Game Stydio" with dissolve 
    $ renpy.pause(2)
    hide text with dissolve 
    $ renpy.pause(1)
    return

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

screen chapt3_splashscr(line):
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