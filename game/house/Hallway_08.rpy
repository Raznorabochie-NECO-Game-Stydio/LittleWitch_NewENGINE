label hallway_08:
    menu:
        "Куда пойти?"

        "Обратно, на лестничную площадку":
            
            if enigma_02 == True:
                #block of code to run
            
                jump lest7
                pass

            elif enigma_02 == False:
                #block of code to run

                e "Маленькая Ведьма оказалась в том же самом каридоре..."

                LW "- Я не могу выйти!?."

                jump hallway_08

        "В первую дверь":
            jump door1z
        "Во вторую дверь":
            jump door2z
        "В третью дверь":
            jump door3z
        "В четвёртую дверь":
            jump door4z
        "В пятую дверь":
            jump door5z
        "В шестую дверь":
            jump door6z
            
    return
#ДВЕРКИ