import tkinter as tk
from tkinter import *
from math import sqrt, pi

class Graphene:
    def __init__(self, origin=(100, 250), a_length= 50, length=6, width=6):
        self.origin = origin
        self.a_length = a_length
        self.width = width
        self.length = length
        self.calculate_coords()
        self.calc_reciprocal_lattice()
        

    def calculate_coords(self):
        self.basis_a1 = (sqrt(3)*self.a_length/2, self.a_length/2)
        self.basis_a2 = (sqrt(3)*self.a_length/2, -self.a_length/2)
        self.basis_d = (self.a_length/sqrt(3), 0)
        
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
    

    def calc_reciprocal_lattice(self, scale_factor = 300):
        self.basis_b1 = (2* pi / sqrt(3) / self.a_length, 2 * pi / self.a_length)
        self.basis_b2 = (2* pi / sqrt(3) / self.a_length, -2 * pi / self.a_length)

        self.basis_M1 = (2 * pi / sqrt(3) / self.a_length, 0)
        self.basis_M2 = (-2 * pi / sqrt(3) / self.a_length, 0)

        self.basis_K = [(2 * pi / sqrt(3) / self.a_length, 2 * pi / 3 / self.a_length),
            (2 * pi / sqrt(3) / self.a_length, -2 * pi / 3 / self.a_length),
            (0, -4 * pi / 3 / self.a_length),
            (-2 * pi / sqrt(3) / self.a_length, -2 * pi / 3 / self.a_length),
            (-2 * pi / sqrt(3) / self.a_length, 2 * pi / 3 / self.a_length),
            (0, 4 * pi / 3 / self.a_length)]

        # reciprocal lattice
        self.reciprocal_lattice_coordinates = [[0 for _ in range(self.length)] for _ in range(self.width)]
        self.k_coordinates = [[[] for _ in range(self.length)] for _ in range(self.width)]
        self.m_coordinates = [[[] for _ in range(self.length)] for _ in range(self.width)]
        self.reciprocal_lattice_coordinates[0][0] = self.origin
        for i in range(self.width):
            if i != 0:
                x, y = self.reciprocal_lattice_coordinates[i-1][0]
                x += self.basis_b1[0] * scale_factor
                y += self.basis_b1[1] * scale_factor
                self.reciprocal_lattice_coordinates[i][0] = (x, y)

            for j in range(self.length):
                if j != 0:
                    x, y = self.reciprocal_lattice_coordinates[i][j-1]
                    x += self.basis_b2[0] * scale_factor
                    y += self.basis_b2[1] * scale_factor
                    self.reciprocal_lattice_coordinates[i][j] = (x,y)
                
                x, y = self.reciprocal_lattice_coordinates[i][j]
                k_group = []
                for basis in self.basis_K:
                    k_group.append(tuple([x + basis[0] * scale_factor , y + basis[1] * scale_factor]))
                self.k_coordinates[i][j] = k_group

        
    def draw_atoms(self, canvas:tk.Canvas, radius = 5):
        for i in range(self.width):
            for j in range(self.length):
                x, y = self.A_coordinates[i][j]
                canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#777777")

                # if i < self.width and j < self.length:
                x, y = self.B_coordinates[i][j]
                canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#ffffff")


    def draw_bonds(self, canvas:tk.Canvas):
        for i in range(self.width):
            for j in range(self.length):
                b_x, b_y = self.B_coordinates[i][j]

                a_x1, a_y1 = self.A_coordinates[i][j]
                canvas.create_line(a_x1, a_y1, b_x, b_y, fill="#999999")

                if i < self.width-1:
                    a_x2, a_y2 = self.A_coordinates[i+1][j]
                    canvas.create_line(a_x2, a_y2, b_x, b_y, fill="#999999")
                    canvas.create_line(a_x1, a_y1, a_x2, a_y2, fill="#555555")

                if j < self.length-1:
                    a_x2, a_y2 = self.A_coordinates[i][j+1]
                    canvas.create_line(a_x2, a_y2, b_x, b_y, fill="#999999")
                    canvas.create_line(a_x1, a_y1, a_x2, a_y2, fill="#555555")
        

    def draw_reciprocal_atoms(self, canvas:tk.Canvas, radius = 5, radius2 = 3):
        for i in range(self.width):
            for j in range(self.length):
                x, y = self.reciprocal_lattice_coordinates[i][j]
                canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#777777")

                for x, y in self.k_coordinates[i][j]:
                    canvas.create_oval(x - radius2, y - radius2, x + radius2, y + radius2, fill="#ffffff")

    
    def draw_reciprocal_bonds(self, canvas:tk.Canvas):
        for i in range(self.width):
            for j in range(self.length):
                b_x, b_y = self.reciprocal_lattice_coordinates[i][j]

                if i < self.width-1:
                    a_x, a_y = self.reciprocal_lattice_coordinates[i+1][j]
                    canvas.create_line(a_x, a_y, b_x, b_y, fill="#555555")

                if j < self.length-1:
                    a_x, a_y = self.reciprocal_lattice_coordinates[i][j+1]
                    canvas.create_line(a_x, a_y, b_x, b_y, fill="#555555")

                for k in range(6):
                    if k == 0:
                        x1, y1 = self.k_coordinates[i][j][-1]
                    else:
                        x1, y1 = self.k_coordinates[i][j][k-1]
                    x2, y2 = self.k_coordinates[i][j][k]
                    canvas.create_line(x1, y1, x2, y2, fill="#999999")
