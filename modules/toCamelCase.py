def camelCase(name):
    s = name.lower()
    print(s)
    s = s.replace("-", " ").replace("_", " ")
    print(s)
    s = s.split()
    print(s)
    if len(name) == 0:
        return name
    return s[0] + ''.join(i.capitalize() for i in s[1:])