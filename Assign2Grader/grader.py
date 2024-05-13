import os
import subprocess
import re
import csv
import time


def jplag() -> bool:
    try:
        subprocess.check_output(['java', '-jar', 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\jplag.jar',
                                 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\Assign3Grader\\StudentSubmissions',
                                 '-l', 'python3', '-r', 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\jplag.jar',
                                 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\Assign3Grader\\assign2results'],
                                stderr=subprocess.STDOUT, timeout=60).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False
    except subprocess.CalledProcessError as e:
        return False

    return True


def get_fitness(matrix: list[list[int]]) -> int:
    fit: int = 0
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                for k in range(1, len(matrix[0]) - i):
                    if matrix[i + k][j] == 1:
                        fit += 1
                    if j - k >= 0 and matrix[i + k][j - k] == 1:
                        fit += 1
                    if j + k < len(matrix[0]) and matrix[i + k][j + k] == 1:
                        fit += 1
    return fit


def parse_output(student_output: str, student: str) -> list[list[int]]:
    split: list[str] = student_output.split('\n')
    matrix: list[list[int]] = [[1 for j in range(5)] for i in range(5)]
    try:
        for i, line in enumerate(split):
            line = re.sub(r'\s|\[|\,|\]', '', line).lower()
            if 'run' in line or 'time' in line or 'exec' in line or len(line) == 0:
                continue
            for j, char in enumerate(line):
                if char != '1':
                    matrix[i - 1][j - 1] = 0
    except Exception as e:
        print(f'Error for {student}: {e}: {split}')
    return matrix


def test_app(filename: str, student: str) -> tuple[bool, str]:
    try:
        output: str = subprocess.check_output(['python', 'StudentSubmissions\\' + filename, '5', '5'],
                                              stderr=subprocess.STDOUT, timeout=5).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False, 'timedout'
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')

    if output.isspace():
        return False, ''
    return get_fitness(parse_output(output, student)) == 0, output


def merge_map(map1: dict[str, list[str]], map2: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = dict()
    diff_keys = set(map2.keys()).difference(map1.keys())

    for key in diff_keys:
        merged[key] = map2[key][:3] + ['Missing', 'Missing', 'Missing', 'Missing', 'Missing', 'Missing'] + map2[key][3:]

    for key in map1.keys():
        merged_list = map1[key]
        if key in map2:
            merged_list += map2[key][3:]
        else:
            merged_list += ['Missing', 'Missing', 'Missing', 'Missing', 'Missing', 'Missing']
        merged[key] = merged_list

    return merged


def main():
    jplag()
    hill_map: dict[str, list[str]] = dict()
    gen_map: dict[str, list[str]] = dict()
    for filename in os.listdir('./StudentSubmissions'):
        if filename.endswith(".py") and filename != "board.py":
            name, number, id, hil_or_gen = filename.split('_')
            t1a, t1b = test_app(filename, name)
            time.sleep(1)
            t2a, t2b = test_app(filename, name)
            time.sleep(1)
            t3a, t3b = test_app(filename, name)

            if 'hill' in hil_or_gen:
                hill_map[name] = [name, number, id, t1a, t1b, t2a, t2b, t3a, t3b]
            else:
                gen_map[name] = [name, number, id, t1a, t1b, t2a, t2b, t3a, t3b]

    with open('gradedResults.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        merged: dict[str, list[str]] = merge_map(hill_map, gen_map)
        for keys in merged.keys():
            writer.writerow(merged[keys])


main()
