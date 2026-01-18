label room_029:
    #комната 029, этажа 07
    #Комната где может лежат Key
    #Key_N = True
    #если условия при котором параметр ключа не выставлен, комната так же дольжна быть закрытой
    if Key_05 == False:

        e "....."

        $ Room_29 = True
        jump hallway_07
        pass


    elif Key_05 == True:

        e ",,"


        #
        
        $ Key = True
        $ Room_29 = True

        jump hallway_07
        pass


    return