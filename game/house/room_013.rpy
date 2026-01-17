label room_013:
    #комната 013, этажа 04
    #Комната где может лежат Key
    #Key_N = True
    #если условия при котором параметр ключа не выставлен, комната так же дольжна быть закрытой
    if Key_03 == False:

        e "....."

        $ Room_13 = True
        jump hallway_04
        pass


    elif Key_03 == True:

        e ",,"


        #шахматы
        
        $ Key = True
        $ Room_13 = True

        jump hallway_04
        pass


    return