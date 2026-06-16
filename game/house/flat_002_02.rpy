label prihojay_001_02:

    menu:
        #"Say Statement"
        "Коридор":
            #block of code to run

            jump hallway_flat_002_01



        "выйти":
            #block of code to run
            jump hallway_02


    return

label hallway_flat_002_01:

    menu:
        #"Say Statement"
        "Шкаф":
            #block of code to run

            e "..."

            jump hallway_flat_002_01

        "Ванная":
            #block of code to run

            e ".."

            jump hallway_flat_002_01

        "туалет":

            e "."

            jump hallway_flat_002_01

        "гостиная":

            e "."

            jump living_room_002_01


        "Кухня":

            e "."

            jump kitchen_flat_002_01

        "Комната 02":

            jump flat_room_002_02

        "обратно":

            jump prihojay_001_02
        

    return

label kitchen_flat_002_01:

    menu:
        #"Say Statement"
        "Комната 01":
            #block of code to run
            #На столе шахматы. 
            #На столе, в столе ящик с ключом, чтобы получит ключ нужно победит в шахматах.

            jump flat_room_002_01

        "обратно":
            #block of code to run

            jump hallway_flat_002_01


        

    
    return

label living_room_002_01:

    e "...."

    menu:
        #"Say Statement"
        "тумбачка":
            #block of code to run

            e "Это был младший аркан таро."

            $ Minor_Arcane_Taro = 2
            call Minor_Arcane

            pass
        "комната":
            #block of code to run
            pass
                

    jump hallway_flat_002_01

    return

label flat_room_002_01:


    e "..."

    if F_Room_002_01 == 0:
        #block of code to run
        $ F_Room_002_01 = F_Room_002_01 + 1

        e "....."

        pass

    elif F_Room_002_01 == 1:
        #block of code to run:
        $ F_Room_002_01 = F_Room_002_01 + 1

        e ".."
        pass

    elif F_Room_002_01 >= 2:
        #block of code to run:
        $ F_Room_002_01 = F_Room_002_01 + 1

        e ".."
        pass


    
    menu:
        
        "осмотреть комнату":

            e "....."

            menu:
                #"Say Statement"
                
                "осмотреть стол":
                    #block of code to run

                    e "На столе была игра."

                    #jump chess_game_01
                    $ max_time = 75
                    $ ww, hh = 6, 5
                    call memoria_game

                    #$ cards_Key = True
                    jump flat_room_002_01

                "осмотреть ящик стола":
                    #block of code to run

                    if Box_002_02_01 == False:
                        #block of code to run

                        $ Box_002_02_01 = True

                        if cards_Key == True:
                            #block of code to run

                            e "///"
                            pass

                        else:

                            e "////"
                            pass

                        if Key == False:
                            #block of code to run

                            menu:
                                #"Say Statement"
                                "взять ключ" if cards_Key == True:
                                    #block of code to run
                                    e ".."
                                    $ Key = True

                                    pass
                                "закрыт ящик":
                                    #block of code to run

                                    e "///"

                                    pass
                        
                        else:
                            #block of code to run
                            

                            e "в ящике не было больше ничего."

                            pass

                    else:
                        #block of code to run

                        if Key == False:

                            menu:
                                #"Say Statement"
                                "взять ключ" if cards_Key == True:
                                    #block of code to run
                                    e ".."
                                    $ Key = True

                                    pass
                                "закрыт ящик":
                                    #block of code to run

                                    e "///"

                                    pass

                        else:
                            #block of code to run
                            

                            e "в ящике не было больше ничего"

                            pass
                        

                    jump flat_room_002_01

        "обратно":

            jump kitchen_flat_002_01
        


    

    #jump kitchen_flat_002_01

    return

label flat_room_002_02:

    e ".."

    jump hallway_flat_002_01


    return
    
    
    


    