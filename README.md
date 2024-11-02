# Game-of-Life
Simulates changes in cells given by an initial matrix and changes through 100 iterations. Matrix size is variable and was tested against sizes as large as 100000x100000 which necessitated the implementation of multiprocessing. 

Game of Life Rules:
1) Any position in the matrix with a period ‘.’ is considered “dead” during the current time step.
2) Any position in the matrix with a capital letter ‘O’ is considered “alive” during the current time step.
3) If an “alive” square has a prime number of living neighbors, then it will be “alive” in the next time step.
4) If a “dead” square has 1, 3, 5, or 7 living neighbors, then it will be “alive” in the next time step.
5) Every other square dies or remains dead, causing it to be “dead” in the next time step.
   
Example execution in command prompt:
python3 GameOfLife.py -i inputFile.txt -o timeStep100.txt -p 36
python file, input file name, output file name, number of processes (default is 1 if none are specified.)
