import os
import subprocess
import re
import csv
import sys


def jplag() -> bool:
    try:
        subprocess.check_output(['java', '-jar', 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\jplag.jar',
                                 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\Assign3Grader\\StudentSubmissions',
                                 '-l', 'python3', '-r', 'assign3results'],
                                stderr=subprocess.STDOUT, timeout=60).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False
    except subprocess.CalledProcessError as e:
        return False

    return True


def createConvertCommands():
    with open('convertCommands.txt', 'w', newline='') as file:
        for filename in os.listdir('./StudentSubmissions'):
            if filename.endswith(".ipynb"):
                file.write(f'jupyter nbconvert --execute --to {filename} --inplace {filename}\n')


def convert(file_name: str) -> None:
    try:
        subprocess.run(
            ['jupyter', 'nbconvert', f'StudentSubmissions/{file_name}', '--to', 'script', '--output',
             '../converted/' + file_name], shell=True)
    except subprocess.TimeoutExpired:
        return None
    except subprocess.CalledProcessError as e:
        return


def createCommands() -> None:
    with open('commands.txt', 'w', newline='') as file:
        for filename in os.listdir('./StudentSubmissions'):
            if filename.endswith(".ipynb"):
                file.write(f'jupyter nbconvert --execute --to \'StudentSubmissions/{filename}\' --inplace \'StudentSubmissions/{filename}\'\n')


def main():
    jplag()
    createCommands()
    # convert('n-airports-1.ipynb')


main()
