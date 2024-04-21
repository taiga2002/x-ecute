import re

def splitter(text, num):
    # Split on '\n' only when not followed by ' '
    parts = re.split(r'\n(?!\s)', text)
    for i in range(len(parts)):
        if i > 0 and len(parts[i]) > 4 and ("else" == parts[i][0:4] or "elif" == parts[i][0:4]) and parts[i-1]:
            parts[i] = []
            continue
        adder = []
        # print([parts[i]])
        while '\n' in parts[i]:
            parts[i] = extracter(parts[i], str(num))
            if len(parts[i]) > 1:
                for j in range(len(parts[i])):
                    if j > 0 and len(parts[i][j]) > 4 and ("else" == parts[i][j][0:4] or "elif" == parts[i][j][0:4]) and adder[j-1]:
                        adder.insert(0, [])
                        continue
                    adder = adder + splitter(parts[i][j], num + 2)
        if adder:
            parts[i] = adder
            parts[i] = flatten_list(parts[i])
    # print(parts)
    return parts

def extracter(text, num):
    inner = re.split(r'\n(?=\s{'+ num + '}[^ ])', text)
    # print(inner)
    cont = evaluate(inner[0])
    if not cont:
        return []
    inner = inner[1:]
    for i in range(len(inner)):
        inner[i] = inner[i].strip()
    return inner

def evaluate(text):
    # print(text)
    andSplit = re.split(r'\s+(and|or)\s+', text)
    
    result = andSplit

    # print(result)
    output = False
    if len(result) > 1:
        for i in range(len(result)):
            if result[i] == 'and':
                return evaluate(result[i-1]) and evaluate(result[i+1])
            if result[i] == 'or':
                if evaluate(result[i-1]) or evaluate(result[i+1]):
                    return True
            
    tok = re.split(r'\s+(==|>|>=|<|<=)\s+', text)
    if len(tok) == 1:
        return True
    left = tok[0]
    if "elif" in left:
        left = left[5:]
    if "if" in left:
        left = left[3:]
    left = reduce(left)
    right = tok[2]
    right = reduce(right)
    if tok[1] == "==":
        if left == right:
            return True
    if tok[1] == ">":
        if left > right:
            return True
    if tok[1] == ">=":
        if left >= right:
            return True
    if tok[1] == "<":
        if left < right:
            return True
    if tok[1] == "<=":
        if left <= right:
            return True
    return False

def reduce(text):
    if text[0] == '\"':
        return text[1:len(text) - 2]
    if text == "True":
        return True
    if text == "False":
        return False
    output = ""
    tok = text.split(' ')
    for token in range(len(tok)):
        if tok[token] == '+':
            if output:
                output = str(int(output) + int(tok[token + 1]))
            else:
                output = str(int(tok[token - 1]) + int(tok[token + 1]))
        elif tok[token] == '-':
            if output:
                output = str(int(output) - int(tok[token + 1]))
            else:
                output = str(int(tok[token - 1]) - int(tok[token + 1]))
        elif tok[token] == '*':
            if output:
                output = str(int(output) * int(tok[token + 1]))
            else:
                output = str(int(tok[token - 1]) * int(tok[token + 1]))
        elif tok[token] == '//':
            if output:
                output = str(int(output) // int(tok[token + 1]))
            else:
                output = str(int(tok[token - 1]) // int(tok[token + 1]))
        elif tok[token] == '%':
            if output:
                output = str(int(output) % int(tok[token + 1]))
            else:
                output = str(int(tok[token - 1]) % int(tok[token + 1]))
    if not output:
        try:
            x = int(text)
            return x
        except:
            return text
    return int(output)

def flatten_list(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

if __name__ == "__main__":
    split = splitter("if 4 + 3 == 12 - 4 and 4 == 14 % 5 or 5 == 3\n  fn()\n  if 3 * 6 == 54 // 3 and \"abc\" <= \"abd\"\n    fn2()\n    if False == True\n      fn4()\n    elif True == True and 4 == 4\n      fn5()\n    else\n      fn6()\nelif 4 == 4\n  fn3()", 2)
    split = flatten_list(split)
    print(split)

"""
if 4 + 3 == 12 - 4 and 4 == 14 % 5 or 5 == 3
  fn()
  if 3 * 6 == 54 // 3 and "abc" <= "abd"
    fn2()
    if False == True
      fn4()
    elif True == True and 4 == 4
      fn5()
    else
      fn6()
elif 4 == 4
  fn3()
"""