from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        dp = [0] * (n + 1)
        for i in range(2, n + 1):
            dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
        return dp[n]


if __name__ == '__main__':
    s = Solution()
    cost = [1,100,1,1,1,100,1,1,100,1]
    print(s.minCostClimbingStairs(cost))