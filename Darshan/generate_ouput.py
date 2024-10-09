import subprocess
import os

# run the correct cpp code for input testcacses naming convention is 1.in , 2.in , 3.in etc .. and store the output in 1.out , 2.out , 3.out etc ..

questions_path = "Questions" # path to the folder where input testcases are stored and outputs will be stored

'''
Question
    -Ques1
        -correct.cpp
        -1.in
        -2.in
        ...
    -Ques2
        -correct.cpp
        -1.in
        -2.in
        ...
    ...

'''

def compile_cpp(user_code):
    try:
        result = subprocess.run(["g++", user_code, "-o", "temp_executable"], capture_output=True)
        return result.returncode == 0
    except subprocess.SubprocessError as e:
        print(f"Error compiling C++ code '{user_code}': {e}")
        return False

def run_cpp(input_data):
    try:
        result = subprocess.run(
            "./temp_executable",
            input=input_data,
            capture_output=True,
            text=True,
            timeout=1,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except subprocess.TimeoutExpired:
        print("Error: Code execution timed out.")
        return None
    except subprocess.SubprocessError as e:
        print(f"Error running C++ code: {e}")
        return None

# iterate through all the input testcases and run the correct cpp code and store the output in the output file

for question in os.listdir(questions_path):
    question_path = os.path.join(questions_path, question)
    # compiling the correct cpp code
    correct_code_destination = os.path.join(question_path, "correct.cpp")
    if not os.path.exists(correct_code_destination):
        print(f"Error: Correct code not found for question '{question}'.")
        continue
    if compile_cpp(correct_code_destination):
        print(f"Compiled Correct Code for question '{question}'")
    if os.path.isdir(question_path):
        for testcase in os.listdir(question_path):
            if testcase.endswith(".in"):
                with open(os.path.join(question_path, testcase), "r") as f:
                    # also strip the input data to remove any leading or trailing whitespaces and store the output in the output file
                    input_data = f.read().strip()
                    output = run_cpp(input_data)
                    output = output.strip()
                    if output is not None:
                        with open(os.path.join(question_path, testcase.replace(".in", ".out")), "w") as f:
                            f.write(output)
                    else:
                        print("Error: Code execution failed.")
                        break
    
            
                        
    
