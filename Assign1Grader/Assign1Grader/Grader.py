import os
import subprocess
import re
import csv

TEST_CASE_1 = re.sub(r'\s', '',
                     'From city: Eureka To city: SanDiego Best Route: Eureka - SanFrancisco - SanJose - Fresno - '
                     'LosAngeles - SantaMonica - SanDiego Total distance: 795.60 mi').lower()
TEST_CASE_2 = re.sub(r'\s', '',
                     'From city: SouthLakeTahoe To city: Anaheim Best Route: SouthLakeTahoe - Sacramento - '
                     'SanFrancisco - SanJose - Fresno - LosAngeles - Anaheim Total distance: 635.80 mi').lower()
TEST_CASE_3 = re.sub(r'\s', '',
                     'From city: NewportBeach To city: Sacramento Best Route: NewportBeach - LongBeach - LosAngeles - '
                     'Fresno - SanJose - SanFrancisco - Sacramento Total distance: 550.30 mi').lower()
TEST_CASE_4 = re.sub(r'\s', '',
                     'From city: SantaBarbara To city: LongBeach Best Route: SantaBarbara - SantaMonica - LosAngeles '
                     '- LongBeach Total distance: 132.60 mi').lower()
TEST_CASE_5 = re.sub(r'\s', '',
                     'From city: LongBeach To city: SanFrancisco  Best Route: LongBeach - LosAngeles - Fresno - '
                     'SanJose - SanFrancisco  Total distance: 442.50 mi').lower()
TEST_CASE_6 = re.sub(r'\s', '',
                     'From city: Eureka To city: SouthLakeTahoe  Best Route: Eureka - Sacramento - SouthLakeTahoe  '
                     'Total distance: 392.00 mi').lower()


def testCase1(filename: str) -> tuple[bool, str]:
    try:
        output = subprocess.check_output(['python', 'StudentSubmissions\\' + filename, 'Eureka', 'SanDiego'],
                                         stderr=subprocess.STDOUT, timeout=5).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False, 'timedout'
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
    student_output = re.sub(r'\s', '', output).lower()
    return (student_output == TEST_CASE_1), output


def testCase2(filename: str) -> tuple[bool, str]:
    try:
        output = subprocess.check_output(['python', 'StudentSubmissions\\' + filename, 'SouthLakeTahoe', 'Anaheim'],
                                         stderr=subprocess.STDOUT, timeout=5).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False, 'timedout'
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')

    return re.sub(r'\s', '', output).lower() == TEST_CASE_2.lower(), output


def testCase3(filename: str) -> tuple[bool, str]:
    try:
        output = subprocess.check_output(['python', 'StudentSubmissions\\' + filename, 'NewportBeach', 'Sacramento'],
                                         stderr=subprocess.STDOUT, timeout=5).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False, 'timedout'
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
    return re.sub(r'\s', '', output).lower() == TEST_CASE_3.lower(), output


def testCase4(filename: str) -> tuple[bool, str]:
    try:
        output = subprocess.check_output(['python', 'StudentSubmissions\\' + filename, 'SantaBarbara', 'LongBeach'],
                                         stderr=subprocess.STDOUT, timeout=5).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False, 'timedout'
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
    student_output = re.sub(r'\s', '', output).lower()
    return (student_output == TEST_CASE_4), output


def testCase5(filename: str) -> tuple[bool, str]:
    try:
        output = subprocess.check_output(['python', 'StudentSubmissions\\' + filename, 'LongBeach', 'SanFrancisco'],
                                         stderr=subprocess.STDOUT, timeout=5).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False, 'timedout'
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
    student_output = re.sub(r'\s', '', output).lower()
    return (student_output == TEST_CASE_5), output


def testCase6(filename: str) -> tuple[bool, str]:
    try:
        output = subprocess.check_output(['python', 'StudentSubmissions\\' + filename, 'Eureka', 'SouthLakeTahoe'],
                                         stderr=subprocess.STDOUT, timeout=5).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False, 'timedout'
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
    student_output = re.sub(r'\s', '', output).lower()
    return (student_output == TEST_CASE_6), output


def main():
    with open('gradedResults.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['name', 'number', 'studentId', 'TEST_CASE_1 Result', 'TEST_CASE_1 Output', 'TEST_CASE_2 Result',
             'TEST_CASE_2 Output', 'TEST_CASE_3 Result', 'TEST_CASE_3 Output', 'TEST_CASE_4 Result',
             'TEST_CASE_4 Output', 'TEST_CASE_5 Result', 'TEST_CASE_5 Output', 'TEST_CASE_6 Result',
             'TEST_CASE_6 Output'])
        for filename in os.listdir('./StudentSubmissions'):
            if filename.endswith(".py"):
                name, number, id, _ = filename.split('_')
                t1a, t1b = testCase1(filename)
                t2a, t2b = testCase2(filename)
                t3a, t3b = testCase3(filename)
                t4a, t4b = testCase4(filename)
                t5a, t5b = testCase5(filename)
                t6a, t6b = testCase6(filename)

                writer.writerow([name, number, id, t1a, t1b, t2a, t2b, t3a, t3b, t4a, t4b, t5a, t5b, t6a, t6b])


main()
