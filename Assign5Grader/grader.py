import os
import subprocess
import re
import csv

answers: list[str] = ['0.5,0.7,0.3,0.9,0.2,t,t--><0.8834,0.1166>',
                      '0.7,0.8,0.3,0.2,0.7,t,f--><0.7056,0.2944>',
                      '0.5,0.6,0.3,0.7,0.2,f,t--><0.6731,0.3269>',
                      '0.3,0.9,0.2,0.8,0.3,f,f--><0.1166,0.8834>',
                      '0.5,0.7,0.3,0.9,0.2,t,t,f--><0.1907,0.8093>',
                      '0.7,0.8,0.3,0.2,0.7,t,f,t--><0.3495,0.6505>',
                      '0.5,0.6,0.3,0.7,0.2,f,t,f--><0.2743,0.7257>',
                      '0.3,0.9,0.2,0.8,0.3,f,f,t--><0.5111,0.4889>',
                      '0.5,0.6,0.3,0.7,0.2,f,t,t,f--><0.3003,0.6997>',
                      '0.3,0.9,0.2,0.8,0.3,t,f,f,t--><0.5687,0.4313>',]


def jplag() -> bool:
    try:
        subprocess.check_output(['java', '-jar', 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\jplag.jar',
                                 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\Assign5Grader\\StudentSubmissions',
                                 '-l', 'python3', '-r', 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\jplag.jar',
                                 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\Assign5Grader\\assign5results'],
                                stderr=subprocess.STDOUT, timeout=60).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False
    except subprocess.CalledProcessError as e:
        return False
    return True


def test_app(filename: str, input_file: str) -> str:
    try:
        output: str = subprocess.check_output(
            ['python', 'StudentSubmissions\\' + filename, input_file],
            stderr=subprocess.STDOUT, timeout=60).decode('utf-8')
    except subprocess.TimeoutExpired:
        return 'timedout'
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')

    return output


def grade_testcase(output: str) -> int:
    total: int = 0
    output = output.splitlines()
    for student_output, answer in zip(output, answers):
        if student_output == answer:
            total += 4
    return total


def main():
    jplag()
    with open('gradedResults.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['name', 'id', 'Raw Output', 'Grade'])
        for filename in os.listdir('./StudentSubmissions'):
            output: str = ''
            if filename.endswith(".py"):
                name, number, id_num, id2, *_ = filename.split('_')
                if number == 'LATE':
                    id_num = id2
                output = test_app(filename, 'cpt_eval.txt')
                output = re.sub(' |\t', '', output)
                grade = grade_testcase(output)
                writer.writerow([name, id_num, output, grade])


if __name__ == '__main__':
    main()
