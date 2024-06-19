from typing import List


class Solution:
    def countTestedDevices(self, batteryPercentages: List[int]) -> int:
        n = len(batteryPercentages)
        res = 0
        for i in range(n):
            if batteryPercentages[i] >0:
                res += 1
                for j in range(i+1,n):
                    batteryPercentages[j] =max(batteryPercentages[j]-1,0)
        return res

if __name__ == '__main__':
    s = Solution()
    print(s.countTestedDevices([1,1,2,1,3]))