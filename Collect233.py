# -*- coding: utf-8 -*-

__author__ = 'eraserking'

import sys
import matplotlib.pyplot as plt

height = 20
width = 80


def parseXmlFile(fileName):
    countBySecond = {}

    fileHandler = open(fileName, 'r', encoding='utf-8', errors='ignore')
    fileLines = fileHandler.readlines()
    fileHandler.close()
    for fileLine in fileLines:
        if fileLine.startswith('<d '):  # This line is a comment
            timeInString = fileLine[fileLine.find('"') + 1: fileLine.find(',')]
            if timeInString.find('.') != -1:
                timeInString = timeInString[:timeInString.find('.')]
            comment = fileLine[fileLine.find('>') + 1: fileLine.rfind('<')]

            if comment.find('233') != -1 or comment.find('哈哈') != -1 or comment.find('hhhh') != -1:
                time = int(timeInString)
                if time not in countBySecond.keys():
                    countBySecond[time] = 0
                countBySecond[time] = countBySecond[time] + 1

    # We have created a table with 233 count by second.
    # But it's too wide. We need to combine.
    totalTimeInSecond = getLastSecond(countBySecond)

    # Normally maximum count is less than 3 digits, so minus 5 is enough
    countByPeriod = combineTimePeriod(countBySecond, totalTimeInSecond, width - 5)

    drawCount(countByPeriod, totalTimeInSecond)

    # Then we generate time table by 15 seconds
    countByPeriod = combineTimePeriod(countBySecond, totalTimeInSecond, totalTimeInSecond // 15)

    drawFigure(countByPeriod, fileName)


def drawFigure(countByPeriod, title):
    plt.figure(figsize=(15, 8))
    plotX = sorted(countByPeriod.keys())
    plotY = [countByPeriod[x] for x in plotX]
    plt.plot(plotX, plotY)
    # Set texts
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.title(title)
    # Set plot X axis texts (by minute)
    plotX = [x for x in plotX if x % 60 == 0]
    plt.xticks(plotX, [x // 60 for x in plotX])
    plt.show()


def getLastSecond(countBySecond):
    lastSecond = 0
    for second in countBySecond.keys():
        if second > lastSecond:
            lastSecond = second
    return lastSecond


def convertToMinuteSecond(secondCount):
    minute = secondCount // 60
    second = secondCount % 60
    return ('{:02}:{:02}'.format(minute, second))


def combineTimePeriod(countBySecond, totalTimeInSecond, arrayLength):
    countByPeriod = {}
    timePiece = totalTimeInSecond // arrayLength

    for i in range(arrayLength):
        countByPeriod[i * timePiece] = 0
        for second in countBySecond.keys():
            if (i * timePiece) <= second < ((i + 1) * timePiece):
                countByPeriod[i * timePiece] = countByPeriod[i * timePiece] + countBySecond[second]

    return (countByPeriod)


def drawCount(countByPeriod, totalTimeBySecond):
    arrayWidth = len(countByPeriod)
    sortedKeys = sorted(countByPeriod.keys())
    graphArray = []

    maxCount = 0
    for countKey in countByPeriod.keys():
        if countByPeriod[countKey] > maxCount:
            maxCount = countByPeriod[countKey]
    countPiece = maxCount // (height - 1)

    for i in range(0, height):
        line = ('{:>' + str(len(str(maxCount))) + '}|').format(str(i * countPiece))  # Set column header
        for piece in sortedKeys:
            if countByPeriod[piece] > i * countPiece:
                line = line + '#'
            else:
                line = line + ' '
        graphArray.insert(0, line)  # Insert to the first line since we create lines from the least maximum count

    graphArray.append(' ' * len(str(maxCount)) + '+' + '-' * arrayWidth)

    maxMinute = totalTimeBySecond // 60
    maxMinuteLength = len(str(maxMinute))

    # Write minute line
    line = ' ' * (len(str(maxCount)) + 1)
    for j in range(len(sortedKeys) // (maxMinuteLength + 1)):
        line = line + '{:02}'.format(sortedKeys[j * (maxMinuteLength + 1)] // 60) + ' '
    graphArray.append(line)

    # Write second line
    line = ' ' * (len(str(maxCount)) + 1)
    for j in range(len(sortedKeys) // (maxMinuteLength + 1)):
        line = line + '{:02}'.format(sortedKeys[j * (maxMinuteLength + 1)] % 60) + ' '
    graphArray.append(line)

    for line in graphArray:
        print(line)


if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print('USAGE: Collect233.py <XML file name>')
    parseXmlFile(sys.argv[1])
