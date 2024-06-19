from typing import List
import numpy as np

# 给你一个正整数 n ，生成一个包含 1 到 n2 所有元素，且元素按顺时针顺序螺旋排列的 n x n 正方形矩阵 matrix 。

class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        # nums = np.zeros((n, n), dtype=int)
        nums=[[0 for _ in range(n)] for _ in range(n)]
        startx,starty,count,offset,t=0,0,1,1,n//2
        while t>0:
            for j in range(starty,n-offset):
                nums[startx][j]=count
                count+=1
            j+=1
            for i in range(startx,n-offset):
                nums[i][j]=count
                count+=1
            i+=1
            while j>starty:
                nums[i][j]=count
                count+=1
                j-=1
            while i>startx:
                nums[i][j]=count
                count+=1
                i-=1
            startx+=1
            starty+=1
            offset+=1
            t-=1
        if n%2==1:
            nums[n//2][n//2]=count
        return nums

if __name__=='__main__':
    print(Solution().generateMatrix(5))