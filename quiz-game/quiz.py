"""
Quiz Game
---------
A command-line multiple-choice quiz that loads questions from questions.json,
tracks the player's score, and shows a final result.

Usage:
    python quiz.py
"""

import json
import random
import string
import sys


def load_questions(filepath="questions.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: could not find '{filepath}'. Make sure it's in the same folder.")
        sys.exit(1)


def ask_question(index, question_data):
    print(f"\nQ{index}. {question_data['question']}")

    options = question_data["options"][:]
    random.shuffle(options)
    labels = string.ascii_uppercase[: len(options)]

    for label, option in zip(labels, options):
        print(f"  {label}. {option}")

    while True:
        choice = input("Your answer: ").strip().upper()
        if choice in labels:
            selected = options[labels.index(choice)]
            return selected == question_data["answer"], question_data["answer"]
        print(f"Please enter one of: {', '.join(labels)}")


def run_quiz():
    questions = load_questions()
    random.shuffle(questions)

    score = 0
    total = len(questions)

    print("=" * 40)
    print("       WELCOME TO THE PYTHON QUIZ")
    print("=" * 40)
    print(f"There are {total} questions. Good luck!\n")

    for i, q in enumerate(questions, start=1):
        correct, correct_answer = ask_question(i, q)
        if correct:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. The correct answer was: {correct_answer}")

    print("\n" + "=" * 40)
    print(f"Quiz finished! Your score: {score}/{total} ({score / total:.0%})")
    print("=" * 40)


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")
