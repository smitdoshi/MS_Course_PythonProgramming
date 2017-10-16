from tkinter import *
from tkinter import messagebox


# BASE DIALOG CLASS


class Dialog(Toplevel):
    def __init__(self, parent, title = None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.ok)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override


# CONCRETE DIALOG CLASS


class PlayerNameDlg( Dialog ):
    def body( self, master ):

        Label( master, text="Player 1 name:" ).grid( row = 0 )
        Label( master, text="Player 2 name:" ).grid( row = 1 )

        self.e1 = Entry( master )
        self.e2 = Entry( master )

        self.e1.insert( 0, "" )
        self.e2.insert( 0, "" )

        self.e1.grid( row=0, column=1 )
        self.e2.grid( row=1, column=1 )

        self.entries = [ self.e1, self.e2 ]

        return self.e1 # initial focus

    def validate( self ):
        success = True

        for e in self.entries:
            if len( e.get() ) == 0:
                success = False

        if not success:
            messagebox.showerror( "Error", "One or more fields are empty." )
            return False

        return True

    def apply( self ):
        self.result = []
        self.result.append( self.e1.get() )
        self.result.append( self.e2.get() )


# PLAYER CLASS

class Player( object ):
    """ Class used to represent a Tic Tac Toe player. """
    MARK_X = "X"
    MARK_O = "O"

    def __init__( self, name = None, mark = None ):
        """ Create a new player instance. """

        # Name and mark cannot be None.
        if name == None:
            raise Exception( "Name of player is None" )
        if mark == None:
            raise Exception( "Mark of player named " + name + " is None" )

        self.name = name
        self.mark = mark
        self.won = 0
        self.draw = 0
        self.lost = 0

    def __str__( self ):
        """ Returns a string representation of a player. """

        s = "Player name: " + self.name + "\n\t"
        s += "Mark: " + self.mark + "\n\t"
        s += "Win: " + str( self.won ) + "\n\t"
        s += "Draw: " + str( self.draw ) + "\n\t"
        s += "Lose: " + str( self.lost ) + "\n\t"
        s += "Score: " + str( self.get_score() )

        return  s

    def get_score( self ):
        return ( ( self.won * 2 ) + self.draw - self.lost )

    def __lt__( self, other ):
        """ Returns true if this player has fewer victories than the other
        player. """
        return self.get_score() < other.get_score()

    def __eq__( self, other ):
        """ Returns true if both players have the same number of victories. """
        return self.get_score() == other.get_score()


# DECK CLASS

class Deck( object ):
    """ Class used to represent a TicTacToe game board. """

    EMPTY = " "

    def __init__( self ):
        """ Create a new deck. """

        self.board = {}
        self.p1Choices = []
        self.p2Choices = []

        # Fill the board with empty cells.
        for i in range( 9 ):
            self.board[ i ] = Deck.EMPTY

    def __str__( self ):
        c0 = self.board[ 0 ]
        c1 = self.board[ 1 ]
        c2 = self.board[ 2 ]
        c3 = self.board[ 3 ]
        c4 = self.board[ 4 ]
        c5 = self.board[ 5 ]
        c6 = self.board[ 6 ]
        c7 = self.board[ 7 ]
        c8 = self.board[ 8 ]

        s  = "       |     |     \n"
        s += "  {" + c0 + "}  | {" + c1 + "} |  {" + c2 + "} \n"
        s += "_____|_____|_____\n"
        s += "     |     |     \n"
        s += " {" + c3 + "} | {" + c4 + "} | {" + c5 + "} \n"
        s += "_____|_____|_____\n"
        s += "     |     |     \n"
        s += " {" + c6 + "} | {" + c7 + "} | {" + c8 + "} \n"
        s += "     |     |     "

        return s


# GAME CLASS

