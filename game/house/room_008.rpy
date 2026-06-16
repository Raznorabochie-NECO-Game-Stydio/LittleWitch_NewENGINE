label room_008:
    #комната 008, этажа 03
    #Комната где может лежат Key
    #Key_N = True
    #если условия при котором параметр ключа не выставлен, комната так же дольжна быть закрытой
    if Key_02 == False:

        e "....."

        $ Room_08 = True
        jump hallway_03
        pass


    elif Key_02 == True:

        e ",,"


        #Загадка Эйнштейна
        
        $ Key = True
        $ Room_08 = True

        jump hallway_03
        pass


    return