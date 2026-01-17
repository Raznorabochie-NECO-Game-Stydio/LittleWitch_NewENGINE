label hallway_05:

    if hallway_005 == False:

        e "Там был коридор с дверьми, "
        e " он казалась каким-то пустым и совершенно заброшенным. "
        e "Длинный коридор, с высоким потолком,"
        e "все двери в нём были закрыты, а следы внезапно обрывались. "

        Ananim "- Проснись... Пробудись ото сна…"

        e "Послышалась девочки из глубины коридора."

        $ hallway_005 = True

        pass

    else:

        pass

    jump coridor_05
    return

label coridor_05:
    #Коридор

    e "Девочка пробовала открывать двери по очереди, авось какая из них и отворится. "

    menu:
        "Куда пойти?"
        "Обратно, на лестничную площадку":
            jump lest5
        "В первую дверь":
            jump door_016
        "Во вторую дверь":
            jump door_017
        "В третью дверь":
            jump door_018
        "В четвёртую дверь":
            jump door_019
        "В пятую дверь":
            jump door_020
        "В шестую дверь":
            jump door_021


    return

label door_016:

    return

label door_017:

    return

label door_018:

    return

label door_019:

    return

label door_020:

    return

label door_021:

    return
    