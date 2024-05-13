import os
import subprocess
import re
import csv

raw_input = 'Part A. The sampling probabilities\r\nP(C|-s,r) = <0.8840, 0.1160>\r\nP(C|-s,-r) = <0.3020, 0.6980>\r\nP(R|c,-s,w) = <0.8920, 0.1080>\r\nP(R|-c,-s,w) = <0.8720, 0.1280>\r\n\r\nPart B. The transition probability matrix\r\n     S1      S2      S3      S4\r\nS1 0.9322  0.0068  0.0610  0.0000\r\nS2 0.4932  0.1620  0.0000  0.3448\r\nS3 0.4390  0.0000  0.4701  0.0909\r\nS4 0.0000  0.1552  0.4091  0.4357\r\n\r\nPart C. The probability for the query P(C|-s,w)\r\nExact probability: <0.8566, 0.1434>\r\nn = 10 ^ 3: <0.8800, 0.1200>, error = 2.73%\r\nn = 10 ^ 4: <0.8640, 0.1360>, error = 0.87%\r\nn = 10 ^ 5: <0.8720, 0.1280>, error = 1.80%\r\nn = 10 ^ 6: <0.8740, 0.1260>, error = 2.03%\r\n'

a_answers: list[list[float]] = [[0.8780, 0.1220],
                                [0.3103, 0.6897],
                                [0.9863, 0.0137],
                                [0.8180, 0.1820]]

b_answer_matrix: list[list[float]] = [[0.9321, 0.0069, 0.0610, 0.0001],
                                      [0.0001, 0.4931, 0.1620, 0.3449],
                                      [0.4390, 0.0001, 0.4701, 0.0909],
                                      [0.0001, 0.1550, 0.4090, 0.4360]]

c_answer_matrix: list[list[float]] = [[0.8562, 0.1438,0.0],
                                      [0.8800, 0.1200,2.73],
                                      [0.8640, 0.1360,0.87],
                                      [0.8720, 0.1280,1.80],
                                      [0.8740, 0.1260,2.03]]



def grade_parts(raw_parts: list[str]) -> list:
    graded_parts: list = []
    # print(raw_parts)
    graded_parts.append(grade_part_A(raw_parts[0]))
    graded_parts.append(grade_part_B(raw_parts[1]))
    graded_parts.append(grade_part_C(raw_parts[2]))
    return graded_parts


def grade_part_A(raw_part: str) -> float:
    sum_correct = 0
    for i, line in enumerate(raw_part.strip().split('\n')[1:]):
        a, b = parse_coord(line.split('=')[1].strip())
        a = (a - a_answers[i][0]) / a_answers[i][0]
        b = (b - a_answers[i][1]) / a_answers[i][1]
        if a <= 0.1 and b <= 0.1:
            sum_correct += 1

    return sum_correct


def parse_coord(line: str) -> tuple[float, float]:
    after_equals = re.sub(r"[<> ]", "", line)
    a, b = after_equals.split(',')
    return float(a), float(b)


def grade_part_B(raw_part: str) -> float:
    trans_matrix = parse_matrix(raw_part)
    sum_correct = 0
    # print(trans_matrix)
    for i, line in enumerate(trans_matrix):
        for j, value in enumerate(line):
            print(b_answer_matrix[i][j])
            value = (value - b_answer_matrix[i][j]) / b_answer_matrix[i][j]
            if value <= 0.1:
                sum_correct += 1
    return sum_correct


def parse_matrix(raw_part: str) -> list[list[float]]:
    matrix: list[list[float]] = []
    splitted = raw_part.split('\n')[2:]

    for line in splitted:
        if len(line.strip()) == 0:
            continue
        line = re.sub(r"\s+", " ", line.strip())
        line_splitted = line.lower().strip().split(' ')
        matrix.append([float(item) for item in line_splitted[1:]])
    return matrix


def grade_part_C(raw_part: str) -> int:
    sum_correct = 0
    for i, line in enumerate(raw_part.strip().split('\n')[1:]):
        if i == 0:
            a, b = parse_coord(line.split(':')[1])
            a = (a - c_answer_matrix[i][0]) / c_answer_matrix[i][0]
            b = (b - c_answer_matrix[i][1]) / c_answer_matrix[i][1]
            if a <= 0.1 and b <= 0.1:
                sum_correct += 1
        else:
            a, b, error = parse_c_line(line.split(':')[1])
            a = (a - c_answer_matrix[i][0]) / c_answer_matrix[i][0]
            b = (b - c_answer_matrix[i][1]) / c_answer_matrix[i][1]
            error = (error - c_answer_matrix[i][2]) / c_answer_matrix[i][2]
            if a <= 0.1 and b <= 0.1 and error <= 0.1:
                sum_correct += 1
    return sum_correct * 4


def parse_c_line(line: str) -> tuple[float, float, float]:
    splitted = re.sub('\s+', '', line).split(',error=')
    a, b = parse_coord(splitted[0])
    c = re.sub('[^0-9.]+', '', splitted[1])
    return float(a), float(b), float(c)


def main():
    output = (True, raw_input)
    parts = (0, '')
    parts_grade = [0, 0, 0]
    if output[0]:
        parts = output[1].split('Part ')
        parts_grade = grade_parts(parts[1:])
    else:
        parts_grade = [0, 0, 0]
    print(f'{parts_grade}')


if __name__ == '__main__':
    main()
