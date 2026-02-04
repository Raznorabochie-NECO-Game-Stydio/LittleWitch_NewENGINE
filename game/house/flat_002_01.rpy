label hallway_prihojay_001:


    menu:
        #"Say Statement"
        "Второй Коридор":
            #block of code to run

            if hallway_prihojay_002_02 == False:
                #block of code to run
                $ hallway_prihojay_002_02 = True

                e "Девочка, неспешно пошла в противоположную его часть. "
                e "Изучая его.  "
                e "Коридор, упирался в стену так же с окнами, но, похоже, не заканчивался, "
                e "а, по всей видимости, продолжался, заворачивая за угол."
                
                jump hallway_prihojay_002

            else:
                #block of code to run

                e "Девочка прошла в другую часть коридора."

                jump hallway_prihojay_002


        "Комната 01":
            #block of code to run


            jump room_002_01

            pass
        "Комната 02":


            jump room_002_02

            pass


        "Комната 03":


            jump room_002_03

            pass

        "кухня":

            jump room_002_kitchen

            pass

        "Посмотреть в окна":

            jump room_002_Windows

            pass 

        "Выход из квартиры":

            jump hallway_02

    return

label hallway_prihojay_002:

    menu:
        #"Say Statement"
        "туалет":
            #block of code to run


            jump room_002_WC

            pass

        "ванная":


            jump room_002_bathroom    

            pass

        "Комната 04":


            jump room_002_04

            pass

        "Вернутся обратно в коридор-прихожую":
            #block of code to run

            $ replica = renpy.random.choice([1, 2])

            if replica == 1:

                e "Девочка вернулась обратно."

                pass

            if replica == 2:
                #block of code to run

                e "Девочка развернулась и пошла обратно."

                pass

            jump hallway_prihojay_001

            pass
            



    return

label room_002_01:

    if F_room_002_01_01 == 0:
        #block of code to run

        e "..."


        pass

    elif F_room_002_01_01 >= 1:
        #block of code to run

        e "..."

        pass

    $ F_room_002_01_01 = F_room_002_01_01 + 1


    jump hallway_prihojay_001

    return

label room_002_02:

    if F_room_002_02_01 == 0:
        #block of code to run

        e "..."


        pass

    elif F_room_002_02_01 >= 1:
        #block of code to run

        e "..."

        pass

    $ F_room_002_02_01 = F_room_002_02_01 + 1



    jump hallway_prihojay_001

    return

label room_002_03:

    #три варианта использоват написаный генератор СЧ 
    #в варианте 3 самым менее вероятном МВ видит тень. возможен скример 

    if F_room_002_03_01 == 0:
        #block of code to run

        e "..."


        pass

    elif F_room_002_03_01 >= 1:
        #block of code to run

        e "..."

        pass

    $ F_room_002_03_01 = F_room_002_03_01 + 1

    jump hallway_prihojay_001

    return

label room_002_04:

    # На столе стоял компьютер на экране, которого был BSOD

    if F_room_002_04_01 == 0:
        #block of code to run

        e "..."


        pass

    elif F_room_002_04_01 >= 1:
        #block of code to run

        e "..."

        pass

    $ F_room_002_04_01 = F_room_002_04_01 + 1


    jump hallway_prihojay_002

    return

label room_002_kitchen:

    if F_room_002_kitchen_01 == 0:

        e ".."

        pass

    elif F_room_002_kitchen_01 >= 1:

        e "..."

        pass

    $ F_room_002_kitchen_01 = F_room_002_kitchen_01 + 1


    jump hallway_prihojay_001

    return

label room_002_bathroom:

    if F_room_002_bathroom_01 == 0:
        #block of code to run

        e ".."

        pass

    elif F_room_002_bathroom_01 >= 1:
        #block of code to run

        e "..."

        pass

    $ F_room_002_bathroom_01 = F_room_002_bathroom_01 + 1

    jump hallway_prihojay_002
    
    return

label room_002_WC:

    if F_room_002_WC_01 == 0:
        #block of code to run

        e ".."

        pass

    elif F_room_002_WC_01 >= 1:
        #block of code to run

        e "..."

        pass

    $ F_room_002_WC_01 = F_room_002_WC_01 + 1

    jump hallway_prihojay_002
    
    return

label room_002_Windows:

    if F_room_002_Windows_01 == 0:
        #block of code to run

        e "..."

        e "Пейзаж действительно быль странным… "
        e "Не то чтобы пугающим, но определённо не из этого мира. "
        e "За мутноватыми стёклами простирались ландшафты,"
        e " словно вырванные из сновидений: деревья с серебристой листвой, небо, "
        e "переливающееся всеми оттенками фиолетового, и далёкие силуэты, "
        e "напоминающие то ли горы, то ли гигантские статуи. "

        e "Всё это выглядело настолько чуждо и в то же время завораживающе, "
        e "что ведьма на мгновение забыла о своём первоначальном намерении двигаться дальше. "
        e "Она стояла, заворожённая этим зрелищем, и в голове её роились вопросы:"

        LW "Что это? "
        LW "Как оно связано с тем, куда я направляюсь? "
        LW "И что ждёт меня за следующей дверью?"

        pass

    elif F_room_002_Windows_01 >= 1:
        #block of code to run

        e ".."

        pass

    $ F_room_002_Windows_01 = F_room_002_Windows_01 + 1

    jump hallway_prihojay_001
    
    return
    
    
    
    