import os
import subprocess


def jplag() -> bool:
    try:
        subprocess.check_output(['java', '-jar', 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\jplag.jar',
                                 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\Assign6Grader\\StudentSubmissions',
                                 '-l', 'python3', '-r', 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\jplag.jar',
                                 'C:\\Users\\metal\\OneDrive\\Desktop\\ISA CECS 451\\Assign6Grader\\assign6results'],
                                stderr=subprocess.STDOUT, timeout=60).decode('utf-8')
    except subprocess.TimeoutExpired:
        return False
    except subprocess.CalledProcessError as e:
        return False
    return True



def createCommands() -> None:
    with open('commands.txt', 'w', newline='') as file:
        for filename in os.listdir('./StudentSubmissions'):
            if filename.endswith(".ipynb"):
                file.write(f'jupyter nbconvert --to notebook --execute StudentSubmissions/{filename} --inplace\n')

def main():
    jplag()
    # run_each_file()
    createCommands()


if __name__ == '__main__':
    main()
