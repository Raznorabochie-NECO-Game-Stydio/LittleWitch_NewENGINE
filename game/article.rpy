label article:
    menu(nvl = True):
        "Статья 1":

            e "1"
            jump article1
            
        "Статья 2":

            e "2"
            jump article2
            
        "Статья 3":

            e "3"
            jump article3
            
        "Статья 4":

            e "4"
            jump article4
            
        "Статья 5":

            e "5"
            jump article5
            
        "Статья 6":

            $ Key = True

            $ ran_dig = renpy.random.choice([1,6])

            if ran_dig == 1:
                #block of code to run

                $ Key_01 = True

                pass

            elif ran_dig == 2:
                #block of code to run

                $ Key_02 = True

                pass

            elif ran_dig == 3:
                #block of code to run

                $ Key_03 = True

                pass

            elif ran_dig == 4:
                #block of code to run

                $ Key_04 = True

                pass

            elif ran_dig == 5:
                #block of code to run

                $ Key_05 = True

                pass

            elif ran_dig == 6:
                #block of code to run

                $ Key_06 = True

                pass

            e "6"
            jump article6
            
        "Статья 7":

            e "7"
            jump article7
            
        "Статья 8":

            e "8"
            jump article8
            
        "Статья 9":

            e "9"
            jump article9
            
        "Статья 10":

            e "10"
            jump article10
            
        "Статья 11":

            e "11"
            jump article11

        "Выход":
            jump podezd
            
    return
    
label article1:
    
    jump article
    
    return
    
label article2:
    
    jump article
    
    return
    
label article3:
    
    jump article
    
    return
    
label article4:
    
    jump article
    
    return
    
label article5:
    
    jump article
    
    return
    
label article6:

    

    
    jump article
    
    return
    
label article7:
    
    jump article
    
    return
    
label article8:
    
    jump article
    
    return
    
label article9:
    
    jump article
    
    return
    
label article10:
    
    jump article
    
    return
    
label article11:
    
    jump article
    
    return