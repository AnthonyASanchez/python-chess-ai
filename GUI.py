# Chess Graphical User Interface (GUI)
# Written by Rutuparn Pawar <InputBlackBoxOutput>

import tkinter
from tkinter import *
import tkinter.messagebox as msgbox

import chess
import bot
import time

import os
import sys
#-------------------------------------------------------------------------------------------
# Unicode for chess pieces
# white king	  ♔   U+2654
# white queen	  ♕   U+2655
# white rook	  ♖   U+2656
# white bishop    ♗   U+2657
# white knight    ♘   U+2658
# white pawn	  ♙   U+2659
# black king	  ♚   U+265A
# black queen	  ♛   U+265B
# black rook	  ♜   U+265C
# black bishop    ♝   U+265D
# black knight    ♞   U+265E
# black pawn	  ♟   U+265F

unicode_map = { "K": "\u2654",
				"Q": "\u2655",
				"R": "\u2656",
				"B": "\u2657",
				"N": "\u2658",
				"P": "\u2659",

				"k": "\u265A",
				"q": "\u265B",
				"r": "\u265C",
				"b": "\u265D",
				"n": "\u265E",
				"p": "\u265F",

				"-":" "
			  }
#----------------------------------------------------------------------------------
# Button map
btn_map = {
	"a8":0 , "b8":1 , "c8":2 , "d8":3 , "e8":4 , "f8":5 , "g8":6 , "h8":7,
	"a7":8 , "b7":9 , "c7":10, "d7":11, "e7":12, "f7":13, "g7":14, "h7":15,
	"a6":16, "b6":17, "c6":18, "d6":19, "e6":20, "f6":21, "g6":22, "h6":23,
	"a5":24, "b5":25, "c5":26, "d5":27, "e5":28, "f5":29, "g5":30, "h5":31,
	"a4":32, "b4":33, "c4":34, "d4":35, "e4":36, "f4":37, "g4":38, "h4":39,
	"a3":40, "b3":41, "c3":42, "d3":43, "e3":44, "f3":45, "g3":46, "h3":47,
	"a2":48, "b2":49, "c2":50, "d2":51, "e2":52, "f2":53, "g2":54, "h2":55,
	"a1":56, "b1":57, "c1":58, "d1":59, "e1":60, "f1":61, "g1":62, "h1":63
}
#----------------------------------------------------------------------------------
class GUI(Tk):
	def __init__(self, width, height):
		super().__init__()

		self.title("Chess")
		self.geometry(f"{width}x{height}") 
		self.wm_resizable(width=False, height=False)

		self.board = chess.Board()
		self.moveStr = ""

		self.gameOver = False

	#-------------------------------------------------------------------------------
	# Menu bar
	def newGame(self):
		self.board = chess.Board()
		self.updateBoard()
		self.removeMarking()

	def recommendMove(self):
		if self.board.turn:
			move = bot.minimaxRoot(3, self.board, True)
			if move == None:
				rec_move = chess.Move.from_uci(str(bot.randomMove(self.board)))
			else:
				rec_move = chess.Move.from_uci(str(move))

			m = str(rec_move)
			self.b_list[btn_map[m[:2]]].configure(bg='#AFFFAF')
			self.b_list[btn_map[m[2:]]].configure(bg='#AFFFAF')
	
	def about(self):
		try:
			with open(os.path.join(sys.path[0], "about.txt"), "r") as about_file:
				msgbox.showinfo('About', about_file.read())
		except FileNotFoundError:
			self.status.configure(text="File about.txt not found!")

	def createMenuBar(self):
		self.menu = Menu(self)
		self.menu.add_command(label='New game', command=self.newGame)
		self.menu.add_command(label='Recommend move', command=self.recommendMove)
		self.menu.add_command(label='About', command=self.about)
		self.menu.add_command(label='Close', command=self.quit)

		self.config(menu=self.menu)

	#-------------------------------------------------------------------------------
	# Status bar
	def createStatusBar(self):
		self.status = Label(self, text="Developed by InputBlackBoxOutput", font='calibri 12 normal', borderwidth=1, relief=SUNKEN, anchor='s', pady=4)
		self.status.pack(side=BOTTOM, fill=X)

		Label(window).pack(side=BOTTOM) # Spacer

	#-------------------------------------------------------------------------------
	def updateBoard(self):
		boardState = ""

		for x in str(self.board.fen).split("'")[1].split(" ")[0]:
			if x.isnumeric():
				for n in range(0, int(x)):
					boardState += "-"
			else:
				if x != "/":
					boardState += x

		#print(boardState)

		for i in range(64):
				self.b_list[i].configure(text= unicode_map[boardState[i]])
	
	def markMove(self, move):
		m = str(move)
		self.b_list[btn_map[m[:2]]].configure(bg='#AFAFFF')
		self.b_list[btn_map[m[2:]]].configure(bg='#AFAFFF')


	def removeMarking(self):
		each = 0
		for r in range(0, 8):
			for c in range(0, 8):
				self.b_list[each].configure(bg='#F0F0F0')

				if r%2 != 0:
					if each%2 == 0:
						self.b_list[each].configure(bg='#DFDFDF')
				else:
					if each%2 != 0:
						self.b_list[each].configure(bg='#DFDFDF')
				each = each + 1

	def positionHasWhitePiece(self, position):
		boardState = ""

		for x in str(self.board.fen).split("'")[1].split(" ")[0]:
			if x.isnumeric():
				for n in range(0, int(x)):
					boardState += "-"
			else:
				if x != "/":
					boardState += x

		if len(position) == 2:
			if boardState[btn_map[position]] in ['K','Q','R','B','N','P']:
				return True
			else:
				return False


	def onButtonClick(self, button):
		self.removeMarking()
		self.status.configure(text = "")

		if self.gameOver == False:
			# Get row
			if button >=0 and button <=31:
				if button >= 0 and button <= 7:
					r = 8
				if button >= 8 and button <=15:
					r = 7
				if button >=16 and button <=23:
					r = 6
				if button >=24 and button <=31:
					r = 5
			else:
				if button >=32 and button <=39:
					r = 4
				if button >=40 and button <=47:
					r = 3
				if button >=48 and button <=55:
					r = 2
				if button >=56 and button <=63:
					r = 1	

			# Get column
			c = chr(97 + button%8)
			
			if len(self.moveStr) == 2:
				self.removeMarking()
				try:
					self.moveStr += c + str(r)
					print(self.moveStr)

					if self.positionHasWhitePiece(self.moveStr[:2]) and self.positionHasWhitePiece(self.moveStr[2:]):
						self.moveStr = self.moveStr[2:]
						self.removeMarking()
						self.b_list[btn_map[self.moveStr]].configure(bg='#FFFFAF')
						return

					if self.moveStr[:2] == self.moveStr[2:]:
						self.moveStr = ""
						return

					move = chess.Move.from_uci(str(self.moveStr))
					self.moveStr = ""
					if move in self.board.legal_moves :
						self.board.push(move)
						self.updateBoard()

						# time.sleep(0.1)
						move = bot.minimaxRoot(3, self.board, True)

						if move == None:
							bot_move = chess.Move.from_uci(str(bot.randomMove(self.board)))
						else:
							bot_move = chess.Move.from_uci(str(move))

						self.board.push(bot_move)
						self.markMove(bot_move)
						self.updateBoard()
					else:
						self.status.configure(text="Illegal move")
						# self.status.configure(bg="#FFAFAF")

				except ValueError:
					self.status.configure(text = "Invalid move")
					self.moveStr = ""
				

				if self.board.is_stalemate():
					self.status.configure(text = "Game Over: Stalemate")
					self.gameOver = True
				if self.board.is_insufficient_material():
					self.status.configure(text = "Game Over: Insufficient Pieces")
					self.gameOver = True
				if self.board.is_game_over():
					self.status.configure(text = "Game Over: Checkmate")
					self.gameOver = True
					
				if self.board.is_check():
					self.status.configure(text = "Check")

			else:
				self.moveStr += c + str(r)
				if(self.positionHasWhitePiece(self.moveStr)):
					self.b_list[btn_map[self.moveStr]].configure(bg='#FFFFAF')
				else:
					self.moveStr = ""


	def createChessBoard(self, font, w, h):
		self.grid_map = Frame(window, bg='#AFAFAF', padx=1, pady=1)

		# Generate 64 button widgets
		self.b_list = []
		for each in range(0, 64):
			self.b_list.append( Button(self.grid_map, text=' ', command=lambda each=each:self.onButtonClick(each), font=f"consolas {font} normal", width=w, height=h))

		# Place 64 button widgets in a 8x8 grid
		each = 0
		for r in range(0, 8):
			for c in range(0, 8):
				self.b_list[each].grid(row=r, column=c)

				if r%2 != 0:
					if each%2 == 0:
						self.b_list[each].configure(bg='#DFDFDF')
				else:
					if each%2 != 0:
						self.b_list[each].configure(bg='#DFDFDF')
				each = each + 1

		self.grid_map.pack(side=BOTTOM)
		self.updateBoard()
#-------------------------------------------------------------------------------------------
if __name__ == '__main__':
	print("Please minimize this window")
	window = GUI(740, 680)
	window.createMenuBar()
	window.createStatusBar()
	window.createChessBoard(18, 6, 2)
	window.mainloop()

#-------------------------------------------------------------------------------------------
# EOF