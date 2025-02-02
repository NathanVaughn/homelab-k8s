import subprocess

output = subprocess.check_output(
    [
        "kubectl",
        "get",
        "pods",
        "--all-namespaces",
        "-o",
        "jsonpath={.items[*].spec['initContainers', 'containers'][*].image}",
    ]
).decode("utf-8")
# output is space seperated
items = set(output.split(" "))
# create a sorted unique list
print("\n".join(sorted(items)))
