import pandas as pd
from database import add_test, add_question


def load_questions_from_csv(path, title=None, subject=None, time_limit=10, negative_marking=0.0):
    df = pd.read_csv(path)
    # expected columns: question, option1..4, correct_option (1-4), explanation (optional)
    test_id = add_test(title or 'Imported Test', subject or 'General', time_limit, negative_marking)
    cnt = 0
    for _, row in df.iterrows():
        q = str(row.get('question', ''))
        o1 = str(row.get('option1', ''))
        o2 = str(row.get('option2', ''))
        o3 = str(row.get('option3', ''))
        o4 = str(row.get('option4', ''))
        correct = int(row.get('correct_option', 1))
        explanation = str(row.get('explanation', ''))
        add_question(test_id, q, o1, o2, o3, o4, correct, explanation)
        cnt += 1
    # Update total_questions
    return test_id, cnt

