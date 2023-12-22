"""Map letters from string into dictionary & print bar chart of frequency."""
import sys
import pprint
from collections import defaultdict

# Note: text should be a short phrase for bars to fit in IDLE window
text = 'Like the castle in its corner in a medieval game, I foresee terrible \
trouble and I stay here just the same.'

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

# defaultdict module lets you build dictionary keys on the fly!
mapped = defaultdict(list)
for character in text:
    character = character.lower()
    if character in ALPHABET:
        mapped[character].append(character)

# pprint lets you print stacked output
print("\nYou may need to stretch console window if text wrapping occurs.\n")
print("text = ", end='')
print("{}\n".format(text), file=sys.stderr)
pprint.pprint(mapped, width=110)

# 这段代码的作用是将字符串中每个字母出现的数量映射为一个字典，并将其以柱状图的形式输出。具体实现如下：
#
# ```python
# import sys  # 导入系统模块
# import pprint  # 导入 pretty print 模块用于将结果以更加美观的方式输出
# from collections import defaultdict  # 导入 defaultdict 模块
#
# # 定义输入文本
# text = 'Like the castle in its corner in a medieval game, I foresee terrible trouble and I stay here just the same.'
#
# ALPHABET = 'abcdefghijklmnopqrstuvwxyz'  # 定义英文字母表
#
# # defaultdict 允许在创建字典时给新键一个默认值；此处将默认值设置为列表类型
# mapped = defaultdict(list)  # 创建一个字典，并将每个字母的默认值初始化为空列表
# for character in text:  # 遍历文本中每一个字符
#     character = character.lower()  # 小写化当前字符，以只保留字母的统计
#     if character in ALPHABET:  # 如果当前字符为英文字母
#         mapped[character].append(character)  # 将当前该字母加入它对应的列表里
#
# # pretty print 把字典的key-value打印输出得较为美观；输出结果会根据终端窗口的大小自动调整行宽
# print("\nYou may need to stretch console window if text wrapping occurs.\n")
# print("text = ", end='')
# print("{}\n".format(text), file=sys.stderr)
# pprint.pprint(mapped, width=110)  # 在控制台输出字典数据
#
# ```
#
# 通过 `defaultdict` 建立默认值为列表的字典，各字符的频率被映射到字典的相应条目，作为键值的列表存在，该列表可以用于在柱状图中打印相应的频率。
#
# 另外，值得注意的是，该代码中的 `pprint` 模块可以美化字典的输出，使其更容易阅读和理解，并帮助开发人员在代码调试期间更快地找到问题。 这特别适合于开发人员需要阅读打印输出很多的高复杂度的字典数据结构的情况。