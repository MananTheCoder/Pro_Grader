import os
import time
import subprocess

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Step 1: Read the question file
question_file_path = os.path.join(script_dir, 'question_file.cpp')  # Relative path
with open(question_file_path, 'r') as f:
    code = f.read()

# Step 2: Compile the code (if necessary)
if question_file_path.endswith('.cpp'):
    # Compile C++ code
    compile_command = f'g++ -o {os.path.join(script_dir, "question_file.exe")} {question_file_path}'
    subprocess.run(compile_command, shell=True)
elif question_file_path.endswith('.java'):
    # Compile Java code
    compile_command = f'javac {os.path.join(script_dir, "question_file.java")}'
    subprocess.run(compile_command, shell=True)

# Step 3: Read the test case file
test_case_file_path = os.path.join(script_dir, 'test_case_file.txt')  # Relative path
with open(test_case_file_path, 'r') as f:
    lines = f.readlines()
    a = None
    b = None
    expected_output = None
    for line in lines:
        line = line.strip()
        if line.startswith('input 1:'):
            a = line.split(':')[1].strip()
        elif line.startswith('input 2:'):
            b = line.split(':')[1].strip()
        elif line.startswith('Expected Output:'):
            expected_output = line.split(':')[1].strip()
    test_cases = [((a, b), expected_output)]  # Store the input values and expected output as a tuple

# Step 4: Execute the code with test cases
results = []
for test_case in test_cases:
    input_values, expected_output = test_case
    a, b = input_values  # Extract the input values a and b
    output = ''  # Define output variable with a default value
    try:
        # Execute the code with input values
        start_time = time.time()
        if question_file_path.endswith('.cpp'):
            # Run C++ program
            input_str = f"{a}\n{b}"  # Create input string for C++
            run_command = os.path.join(script_dir, 'question_file.exe')  # Path to compiled C++ executable
            process = subprocess.run(run_command, input=input_str, capture_output=True, text=True)
            output = process.stdout.strip()  # Capture the output
        elif question_file_path.endswith('.java'):
            # Run Java program
            input_str = f"{a}\n{b}"  # Ensure inputs are separated by a newline
            with open(os.path.join(script_dir, 'input.txt'), 'w') as f:
                f.write(input_str)  # Write the input to the file
            run_command = f'java -cp {script_dir} question_file < input.txt'  # Make sure to include the classpath
            output = subprocess.run(run_command, shell=True, capture_output=True, text=True).stdout.strip()
        end_time = time.time()
        execution_time = end_time - start_time
        # Compare output with expected result
        if output.strip() == expected_output.strip():
            result = 'Pass'
        else:
            result = 'Fail'
    except Exception as e:
        result = 'Fail'
        execution_time = 'N/A'
        print(f"Error: {e}")
    results.append((test_case, output, execution_time, result))

# Step 5: Write the result to the result file
with open(os.path.join(script_dir, 'result_file.txt'), 'w') as f:
    for result in results:
        f.write(f"Test Case: {result[0][0]}, Expected: {result[0][1]}, Actual Output: {result[1]}, Execution Time: {result[2]} seconds, Result: {result[3]}\n")  # Use \n for newline
