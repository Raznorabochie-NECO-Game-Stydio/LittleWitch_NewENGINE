label room_037:
    #комната 037, этажа 08
    #Комната где может лежат Key
    #Key_N = True
    #если условия при котором параметр ключа не выставлен, комната так же дольжна быть закрытой
    if Key_06 == False:

        e "....."

        $ Room_37 = True
        jump hallway_08
        pass


    elif Key_01 == True:

        e ",,"


        #
        
        $ Key = True
        $ Room_37 = True

        jump hallway_08
        pass
