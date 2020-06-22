import re

def Func01():
    testText = '36 79'
    pattern = re.compile(r'([1-9]\d?|0) ([1-9]\d?|0)')
    searchResult = pattern.search(testText)
    print('匹配结果: ' + searchResult.group())
    print('匹配结果: 数字1:' + searchResult.group(1) + ' 数字2:' + searchResult.group(2))

Func01()