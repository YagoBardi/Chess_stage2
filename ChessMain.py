"""
This is out main driver file. It will be responsible for handeling user input and displaying
current gamestate object
"""

import pygame as p
import ChessEngine #call the file ChessEngine (not a library)

import random
import warnings

warnings.filterwarnings("ignore")
import time


WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #chessboard are 8x8
SQ_SIZE = HEIGHT // DIMENSION #size of each square
MAX_FPS = 15 #for animations later on
IMAGES = {}
p.init() #initialize pygame (could also be done right at the top)

""" Main_menu() allows the user to select the time of game
"""

def main_menu():
    intro = True
    # create default screen for the user input before the game
    screen_intro,clock = user_input_screens("Who do you want to play?")
    # adjust the default screen for the respective user input that is supposed to be obtained
    human_vs_human = p.Rect(WIDTH/5, (HEIGHT/4), 240, 26)
    human_vs_npc = p.Rect(WIDTH / 5+ 240+50, (HEIGHT / 4), 210, 26)
    quote_text_post = p.Rect(WIDTH / 5 - 70, (HEIGHT) - 40, 100, 100)
    IntroTexts(screen_intro, "Human", human_vs_human, 25, "dark blue",
               option=True)
    IntroTexts(screen_intro, "Computer", human_vs_npc, 25, "dark blue",
               option=True)
    IntroTexts(screen_intro,
               "Its just you and your opponent at the board and you’re trying to prove something - Bobby Fischer",
               quote_text_post, 16, "white")

    while intro:

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()
            # mouse handler
            elif event.type ==p.MOUSEBUTTONDOWN:
                    location =p.mouse.get_pos()
                    # If the user clicked on the normal_chess_option_pos rect.
                    if human_vs_human.collidepoint(location):
                        countdown_selection("Human vs. Human Chess")

                    if human_vs_npc.collidepoint(location):
                        countdown_selection("Human vs. NPC Chess")

        clock.tick(5)
        p.display.flip()


""" countdown_selection() allows the user to select the length of the countdown
"""
def countdown_selection(game_kind):
    countdown_selection_active = True
    screen_intro, clock = user_input_screens("From how many minutes should the countdown start?")
    #set the dimensions
    countdown_len_02 = p.Rect(WIDTH/6, (HEIGHT/4), 80, 26)
    countdown_len_05 = p.Rect(WIDTH / 6+ 100, (HEIGHT / 4), 80, 26)
    countdown_len_10 = p.Rect(WIDTH / 6+ 200, (HEIGHT / 4), 80, 26)
    countdown_len_20 = p.Rect(WIDTH / 6 + 300, (HEIGHT / 4), 80, 26)
    back_to_game_selection= p.Rect(WIDTH / 5 - 50, (HEIGHT) - 40, 100, 100)
    # set the text to be displayed
    IntroTexts(screen_intro, "2 min", countdown_len_02, 25, "dark blue",
               option=True)
    IntroTexts(screen_intro, "5 min", countdown_len_05, 25, "dark blue",
               option=True)
    IntroTexts(screen_intro, "10 min", countdown_len_10, 25, "dark blue",
               option=True)
    IntroTexts(screen_intro, "20 min", countdown_len_20, 25, "dark blue",
               option=True)
    IntroTexts(screen_intro, "\u2190 Back to Game selection", back_to_game_selection, 20,
               "white")

    while countdown_selection_active:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()

            # mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                # If the user clicked on the normal_chess_option_pos rect.
                if countdown_len_02.collidepoint(location):
                    board_selection(game_kind,2)
                if countdown_len_05.collidepoint(location):
                    board_selection(game_kind,5)
                if countdown_len_10.collidepoint(location):
                    board_selection(game_kind,10)
                if countdown_len_20.collidepoint(location):
                    board_selection(game_kind,20)
                if back_to_game_selection.collidepoint(location):
                    main_menu()



        clock.tick(15)
        p.display.flip()

""" board_selection() allows the user to select the type of board
"""
def board_selection(game_kind,countdown_len):
    board_selection_active = True
    screen_intro, clock = user_input_screens("What kind of board would you like?")
    traditional_board = p.Rect(WIDTH/5, (HEIGHT/4), 240, 26)
    soccer_board = p.Rect(WIDTH / 5+ 240+50, (HEIGHT / 4), 210, 26)
    back_to_countdown_selection = p.Rect(WIDTH / 5 - 50, (HEIGHT) - 40, 100, 100)

    IntroTexts(screen_intro, "Traditional Board", traditional_board, 25, "dark blue",
               option=True)
    IntroTexts(screen_intro, "Soccer Board", soccer_board, 25, "dark blue",
               option=True)
    IntroTexts(screen_intro, "\u2190 Back to Countdown Selection", back_to_countdown_selection, 20,
               "white")

    while board_selection_active:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()

            # mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                # If the user clicked on the normal_chess_option_pos rect.
                if traditional_board.collidepoint(location):
                    chess_game(game_kind,"traditional_board",countdown_len)
                if soccer_board.collidepoint(location):
                    chess_game(game_kind,"soccer_board",countdown_len)
                if back_to_countdown_selection.collidepoint(location):
                    countdown_selection(game_kind)

        clock.tick(15)
        p.display.flip()

