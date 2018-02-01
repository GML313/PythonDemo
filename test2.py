#coding:utf-8
import re
import random
class Solution(object):
    def twoSum(self,nums,target):
        for i in range(nums.__len__()):
            for j in range(i):
                if nums[i]+nums[j] == target:
                    return [j,i]
    def reverse(self,x):
        if x == 0: return 0
        else:
            tmp = str(x)
            if tmp[0] == '-':
                flag = '-';
                tmp = tmp[1:]
            else:
                flag = ''
            str_len = len(tmp)-1
            while tmp[str_len] == '0':
                tmp = tmp[:str_len]
                str_len -= 1
            if int(tmp[::-1]) < int(0x7fffffff):
                return int(flag+tmp[::-1])
            else:
                return 0
    def maxArea(self, s):
        i = 0
        j = len(s)-1
        water = 0
        while i < j:
            h = min(s[i],s[j])
            water = max(water,(j-i)*h)
            while s[i] <= h and i < j: i += 1
            while s[j] <= h and i < j: j -= 1
        return water
    def test(self):
        pattern = re.compile(r'\d{2,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}')
        result =  re.search(pattern,'192.13.2.90:9000')
        print type(result),result.group()
        tmp = None
        if not tmp : print 123;
        else: print 'None'
        open_proxy = open('proxy_url.txt','r')
        proxy_tmp = open_proxy.readlines()
        open_proxy.close()
        one_proxy = random.choice(proxy_tmp)
        proxies = {"http:": ('http://' + one_proxy).replace("\n","")}
        print proxies

if __name__ == "__main__":
    test1 = Solution()
    #print test1.twoSum([3,2,4],6)
    print test1.reverse(1563847412)
    print test1.maxArea([1,2,4,2,3])
    test1.test()