class TicTacToe( object ):
    """ Class that represents a TicTacToe game. """

    DRAW = "-"
    NOT_OVER = " "

    def __init__( self,gui, master = None ):
        """ Creates a new TicTacToe game. """

        self.deckList = []
        self.player1  = None
        self.player2  = None
        self.master   = master
        self.gui = gui
        self._create_players()

    def _create_players( self ):
        """ Reads the names of the players from standard input. """

        d = PlayerNameDlg( self.master, title = "Player names" )
        if d.result != None:
            self.player1 = Player( name = d.result[0], mark = Player.MARK_X )
            self.player2 = Player( name = d.result[1], mark = Player.MARK_O )

    def _play_again( self ):
        """ Asks the players if they would like to play again. """
        return messagebox.askyesno("Question", "Would you like to play again?")

    def _check_player( self, choices ):
        """ Checks if a player has won. """

        # Check the horizontal rows.
        if 0 in choices and 1 in choices and 2 in choices:
            return True
        elif 3 in choices and 4 in choices and 5 in choices:
            return True
        elif 6 in choices and 7 in choices and 8 in choices:
            return True

        # Check the vertical rows.
        elif 0 in choices and 3 in choices and 6 in choices:
            return True
        elif 1 in choices and 4 in choices and 7 in choices:
            return True
        elif 2 in choices and 5 in choices and 8 in choices:
            return True

        # Check both diagonals.
        elif 0 in choices and 4 in choices and 8 in choices:
            return True
        elif 2 in choices and 4 in choices and 6 in choices:
            return True

        # The player has not won yet.
        else:
            return False

    def _check_winner( self, verbose ):
        """ Returns the mark of the winning player or - if there is a draw. """

        d = self.deckList[ -1 ]

        # Check if player 1 won.
        if self._check_player( d.p1Choices ):
            return Player.MARK_X

        elif self._check_player( d.p2Choices ):
            # Else, check if player 2 won.
            return Player.MARK_O

        elif len( d.p1Choices ) + len( d.p2Choices ) == 9:
            # If no player won and the deck is full then it is a tie.
            return TicTacToe.DRAW

        else:
            return TicTacToe.NOT_OVER

    def validate_user_input( self, play ):
        """ Checks if the number entered by a player is an int in [0, 8]. """

        try:
            # Cast to int first.
            i = int( play )

            # If the cast passes then check if the input is in range.
            if i < 0 or i > 8:
                return False
            else:
                # Check if the input has not been made before.
                if i in self.deckList[ -1 ].board and self.deckList[ -1 ].board[ i ] != Deck.EMPTY:
                    messagebox.showinfo( "Invalid play", "That play has already been made." )
                    return False
                else:
                    return True

        except ValueError:
            # Casting play to int may raise a ValueError if play is not an int.
            return False

    def is_game_over( self ):
        """ Checks if the game is finished. """

        if self._check_winner( False ) == TicTacToe.NOT_OVER:
            return False
        else:
            # Append the deck to the log file.
            f = open( "ticTacToe.txt", "a")
            f.write( str( self.deckList[ -1 ] ) )
            f.write( "\n\n" )
            f.close()

            return True

    def reset(self):
        self.deckList.append( Deck() )

    def turn( self, player, play ):
        """ Game logic. """
        # Process each player one by one, checking if the game is over
        # after every turn.
        if(player % 2 == 0):
            p1_int = play
            self.deckList[ -1 ].board[ p1_int ] = self.player1.mark
            self.deckList[ -1 ].p1Choices.append( p1_int )

        else:

            p2_int = play
            self.deckList[ -1 ].board[ p2_int ] = self.player2.mark
            self.deckList[ -1 ].p2Choices.append( p2_int )

        if self.is_game_over():
            return True
        else:
            return False

    def end_match(self):
        # Find out who won, if any.
        mark = self._check_winner( True )
        if mark == Player.MARK_X:
            self.player1.won += 1
            self.player2.lost += 1
            messagebox.showinfo( "Game over!", self.player1.name + " won!" )

        elif mark == Player.MARK_O:
            self.player2.won += 1
            self.player1.lost += 1
            messagebox.showinfo( "Game over!", self.player2.name + " won!" )

        elif mark == TicTacToe.DRAW:
            self.player1.draw += 1
            self.player2.draw += 1
            messagebox.showinfo( "Game over!", "It's a draw!" )

        # Report scores.
        if self.player1 > self.player2:
            messagebox.showinfo( "Game over!", "Player " + self.player1.name + " has a higher score!\n" +
                                 str( self.player1 ) + "\n" +
                                 str( self.player2 )
            )
        else:
            messagebox.showinfo( "Game over!", "The scores are tied.\n" +
                                 str( self.player1 ) + "\n" +
                                 str( self.player2 )
            )

        # Ask for a rematch.
        return self._play_again()


