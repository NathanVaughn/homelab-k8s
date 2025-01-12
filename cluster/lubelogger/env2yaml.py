with open("temp.env", "r") as fp:
    lines = fp.readlines()

with open("temp.yaml", "w") as fp:
    for line in lines:
        split = line.split("=", maxsplit=1)
        name = split[0]
        value = split[1].strip()

        if value[0] != '"' and value[-1] != '"':
            value = f'"{value}"'

        fp.write(f"- name: {name}\n")
        fp.write(f"  value: {value}\n")
