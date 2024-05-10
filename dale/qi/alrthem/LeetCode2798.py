class Solution:
    def numberOfEmployeesWhoMetTarget(self, hours: list[int], target: int) -> int:
        i=0
        for hour in hours:
            if hour > target:
                i+=1
        return i
s=Solution()
print(s.numberOfEmployeesWhoMetTarget([5,1,4,2,2],2))