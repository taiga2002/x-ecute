import re

def splitter(text, num):
    # Split on '\n' only when not followed by ' '
    parts = re.split(r'\n(?!\s)', text)
    for i in range(len(parts)):
        adder = []
        # print([parts[i]])
        while '\n' in parts[i]:
            parts[i] = extracter(parts[i], str(num))
            for j in parts[i]:
                adder = adder + splitter(j, num + 2)
        if adder:
            parts[i] = adder
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
    left = tok[0]
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
    split = splitter("if 5 + 3 == 12 - 4 and 4 == 14 % 5 or 5 == 3\n  fn()\n  if 3 * 6 == 54 // 3 and \"abc\" <= \"abd\"\n    fn2()\n    if True == True\n      fn4()\nif 4 == 4\n  fn3()", 2)
    split = flatten_list(split)
    print(split)

# if 5 == 5 and 4 == 4 or 5 == 3
#     fn()
#     if 3 == 3 and b <= a
#         fn2()
#         if True == True
#            fn4()
# if 4 == 4
#     fn3()