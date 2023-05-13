import random

list_1 = 'あ　い　う　え　お'.split()
ans_1 = 'a i u e o'.split()
raw1 = list(zip(list_1, ans_1))

list_2 = 'か　き　く　け　こ'.split()
ans_2 = 'ka ki ku ke ko'.split()
raw2 = list(zip(list_2, ans_2))

list_3 = 'さ　し　す　せ　そ'.split()
ans_3 = 'sa shi su se so'.split()
raw3 = list(zip(list_3, ans_3))

list_4 = 'た　ち　つ　て　と'.split()
ans_4 = 'ta chi tsu te to'.split()
raw4 = list(zip(list_4, ans_4))

list_5 = 'な　に　ぬ　ね　の'.split()
ans_5 = 'na ni nu ne no'.split()
raw5 = list(zip(list_5, ans_5))

list_6 = 'は　ひ　ふ　へ　ほ'.split()
ans_6 = 'ha hi fu he ho'.split()
raw6 = list(zip(list_6, ans_6))

list_7 = 'ま　み　む　め　も'.split()
ans_7 = 'ma mi mu me mo'.split()
raw7 = list(zip(list_7, ans_7))

list_8 = 'や　い　ゆ　え　よ'.split()
ans_8 = 'ya i yu e yo'.split()
raw8 = list(zip(list_8, ans_8))

list_9 = 'ら　り　る　れ　ろ'.split()
ans_9 = 'ra ri ru re ro'.split()
raw9 = list(zip(list_9, ans_9))

list_a = 'わ　い　う　え　を'.split()
ans_a = 'wa i u e wo'.split()
rawa = list(zip(list_a, ans_a))

test = raw1 + raw2
random.shuffle(test)

count = 0
correct = 0
wrong = 0

for it in test:
    count += 1
    print(f'{count}、', it[0], end=' ')
    c = input(":")
    if c == it[1]:
        print('Yes')
        correct += 1
    else:
        print('No:', it[1])
        wrong += 1

print(f"total:{count}")
print(f"correct:{correct}")
print(f"wrong:{wrong}")
