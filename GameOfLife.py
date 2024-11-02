import multiprocessing
import sys
import os
import copy
from multiprocessing import Pool
def main():
    pNum = 0
    oCount = 0
    runCount = 0
    argLen = len(sys.argv)
    fileCheck = True

    #Gets user arguments from command line
    for x in range(argLen):
        if (sys.argv[x] == '-o'):
            outName = sys.argv[x+1]
        if (sys.argv[x] == '-i'):
            inName = sys.argv[x+1]

        if (sys.argv[x] == '-p'):
            #if no number of processes are not provided it sets it to default which is 1
            if(argLen <= x+1):
                pNum = 1
            else:
                pNum = sys.argv[x+1]

            if(pNum == None):
                pNum = 1
            pNum = int(pNum)
            if(pNum <= 0):
                print("Error threads must be a positive int greater than 0")
                exit(0)
        #sets pnum to the default of 1 if no -p is entered
        if(pNum == 0):
            pNum = 1

    processPool = Pool(processes=pNum)

    #Checks to see if the file path exists and exits if it doesn't exit
    path = inName
    fileCheck = os.path.isfile(path)
    if(fileCheck == False):
        print("File does not exist")
        exit(1)

    filename = open(inName,'r')
    #stores input file into list line by line after converting O to 1 and . to 0 and then stores the list inside another list
    matArray = []
    for line in filename.readlines():
        a = []
        for x in line:
            if(x == 'O'):
                a.append(1)
            elif(x == '.'):
                a.append(0)
            elif(x == '\n'):
                oCount = oCount
            else:
                print("Error: unidentified object in matrix")
                exit(0)
        matArray.append(a)
    filename.close()
    #Gets number of rows and columns of matrix
    horizLength =len(matArray)
    vertLength= len(matArray[0])


    #Process Matrix
    while(runCount < 100):
        poolData = []
        newMat = []
        newMatRow = []

        #moves matrix into a list with the corresponding row that will be processed
        for row in range(horizLength):
            matData = []
            sendRow = 0
            #seperate each array into 3 rows that will be accessed instead of the whole array
            #ensures that 3 row array is put in order if the row being processed is the last
            if(((row+1) % horizLength) == 0):
                matData.append(matArray[0])
                matData.append(matArray[row - 1])
                matData.append(matArray[row])
                sendRow = 2
            #ensures the rows being processed is correct if the row being processed is the first row
            elif(row == 0):
                matData.append(matArray[0])
                matData.append(matArray[row+1])
                matData.append(matArray[horizLength-1])
            else:
                matData.append(matArray[row - 1])
                matData.append(matArray[row])
                matData.append(matArray[row + 1])
                sendRow = 1
            poolData.append([matData, sendRow, row])

        newMatRow = processPool.map(neighbors,poolData)
        #appends row to the newmatrix after being processed. Checks the row to ensure that it's being put in the correct place
        for row in range(horizLength):
            if(newMatRow[row][1] == row):
                newMat.append(newMatRow[row][0])
        # copies the updated array to matArray to be used in the next time step
        matArray = copy.deepcopy(newMat)
        runCount = runCount + 1

    #convert numbered matrix back to O and .
    finalArr = []
    for line in matArray:
        a = []
        for x in line:
            if(x == 1):
                a.append('O')
            if(x == 0):
                a.append('.')
        a.append('\n')
        finalArr.append(a)
    #write output text file
    with open(outName, 'w') as outputFile:
        for row in finalArr:
            outputFile.writelines(row)




def neighbors(matDat):


    horizLength = len(matDat[0])
    vertLength = len(matDat[0][0])

    #row that will be processed
    row = matDat[1]
    #so the program knows where to place the row so it does not get out of order
    placeRow = matDat[2]
    matArray = matDat[0]

    a = []
    for col in range(vertLength):
        oCount = 0
        # Finds value for all 8 neighbors and adds to oCount
        # Uses negative indexing in python to find correct neighbor
        oCount = matArray[row - 1][col - 1]
        oCount = oCount + matArray[row - 1][col]
        oCount = oCount + matArray[row][col - 1]
        # uses modulus to wrap around the array
        oCount = oCount + matArray[row][(col + 1) % vertLength]
        oCount = oCount + matArray[(row + 1) % horizLength][col]
        oCount = oCount + matArray[(row + 1) % horizLength][col - 1]
        oCount = oCount + matArray[(row + 1) % horizLength][(col + 1) % vertLength]
        oCount = oCount + matArray[row - 1][(col + 1) % vertLength]

        if ((matArray[row][col] == 1)):
            # If cell does not have prime number of neighbors then it replaces with dead cell
            if (oCount == 2 or oCount == 3 or oCount == 5 or oCount == 7):
                a.append(1)
            else:
                a.append(0)
        # if a dead cell has a certain number of living neigbors it becomes a living cell
        elif (matArray[row][col] == 0):
            if ((oCount == 1) or (oCount == 3) or (oCount == 5) or (oCount == 7)):
                a.append(1)
            else:
                a.append(0)
    return [a, placeRow]

if __name__ == '__main__':
    main()
