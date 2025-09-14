init python:

    Neutral = Animation(
        "gui/extra/neut/B01.png", 0.35,
        "gui/extra/neut/B02.png", 0.35,
        "gui/extra/neut/B03.png", 0.35,
        "gui/extra/neut/B04.png", 0.35,
        loop=True
    )
    Left = Animation(
        "gui/extra/left/A01.png", 0.35,
        "gui/extra/left/A02.png", 0.35,
        "gui/extra/left/A03.png", 0.35,
        "gui/extra/left/A04.png", 0.35,
        loop=True
    )
    Right = Animation(
        "gui/extra/right/C01.png", 0.35,
        "gui/extra/right/C02.png", 0.35,
        "gui/extra/right/C03.png", 0.35,
        loop=True
    )
    
screen left_anim():
    zorder 101
    add Left:
        align (0.0, 0.0)
        at transform:
            alpha 0.0
            linear 0.3 alpha 1.0

screen neutral_anim():
    zorder 101
    add Neutral:
        align (0.5, 0.0)
        at transform:
            alpha 0.0
            linear 0.3 alpha 1.0

screen right_anim():
    zorder 101
    add Right:
        align (1.0, 0.0)
        at transform:
            alpha 0.0
            linear 0.3 alpha 1.0

screen extra():
    tag menu
    zorder 100
    add Movie(play="gui/extra/extra3.webm")

    text "{b}{color=#FF0000}ЭТО МЕНЮ ЭКСТРА{/color}{/b}\n{b}{color=#FF0000}И{/color}{/b}\n{b}{color=#FF0000}ОНО ПОКА НЕ ГОТОВО{/color}{/b}\n{b}{color=#FF0000}ЧТОБЫ ВЫЙТИ ИЗ ЭКСТРЫ{/color}{/b}\n{b}{color=#0000FF}НАЖМИ НА ЦЕНТРАЛЬНУЮ ДЕВЧУШКУ{/color}{/b}":
        xalign 0.5
        yalign 0.5
        text_align 0.5
        size 36
        outlines [(2, "#000", 0, 0)]
    
    
    imagebutton:
        idle Null()
        action [Hide("left_anim"), Hide("neutral_anim"), Hide("right_anim"), ShowMenu("music_room")]
        hovered [Show("left_anim"), Hide("neutral_anim"), Hide("right_anim")]
        unhovered Hide("left_anim")
        xpos 0 ypos 0
        xsize 640 ysize 1080
    
    imagebutton:
        idle Null()
        action [Hide("left_anim"), Hide("neutral_anim"), Hide("right_anim"), ShowMenu("main_menu")]
        hovered [Show("neutral_anim"), Hide("left_anim"), Hide("right_anim")]
        unhovered Hide("neutral_anim")
        xpos 640 ypos 0
        xsize 640 ysize 1080
    
    imagebutton:
        idle Null()
        action [Hide("left_anim"), Hide("neutral_anim"), Hide("right_anim"), ShowMenu("gallery")]
        hovered [Show("right_anim"), Hide("left_anim"), Hide("neutral_anim")]
        unhovered Hide("right_anim")
        xpos 1280 ypos 0
        xsize 640 ysize 1080