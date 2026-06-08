import json

from Tile import *

#resources
with open("settings.json") as settings:
    settingsData = json.load(settings)

    scaleFactor = settingsData["screen scale"]
    extraButtonRows = settingsData["extra button rows"]
    lineWidth = 40

    backgroundList = []
    blockList = []
    multiList = []

    tileSize = (8,8)
    spritesheetWidth = int(settingsData["spritesheet dimensions"]["standard tiles"]["dimensions"][0] / tileSize[0])
    spritesheetHeight = int(settingsData["spritesheet dimensions"]["standard tiles"]["dimensions"][1] / tileSize[1])

    for forest in settingsData["resource locations"]["backgrounds"].items():
        backgroundList.append(forest[1])
    for tileMap in settingsData["resource locations"]["blocks"].items():
        blockList.append(tileMap[1])
    for i in range(4):
        multiList.append(settingsData["resource locations"]["multiblocks"]["default"])
    for i in range(2):
        multiList.append(settingsData["resource locations"]["multiblocks"]["holy forest"])
    entityTilesetLocation = settingsData["resource locations"]["entity tileset"]
    iconFile = settingsData["resource locations"]["icon"]
    noTextureImage = settingsData["resource locations"]["no texture"]

#gets all important lists
with open("tiles.json") as tileData:
    tileDict = json.load(tileData)
    
    #make list of tile objects
    tileList = []

    #adding specials
    for i, entry in tileDict["specialTiles"].items():
        Hex = int(entry["hex"], 16)
        Type = "special"
        image = entry["image"]
        coords = "none"
        size = tileSize
        isDrawable = entry["isDrawable"]
        nextAddedTile = Tile(Hex, Type, image, coords, size, isDrawable)
        tileList.append(nextAddedTile)

    #adding multis
    for i, entry in tileDict["multiBlocks"].items():
        Hex = int(entry["hex"], 16)
        Type = "multi"
        image = entry["image"]
        coords = entry["location"]
        size = tuple(8*value for value in entry["dimensions"])
        isDrawable = True
        nextAddedTile = Tile(Hex, Type, image, coords, size, isDrawable)
        tileList.append(nextAddedTile)

    #adding standard
    for spritey in range(spritesheetHeight):
        for spritex in range(spritesheetWidth):
            #standard tiles start with 01 as their first byte and their second byte is ypos,xpos (1,2) would be 0x0121
            Hex = (spritex + 16*spritey + 256) #I LOVE BASE 16!!!!!!!!!!!!!!!!! <-(not factorials)
            Type = "standard"
            image = "none"
            coords = ((spritex, spritey))
            size = tileSize
            isDrawable = True
            nextAddedTile = Tile(Hex, Type, image, coords, size, isDrawable)
            tileList.append(nextAddedTile)

    #adding entities
    for i, entry in tileDict["entities"].items():
        Hex = int(entry["hex"], 16)
        Type = "entity"
        image = entry["image"]
        coords = entry["location"]
        size = (48,48)
        isDrawable = True
        nextAddedTile = Tile(Hex, Type, image, coords, size, isDrawable)
        tileList.append(nextAddedTile)

    #get a list of all used hex values in tile list
    tileHexList = []
    for i in range(len(tileList)):
            tileHexList.append(tileList[i].hex)

    tileData.close()


    