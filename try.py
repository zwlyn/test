def calc():
    num1 = input('请输入第一个参数：')
    num2 = input('请输入第二个参数：')
    try:
        answer = float(num1) / float(num2)
    except ZeroDivisionError as e:
        print('除数不可以为0')
    else:                        # 当不走 except 时才走else
        print(answer)  


if __name__ == '__main__':
    calc()