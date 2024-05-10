# 给定一个含有n个正整数的数组和一个正整数target 。找出该数组中满足其总和大于等于target的长度最小的连续子数组
# [numsl, numsl + 1, ..., numsr - 1, numsr] ，并返回其长度。如果不存在符合条件的子数组，返回0 。
# 示例
# 1：输入：target = 7, nums = [2, 3, 1, 2, 4, 3]
# 输出：2
# 解释：子数组[4, 3]
# 是该条件下的长度最小的子数组。
# 示例
# 2：输入：target = 4, nums = [1, 4, 4]
# 输出：1
# 示例
# 3：输入：target = 11, nums = [1, 1, 1, 1, 1, 1, 1, 1]
# 输出：0
from typing import List


class Solution:
    def minSubArrayLen_Force(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        m = n+1
        if n == 0:
            return 0
        for i in range(n):
            sum=0
            for j in range(i,n):
                sum+=nums[j]
                if sum>=target:
                    if j - i + 1 < m:
                        m = j - i + 1
        if m == n+1:
            m=0
        return m
    def minSubArrayLen_Swindow(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        i = 0
        result=n+1
        sum = 0
        for j in range(n):
            sum+=nums[j]
            while sum>=target:
                result=min(result,j-i+1)
                sum-=nums[i]
                i+=1
        return 0 if result==n+1 else result
target = 7
nums = [2, 3, 1, 2, 4, 3]
print(Solution().minSubArrayLen_Swindow(target, nums))