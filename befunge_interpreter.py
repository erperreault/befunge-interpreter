from random import choice

def interpret(original):    
    code = [list(line) for line in original.split('\n')]
    x = 0
    y = 0
    direction = '>'
    stringmode = False
    stack = []
    output = ''

    while True:
        command = code[y][x]
        step = 1

        if stringmode:
            if command == '"':
                stringmode = False
            else:
                stack.append(ord(command))

        elif command.isdigit():
            stack.append(int(command))
        elif command in '+-*/%':
            a, b = stack.pop(), stack.pop()
            if command == '+':
                stack.append(a+b)
            elif command == '-':
                stack.append(b-a)
            elif command == '*':
                stack.append(a*b)
            elif command == '/':
                stack.append(b/a)
            elif command == '%':
                stack.append(b%a)
        elif command == '!':
            stack.append(stack.pop() == 0)
        elif command == '`':
            a, b = stack.pop(), stack.pop()
            stack.append(b>a)
        elif command == '?':
            direction = choice('^v><')
        elif command in '><^v':
            direction = command
        elif command == '_':
            direction = '<' if stack.pop() else '>'
        elif command == '|':
            direction = '^' if stack.pop() else 'v'
        elif command in '"':
            stringmode = True
        elif command == ':':
            stack.append(stack[-1] if stack else 0)
        elif command == '\\':
            stack.extend((stack.pop(), stack.pop()))
        elif command == '$':
            stack.pop()
        elif command == '.':
            output += str(stack.pop())
        elif command == ',':
            output += chr(stack.pop())
        elif command in '#':
            step = 2
        elif command == 'p':
            temp_y, temp_x, v = stack.pop(), stack.pop(), stack.pop()
            code[temp_y][temp_x] = chr(v)
        elif command == 'g':
            temp_y, temp_x = stack.pop(), stack.pop()
            stack.append(ord(code[temp_y][temp_x]))
        elif command == '@':
            return output

        if direction == '^':
            y = (y-step) % len(code)
        elif direction == 'v':
            y = (y+step) % len(code)
        elif direction == '<':
            x = (x-step) % len(code[y])
        elif direction == '>':
            x = (x+step) % len(code[y])

if __name__ == '__main__':
    assert interpret(">987v>.v\nv456<  :\n>321 ^ _@") == "123456789"
    assert interpret('>25*"!dlroW olleH":v\n                v:,_@\n                >  ^') == "Hello World!\n"
    assert interpret("08>:1-:v v *_$.@ \n  ^    _$>\:^") == "40320"
    assert interpret("01->1# +# :# 0# g# ,# :# 5# 8# *# 4# +# -# _@") == "01->1# +# :# 0# g# ,# :# 5# 8# *# 4# +# -# _@"
    assert interpret(R"""2>:3g" "-!v\  g30          <
 |!`"&":+1_:.:03p>03g+:"&"`|
 @               ^  p3\" ":<
2 2345678901234567890123456789012345678
32""")