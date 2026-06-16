label room_003:

    #Псевдо закрытая комната.
    #доступ, которой может быть 
    #получен с помощью фомки.

    #В этой квартире лежит ключ от 
    #квартиры где лежат батарейки
 
    #

    e "....."

    if Room_03 == False:

        $ Room_03 = True

        pass

    else:
        #block of code to run

        e "Она снова оказалась в прихожей."

        pass

    jump hallway_flat_003_01

    return

label hallway_flat_003_01:

    menu:
        #"Say Statement"
        "Санузел":
            #block of code to run
            #Помещения в крови, в унитазе лежит человеческий эмбрион (выкидыш),
            #в шкафчики много сильных лекарств. 
            #Есть следы и некоторых запрещенных веществ. 

            jump room_003_bathroom

        "Кухня":
            #block of code to run
            #На шкафчике лежит ключ и записка, в которой хозяев просят присмотреть за квартирой (N на этаже N)

            jump room_003_kitchen

        "Комната 01":

            menu:
                #"Say Statement"
                "карта таро":
                    #block of code to run

                    e "Это был младший аркан таро."

                    $ Minor_Arcane_Taro = 3
                    call Minor_Arcane

                    pass
                "комната":
                    #block of code to run

                    pass
                

            jump room_003_01

        "Гостиная":
            #О девушке, ее бывшем парне, беременности, и аборте, которая совершила сама девушка, 
            #эмбриона она выкинула или в туалет или в мусорное ведро. 
            #Написать с намеками, но чтоб считывалась. Местами натурестично.

            jump room_003_iving

        "выйти из...":
        

            jump hallway_02

    return

label room_003_bathroom:




    jump hallway_flat_003_01

    return

label room_003_kitchen:

    menu:

        "Осмотреть стол":


            pass

        "Осмотреть шкафчик":

            $ Key_flat_01 = True

            e "...."

            pass

        "Осмотреться":

            pass
        
        "обратно":

            pass


    jump hallway_flat_003_01

    return

label room_003_01:

    jump hallway_flat_003_01

    return

label room_003_iving:


    jump hallway_flat_003_01

    return
    
    
    