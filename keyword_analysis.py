from konlpy.tag import Okt
from collections import Counter
import csv
f_name = 'C:\\Users\\tlswo\\Documents\\카카오톡 받은 파일\\2021-11-24  16시 33분 47초 merging.csv'
'''
special_char = '\/'
for c in special_char:
    if c in f_name:
        f_name = f_name.replace(c, '/')
'''
f = open(f_name,
         'r', encoding='UTF8')
rr = csv.reader(f)
lines = []
for row in rr:
    # lines.append(row[2])
    lines.append(row[4])

print(lines)
#filename = "C:/Users/tlswo/Desktop/kunghung.txt"
'''
f = open(filename, 'r', encoding='utf-8')
news = f.read()
'''
# okt 객체생성
okt = Okt()
n_list = []
for s in lines:
    noun = okt.nouns(s)

    for i, v in enumerate(noun):
        if len(v) < 2:
            noun.pop(i)
    n_list.extend(noun)


count = Counter(n_list)


# 명사 빈도 카운트
noun_list = count.most_common(100)
for v in noun_list:
    print(v)
'''
# txt 파일에 저장
with open("noun_list.txt", 'w', encoding='utf-8') as f:
    for v in noun_list:
        f.write(" ".join(map(str, v)))
        f.write("\n")'''

# csv 파일 저장
with open('한겨례제목+내용.csv', "w", newline='', encoding='euc-kr') as f:
    csvw = csv.writer(f)
    for v in noun_list:
        csvw.writerow(v)
