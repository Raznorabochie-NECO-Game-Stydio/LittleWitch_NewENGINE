# The game starts here.
label chess_game_01:
    # board notation
    $ fen = STARTING_FEN
    $ global_objects['STOCKFISH_ENGINE'] = chess.engine.SimpleEngine.popen_uci(STOCKFISH, startupinfo=STARTUPINFO)

    
    menu:
                

        "Easy":
            $ depth = 2

        "Medium":
            $ depth = 6

        "Hard":
            $ depth = 12

    # $ depth = 12
    
    menu:
        #"Please select Player color"

        "White":
            $ player_color = chess.WHITE # this constant is defined in chess_displayable.rpy 

        "Black":
            # board view flipped so that the player's color is at the bottom of the screen
            $ player_color = chess.BLACK

    window hide
    $ quick_menu = False

    # avoid rolling back and losing chess game state
    $ renpy.block_rollback()

    # disable Esc key menu to prevent the player from saving the game
    $ _game_menu_screen = None

    call screen chess(fen, player_color, depth)

    # re-enable the Esc key menu
    $ _game_menu_screen = 'save'

    # avoid rolling back and entering the chess game again
    $ renpy.block_rollback()

    # restore rollback from this point on
    $ renpy.checkpoint()

    # kill stockfish engine
    $ quit_stockfish()

    $ quick_menu = True
    window show

    if _return == DRAW:
        e "Игра закончилась вничью."
        $ shess_Key = True

    else: # RESIGN or CHECKMATE
        $ winner = "White" if _return == chess.WHITE else "Black"
        e "Победителем становится [winner]."
        if player_color is not None: # PvC
            if _return == player_color:
                e "Поздравляю, игрок!"
                $ shess_Key = True
                e "ключ в ящике"

            else:
                e "В следующий раз тебе повезет больше, игрок."

    #menu:
        #"Would you like to play another game?"

        #"Yes":
            #jump chess_game

        #"No":
            #pass
    
    jump flat_room_002_01

    return
