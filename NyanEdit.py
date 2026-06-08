import os
import struct
import pygame
import json

from TileFunctions import *
from ScreenFunctions import *
from GetResources import *

pygame.init()

#get initial tile file
previousTileData = []
tileData = getTileData(tileData, tileList, previousTileData, True)
previousTileData = tileData
#size of each tile is 8x8px, so the whole screen should be 40x60 tiles or 320x480px plus some room for the editor tiles, save button, and swap bg button

#screenbuffer
(bufferWidth, bufferHeight) = (320, 480 + 8*extraButtonRows)
screenBuffer = pygame.Surface((bufferWidth, bufferHeight))

#screen
(width, height) = (scaleFactor*320, scaleFactor*(480 + 8*extraButtonRows))
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("NyanEdit")
icon = pygame.image.load(iconFile)
pygame.display.set_icon(icon)
updateBackground(backgroundList[1], screenBuffer, bufferWidth, bufferHeight - 8*extraButtonRows)
updateFlag = True
currentForest = 0

#dummy event so things dont update every frame
nothingEverHappens = pygame.event.Event(0)


#define buttonList
buttonData = getButtonData(tileList, extraButtonRows, lineWidth)
selectedButton = 0x0000 #air

#setup tile buffer
tileBuffer = Tilemap(tileList, tileData, currentForest, bufferWidth, bufferHeight, extraButtonRows)

running = True
while running:

    #handle closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if askForSave():
                    if not saveFile(tileData):
                        displayCantSave()
                        continue
            running = False
    
    #background swap
    if event.type == pygame.MOUSEBUTTONUP:

        updateFlag = True

        tileClickPos = tuple((int(n/(scaleFactor*8))) for n in pygame.mouse.get_pos())
        previousSelected = selectedButton
        if tileClickPos[1] <= 59: #within main tilemap
            if tileList[tileHexList.index(selectedButton)].drawable:
                tileData = editTile(tileClickPos, selectedButton, tileData)

        else: #within button map

            selectedButton = getClickedButton(tileClickPos, buttonData, selectedButton)

            #this code should only occur if you clicked the swap bg button
            if selectedButton == 0xFFFD: #swap bg
                if currentForest != len(backgroundList)-1:
                    currentForest += 1
                else:
                    currentForest = 0
                selectedButton = previousSelected

            elif selectedButton == 0xFFFE: #save
                if not saveFile(tileData):
                    displayCantSave()

                selectedButton = previousSelected

            elif selectedButton == 0xFFFC: #load file again

                if askForSave():
                    if not saveFile(tileData):
                        displayCantSave()
                        
                tileData = getTileData(tileData, tileList, previousTileData, False)
                previousTileData = tileData
                
                selectedButton = previousSelected

    pygame.event.post(nothingEverHappens)

    #update tileBuffer vars
    tileBuffer.currentForest = currentForest
    tileBuffer.tileData = tileData + buttonData

    #display tiles
    if updateFlag:
        updateBackground(backgroundList[currentForest], screenBuffer, bufferWidth, bufferHeight - 8*extraButtonRows)
        screenBuffer = tileBuffer.getTileBuffer(tileList, screenBuffer)
        
        scaledBuffer = pygame.transform.scale(screenBuffer, (width, height))
        screen.blit(scaledBuffer, (0,0))
        updateFlag = False

    #display buttons
    
    pygame.display.flip()
