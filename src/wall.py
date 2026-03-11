import pygame
from math import sin,cos,radians
class Wall:
    def __init__(self, x, y, width, height,surface,rotation = 0, color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = surface
        self.color = color
        self.rotation = radians(rotation)
    def draw(self):
        x,y,width,height = self.x,self.y,self.width,self.height
        self.points = [ self.rotate_point(point,self.rotation) for point in [(x-(width/2),y-(height/2)),(x-(width/2),y+(height/2)),(x+(width/2),y+(height/2)),(x+(width/2),y-(height/2))]]
        pygame.draw.polygon(self.surface,self.color,self.points,0)
    def rotate_point(self,point,theta):
        x = point[0] - self.x
        y = point[1] - self.y
        xd = (x * cos(theta)) - (y * sin(theta))
        xy = (x * sin(theta)) + (y * cos(theta))
        xd += self.x
        xy += self.y
        return (xd,xy)

        