label room_002:
    #комната 002, этажа 02
    #Комната где может лежат Key
    #Key_N = True
    #если условия при котором параметр ключа не выставлен, комната так же дольжна быть закрытой
    if Key_01 == False:

        e "....."

        $ Room_02 = True
        jump hallway_02
        pass


    elif Key_01 == True:

        e ",,"


        #
        
        $ Key = True
        $ Room_02 = True

        jump hallway_02
        pass


    return