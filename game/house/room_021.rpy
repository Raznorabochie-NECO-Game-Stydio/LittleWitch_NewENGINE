label room_021:
    #Комната с консолью
    #Комната игры
    window hide
    if WCRoom_01 == False:

        e "....."
        e "Ведьмочка очутилась в комнате,"
        e "в которой царила полутьма, "
        e "и единственным источником света служила панель, "
        e "воспроизводящая некий логотип и надпись."
        e "В комнате был стул,"
        e "а рядом с ним непонятная коробка с моргающей индикацией."
        menu:
        
            "Осмотреть коробку":

                e "Маленькая ведьма осмотрела коробку. "
                e "На ней была выгравирована гласящая надпись «PS8»." 
                e "Рядом с коробкой лежала небольшая книжечка, "
                e "её глянцевые страницы покрывали красочные рисунки. "
                e "Устройство носила полное название {i}«PS8 – Квантовая игровая приставка»{/i}"
                e "Из инструкции к устройству маленькая ведьма поняла,"
                e "что это странное устройства предназначено для игр."

                jump demo_minigame_pong
                pass

            "Выйти из комнаты.":

                LW "- Мне не интересно тут находиться"

                e "Маленькая ведьма вышла в коридор."
                
                #$ Room_21 = True
                pass
        jump coridor_05

    else:
        #block of code to run
        LW "{i} - Здесь я уже была…{/i}"
        LW "{i} - И почему я снова зашла!?.{/i}"
        LW "{i}- …но все же коробка странная…{/i}"

        e "Маленькая ведьма выскочила в коридор."
        $ Room_21 = True

        jump coridor_05

    return

label demo_minigame_pong:

    scene bg pong field
    with pixellate

    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)
    

    if winner == "IA":

        scene bg0000 with diss
        
        #show LW n at left onlayer demo with dissolve
        #show LW s04 at left onlayer demo with dissolve
        #show C at loposL onlayer dexm
        
        #voice "Voise/LW/p_30054683_686.mp3"
        LW "{i}- Какая странная игра!{/i}"
        
        #hide C onlayer dexm
        #show LW s06 at left onlayer demo with dissolve
        #show D at loposL onlayer dexm
        
        #voice "Voise/LW/p_30054707_747.mp3"
        LW "{i}- Похоже, в нее не возможно выиграть!{/i}"
        
        #hide D onlayer dexm
        #show LW rn at left onlayer demo with dissolve
        #show GI at loposL onlayer dexm
        
        #voice "Voise/LW/p_30054762_837.mp3"
        LW "- Этот ИИ довольно серьезный противник."
        
        #hide GI onlayer dexm
        #show S02 at loposL onlayer dexm
        
        #voice "Voise/LW/p_30054802_909.mp3"
        LW "- И, похоже мне тут, не зачем больше оставаться."
        
        #hide S02 onlayer dexm
        #hide LW rn onlayer demo
        #show LW n at Transform(function=move_rotate_zoom) onlayer demo
        #scene bg000b with diss
        
        e "Маленькая ведьма вышла в коридор."

        $ WCRoom_01 = True

        pass
        
    else:
        
        scene bg0000 with diss
        #show LW r at Motion(Trampoline, 5.0, repeat=True, bounce=True)
        #show VP at loposC onlayer dexm
        
        #voice "Voise/LW/p_30054836_997.mp3"
        LW "- Я выиграла!"
        
        #hide VP onlayer dexm
        #show LW n at left with move
        #hide LW n
        #show LW rn at left onlayer demo
        
        #voice "Voise/LW/p_30054847_57.mp3"
        LW "- Столько мощностей затрачивается на такую простенькую игру!"
        
        #hide LW rn onlayer demo
        #show LW n at Transform(function=move_rotate_zoom)
        #scene bg0000 with diss
        $ WCRoom = True
        $ WCRoom_01 = True
        
        e "Маленькая ведьма вышла в коридор."

        pass
        
    #$ Room_21 = True
    

    jump coridor_05

    return