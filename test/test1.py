
def hexToString(str):
    str_list = list(str)
    if len(str_list) == 3:
        str_list.insert(2, '0')
    return "".join(str_list[2:])
print(hexToString('0x0'))
print("".join((hexToString(hex(30)),"sss",hexToString('0x0'),'FF00')))
print("".join(("1","2","3")))