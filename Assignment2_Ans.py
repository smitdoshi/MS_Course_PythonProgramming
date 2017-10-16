import os
import platform
from time import strftime, gmtime

__author__ = 'SMIT'


'''
A simple implementation of Tic Tac Toe
Student name: SMIT N DOSHI
Student ID#: 0988814
'''


class Player:
    '''
    This class will have the variable PlayerName, Playing Mark and Score Statistics. Thus it will have
    some validation for PlayerName, Playing Mark and the Score Updation
    '''

    # we will use tuple for playing mark option as there are only 2 marks 'X' or 'O' and as this are in upper case so
    # we will need a function that gets the userinput and makes it upper case

    playing_mark_option = ('X','O')
    won = 0
    draw = 0
    lost = 0

    '''
        Over ridding the Default Constructor
    '''

    def __init__(self):
        self.PlayerName = " "
        self.PlayersMark = " "
        self.Statistics = {'won':0,'draw':0,'lost':0}
        self.PlayersTurn = 0        # Which players turn is
        self.game_continue = "Y"

    '''
        Over ridding the Default Constructor
        :return: it will return the Player Name and the Player Mark
    '''
    def __str__(self):
        return "Player Name: "+str(self.PlayerName)+"---- Player Mark: "+str(self.PlayersMark)

    '''
        Get Score to display the Score
        :return: the score in the given format
    '''

    def getscore(self):
        return ((self.Statistics['won']*2)+(self.Statistics['draw'])-(self.Statistics['lost']))


    '''
        On getting the Input from the USER
        Initialize the PLaye Attributes Like the Name, Mark, Numbers
    '''

    def initializer_player_attribute(self,name,mark, number):
        self.Player_Name = name
        self.Players_Mark = mark
        self.Players_Turn = number

    '''
        Validate the mark input from the User
        This is called by other class
    '''

    def validate_player_mark(self,mark_str):
        mark_str = mark_str.upper()
        if(mark_str in self.playing_mark_option):
            return True
        return False

    '''
        Once we have got the Player1 options then automatically assign the
        player2 the left out mark
    '''

    def assign_mark_player2(self,player1Mark):
        player1Option = self.playing_mark_option.index(player1Mark)

        # Now we got what player1 option is, If player has selected 0 then return 1 for player2
        if(player1Option==0):
            return self.playing_mark_option[1]
        return self.playing_mark_option[0]


class Deck:
    '''
    Class Deck will have Board Values in dictionary, Player1choices in list, Player2Choice in list
    Methods: Operations on Board like: Validate user's board input,
    insert of the option the board, display of avaliable choices
    '''


    win_combination = [
        [1,2,3],
        [7,8,9],
        [4,5,6],
        [1,4,7],
        [2,5,8],
        [3,6,9],
        [3,5,7],
        [1,5,9],
    ]

    '''
        Over Ridding the Default Constructor
    '''

    def __init__(self):
        self.Board = {1:'',2:'',3:'',4:'',5:'',6:'',7:'',8:'',9:''}
        self.Player1Choice = []
        self.Player2Choice = []
        self.PlayerMoves = []

    '''
        Over ridding the __str__ Constructor
        :return: it will return the Board and the available choices
    '''

    def __str__(self):
        return "       |     |     \n  {key1}  | {key2} |  {key3}\n  _____|_____|_____\n       |     |     \n  {key4}  | {key5} |  {key6}\n  _____|_____|_____\n       |     |     \n  {key7}  | {key8} |  {key9}\n       |     |     " \
                      "\n".format(**self.get_board_list())

    '''
       Method to display all the available choices
        :return: a list will be return which will have all the board keys
    '''

    def get_available_board_choices(self):
        return list(self.Board.keys())

    '''
       Method to update the board choices
    '''

    def get_board_list(self):

        updated_board = self.get_available_board_choices();
        updated_board_list = {};
        for key, value in enumerate(updated_board):
            if(self.Board[value] != ""):
                updated_board_list["key"+str(value)+""] = " "+self.Board[value]+" ";
            else:
                updated_board_list["key"+str(value)+""] = "{"+str(value)+"}";
        return updated_board_list;


    '''
    We would also like to validate the Players Input for the Board

    '''

    def valid_players_boardInput(self,choices):
        tmpPlayerObject = Player()
        try:
            if(int(choices) in self.get_available_board_choices()):
            # Check if the choices are in the list of Player1Mover or Player2 Moves
                choices = int(choices)
                if(choices in self.Player1Choice or choices in self.Player2Choice):
                    return "This Choice is already taken"
                else:
                    return "No Error";
        except ValueError:
            return "Please enter a valid choice"
        return "Choice is not in List"

    '''
    Set  the Move of the Player
    '''

    def player_move(self,str):
        self.PlayerMoves.append(str)

    '''
    Check if the Board is Full or Not
    '''
    def board_full_check(self):
        block_occupied = 0
        for key, value in self.Board.items():
            if(value!= ""):
                # increase the block occupied count

                block_occupied+=1
        if(len(self.Board)==block_occupied):
            # Then the board is full
            return True
        return False


    '''
    Insert the Choice entered by the player
    '''

    def insert_values_onBoard(self,choices,playerObject):
        self.player_move(playerObject.Player_Name+ " marked "+playerObject.Players_Mark+" at position "+choices+" .")
        choices = int(choices)
        # print(playerObject.Players_Mark+" helloooo");
        self.Board[choices] = playerObject.Players_Mark

        if(playerObject.Players_Turn==1):
            self.Player1Choice.append(choices)
            self.Player1Choice.sort()
        else:
            self.Player2Choice.append(choices)
            self.Player2Choice.sort()




