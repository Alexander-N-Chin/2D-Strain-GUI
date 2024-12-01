import tkinter as tk
from tkinter import *
from math import radians, cos, sin, sqrt, pi

class Graphene:
    length = 0
    width = 0
    origin = (0, 0)
    a_length = 0
    basis_a1 = (0,0)
    basis_a2 = (0,0)
    basis_d = (0,0)
    A_coordinates = None
    B_coordinates = None
    reciprocal_lattice_coordinates = None

    def __init__(self, origin=(100, 250), a_length= 50, length=6, width=6):
        self.origin = origin
        self.a_length = a_length
        self.width = width
        self.length = length
        self.calculate_coords()
        

    def calculate_coords(self):
        self.basis_a1 = (sqrt(3)*self.a_length/2, self.a_length/2)
        self.basis_a2 = (sqrt(3)*self.a_length/2, -self.a_length/2)
        self.basis_d = (self.a_length/sqrt(3), 0)
        
        self.basis_b1 = (2* pi / sqrt(3) / self.a_length, 2 * pi / self.a_length)
        self.basis_b2 = (2* pi / sqrt(3) / self.a_length, -2 * pi / self.a_length)
        
        self.A_coordinates = self.A_coordinates = [[0 for _ in range(self.length)] for _ in range(self.width)]
        self.B_coordinates = self.B_coordinates = [[0 for _ in range(self.length)] for _ in range(self.width)]

        self.A_coordinates[0][0] = self.origin
        for i in range(self.width):
            if i != 0:
                x, y = self.A_coordinates[i-1][0]
                x += self.basis_a1[0]
                y += self.basis_a1[1]
                self.A_coordinates[i][0] = (x, y)

            for j in range(self.length):
                if j != 0:
                    x, y = self.A_coordinates[i][j-1]
                    x += self.basis_a2[0]
                    y += self.basis_a2[1]
                    self.A_coordinates[i][j] = (x,y)
                
                x, y = self.A_coordinates[i][j]
                x += self.basis_d[0]
                y += self.basis_d[1]
                self.B_coordinates[i][j] = (x, y)
    
        # reciprocal lattice
        self.reciprocal_lattice_coordinates = [[0 for _ in range(self.length-1)] for _ in range(self.width-1)]
        self.reciprocal_lattice_coordinates[0][0] = (self.origin[0] + 2 * self.a_length/sqrt(3), self.origin[1])
        for i in range(self.width-1):
            if i != 0:
                x, y = self.reciprocal_lattice_coordinates[i-1][0]
                x += self.basis_b1[0]
                y += self.basis_b1[1]
                self.reciprocal_lattice_coordinates[i][0] = (x, y)

            for j in range(self.length-1):
                if j != 0:
                    x, y = self.reciprocal_lattice_coordinates[i][j-1]
                    x += self.basis_b2[0]
                    y += self.basis_b2[1]
                    self.reciprocal_lattice_coordinates[i][j] = (x,y)
        
        print(self.reciprocal_lattice_coordinates)


    def draw_atoms(self, canvas:tk.Canvas, radius = 5, reciprocal = True):
        for i in range(self.width):
            for j in range(self.length):
                x, y = self.A_coordinates[i][j]
                canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#ffffff")

                # if i < self.width-1 and j < self.length-1:
                x, y = self.B_coordinates[i][j]
                canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#bbbbbb")
        
        if reciprocal:
            for i in range(self.width-1):
                for j in range(self.length-1):
                    x, y = self.reciprocal_lattice_coordinates[i][j]
                    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#ffffff")


    def draw_bonds(self, canvas:tk.Canvas, reciprocal = True):
        for i in range(self.width):
            for j in range(self.length):
                b_x, b_y = self.B_coordinates[i][j]

                a_x, a_y = self.A_coordinates[i][j]
                canvas.create_line(a_x, a_y, b_x, b_y, fill="#999999")

                if i < self.width-1:
                    a_x, a_y = self.A_coordinates[i+1][j]
                    canvas.create_line(a_x, a_y, b_x, b_y, fill="#999999")

                if j < self.length-1:
                    a_x, a_y = self.A_coordinates[i][j+1]
                    canvas.create_line(a_x, a_y, b_x, b_y, fill="#999999")
        
        if reciprocal:
            for i in range(self.width-1):
                for j in range(self.length-1):
                    b_x, b_y = self.reciprocal_lattice_coordinates[i][j]

                    if i < self.width-2:
                        a_x, a_y = self.reciprocal_lattice_coordinates[i+1][j]
                        canvas.create_line(a_x, a_y, b_x, b_y, fill="#999999")

                    if j < self.length-2:
                        a_x, a_y = self.reciprocal_lattice_coordinates[i][j+1]
                        canvas.create_line(a_x, a_y, b_x, b_y, fill="#999999")

    
                
        
