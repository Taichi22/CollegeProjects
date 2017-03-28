import cards        # this is required
import re
import copy
"""
Author: Brian Cong
Unfinished version. Unimplemented are:
Victory
Waste-to-tableau
Stock-to-waste
Restart
"""

YAY_BANNER = """
__   __             __        ___                       _ _ _ 
\ \ / /_ _ _   _    \ \      / (_)_ __  _ __   ___ _ __| | | |
 \ V / _` | | | |    \ \ /\ / /| | '_ \| '_ \ / _ \ '__| | | |
  | | (_| | |_| |_    \ V  V / | | | | | | | |  __/ |  |_|_|_|
  |_|\__,_|\__, ( )    \_/\_/  |_|_| |_|_| |_|\___|_|  (_|_|_)
           |___/|/                                            

"""

RULES = """
    *------------------------------------------------------*
    *-------------* Thumb and Pouch Solitaire *------------*
    *------------------------------------------------------*
    Foundation: Columns are numbered 1, 2, ..., 4; built 
                up by rank and by suit from Ace to King. 
                You can't move any card from foundation, 
                you can just put in.

    Tableau:    Columns are numbered 1, 2, 3, ..., 7; built 
                down by rank only, but cards can't be laid on 
                one another if they are from the same suit. 
                You can move one or more faced-up cards from 
                one tableau to another. An empty spot can be 
                filled with any card(s) from any tableau or 
                the top card from the waste.
     
     To win, all cards must be in the Foundation.
"""

MENU = """
Game commands:
    TF x y     Move card from Tableau column x to Foundation y.
    TT x y n   Move pile of length n >= 1 from Tableau column x 
                to Tableau column y.
    WF x       Move the top card from the waste to Foundation x                
    WT x       Move the top card from the waste to Tableau column x        
    SW         Draw one card from Stock to Waste
    R          Restart the game with a re-shuffle.
    H          Display this menu of choices
    Q          Quit the game
"""

def valid_fnd_move(src_card, dest_card):
    """
    If foundation move is valid, return true, else false.
    """
    vd = True
    if src_card.suit() != dest_card.suit():
        vd = False
        print("Invalid suit,", src_card.suit(), "---> ", dest_card.suit())
    return vd
    if src_card.rank() != (dest_card.rank()+1):
        vd = False
        print("Invalid rank,", src_card.rank(), "---> ", dest_card.rank())
    return vd

def valid_tab_move(src_card, dest_card):
    """
    If the tableau move is valid, return true, else false.
    """
    vd = True
    if src_card.suit() == dest_card.suit():
        vd = False
        print("Invalid suit,", src_card.suit(), "---> ", dest_card.suit())
        #print(src_card)
    if src_card.rank() != (dest_card.rank()-1):
        vd = False
        print("Invalid rank,", src_card.rank(), "---> ", dest_card.rank())
    return vd

def tableau_to_foundation(tab, fnd):
    """
        Check for validity, then move card from tableau to foundation.
    """    
    if tab[-1].rank() != 1: 
        if fnd:
            if valid_fnd_move(tab[-1], fnd[-1]):
                fnd.append(tab.pop())
        else:
            print("Invalid move.")
    else:
        fnd.append(tab.pop())
    return True

def tableau_to_tableau(tab1, tab2, n):
    """
        Check for validity, then move card from tableau to tableau
    """    
    if tab2:
        if valid_tab_move(tab1[-n], tab2[-1]):
            for x in range(len(tab1[-n:])):
                #DEBUG print(tab1[-n:])
                tab2.append(tab1[-n + x])
            del tab1[-n:]
    else:
        for x in range(len(tab1[-n:])):
                #DEBUG print(tab1[-n:])
                tab2.append(tab1[-n + x])
        del tab1[-n:]
            
def waste_to_foundation(waste, fnd, stock):
    """
        Check for validity, then move card from waste to foundation.
    """    
    worked = False
    if len(fnd) != 0:
        if valid_fnd_move(waste[-1],fnd[-1]):
            fnd.append(waste[-1])
            del waste[-1]
            worked = True
    else:
        if waste[-1].rank() == 1:
            fnd.append(waste[-1])
            del waste[-1]
            worked = True
        else:
            print("Invalid move.")
            worked = False
    return worked
def waste_to_tableau(waste, tab, stock):
    """
        Check for validity, then move card from waste to tableau
    """    
    worked = False
    if tab:
        if valid_tab_move(waste[-1], tab[-1]):
            tab.append(waste[-1])
            del waste[-1]
            worked = True
    else:
        tab.append(waste[-1])
        del waste[-1]
        worked = True
    return worked
    
def stock_to_waste(stock, waste):
    """
        Pop card from stock to waste
    """    
    waste.append(stock.deal())
    if stock.is_empty():
        print("Empty")
        #print(waste)
        stock = copy.deepcopy(waste)
        waste.clear()
        waste.append(stock[-1])
        del stock[-1]
                            
def is_winner(foundation):
    """
        Print winning lines and check
    """    
    winvar = True
    for pile in range(len(foundation)):
        if foundation[pile]:
            #print(foundation[pile][-1])
            if foundation[pile][-1].rank() != 13:
                winvar = False
        if not foundation[pile]:
            winvar = False
    if winvar == True:
        print("You've won! Congradulations!")
        #print("Press \"R\" to restart!")
    return winvar

