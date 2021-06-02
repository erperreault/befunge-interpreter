#!/usr/bin/env python

import sys
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
    with open(sys.argv[1], 'r') as input:
        print(interpret(input.read()))