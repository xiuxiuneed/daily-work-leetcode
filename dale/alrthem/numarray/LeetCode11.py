from typing import List
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height)-1
        cap =0
        while left < right:
            width = right-left
            tmp = min(height[left],height[right])*width
            cap =max(tmp,cap)
            if height[left]<height[right]:
                left+=1
            else:
                right-=1
        return cap

height = [1,8,6,2,5,4,8,3,7]
solu = Solution()
a = solu.maxArea(height)
print(a)