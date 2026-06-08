import os
import struct
import pygame
import json
import numpy

from TileFunctions import *
from GetResources import *

pygame.font.init()

def updateBackground(newBackground, surface, width, height):
    image = pygame.image.load(newBackground)
    background = pygame.transform.scale(image, (width, height))
    surface.fill((0,0,0))
    surface.blit(background, (0,0))

def displayMessage(screenBuffer, message, color, size):
    font = pygame.font.SysFont(0, size)
    textSurface = font.render(message, False, color)
    screenBuffer.blit(textSurface, tileSize)

class Tilemap:

    def __init__(self, tileList, tileData, currentForest, width, height, extraButtonRows):
        self.extraButtonRows = extraButtonRows
        self.tileList = tileList
        self.tileData = tileData
        self.currentForest = currentForest
        self.width = width
        self.height = height

    def getTileBuffer(self, tileList, backgroundBuffer):

        screenBuffer = backgroundBuffer

        standardTileset = pygame.image.load(blockList[self.currentForest]).convert_alpha()
        multiTileset = pygame.image.load(multiList[self.currentForest]).convert_alpha()
        entityTileset = pygame.image.load(entityTilesetLocation).convert_alpha()
        
        (x, y) = (0, 0)

        for i in range(len(self.tileData)):
                if self.tileData[i] in tileHexList:
                    currentTile = self.tileList[tileHexList.index(self.tileData[i])]
                    #handle specials
                    if currentTile.type == "special":

                        if currentTile.hex == 0x0000: #air
                            if y <=59*8:
                                if i % lineWidth != lineWidth-1:
                                    x = (i % lineWidth)*8

                                else:
                                    x = (i % lineWidth)*8
                                    y += 8
                                continue
                            else:
                                currentTileImage = pygame.image.load(currentTile.image).convert_alpha()
                        else:
                            currentTileImage = pygame.image.load(currentTile.image).convert_alpha()

                    #handle multis
                    elif currentTile.type == "multi":
                        if y <= 59*8:
                            currentTileCoords = tuple(8*num for num in currentTile.coords)
                            dimensions = currentTile.size
                            currentTileImage = pygame.Surface(dimensions, pygame.SRCALPHA)
                            currentTileImage.blit(multiTileset, (0, 0), (currentTileCoords + dimensions))

                            if (i % lineWidth) != (lineWidth-1):
                                x = (i % lineWidth)*8
                                screenBuffer.blit(currentTileImage, (x, y - dimensions[1] + tileSize[1]))

                            else:
                                x = (i % lineWidth)*8
                                screenBuffer.blit(currentTileImage, (x, y - dimensions[1] + tileSize[1]))
                                y += 8

                            continue
                        else:
                            currentTileImage = pygame.image.load(currentTile.image).convert_alpha()

                    #handle standards
                    elif currentTile.type == "standard":
                        currentTileCoords = tuple(8*num for num in currentTile.coords)
                        currentTileImage = pygame.Surface(currentTile.size, pygame.SRCALPHA)
                        currentTileImage.blit(standardTileset, (0, 0), (currentTileCoords + currentTile.size))

                            #draws the no texture file if the tile is completely transparent
                        allEmpty = True
                        surfaceArray = numpy.matrix(pygame.surfarray.pixels_alpha(currentTileImage))
                        for surfx in range(len(surfaceArray)):
                            for surfy in range(len(surfaceArray)):
                                if surfaceArray.item(surfx,surfy) != 0:
                                    allEmpty = False
                        if allEmpty:
                            currentTileImage = pygame.image.load(noTextureImage).convert_alpha()
                    
                    #handle entities
                    elif currentTile.type == "entity":
                        if y <= 59*8:
                            currentTileCoords = tuple(48*num for num in currentTile.coords)
                            dimensions = currentTile.size
                            currentTileImage = pygame.Surface(dimensions, pygame.SRCALPHA)
                            currentTileImage.blit(entityTileset, (0, 0), (currentTileCoords + dimensions))

                            if (i % lineWidth) != (lineWidth-1):
                                x = (i % lineWidth)*8
                                screenBuffer.blit(currentTileImage, (x - (dimensions[0]/2), y - dimensions[1] + tileSize[1]))

                            else:
                                x = (i % lineWidth)*8
                                screenBuffer.blit(currentTileImage, (x - (dimensions[0]/2), y - dimensions[1] + tileSize[1]))
                                y += 8

                            continue
                        else:
                            currentTileImage = pygame.image.load(currentTile.image).convert_alpha()
                    
                        
                else:
                    #undefined tile displayed for anything not yet handled
                    undefinedTile = tileList[0]
                    currentTileImage = pygame.image.load(undefinedTile.image).convert_alpha()
            
    

                #updates tile location and draws
                if (i % lineWidth) != (lineWidth-1):
                    x = (i % lineWidth)*8
                    screenBuffer.blit(currentTileImage, (x,y))

                else:
                    x = (i % lineWidth)*8
                    screenBuffer.blit(currentTileImage, (x,y))
                    y += 8

        #after the main tilebuffer, append the additional tile buttons from the button list to the screen buffer

        return(screenBuffer)
