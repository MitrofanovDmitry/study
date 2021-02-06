import re
fd = open('regex_sum_1109385.txt')
lst = re.findall(r"[0-9]+", fd.read())
print(sum([int(x) for x in lst]))