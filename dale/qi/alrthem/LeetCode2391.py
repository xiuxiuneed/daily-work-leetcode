from typing import List

# 给你一个下标从 0 开始的字符串数组 garbage ，其中 garbage[i] 表示第 i 个房子的垃圾集合。garbage[i] 只包含字符 'M' ，'P' 和 'G' ，
# 但可能包含多个相同字符，每个字符分别表示一单位的金属、纸和玻璃。垃圾车收拾 一 单位的任何一种垃圾都需要花费 1 分钟。
#
# 同时给你一个下标从 0 开始的整数数组 travel ，其中 travel[i] 是垃圾车从房子 i 行驶到房子 i + 1 需要的分钟数。
#
# 城市里总共有三辆垃圾车，分别收拾三种垃圾。每辆垃圾车都从房子 0 出发，按顺序 到达每一栋房子。但它们 不是必须 到达所有的房子。
#
# 任何时刻只有 一辆 垃圾车处在使用状态。当一辆垃圾车在行驶或者收拾垃圾的时候，另外两辆车 不能 做任何事情。
#
# 请你返回收拾完所有垃圾需要花费的 最少 总分钟数。

class Solution:
    def garbageCollection(self, garbage: List[str], travel: List[int]) -> int:
        lastM=lastP=lastG=-1
        time=0
        for i in range(len(garbage)):
            if 'M' in garbage[i]:
                lastM=i
            if 'P' in garbage[i]:
                lastP=i
            if 'G' in garbage[i]:
                lastG=i

        for i in range(len(garbage)):
            if lastM!=-1:
                for j in range(len(garbage[i])):
                    if 'M' in garbage[i][j]:
                        time+=1
                lastM-=1
                if lastM != -1:
                    time+=travel[i]
            if lastP!=-1:
                for j in range(len(garbage[i])):
                    if 'P' in garbage[i][j]:
                        time+=1
                lastP-=1
                if lastP != -1:
                    time+=travel[i]
            if lastG!=-1:
                for j in range(len(garbage[i])):
                    if 'G' in garbage[i][j]:
                        time+=1
                lastG-=1
                if lastG != -1:
                    time+=travel[i]
        return time

    def garbageCollection_1(self, garbage: List[str], travel: List[int]) -> int:
        distance = {}
        res = 0
        cur_dis = 0
        for i in range(len(garbage)):
            res += len(garbage[i])
            if i > 0:
                cur_dis += travel[i - 1]
            for c in garbage[i]:
                distance[c] = cur_dis
        return res + sum(distance.values())

    def garbageCollection_2(self, garbage: List[str], travel: List[int]) -> int:
        # 先算出最长路径再去减
        ans = sum(map(len, garbage)) + sum(travel) * 3
        for c in "MGP":
            for g, t in zip(reversed(garbage), reversed(travel)):
                if c in g:
                    break
                ans -= t
        return ans

if __name__ == '__main__':
    sol = Solution()
    print(sol.garbageCollection_1(["G","P","GP","GG"],[2,4,3]))