'''
Initialize a global dictionary of images. This will be called exactly once in the main. 
One nice feature could be the let the user choose the set of pieces.
'''
def loadImages(board_type):
    pieces = ["wp","wR","wN","wB","wK","wQ","bp","bR","bN","bB","bK","bQ"]
    if board_type =="traditional_board":
        file_images = "images_lichess/"
    else:
        file_images ="images_football/"
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(file_images+ piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #note that now we can access an image by saying "IMAGES["wp"], since IMAGE is a dictionary"

'''
The main driver for our code. This will handle user input and updating the graphics
'''

def chess_game(game_kind,board_type,countdown_len):
    countdown_start = countdown_len*60*60
    screen = p.display.set_mode((WIDTH+200, HEIGHT))
    clock = p.time.Clock() #built in pygame
    screen.fill(p.Color("grey"))
    gs = ChessEngine.GameState() #now all the fields within the ChessEngine.py file can be called using gs.
    board = gs.board
    validMoves = gs.getValidMoves() #get initial valid moves
    moveMade = False #flag varable for when a move is made. Until a move is made, we don't want to regenerate the valid
    #moves function
    whiteToMove = 1 #keep track of whose turn it is
    loadImages(board_type) #only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected, keep track of the last click of the user (tuple: (row,col))
    playerClicks = [] #keep track of player clicks (two tuples: [(6,4), (4,4)]) first clicks on (6,4) and
    #later on (4,4) to move the pawn
    gameOver = False


    time_black = countdown_start
    time_white = countdown_start
    start_ticks = p.time.get_ticks()
    stop_clocks = False
    while running:


        milliseconds_past = (p.time.get_ticks() - start_ticks) / 15 #define time relative to each loop and divide by 15
        if not stop_clocks:
            if whiteToMove % 2 == 0: #alternate clock depending on who'e turn it is
                time_black = time_black - milliseconds_past
            else:
                time_white = time_white - milliseconds_past

        timer_visualize(screen, time_black, time_white) #load clock screen
        start_ticks = p.time.get_ticks() #ensure time does not accelerate
        # if time_white/(60*60) <=0: #end game if time runs out
        #     gameOver = True
        #     stop_clocks = True
        #
        # elif time_black/(60*60) <= 0:
        #     gameOver = True
        #     stop_clocks = True



        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            ## The below takes care of AI moves from the black side.
            elif whiteToMove % 2 == 0 and game_kind == "Human vs. NPC Chess" : #When it's blacks turn
                if not gameOver:
                    bestMove = gs.minimax(3, -999999999, 999999999, False) #call the minimax function which returns the best move
                    gs.makeMove(bestMove[1]) #do best move
                    moveMade = True #set to True so we can get the valid moves for white next
                else: #in case we make a check mate to black and we want to go back, we need to include this piece of code
                    if e.type == p.KEYDOWN:
                        if e.key == p.K_z:  # undo when "z" is pressed
                            gs.undoMove()
                            moveMade = True

                            if gameOver:
                                gameOver = False
                            break

                        if e.key == p.K_r:  # reset the board
                            gs = ChessEngine.GameState()
                            validMoves = gs.getValidMoves()
                            sqSelected = ()
                            playerClicks = []
                            whiteToMove = 1
                            moveMade = False
                            if gameOver:
                                gameOver = False
                break
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and p.mouse.get_pos()[0]<WIDTH:
                    bestMove = gs.minimax(1, -999999999, 999999999, True)  # call the minimax function which returns the best move

                    location = p.mouse.get_pos() #(x,y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if sqSelected == (row,col): #this means the user clicked the same square twice
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: #after the second click, we want to make the move
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        ## See that creating the move is pretty inexpensive, we are just creating 4 variables and accessing
                        ## two elements of an array
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                # whiteToMove = whiteToMove + 1
                                animateMove(gs.moveLog[-1], screen, gs.board, clock,board_type)
                                moveMade = True #a move was made, so now go ahead and regenerate the list of valid moves
                                sqSelected = () #reset user clicks
                                playerClicks = []
                        if not moveMade: #this allows to select a new piece and dislect the previous one
                            playerClicks = [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when "z" is pressed
                    gs.undoMove()

                    moveMade = True

                    if gameOver:
                        gameOver = False
                    break

                if e.key == p.K_r: #reset the board
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    if gameOver:
                        gameOver = False
                    stop_clocks = False #restart the clocks
                    time_black = countdown_start
                    time_white = countdown_start
                    start_ticks = p.time.get_ticks()
                    whiteToMove = 1 #reset white's turn


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            whiteToMove = whiteToMove + 1 #counter for AI


        drawGameState(screen, gs, validMoves, sqSelected,board_type)

        if gs.checkMate:
            gameOver = True
            drawText(screen, "Checkmate")
            stop_clocks = True


        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")
            stop_clocks = True

        elif gameOver:
            drawText(screen, "Time out")



        clock.tick(MAX_FPS)
        p.display.flip()



"""
Highlight squares selected and available moves of the piece
"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != (): #ensure the square is not empty
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"): #ensure the piece selected is an ally
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value, 0 is transparent, 250 is solid
            s.fill(p.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

'''
Responsible for all the graphics within a current game state
'''
def drawGameState(screen, gs, validMoves, sqSelected,board_type): #define gamestate method
    drawBoard(screen,board_type) #draw squares on the board
    #add in piece highlighting or move suggestions
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of those squares

'''
Draw the squares on the board
coffee_brown =((200,190,140))
rust = ((210,150,75))
moon_glow = ((235,245,255)),

football pitch:
colors = [p.Color((0, 205, 0, 255)),p.Color((210,150,75))]
'''
def drawBoard(screen,board_type):
    global colors
    if board_type == "traditional_board":
        colors = [p.Color((235, 245, 255)), p.Color((200, 190, 140))]
    else:
        colors = [p.Color((0, 205, 0, 255)), p.Color((0, 255, 0, 255))]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw pieces on board using the current GameState.board
'''
def drawPieces(screen, board):
    #pass: to just see the board
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Animating a move
"""
import warnings
def animateMove(move, screen, board, clock,board_type):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5 #frames to move one square
    frameCount = (abs(dR) + abs(dC))*framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen,board_type)
        drawPieces(screen, board)
        #erase piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 50, True, False)
    textObject = font.render(text, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2) #centre text
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Red"))
    screen.blit(textObject, textLocation.move(2, 2))


#todo all_main_menu_ new function
def user_input_screens(screen_question_text):
    clock = p.time.Clock()
    welcome_text_post = p.Rect(WIDTH / 5 , (HEIGHT/10)-40, 100,100)
    screen_question = p.Rect(WIDTH / 5, (HEIGHT / 8), 100,100)
    bg = p.transform.scale(p.image.load("menu_background2.jpg"), (WIDTH + 200, HEIGHT))
    screen_intro = p.display.set_mode((WIDTH + 200, HEIGHT))
    screen_intro.blit(bg, (0, 0))
    IntroTexts(screen_intro, "Welcome to ChESSEC", welcome_text_post, 32, p.Color((200, 190, 140)))
    IntroTexts(screen_intro, screen_question_text,
               screen_question, 20, "white")
    return screen_intro,clock

def IntroTexts(screen, text,textLocation,fontsize,text_color,option = False):
    if option == True:
        p.draw.rect(screen,color=p.Color("lavender"),rect=textLocation.move(-2,-2))
    font = p.font.SysFont("timesnewromanboldttf", fontsize, True, False)
    textObject = font.render(text, 0, p.Color(text_color))
    screen.blit(textObject, textLocation)




def timer_visualize(screen, time_black,time_white):
    time_black_sec = int(time_black/60)
    time_black = "%d:%02d" % (int(time_black_sec/60),int(time_black_sec%60))
    time_white_sec = int(time_white/60)
    time_white = "%d:%02d" % (int(time_white_sec/(60)),int(time_white_sec%60))
    # timer_chess_black_text = p.Rect(WIDTH + 25, 100, 60, 60)
    # timer_chess_white_text = p.Rect(WIDTH + 25, HEIGHT - 100, 60, 60)
    definition_text = p.Rect(WIDTH + 25, HEIGHT/2, 60, 60)
    # IntroTexts(screen, "Countdown Black", timer_chess_black_text, 18, p.Color("white"))
    # IntroTexts(screen, "Countdown White", timer_chess_white_text, 18, p.Color("white"))
    IntroTexts(screen, "Time left", definition_text, 40, p.Color("black"))
    timer_chess_black = p.Rect(WIDTH + 30, 150, 100, 60)
    timer_chess_white = p.Rect(WIDTH + 30, HEIGHT - 150, 100, 60)
    IntroTexts(screen, time_black, timer_chess_black, 40, p.Color("black"),option=True)
    IntroTexts(screen, time_white, timer_chess_white, 40, p.Color("black"),option=True)


if __name__=="__main__":
    main_menu()
