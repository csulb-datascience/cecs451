import os
import subprocess
import re
import csv

a_answers: list[list[float]] = [[0.8780, 0.1220],
                                [0.3103, 0.6897],
                                [0.9863, 0.0137],
                                [0.8180, 0.1820]]

b_answer_matrix: list[list[float]] = [[0.9321, 0.0069, 0.0610, 0.0000],
                                      [0.4931, 0.1620, 0.0000, 0.3449],
                                      [0.4390, 0.0000, 0.4701, 0.0909],
                                      [0.0000, 0.1550, 0.4090, 0.4360]]

c_answer_matrix: list[list[float]] = [[0.8562, 0.1438, 0.0],
                                      [0.8800, 0.1200, 3.32],
                                      [0.8640, 0.1360, 0.45],
                                      [0.8720, 0.1280, 0.19],
                                      [0.8740, 0.1260, 0.01]]


def jplag() -> bool:
    try:
        subprocess.check_output(['java', '-jar', 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\jplag.jar',
                                 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\Assign4Grader\\StudentSubmissions',
                                 '-l', 'python3', '-r', 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\jplag.jar',
                                 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\Assign4Grader\\assign4results'],
                                stderr=subprocess.STDOUT, timeout=60).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False
    except subprocess.CalledProcessError as e:
        return False

    return True


def test_app(filename: str) -> tuple[bool, str]:
    try:
        output: str = subprocess.check_output(['python', 'StudentSubmissions\\' + filename],
                                              stderr=subprocess.STDOUT, timeout=60).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False, 'timedout'
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')

    return True, output


def prepare_output(output: str) -> list[str]:
    output.strip()
    output = re.sub(r"\n+", "\n", output)
    return output.split('Part ')[1:]

def grade_parts(raw_parts: list[str]) -> list:
    graded_parts: list = []
    # print(raw_parts)
    graded_parts.append(grade_part_A(raw_parts[0]))
    graded_parts.append(grade_part_B(raw_parts[1]))
    graded_parts.append(grade_part_C(raw_parts[2]))
    return graded_parts


def grade_part_A(raw_part: str) -> float:
    sum_correct: int = 0
    for i, line in enumerate(raw_part.strip().split('\n')[1:]):
        a, b = parse_coord(line.split('=')[1].strip())
        a: float = abs(a - a_answers[i][0]) / a_answers[i][0]
        b: float = abs(b - a_answers[i][1]) / a_answers[i][1]
        if a <= 0.1 and b <= 0.1:
            sum_correct += 1

    return sum_correct


def parse_coord(line: str) -> tuple[float, float]:
    after_equals:str = re.sub(r"[<> ]", "", line)
    a, b = after_equals.split(',')
    return float(a), float(b)


def grade_part_B(raw_part: str) -> float:
    trans_matrix: list[list[float]] = parse_matrix(raw_part)
    sum_correct: int = 0
    for i, line in enumerate(trans_matrix):
        for j, value in enumerate(line):
            if b_answer_matrix[i][j] == 0 and value <= 0.10:
                sum_correct += 1
            else:
                value: float = abs(value - b_answer_matrix[i][j]) / b_answer_matrix[i][j]
                if value <= 0.1:
                    sum_correct += 1
                # else:
                #     print(f'{value} : {b_answer_matrix[i][j]}')
    return sum_correct


def parse_matrix(raw_part: str) -> list[list[float]]:
    matrix: list[list[float]] = []
    splitted: list[str] = raw_part.split('\n')[2:]

    for line in splitted:
        if len(line.strip()) == 0:
            continue
        line = re.sub(r"\s+", " ", line.strip())
        line_splitted: list[str] = line.lower().strip().split(' ')
        line_splitted = line_splitted[1:]
        matrix.append([float(item) for item in line_splitted])
    # print(matrix)
    return matrix


def grade_part_C(raw_part: str) -> int:
    sum_correct: int = 0
    for i, line in enumerate(raw_part.strip().split('\n')[1:]):
        if i == 0:
            a, b = parse_coord(line.split(':')[1])
            a: float = abs(a - c_answer_matrix[i][0]) / c_answer_matrix[i][0]
            b: float = abs(b - c_answer_matrix[i][1]) / c_answer_matrix[i][1]
            if a <= 0.1 and b <= 0.1:
                sum_correct += 1
        else:
            a, b, error = parse_c_line(line.split(':')[1])
            a: float = abs(a - c_answer_matrix[i][0]) / c_answer_matrix[i][0]
            b: float = abs(b - c_answer_matrix[i][1]) / c_answer_matrix[i][1]
            # error: float = (error - c_answer_matrix[i][2]) / c_answer_matrix[i][2]
            # if a <= 0.1 and b <= 0.1 and error <= 0.1:
            if a <= 0.1 and b <= 0.1:
                sum_correct += 1
            # else:
            #     print(f'part C\n{a} : {c_answer_matrix[i][0]}')
            #     print(f'{b} : {c_answer_matrix[i][1]}')
            #     print(f'{error} : {c_answer_matrix[i][2]}')
    return sum_correct * 4


def parse_c_line(line: str) -> tuple[float, float, float]:
    splitted: list[str] = re.sub('\s+', '', line).split(',error=')
    a, b = parse_coord(splitted[0])
    c: str = re.sub('[^0-9.]+', '', splitted[1])        # remove all non numeric characters
    return float(a), float(b), float(c)


def main():
    jplag()
    with open('gradedResults.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['name', 'id', 'Part A output', 'Part A Grade', 'Part B Output', 'Part B Grade', 'Part C Output',
             'Part C Grade','Total Points', 'Raw Output'])
        for filename in os.listdir('./StudentSubmissions'):
            if filename.endswith(".py"):
                name, number, id, *_ = filename.split('_')
                output: tuple[bool, str] = test_app(filename)
                print(output)
                parts: list[str] = ['', '', '']
                parts_grade: list[float] = [0, 0, 0]
                if output[0]:
                    try:
                        parts = prepare_output(output[1])
                        parts_grade = grade_parts(parts)
                    except Exception as e:
                        pass
                else:
                    parts_grade = [0, 0, 0]
            row = [name, id]
            for part, grade in zip(parts, parts_grade):
                row.append(part)
                row.append(grade)
            row.append(sum(parts_grade))
            row.append(output)
            writer.writerow(row)


if __name__ == '__main__':
    main()
