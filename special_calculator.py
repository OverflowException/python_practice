#!/usr/bin/python3
'''
    File name: special_calculator.py
    Author: Yao Li
    Date created: 10/Jan/2018
    Date last modified: 15/Jan/2018
    Python Version: 3.5.2
'''

import sys
import traceback
import tkinter as tk
from math import *

class mainwindow(tk.Frame):
    
    #Description:
    #  Constructor
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__init_display_pad()
        self.__init_primary_pad()
        self.__init_secondary_pad()
        
        self.list_expr_pieces = []

    #Description:
    #  Destructor        
    def quit(self, event = None):
        sys.exit()

    #Description:
    #  Initialize display pad. Contains Entry widgets. Show expressions and result
    #  Placed at top-most position of the main window
    def __init_display_pad(self):
        self.display_pad = tk.Frame(self, bd = 10)
        self.display_pad.grid(row = 0, column = 0)

        #Initialize formula display
        self.ent_expr = tk.Entry(self.display_pad, width = 32);
        self.ent_expr.pack(side = tk.TOP, fill = tk.X)
        self.ent_expr.configure(state = "readonly")

        #Initialize result display
        self.ent_result = tk.Entry(self.display_pad, width = 32);
        self.ent_result.pack(side = tk.TOP, fill = tk.X)
        self.ent_result.configure(state = "readonly")


    #Description:
    #  Initialize primary pad. Contains digit buttons and operator buttons.
    #  Placed at bottom-most position of the main window        
    def __init_primary_pad(self):
        self.primary_pad = tk.Frame(self, bd = 10)
        self.primary_pad.grid(row = 2, column = 0)

        self.btns_digits = [];
        #Initialize digit buttons
        for index in range(0, 10):
            self.btns_digits.append(tk.Button(self.primary_pad, text = index, width = 3))
    
        for row_index in range(3):
            for col_index in range(3):
                self.btns_digits[(2 - row_index) * 3 + col_index + 1].grid(row = row_index, column = col_index, padx = 5)
                self.btns_digits[(2 - row_index) * 3 + col_index + 1].bind("<Button-1>", self.on_btn_plain_pressed)
        self.btns_digits[0].grid(row = 3, column = 0)
        self.btns_digits[0].bind("<Button-1>", self.on_btn_plain_pressed)
    
        #Initialize [.] [,] [=] [+] [-] [*] [/] [AC] [DEL] [pi] buttons
        self.btn_plus = tk.Button(self.primary_pad, text = "+", width = 3)
        self.btn_minus = tk.Button(self.primary_pad, text = "-", width = 3)
        self.btn_mul = tk.Button(self.primary_pad, text = "*", width = 3)
        self.btn_div = tk.Button(self.primary_pad, text = "/", width = 3)
        self.btn_dot = tk.Button(self.primary_pad, text = ".", width = 3)
        self.btn_coma = tk.Button(self.primary_pad, text = ",", width = 3)
        self.btn_equ = tk.Button(self.primary_pad, text = "=", width = 3, height = 6, bg = "green")
        self.btn_del = tk.Button(self.primary_pad, text = "DEL", width = 3, bg = "orange")
        self.btn_ac = tk.Button(self.primary_pad, text = "AC", width = 3, bg = "red")
        self.btn_pi = tk.Button(self.primary_pad, text = "\u03c0", width = 3)

        self.btn_plus.grid(row = 1, column = 3, padx = 5)
        self.btn_plus.bind("<Button-1>", self.on_btn_plain_pressed)

        self.btn_minus.grid(row = 1, column = 4, padx = 5)
        self.btn_minus.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_mul.grid(row = 2, column = 3, padx = 5)
        self.btn_mul.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_div.grid(row = 2, column = 4, padx = 5)
        self.btn_div.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_dot.grid(row = 3, column = 1, padx = 5)
        self.btn_dot.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_pi.grid(row = 3, column = 2, padx = 5)
        self.btn_pi.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_coma.grid(row = 3, column = 3, padx = 5)
        self.btn_coma.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_del.grid(row = 0, column = 3, padx = 5)
        self.btn_del.bind("<Button-1>", self.on_btn_del_pressed)
        
        self.btn_ac.grid(row = 0, column = 4, padx = 5)
        self.btn_ac.bind("<Button-1>", self.on_btn_ac_pressed)
        
        self.btn_equ.grid(row = 0, column = 5, rowspan = 4, padx = 5)
        self.btn_equ.bind("<Button-1>", self.on_btn_equ_pressed)
        
        self.bracket_pad = tk.Frame(self.primary_pad)
        self.bracket_pad.grid(row = 3, column = 4)
        
        self.btn_l_bracket = tk.Button(self.bracket_pad, text = "(")
        self.btn_r_bracket = tk.Button(self.bracket_pad, text = ")")
        
        self.btn_l_bracket.pack(side = tk.LEFT)
        self.btn_l_bracket.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_r_bracket.pack(side = tk.LEFT)
        self.btn_r_bracket.bind("<Button-1>", self.on_btn_plain_pressed)

    #Description:
    #  Initialize primary pad. Contains advanced function buttons
    #  Placed in the middle if main window
    def __init_secondary_pad(self):
        self.secondary_pad = tk.Frame(self, bd = 10)
        self.secondary_pad.grid(row = 1, column = 0)
        
        self.deg_rad_pad = tk.Frame(self.secondary_pad)
        self.deg_rad_pad.grid(row = 0, column = 0, rowspan = 2, columnspan = 2)
        
        self.deg_rad_var = tk.StringVar()
        self.rbtn_deg = tk.Radiobutton(self.deg_rad_pad, text = "Deg", variable = self.deg_rad_var, value = "deg")
        self.rbtn_deg.grid(row = 0, column = 0, padx = 5, pady = 4)
        
        self.rbtn_rad = tk.Radiobutton(self.deg_rad_pad, text = "Rad", variable = self.deg_rad_var, value = "rad")
        self.rbtn_rad.grid(row = 1, column = 0, padx = 5, pady = 4)
        
        self.rbtn_deg.select()
        
        self.btn_sin = tk.Button(self.secondary_pad, text = "sin", width = 4)
        self.btn_sin.grid(row = 0, column = 3, padx = 5)
        self.btn_sin.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_cos = tk.Button(self.secondary_pad, text = "cos", width = 4)
        self.btn_cos.grid(row = 0, column = 4, padx = 5, pady = 4)
        self.btn_cos.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_tan = tk.Button(self.secondary_pad, text = "tan", width = 4)
        self.btn_tan.grid(row = 0, column = 5, padx = 5, pady = 4)
        self.btn_tan.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_pow = tk.Button(self.secondary_pad, text = "pow", width = 4)
        self.btn_pow.grid(row = 1, column = 3, padx = 5, pady = 4)
        self.btn_pow.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_log = tk.Button(self.secondary_pad, text = "log", width = 4)
        self.btn_log.grid(row = 1, column = 4, padx = 5, pady = 4)
        self.btn_log.bind("<Button-1>", self.on_btn_plain_pressed)
        
        self.btn_sqrt = tk.Button(self.secondary_pad, text = "sqrt", width = 4)
        self.btn_sqrt.grid(row = 1, column = 5, padx = 5, pady = 4)
        self.btn_sqrt.bind("<Button-1>", self.on_btn_plain_pressed)



    def on_btn_plain_pressed(self, event):
        piece = str(event.widget["text"])
        
        if piece == "log":
            piece = "log10"
        #add '(' to sin, cos, tan or log
        if len(piece) > 1:
                piece += "("
        
        self.list_expr_pieces.append(piece)
        self.flush_display(self.list_expr_pieces, self.ent_expr)
        self.flush_display([], self.ent_result)


    def on_btn_del_pressed(self, event):
        if self.list_expr_pieces:
            self.list_expr_pieces.pop()
        
        self.flush_display(self.list_expr_pieces, self.ent_expr)
        self.flush_display([], self.ent_result)


    def on_btn_ac_pressed(self, event):
        self.list_expr_pieces.clear()
        self.flush_display(self.list_expr_pieces, self.ent_expr)
        self.flush_display([], self.ent_result)


    def on_btn_equ_pressed(self, event):
        try:
            if not self.list_expr_pieces:
                return
    
            list_solvable = self.list_expr_pieces[:]
            #Convert pi
            for index in range(0, len(list_solvable)):
                if list_solvable[index] == "\u03c0":
                    list_solvable[index] = str(pi)
            
            #deal with rad/deg radiobuttons
            if self.deg_rad_var.get() == "deg":
                self.to_deg(list_solvable)

            str_result = eval("".join(list_solvable))
            self.flush_display([str_result], self.ent_result)
        
        except:
            str_result = str(sys.exc_info()[0])[8:-2]

        finally:
            self.flush_display([str_result], self.ent_result)


        
    def flush_display(self, list, ent_widget):
        ent_widget.configure(state = "normal")
        ent_widget.delete(0, "end")
        for ele in list:
            ent_widget.insert("end", ele)
        ent_widget.configure(state = "readonly")


    def to_deg(self, list_arg):
        list_rad_expr = []
        for ele in list_arg:
            list_rad_expr.append(ele)
            list_rad_expr.append("")

        #This dict takes the starting position of trigometric function
        dict_trigo = dict()
        for index in range(0, len(list_arg)):
            #Found trigonometric functions
            if list_arg[index] == "cos(" or list_arg[index] == "sin(" or list_arg[index] == "tan(":
                dict_trigo = {key: value + 1 for key, value in dict_trigo.items()}
                dict_trigo[index] = 1;
            
            elif list_arg[index] == "(":
                dict_trigo = {key: value + 1 for key, value in dict_trigo.items()}

            elif list_arg[index] == ")":
                dict_trigo = {key: value - 1 for key, value in dict_trigo.items()}
                for key, value in dict_trigo.items():
                    if value == 0:
                        list_rad_expr[key * 2 + 1] = "radians("
                        list_rad_expr[index * 2 - 1] = ")"
                dict_trigo = {key: value for key, value in dict_trigo.items() if value}

        list_arg[:] = [ele for ele in list_rad_expr if ele]




app = tk.Tk()
app.option_add("*Font", "monospace 20 bold")
app.title("Special Calculator");
app.resizable(width = False, height = False)
mainwindow(app).pack()
app.mainloop()
