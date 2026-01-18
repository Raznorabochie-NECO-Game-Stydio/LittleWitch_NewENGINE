label room_007:

    e "....."

    $ Room_07 = True

    if remote_controller == True:
        #block of code to run

        menu :
            #"Say Statement"
            "Включть телевизор":
                #block of code to run

                $ TV_01 = True
                pass
            "не вклучать":
                #block of code to run
                pass
            

        jump hallway_03

    else:
        
        jump hallway_03

    return