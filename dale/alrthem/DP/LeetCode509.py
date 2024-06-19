class Solution:
    def fib(self, n: int) -> int:
        if n < 2:
            return n

        o, p, q = 0, 0, 1
        for i in range(2, n + 1):
            o, p = p, q
            q = o + p
        return q

if __name__ == '__main__':
    s = Solution()
    print(s.fib(3))