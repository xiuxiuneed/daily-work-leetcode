class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[0]*n]*m #dp[i][j]表示到第i行j列的路径个数
        for i in range(0, m):
            dp[i][0]=1
        for j in range(1, n):
            dp[0][j]=1
        for i in range(1,m):
            for j in range(1,n):
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        return dp[m-1][n-1]



s = Solution()
print(s.uniquePaths(3,7))