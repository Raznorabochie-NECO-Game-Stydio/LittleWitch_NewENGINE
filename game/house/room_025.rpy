label room_025:
    #комната 025, этажа 06
    #Комната где может лежат Key
    #Key_N = True
    #если условия при котором параметр ключа не выставлен, комната так же дольжна быть закрытой
    if Key_04 == False:

        e "....."

        $ Room_25 = True
        jump hallway_06
        pass


    elif Key_01 == True:

        e ",,"


        #
        
        $ Key = True
        $ Room_25 = True

        jump hallway_06
        pass


    return