label room_031:
    #Комната которая возвращает сама себя создавая иллюзию 

    # бесконечных комнат. если идти вперед то сшетчик 

    # увеличивается на единицу.

    # Room_infiniti =+ 1

    #если идти назад уменщается

    # Room_infiniti =- 1

    #достигнув 0 только тогда можно покинут комнату


    e "....."

    
    
    $ Room_infiniti += 1

    jump nfiniti_00

    return

label nfiniti_00:
    

    if Room_infiniti == 0:

        menu:
            #"Say Statement"
            "Вернуться":
                #block of code to run
                $ Room_31 = True


                jump hallway_07

            "Вперет":
                #block of code to run

                $ Room_infiniti += 1

                jump nfiniti_00
            

    elif Room_infiniti >= 1:

        menu:
            #"Say Statement"
            "Вернуться":
                #block of code to run

                $ Room_infiniti -= 1

                e "..."
                e "[Room_infiniti]"

                jump nfiniti_00

            "Вперет":
                #block of code to run

                $ Room_infiniti += 1

                e "..."
                e "[Room_infiniti]"

                jump nfiniti_00

    jump hallway_07

    return