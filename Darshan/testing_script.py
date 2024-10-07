import os
import subprocess
import time
import openpyxl
from openpyxl.styles import PatternFill

base_path = "./"
questions_path = os.path.join(base_path, "Questions")
submissions_path = os.path.join(base_path, "Submissions")
results_path = os.path.join(base_path, "Results")
marks_per_question = 4

green_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")


def get_test_cases(question_folder):
    test_cases = []
    for filename in sorted(os.listdir(question_folder)):
        if filename.endswith(".in"):
            in_file = os.path.join(question_folder, filename)
            out_file = in_file.replace(".in", ".out")
            if os.path.exists(out_file):
                test_cases.append((in_file, out_file))
    return test_cases


def compile_code(user_code):
    """Compile user's code and return True if successful, False otherwise."""
    result = subprocess.run(["g++", user_code, "-o", "temp_executable"], capture_output=True)
    return result.returncode == 0


def run_code(input_data):
    """Run compiled code and return output."""
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
        return None


def get_expected_output(expected_output_file):
    with open(expected_output_file, "r") as f:
        return f.read().strip()


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
        code_file = os.path.join(user_path, f"{user_folder[0].lower()}_{user_folder.split('_')[1][0].lower()}_{questionNum}.cpp")
        print(code_file)

        if os.path.exists(code_file) and compile_code(code_file):
            for i, (input_file, expected_output_file) in enumerate(test_cases):
                with open(input_file, "r") as infile:
                    input_data = infile.read().strip()
                current_output = run_code(input_data)

                if current_output:
                    expected_output = get_expected_output(expected_output_file)
                    if current_output == expected_output:
                        passed_cases += 1
                    else:
                        failed_cases.append({
                            "test_case": i + 1,
                            "input": input_data,
                            "expected_output": expected_output,
                            "current_output": current_output,
                        })

        user_results[question] = {
            "passed": passed_cases,
            "total": total_cases,
            "failed_cases": failed_cases,
        }

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
    return user_results


def generate_excel_report(users_results):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Test Results"

    ques_list = os.listdir(questions_path)
    headers = ["Name"] + ques_list + ["Total Marks"]
    sheet.append(headers)

    for row, (user, results) in enumerate(users_results.items(), start=2):
        total_marks = 0
        row_data = [user]
        for question in ques_list:
            result = results.get(question, {"passed": 0, "total": 0})
            passed, total = result["passed"], result["total"]
            score = (passed / total) * marks_per_question if total else 0
            row_data.append(f"{(passed / total) * 100:.1f}%" if total else "0%")
            total_marks += score
        row_data.append(total_marks)
        sheet.append(row_data)

    workbook.save(os.path.join(results_path, "test_results.xlsx"))


def main():
    users_results = {}
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    for user_folder in sorted(os.listdir(submissions_path)):
        user_results = evaluate_user(user_folder)
        users_results[user_folder] = user_results

    generate_excel_report(users_results)
    subprocess.run(["rm", "temp_executable"])


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Execution Time: {time.time() - start:.2f} seconds")
