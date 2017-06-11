import os
import pathlib
import re
from pykakasi import kakasi, wakati


def normalize_sentence(sentence_to_normalize, text_normalizer):
    sentence_without_spaces = re.sub("[ 　]",
                                     "",
                                     sentence_to_normalize)
    sentence_with_colon_added = re.sub("[).]",
                                       ":",
                                       sentence_without_spaces)
    stripped_sentence = sentence_with_colon_added.strip()
    # Assumes contract is text_normalizer.do
    normalized_sentence = text_normalizer.do(stripped_sentence)
    return normalized_sentence


def load_file(file_path, text_normalizer):
    """Returns JSON object."""
    print("Opening:\n{}".format(file_path))
    with open(file_path, "r") as file:
        normalized_lines = [normalize_sentence(line, text_normalizer)
                            for line
                            in file]

    # json_to_return = {
    #     # This is so shameful. I have brought dishonor to my family
    #     (line.split(":")[0]).lower(): (line.split(":")[1]).lower()
    #     for line
    #     in normalized_lines
    #     if line.strip() != ""
    # }
    json_to_return = {}
    for line in normalized_lines:
        print("Reading: {}".format(line))
        if line != "":
            problem_number, sentence = line.split(":")
            json_to_return[problem_number] = sentence

    return json_to_return


def generate_answer_set_paths(file_path):
    if os.path.isdir(file_path):
        answer_set_paths = [os.path.join(file_path, directory_item)
                            for directory_item
                            in os.listdir(file_path)
                            if os.path.isfile(os.path.join(file_path,
                                                           directory_item))]
        return answer_set_paths
    elif os.path.isfile(file_path):
        return [file_path]
    else:
        return []


def perform_grading(answer_key_path, answer_sets_path, output_directory, text_normalizer):
    # Load answer key and student answers
    answer_key = load_file(answer_key_path, text_normalizer)
    student_answer_sets_paths = generate_answer_set_paths(answer_sets_path)
    student_answer_sets = [(student_answer_sets_path, load_file(student_answer_sets_path,
                                                                text_normalizer))
                           for student_answer_sets_path
                           in student_answer_sets_paths]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Perform grading
    for student_answer_file_path, student_answer_set in student_answer_sets:
        student_name = os.path.basename(student_answer_file_path)
        incorrect_answers = []
        for question_number, student_answer in student_answer_set.items():
            if question_number in answer_key:
                correct_answer = answer_key[question_number]
            else:
                correct_answer = "Answer did not exist in answer key."

            if correct_answer != student_answer:
                output_string = ("Question Number: {}\n"
                                 "Expected Answer: {}\n"
                                 "Student Answer: {}"
                                 "\n").format(question_number,
                                              correct_answer,
                                              student_answer)
                incorrect_answers.append(output_string)

        student_output_filepath = os.path.join(output_directory, student_name)
        with open(student_output_filepath, "w+") as student_corrections_file:
            student_corrections_file.write("\n".join(incorrect_answers))

# ------------------------------------------------------------------------------
current_directory = os.path.dirname(os.path.abspath(__file__))
# CHANGE THIS BIT!
master_answer_key = os.path.join(current_directory,
                                 "answer_keys/2017_06_08_lesson_03_part_02.txt")
student_answer_sets = os.path.join(current_directory,
                                   "answer_sets")
# CHANGE THIS BIT!
date_string = "2017_06_08"
current_student_answer_sets = os.path.join(student_answer_sets,
                                           date_string,
                                           "student_answers")
output_directory = os.path.join(student_answer_sets,
                                date_string,
                                "graded_answers")
# ---
kakasi = kakasi()
kakasi.setMode("J", "H")  # default: Japanese no conversion
japanese_text_normalizer = kakasi.getConverter()
# ---
perform_grading(master_answer_key,
                current_student_answer_sets,
                output_directory,
                japanese_text_normalizer)
