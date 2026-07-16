# Quiz Game

A command-line multiple-choice quiz game. Questions are loaded from a JSON
file, shuffled each run, and the player's score is tracked and shown at the end.

## Features

- Questions and answer options load from `questions.json` (easy to edit or extend).
- Both question order and option order are randomized each run.
- Final score and percentage shown at the end.

## Usage

```bash
python quiz.py
```

Answer each question by typing the letter (A, B, C, ...) of your chosen option.

## Adding your own questions

Edit `questions.json`. Each entry looks like:

```json
{
  "question": "Your question here?",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "answer": "Option 2"
}
```

## Requirements

No external dependencies — uses only Python's standard library (`json`, `random`, `string`).
