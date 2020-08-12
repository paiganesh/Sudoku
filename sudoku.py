"""
Description:
Finds all possible solution of a Sudoku problem
Developed By: Ganesh Pai
"""
import numpy as np
import time

class Sudoku:
    solutionList = []

    def __init__(self, table):
        self.grid = table.copy()
        self.zeroList = []
        start = time.time()
        self.__solveSudoku__()
        end = time.time()
        self.computationTime = end - start

    def getComputationTime(self):
        return str(self.computationTime) + "s"

    def __solveSudoku__(self):
        self.__fillZeroList__(self.grid)
        self.__solveSingulars__(self.grid, self.zeroList)  #zeroList is updated and stops at end/at conflict
        if len(self.zeroList) == 0: #if no conflict and reached end
            Sudoku.solutionList.append(self.grid.copy())
        else:                       #if conflict occured
            self.__solveConflicts__(self.grid.copy(), self.zeroList.copy())

    def __fillZeroList__(self, grid):
        for x in range(9):
            for y in range(9):
                if grid[x, y] == 0:
                    self.zeroList.append((x, y))

    __getPossibleCellValues__ = lambda grid, x, y: list({1,2,3,4,5,6,7,8,9} - (set(grid[x]) | set(grid[:, y]) | set(grid[x // 3 * 3:x // 3 * 3+3, y // 3 * 3:y // 3 * 3+3].flatten())))

    def __solveSingulars__(self, grid, zeroList):
        updated = True
        while len(zeroList) > 0 and updated:
            updated = False
            for x, y in zeroList:
                possible = Sudoku.__getPossibleCellValues__(grid, x, y)
                if len(possible) == 1:
                    grid[x, y] = np.int(possible.pop())
                    zeroList.remove((x, y))
                    updated = True

    def __solveConflicts__(self, grid, zeroList):   #received copy of grid n zeroList
        if len(zeroList) > 0:
            grid_ = grid.copy()     #take backup
            x, y = zeroList.pop(0)
            zeroList_ = zeroList.copy()
            for val in Sudoku.__getPossibleCellValues__(grid, x, y):
                grid_[x, y] = val
                self.__solveSingulars__(grid_, zeroList_)
                self.__solveConflicts__(grid_.copy(), zeroList_.copy())
                grid_ = grid.copy()     #restore values
                zeroList_ = zeroList.copy()
        else:
            Sudoku.solutionList.append(grid.copy())

    def __getFormatedTable__(self, x: np.ndarray) -> object:
        soln = "-" * 25 + "\n"
        for i in range(9):
            soln += f"| %d %d %d | %d %d %d | %d %d %d |\n" % tuple(x[i])
            if (i + 1) % 3 == 0: soln += "-" * 25 + "\n"
        return soln

    def __str__(self):
        solutionStr = ""
        if len(self.solutionList) == 0:
            solutionStr = "No Solution exists."
        else:
            for i, solution in enumerate(self.solutionList, start=1):
                solutionStr += "Solution " + str(i) + "\n" + self.__getFormatedTable__(solution) + "\n"

        return solutionStr

    def getSolutionsArray(self):
        return Sudoku.solutionList.copy()

    def printAllSolutions(self):
        print(self.__str__())


if __name__ == "__main__":
     table = [[4, 0, 0, 2, 3, 0, 0, 0, 0],
               [0, 0, 0, 4, 0, 0, 0, 0, 0],
               [7, 0, 9, 0, 0, 1, 0, 6, 4],
    
               [0, 0, 3, 0, 0, 0, 0, 0, 2],
               [8, 0, 0, 0, 6, 0, 0, 9, 0],
               [2, 0, 0, 0, 4, 5, 8, 7, 0],
    
               [0, 4, 0, 7, 0, 8, 0, 0, 3],
               [0, 0, 0, 0, 9, 0, 0, 0, 1],
               [0, 6, 0, 0, 0, 3, 0, 0, 0]]
    
    s = Sudoku(np.array(table))
    print(s)
    print("Time: ", s.getComputationTime())
