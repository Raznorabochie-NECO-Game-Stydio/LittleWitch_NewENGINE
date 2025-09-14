init python:
    mr = MusicRoom(fadeout=1.0)
    
    mr.add("")
    mr.add("")
    mr.add("")

screen music_room():
    
    tag menu
    
    add Movie(play="gui/main_menu/main_menu.webm")
    frame:
        has vbox
        
        textbutton "Track 1" action mr.Play("")
        textbutton "Track 2" action mr.Play("")
        textbutton "Track 3" action mr.Play("")
                
        null height 20
        
        textbutton "Next" action mr.Next()
        textbutton "Previous" action mr.Previous()
        
        null height 20
        
        textbutton "Main Menu" action ShowMenu("main_menu")