class TicTacToe:
    '''
    This clss will have the main sets of rules for running the game i.e the game logic
    '''


    '''
        Over ridding the __int__ Constructor
        Here we will create the Objects of the class Player and Deck
    '''
    def __init__(self):
        self.Player1 = Player()
        self.Player2 = Player()
        self.currentDeck = Deck()
        self.Decklist = ()

    '''
       set Player Winning Details

    '''
    def setPlayerWin(self,playerObj):
        self.currentDeck.player_move(playerObj.Player_Name+" WINS ")
        playerturn = playerObj.Players_Turn
        playerObj.Statistics['won'] = playerObj.Statistics['won'] + 1
        if(playerturn == 1):
            self.Player2.Statistics['lost'] -= 1
        else:
            self.Player2.Statistics['lost'] -=1
        print(playerObj.Player_Name+" Won ")

    '''
    Set Board Full Logic

    '''

    def setBoardFull(self):
        self.currentDeck.player_move(" Game Draw ")
        self.Player1.Statistics['draw'] += 1
        self.Player2.Statistics['draw'] += 1

        print("****** Game Draw ******* ")



    '''
    Game Restart Validation

    '''

    def game_continue_validation(self,restart_game):
        restart_game = restart_game.upper()
        if(restart_game=="Y" or restart_game=="N"):
            return True
        return False

    '''
    Printing of the Game Result

    '''

    def print_finalGameResult(self):

        if(self.Player1.game_continue== "N"):
            print(self.Player1.Player_Name+" left game.")
        else:
            print(self.Player2.Player_Name+" left game.")

        # Display Number of Games Played

        print("Total Game Played: "+str(len(self.Decklist)))
        print(self.Player1.Player_Name)
        print("*** Won : "+str(self.Player1.Statistics['won'])+" lost :"+str(self.Player1.Statistics['lost'])+
              " Draw: "+str(self.Player1.Statistics['draw'])+ " \n Score: "+str(self.Player1.getscore())+"\n")

        print(self.Player2.Player_Name)
        print("*** Won : "+str(self.Player2.Statistics['won'])+" lost :"+str(self.Player2.Statistics['lost'])+
              " Draw: "+str(self.Player2.Statistics['draw'])+ " \n Score: "+str(self.Player2.getscore())+"\n")


    '''
    Create File of Game Details

    '''

    def game_detail_file(self,filePath):
        with open(filePath,'w+') as gameFile:
            game_details = self.Decklist
            for key,value in enumerate(game_details):
                gameFile.write("\n\n Game "+str(key+1)+" : \n")
                for move_key,moves_val in enumerate(value.PlayerMoves):
                    gameFile.write("\t" +str(move_key+1)+" : "+moves_val+"\n")



    '''
       is_gameover to check if the game is over
        :return: it will return whether game is over or not
    '''

    def is_gameover(self,playerTurn):
        deck = self.currentDeck
        win_combos = deck.win_combination

        playerChoices = []

        if(playerTurn== 1):
            playerChoices = deck.Player1Choice
        else:
            playerChoices = deck.Player2Choice

    # Check if anyone won

        for combos in win_combos:
            combo_set = set(combos)
            if(combo_set.issubset(set(playerChoices))):
                if(playerTurn==1):
                    playerObj = self.Player1
                else:
                    playerObj = self.Player2
                self.setPlayerWin(playerObj)
                return True
    # Check if the Board is full

        if(deck.board_full_check()):
            self.setBoardFull()
            return True
        return False

    '''
    Clear Screen
    '''
    def clear(self):
        clear = 'cls';
        if platform.system( ) == 'Linux':
            clear = 'clear'
        os.system(clear);



    '''
       method to get the user input like player name and the choices and the mark
       to avoid
    '''
    def get_user_input(self):
        tmpPlayerObject = Player()

        player1Name = input("Player 1, Enter Name: ")
        player1Mark = input("Please Choose Your Tic Tac Toe Mark From \""+tmpPlayerObject.playing_mark_option[0]+"\"  OR \""+tmpPlayerObject.playing_mark_option[1]+"\" .")
        # Validate this Input
        while not(tmpPlayerObject.validate_player_mark(player1Mark)):

            player1Mark = input(" Mark :- ")

        player1Mark = player1Mark.upper();

        player2Name = input("Player 2, Enter Name: ")

        if(player2Name == player1Name):
            # Name Duplication
            print("Name Entered is Already taken\n")
            player2Name = input("Enter Different Name: ")

        player2Mark = tmpPlayerObject.assign_mark_player2(player1Mark)

        # Now call the Initializer from the Class Player and give all this Value:

        Player1Obj = self.Player1
        Player1Obj.initializer_player_attribute(player1Name,player1Mark,1)

        Player2Obj = self.Player2
        Player2Obj.initializer_player_attribute(player2Name,player2Mark,2)

    '''
       method to get the gameplay user input like the X position or O position
    '''

    def game_play_input(self):

        deck = self.currentDeck
        Player1Choice = deck.Player1Choice
        Player2Choice = deck.Player2Choice
        player1Obj = self.Player1;
        player2Obj = self.Player2;

        playersTurn = 1     # Switching between two players

        while not(self.is_gameover(playersTurn)):
            choices=""
            tmpPlayerObject = Player()
            print(deck)
            if(len(Player1Choice)==len(Player2Choice)):
                choices=input(player1Obj.Player_Name+"("+player1Obj.Players_Mark+")"+" Enter Your Position : ")
                tmpPlayerObject = player1Obj
                playersTurn = 1
            else:
                choices=input(player2Obj.Player_Name+"("+player2Obj.Players_Mark+")"+" Enter Your Position : ")
                tmpPlayerObject = player2Obj
                playersTurn = 2

            validate_choice = deck.valid_players_boardInput(choices)

            if(validate_choice=="Valid Choice"):
                deck.insert_values_onBoard(choices,tmpPlayerObject)
            elif(validate_choice == "No Error"):
                deck.insert_values_onBoard(choices,tmpPlayerObject)
            else:
                print(validate_choice)


        self.Decklist = self.Decklist + (deck,)
        print(deck)
        self.currentDeck = Deck()

    '''
    Method to Start the Game
    '''

    def game_begins(self):
        startgame = self

        startgame.get_user_input()
        player1gameContinuation= "Y"
        player2gameContinuation= "Y"

        while(startgame.Player1.game_continue=="Y" and startgame.Player2.game_continue=="Y"):

            startgame.game_play_input()
            startgame.Player1.game_continue=input(startgame.Player1.Player_Name+" Do you want to continue Y / N: ")
            while not (startgame.game_continue_validation(startgame.Player1.game_continue)):
                startgame.Player1.game_continue=input(startgame.Player1.Player_Name+" Do you want to continue Y / N: ")

            startgame.Player1.game_continue = startgame.Player1.game_continue.upper()

            if(startgame.Player1.game_continue !="N"):
                # Now will check for Player2
                startgame.Player2.game_continue=input(startgame.Player2.Player_Name+" Do you want to continue Y / N: ")
                while not (startgame.game_continue_validation(startgame.Player2.game_continue)):
                    startgame.Player2.game_continue=input(startgame.Player2.Player_Name+" Do you want to continue Y / N: ")

            startgame.Player2.game_continue = startgame.Player2.game_continue.upper()

        self.print_finalGameResult()


        fileName = strftime("%a_%d_%b_%Y_%H_%M_%S", gmtime())+'.txt';
        filePath = os.getcwd();
        filePath = os.path.join(filePath, '')
        filePath = filePath+"Game_Played_at_"+fileName;
        self.game_detail_file(filePath);
        print("View All Games & Moves Details in File : "+filePath);

'''
Object Creation of Tic Tac Toe and Calling of its Function
'''


Start_Game = TicTacToe()
Start_Game.game_begins()
