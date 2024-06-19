class Solution:
    def climbStairs(self, n: int) -> int:
        o, p, q = 0, 0, 1
        for i in range(1, n+1):
            o, p = p, q
            q = o + p
        return q

if __name__ == '__main__':
    s = Solution()
    print(s.climbStairs(3))