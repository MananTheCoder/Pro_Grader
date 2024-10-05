



# Function to read the file and return a list of test case outputs
def read_file(filename):
    with open(filename, 'r') as file:
        data = file.read().splitlines()  # Use splitlines() to preserve line breaks properly
    return data


# Function to calculate the score based on comparison
def calculate_score(student_answers, correct_answers):
    total_cases = len(correct_answers)
    correct_cases = 0

    # Pad student answers with empty strings if the number of answers is less than correct answers
    if len(student_answers) < total_cases:
        student_answers.extend([''] * (total_cases - len(student_answers)))

    # Compare each test case line by line
    for student_answer, correct_answer in zip(student_answers, correct_answers):
        if student_answer.strip() == correct_answer.strip():
        # if student_answer.strip().lower() == correct_answer.strip().lower():
            correct_cases += 1

    return correct_cases, total_cases


# Main script
if __name__ == "__main__":
    # Read student answers and correct answers from files
    correct_answers = read_file('./Files/correct-answers.txt')
    student_answers = read_file('./Files/student-answers.txt')

    # Calculate the score
    correct_cases, total_cases = calculate_score(student_answers, correct_answers)

    # Calculate and print the score
    score = (correct_cases / total_cases) * 100
    print(f"Student's Score: {score:.2f}% ({correct_cases}/{total_cases} correct answers)")