# GUI CLASS


class TicTacToeGUIOnly(object):
    def __init__(self):
        self.counter = 0
        self.root = Tk()
        self.root.title("TIC TAC TOE")

        bottomFrame = Frame(self.root)
        bottomFrame.pack(side = BOTTOM)
        lblmessage = Label(bottomFrame, text="")
        lblmessage.pack(side = BOTTOM)

        topFrame1 = Frame(self.root)
        topFrame1.pack(side=TOP,expand=True)

        topFrame2 = Frame(self.root)
        topFrame2.pack(side=TOP,expand=True)

        lbl_player1 = Label(topFrame1, text="",width=20)
        lbl_player1.pack(side=LEFT,expand=True)
        lbl_Game = Label(topFrame1, text="Game No. : 1",width=20)
        lbl_Game.pack(side=LEFT,expand=True)
        lbl_player2 = Label(topFrame1, text="",width=20)
        lbl_player2.pack(side=LEFT,expand=True)

        lbl_player1_score = Label(topFrame2, text="Player1 Score",width=20)
        lbl_player1_score.pack(side=LEFT,expand=True)
        lbl_Game_score = Label(topFrame2, text="",width=20)
        lbl_Game_score.pack(side=LEFT,expand=True)
        lbl_player2_score = Label(topFrame2, text="Player2 Score",width=20)
        lbl_player2_score.pack(side = LEFT,expand=True)

        self.frame = Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.canvas = Canvas(self.frame, width=300, height=300)
        self.canvas.pack(fill="both", expand=True)
        self.score1= lbl_player1_score;
        self.score2= lbl_player2_score;
        self.msg = lblmessage;
        self.lbl_game_no = lbl_Game;
        self.ttt = TicTacToe(self,master = self.root)

        lbl_player1.config(text=self.ttt.player1.name + '')
        lbl_player2.config(text=self.ttt.player2.name + '')
        lbl_player1_score.config(text=str(self.ttt.player1.get_score()))
        lbl_player2_score.config(text=str(self.ttt.player2.get_score()))

    def player_click(self,event):
        playing_mark = 'X' if self.counter % 2 == 0 else 'O'
        k = (event.x // 100)
        j = (event.y // 100)

        user_input = (k + (j * 3))
        idx = user_input

        if idx != -1 and self.ttt.validate_user_input(str(idx)):
            _x = 100*k + 50
            _y = 100*j + 50
            if playing_mark == 'O':
                self.canvas.create_oval( _x + 25, _y + 25, _x - 25, _y - 25, width=4, outline="black")
            else:
                self.canvas.create_line( _x + 20, _y + 20, _x - 20, _y - 20, width=4, fill="black")
                self.canvas.create_line( _x - 20, _y + 20, _x + 20, _y - 20, width=4, fill="black")

            self.msg.config(text="' "+playing_mark+" ' marked at position "+ str(idx));

            if(self.ttt.turn(self.counter, idx)):
                again = self.ttt.end_match()

                if(again):
                    self._reset()
                else:
                    self.root.destroy()

            self.counter += 1

    def _reset(self):
        self.counter = 0
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(10,5,300,300, outline="black")
        self.canvas.create_rectangle(100,300,200,0, outline="black")
        self.canvas.create_rectangle(10,100,300,200, outline="black")


        self.canvas.bind("<ButtonPress-1>", self.player_click)
        self.ttt.reset()
        self.score1.config(text=str(self.ttt.player1.get_score()))
        self.score2.config(text=str(self.ttt.player2.get_score()))
        player = self.ttt.player1;
        total_game = str(1 + player.won + player.lost + player.draw);
        self.lbl_game_no.config(text="Game No. : "+total_game);
        self.msg.config(text="");

    def start_game(self):
        self._reset()
        self.root.mainloop()


# ENTRY POINT

def main():
    game = TicTacToeGUIOnly()
    game.start_game()

if __name__ == "__main__":
    main()