def setup_game():
    """
        The game setup function, it has 4 foundation piles, 7 tableau piles, 
        1 stock and 1 waste pile. All of them are currently empty. This 
        function populates the tableau and the stock pile from a standard 
        card deck. 

        7 Tableau: There will be one card in the first pile, two cards in the 
        second, three in the third, and so on. The top card in each pile is 
        dealt face up, all others are face down. Total 28 cards.

        Stock: All the cards left on the deck (52 - 28 = 24 cards) will go 
        into the stock pile. 

        Waste: Initially, the top card from the stock will be moved into the 
        waste for play. Therefore, the waste will have 1 card and the stock 
        will be left with 23 cards at the initial set-up.

        This function will return a tuple: (foundation, tableau, stock, waste)
    """
    # you must use this deck for the entire game.
    # the stock works best as a 'deck' so initialize it as a 'deck'
    stock = cards.Deck()
    stock.shuffle()
    # the game piles are here, you must use these.
    foundation = [[], [], [], []]           # list of 4 lists
    tableau = [[], [], [], [], [], [], []]  # list of 7 lists
    waste = []                              # one list
    mxlen = 0
    # Per pile, append shuffled cards, flip cards based upon index mxlen
    for pile in range(len(tableau)):
        for x in range(pile + 1):
            tableau[pile].append(stock.deal())
            if len(tableau[pile]) <= mxlen:
                tableau[pile][x].flip_card()
        mxlen += 1
    waste.append("")
    #waste.append(stock.deal())
    return foundation, tableau, stock, waste




def display_game(foundation, tableau, stock, waste):
    """
        Dislay values of tableau, foundation, stock, and waste.
        Use formatting .format function
    """    
    print("     ==================== FOUNDATIONS ==================")
    print("     f1        f2        f3        f4")
    print("     {}        {}        {}        {}".format(foundation[0][-1:],foundation[1][-1:], foundation[2][-1:], foundation[3][-1:]))
    print("     ====================== TABLEAU ====================")
    print("     t1      t2      t3      t4      t5      t6      t7")

    print("     ", end = "")
    for line in range(0, len(max(tableau,key=len))+1):
        count = 0
        for ts in tableau:
            count += 1
            if len(ts) > line:
                print("{:8.3}".format(str(ts[line])), end = "")
            else:
                print("        ", end = "")
            if ((count == 7) and (line < len(max(tableau,key=len)))) :
                print()
                print("     ", end = "")
    print()
    print("     ==================== STOCK/WASTE ===================")
    print("     Stock #({}) --> [{}]".format(len(stock), waste[-1].__str__()))
    #DEBUG print(stock)
    #DEBUG print(waste)



#Functioning code.
"""
Check command statement and adjust gamestate accordingly
After checking command, check for gamestate of finished game.
"""
print(RULES)
fnd, tab, stock, waste = setup_game()
display_game(fnd, tab, stock, waste)
print(MENU)
command = input("prompt :> ")
winvar = False
while (command.strip().lower() != 'q') or (winvar == True):
    try:
        if command.startswith("t"):
            #regex parse for given format (whitespace, digit){1,3}
            pattern = re.compile("((\s\d){1,3})")
            #set a matchedobject to matched
            matched = pattern.search(command)
            #if matchedobject contains value it is set to true
            if matched:
                #split by whitespace
                vals = matched.group(0).split()
                if len(vals) == 2:
                    #set list indicies to be passed
                    tbx = tab[int(vals[0]) - 1]
                    fdy = fnd[int(vals[1]) - 1]
                    try:                        
                        tableau_to_foundation(tbx, fdy)
                    except IndexError:
                        print("Index not valid. Try again.")
                    try:
                        if tab[int(vals[0])-1][-1]:
                            if not tab[int(vals[0])-1][-1].is_face_up():
                                tab[int(vals[0]) - 1][-1].flip_card()
                    except IndexError:
                        pass
                elif len(vals) == 3:
                    #""
                    tbx = tab[int(vals[0]) - 1]
                    tby = tab[int(vals[1]) - 1]
                    try:                        
                        tableau_to_tableau(tbx,tby,int(vals[2]))
                    except IndexError:
                        print("Index invalid. Try again.")
                    #DEBUG print(tbx, tby)
                    try:
                        if tab[int(vals[0])-1][-1]:                        
                            if not tab[int(vals[0]) - 1][-1].is_face_up():
                                tab[int(vals[0]) - 1][-1].flip_card()
                    except IndexError:
                        pass
            else:
                print("No match in expression.")
        elif command.startswith("wf"):
            #waste to foundation command
            pattern = re.compile("((\s\d))")
            #compile regex pattern
            matched = pattern.search(command)
            if matched:
                vals = matched.group(0).split()
                try:
                    worked = waste_to_foundation(waste, fnd[int(vals[0]) - 1], stock)
                except IndexError:
                    print("Invalid index. Try again.")
                    pass
        elif command.startswith("wt"):
            #waste to tableau command
            pattern = re.compile("((\s\d))")
            matched = pattern.search(command)
            if matched:
                vals = matched.group(0).split()
                try:
                    worked = waste_to_tableau(waste, tab[int(vals[0]) - 1], stock)
                except IndexError:
                    print("Invalid index. Try again.")
                    pass
        elif command.startswith("sw"):
            #Stock to waste command
            stock_to_waste(stock, waste)
        elif command.startswith("r"):
            #Reset command
            print("GAME RESET")
            fnd, tab, stock, waste = setup_game()
        elif command.startswith("h"):
            #Help command
            print(MENU)
    except RuntimeError as error_message:  # any RuntimeError you raise lands here
        print("{:s}\nTry again.".format(str(error_message)))
    display_game(fnd, tab, stock, waste)  
    #DEBUG print(waste)
    #DEBUG print(stock.__str__())              
    command = input("prompt :> ")
    winvar = is_winner(fnd)
#    Questions
#	Q1:	5
#	Q2:	6
#	Q3:	1
#	Q4:	1
