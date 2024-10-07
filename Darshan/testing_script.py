import os
import subprocess
import time
import openpyxl
from openpyxl.styles import PatternFill

base_path = "./"
questions_path = os.path.join(base_path, "Questions")
submissions_path = os.path.join(base_path, "Submissions")
results_path = os.path.join(base_path, "Results")
marks_per_question = {
    "Ques1": 5,
    "Ques2": 3,
    "Ques3": 4,
}

green_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")


def get_test_cases(question_folder):
    test_cases = []
    try:
        for filename in sorted(os.listdir(question_folder)):
            if filename.endswith(".in"):
                in_file = os.path.join(question_folder, filename)
                out_file = in_file.replace(".in", ".out")
                if os.path.exists(out_file):
                    test_cases.append((in_file, out_file))
    except FileNotFoundError:
        print(f"Error: The folder '{question_folder}' was not found.")
    except Exception as e:
        print(f"Error while retrieving test cases: {e}")
    return test_cases


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


def compile_java(user_code, user_path):
    try:
        # Change to the user's directory before compiling
        original_dir = os.getcwd()
        os.chdir(user_path)
        
        result = subprocess.run(["javac", os.path.basename(user_code)], capture_output=True, text=True)
        os.chdir(original_dir)
        return result.returncode == 0
    except subprocess.SubprocessError as e:
        print(f"Error compiling Java code '{user_code}': {e}")
        return False
    finally:
        # Ensure we return to the original directory
        if 'original_dir' in locals():
            os.chdir(original_dir)


def run_java(class_name, input_data, user_path):
    try:
        # Change to the user's directory before running
        original_dir = os.getcwd()
        os.chdir(user_path)
        
        result = subprocess.run(
            ["java", class_name],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=1,
        )
        os.chdir(original_dir)
        return result.stdout.strip() if result.returncode == 0 else None
    except subprocess.TimeoutExpired:
        print("Error: Code execution timed out.")
        return None
    except subprocess.SubprocessError as e:
        print(f"Error running Java code: {e}")
        return None
    finally:
        # Ensure we return to the original directory
        if 'original_dir' in locals():
            os.chdir(original_dir)


def get_expected_output(expected_output_file):
    try:
        with open(expected_output_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: Expected output file '{expected_output_file}' not found.")
    except Exception as e:
        print(f"Error reading expected output file: {e}")
    return ""


def evaluate_user(user_folder):
    user_results = {}
    user_path = os.path.join(submissions_path, user_folder)

    for question in sorted(os.listdir(questions_path)):
        question_path = os.path.join(questions_path, question)
        test_cases = get_test_cases(question_path)
        passed_cases = 0
        total_cases = len(test_cases)
        failed_cases = []

        questionNum = ''.join([i for i in question if i.isdigit()])
        cpp_file = os.path.join(user_path, f"{user_folder[0].lower()}_{user_folder.split('_')[1][0].lower()}_{questionNum}.cpp")
        java_file = os.path.join(user_path, f"{user_folder[0].lower()}_{user_folder.split('_')[1][0].lower()}_{questionNum}.java")
        
        if os.path.exists(cpp_file) and compile_cpp(cpp_file):
            for i, (input_file, expected_output_file) in enumerate(test_cases):
                with open(input_file, "r") as infile:
                    input_data = infile.read().strip()
                current_output = run_cpp(input_data)
                if current_output is not None:
                    expected_output = get_expected_output(expected_output_file)
                    if current_output == expected_output:
                        passed_cases += 1
                    else:
                        failed_cases.append({"test_case": i + 1, "input": input_data, "expected_output": expected_output, "current_output": current_output})
        elif os.path.exists(java_file):
            class_name = os.path.splitext(os.path.basename(java_file))[0]
            if compile_java(java_file, user_path):
                for i, (input_file, expected_output_file) in enumerate(test_cases):
                    with open(input_file, "r") as infile:
                        input_data = infile.read().strip()
                    current_output = run_java(class_name, input_data, user_path)
                    if current_output is not None:
                        expected_output = get_expected_output(expected_output_file)
                        if current_output == expected_output:
                            passed_cases += 1
                        else:
                            failed_cases.append({"test_case": i + 1, "input": input_data, "expected_output": expected_output, "current_output": current_output})

        user_results[question] = {"passed": passed_cases, "total": total_cases, "failed_cases": failed_cases}

    try:
        with open(os.path.join(results_path, f"{user_folder}.txt"), "w") as f:
            for question, result in user_results.items():
                f.write(f"{question}: {result['passed']}/{result['total']} test cases passed.\n")
                if result["failed_cases"]:
                    f.write("Failed cases:\n")
                    for case in result["failed_cases"]:
                        f.write(f"  Test Case {case['test_case']}:\n")
                        f.write(f"    Input:           {case['input']}\n")
                        f.write(f"    Expected Output: {case['expected_output']}\n")
                        f.write(f"    Current Output:  {case['current_output']}\n\n")
    except Exception as e:
        print(f"Error writing results file: {e}")

    return user_results


def generate_excel_report(users_results):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Test Results"

    try:
        ques_list = sorted(os.listdir(questions_path))
        headers = ["Name"] + ques_list + ["Total Marks"]
        sheet.append(headers)

        for row, (user, results) in enumerate(users_results.items(), start=2):
            total_marks = 0
            row_data = [user]
            for question in ques_list:
                result = results.get(question, {"passed": 0, "total": 0})
                passed, total = result["passed"], result["total"]
                question_marks = marks_per_question.get(question, 0)
                score = (passed / total) * question_marks if total else 0
                row_data.append(f"{(passed / total) * 100:.1f}%" if total else "0%")
                total_marks += score
            row_data.append(f"{total_marks:.1f}")
            sheet.append(row_data)

        workbook.save(os.path.join(results_path, "test_results.xlsx"))
    except FileNotFoundError:
        print("Error: Questions directory not found.")
    except Exception as e:
        print(f"Error generating Excel report: {e}")


def clean_up():
    # Clean up compiled files
    for user_folder in os.listdir(submissions_path):
        user_path = os.path.join(submissions_path, user_folder)
        try:
            # Remove C++ executable
            if os.path.exists("temp_executable"):
                os.remove("temp_executable")
            
            # Remove Java class files
            for file in os.listdir(user_path):
                if file.endswith(".class"):
                    os.remove(os.path.join(user_path, file))
        except Exception as e:
            print(f"Error cleaning up files: {e}")


def main():
    users_results = {}
    try:
        if not os.path.exists(results_path):
            os.makedirs(results_path)

        for user_folder in sorted(os.listdir(submissions_path)):
            print(f"Evaluating {user_folder}...")
            user_results = evaluate_user(user_folder)
            users_results[user_folder] = user_results

        generate_excel_report(users_results)
        clean_up()
    except Exception as e:
        print(f"Error in main execution: {e}")


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Execution Time: {time.time() - start:.2f} seconds")