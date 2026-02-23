label room_040:

    e "....."

    $ Room_40 = True

    menu:
        #"Say Statement"
        "Нет. вернуться в коридор":
            #block of code to run
            $ ppoints = ppoints + 1

            jump hallway_06_5


        "Да, перейти границу окна":
            #block of code to run
        

            jump additional_history

    return