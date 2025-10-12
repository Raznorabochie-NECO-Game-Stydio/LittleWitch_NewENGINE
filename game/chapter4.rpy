label chapter4:







    menu:
    
        "Налево":
            $ ppoints = 0
            menu:
                "Обойти фонтан.":
                    jump podezd
                "под арку":
                    jump podezd
            
        "Направо":
            $ ppoints =+ 1

label podezd:
    menu:
        "Куда пойти"
        "На выход":
            LW "Дверь закрыта"
            jump podezd
        
        "К почтовому ящику":
            jump letterbox

        "На лестничную площадку":
            jump lest1

    return

label letterbox:

    if key == False:
        jump article
        
    elif key == True:
        jump lest1
        
    return