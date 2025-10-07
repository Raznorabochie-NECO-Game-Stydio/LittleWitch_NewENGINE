#ЛЕСТНИЦЫ
label lest1:
    menu:
        "Куда пойти?"
        "Обратно в подъезд":
            jump podezd
            
        "На следующий этаж":
            jump lest2
        
    
    return
    
label lest2:
    menu:
        "Куда пойти?"
        "На этаж ниже":
            jump lest1
            
        "На следующий этаж":
            jump lest3
            
    return

label lest3:
    menu:
        "Куда пойти?"
        "На этаж ниже":
            jump lest2
            
        "На следующий этаж":
            jump lest4
            
    return
    

label lest4:
    menu:
        "Куда пойти?"
        "На этаж ниже":
            jump lest3
            
        "На следующий этаж":
            jump lest5
            
    return

label lest5:
    menu:
        "Куда пойти?"
        "На этаж ниже":
            jump lest4
            
        "На следующий этаж":
            jump lest6
            
    return
    

label lest6:
    menu:
        "Куда пойти?"
        "На этаж ниже":
            jump lest5
            
        "На следующий этаж":
            jump lest7
            
    return    


label lest7:
    menu:
        "Куда пойти?"
        "На этаж ниже":
            jump lest6
            
        "На следующий этаж":
            jump lest8
            
    return
    

label lest8:
    menu:
        "Куда пойти?"
        "На этаж ниже":
            jump lest7

        "В коридор":
            jump kor8
            
        "На крышу":
            jump roof
            
    return
#КРЫША
label roof:
    #menu:
    
    jump suicide
        
    return

label suicide:
    
    return

#КОРИДОРЫ
