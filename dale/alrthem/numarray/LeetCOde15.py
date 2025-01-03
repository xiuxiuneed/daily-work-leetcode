from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()  # 对数组进行排序以方便后续操作
        result = []
        length = len(nums)

        for i in range(length):
            # 如果当前值大于0，则之后的值也必然大于0，因为数组已经排序，所以直接返回结果
            if nums[i] > 0:
                break

            # 跳过重复元素，避免产生重复的结果
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, length - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1  # 需要更大的数，移动左指针
                elif total > 0:
                    right -= 1  # 需要更小的数，移动右指针
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    # 跳过所有重复的left和right，以避免重复的答案
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1

        return result

nums = [-1,0,1,2,-1,-4]
sulo = Solution()
a = sulo.threeSum(nums)
print(a)
