import randomness_check
import os


def show():
    print('1.频数检测')
    print('2.poke检测')
    print('3.游程检测')
    print('4.二元推导检测')
    print('5.自相关检测')


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_bit(s):
    try:
        int(s, 2)
        return True
    except ValueError:
        return False


def get_data(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as f:
        z = f.read().strip()
        if is_bit(z):
            return z, False
        else:
            print('数据错误，数据请选择二进制序列，请勿加其他符号。')
            return None, True


def main():
    print('欢迎使用随机性检测程序，该程序提供以下检测方案：')
    show()
    print('##  请将检测数据以二进制序列存储于txt文件（UTF-8）中，并保存于该程序同目录。  ##')
    print('##  请输入检测方案前数字来选择使用的方案，输入all使用所有程序进行检测，输入help查看方案种类，输入quit退出程序。  ##')
    while True:
        while True:
            file_name = input("输入数据文件名或退出（quit）：").strip()
            if file_name == 'quit':
                print('程序结束')
                return 0
            if os.path.exists(file_name):
                data = get_data(file_name)
                if data[1]:
                    continue
                else:
                    z = data[0]
                    if len(z) < 100:
                        print('数据量过低（小于100）')
                        continue
                    else:
                        break
            else:
                print('文件不存在，请输入正确的文件名。')

        while True:
            choice = input("选择方案，请求帮助（help），或退出（quit）：").strip()
            if choice == 'quit':
                print('程序结束')
                return 0
            elif choice == 'help':
                show()
                continue
            elif choice == 'all':
                # 频数检测
                print("频数检验".center(75, '='))
                print(randomness_check.f_check(z))

                # poke检测
                print("扑克检验".center(75, '='))
                print(randomness_check.poke_check(z))

                # 游程检测
                print("游程检测".center(75, '='))
                print(randomness_check.R_check(z))

                # 二元推导检测
                print("二元推导检测".center(75, '='))
                print(randomness_check.bd_check(z))

                # 自相关检验
                print("自相关检测".center(75, '='))
                print(randomness_check.a_check(z))
                break
            else:
                if is_number(choice):
                    choice = int(choice)
                    if 1 <= choice <= 5:
                        if choice == 1:
                            print("频数检验".center(75, '='))
                            print(randomness_check.f_check(z))
                            break
                        elif choice == 2:
                            print("扑克检验".center(75, '='))
                            print(randomness_check.poke_check(z))
                            break
                        elif choice == 3:
                            print("游程检测".center(75, '='))
                            print(randomness_check.R_check(z))
                            break
                        elif choice == 4:
                            print("二元推导检测".center(75, '='))
                            print(randomness_check.bd_check(z))
                            break
                        else:
                            print("自相关检测".center(75, '='))
                            print(randomness_check.a_check(z))
                            break
                    else:
                        print('输入错误...')
                else:
                    print('输入错误，', end='')

        print('检测结束。')


if __name__ == "__main__":
    main()
