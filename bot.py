# Chess AI bot
# Code originally written by AnthonyASanchez
# Modified by Rutuparn Pawar <InputBlackBoxOutput>

import chess
import sys
import random

from AlphaBetaPruning import getPieceValue, evaluation, calculateMove, minimax

#-----------------------------------------------------------------------------------
def minimaxRoot(depth, board,isMaximizing):
	possibleMoves = board.legal_moves
	bestMove = -9999
	bestMoveFinal = None
	moveValueList = []

	for x in possibleMoves:
		move = chess.Move.from_uci(str(x))
		board.push(move)
		value = max(bestMove, minimax(depth - 1, board,-10000,10000, not isMaximizing))
		board.pop()
		moveValueList.append(value)

		if( value > bestMove):
			bestMove = value
			bestMoveFinal = move

	if all(element == moveValueList[0] for element in moveValueList):
		bestMoveFinal = None
	return bestMoveFinal

#-----------------------------------------------------------------------------------
def randomMove(board):
	possibleMoves = board.legal_moves
	return list(possibleMoves)[random.randint(0, possibleMoves.count()-1)]

#-----------------------------------------------------------------------------------
def showHelp():
	print("\nHelp:")
	print("\nRows are 8 to 1 from top to bottom")
	print("Columns are a to h from left to right")
	print("\nIf you wish to move your piece from row 2 col 2 to row 2 col 3,")
	print("Enter your move as b2b3\n")

#-----------------------------------------------------------------------------------
def main():
	print("Chess AI")
	print("-> Enter q to quit")
	print("-> Enter h for help")

	board = chess.Board()
	n = 0
	print(board)
	while n < 200:
		usr_move = input("\nEnter move: ")

		if usr_move == 'q':
			sys.exit()

		if usr_move == 'h':
			showHelp()

		if(len(usr_move) == 4):
			move = chess.Move.from_uci(str(usr_move))
			
			if(move in board.legal_moves):
				board.push(move)
				
				print("\nComputers Turn:")
				move = minimaxRoot(3,board,True)
				if move == None:
					move = chess.Move.from_uci(str(randomMove(board)))
				else:
					move = chess.Move.from_uci(str(move))
				
				board.push(move)
				print(board)
				
				if board.is_stalemate():
					print("Game Over: Stalemate")
					break
				if board.is_insufficient_material():
					print("Game Over: Insufficient Pieces")
					break
				if board.is_game_over():
					print("Game Over: Checkmate")
					break
					
				if board.is_check():
					print("Check")

			else:
				print("Illegal move")
			
		n += 1

#-----------------------------------------------------------------------------------
if __name__ == "__main__":
	main()
	
#-----------------------------------------------------------------------------------