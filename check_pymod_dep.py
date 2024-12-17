import subprocess
import sys

def get_pip_list() -> list[str]:
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    lines = [l[:l.find(' ')].strip() for l in result.stdout.splitlines()]
    pip_list = []
    for i in range(len(lines)):
        if lines[i].startswith('-'):
            for line in lines[i+1:]:
                pip_list.append(line)
            break
    return pip_list

def get_requires(module: str) -> set[str]:
    show = subprocess.run(["pip", "show", module], capture_output=True, text=True)
    if show.returncode != 0:
        raise Exception(f"コンソールエラー発生: {show.stderr}")
    requires_str = 'Requires:'
    requires = set()
    lines = [l.strip() for l in show.stdout.splitlines()]
    for line in lines:
        if line.startswith(requires_str):
            list_str = line[line.find('Requires:')+len(requires_str)+1:]
            requires = set(list_str.split(', '))
            break
    return requires

if __name__ == '__main__':
    args = sys.argv
    specified_module = args[1] # e.g. requests
    requires_for_specified = get_requires(specified_module)
    pip_list = get_pip_list()
    requires_ex_specified = set()
    for module in pip_list:
        if module != specified_module:
            requires_ex_specified |= get_requires(module)
    print(f'You can delete these modules after you delete {specified_module}:',requires_for_specified - requires_ex_specified)
