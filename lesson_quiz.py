"""
This module is a complete lesson in 'Mnogomov'
"""


import question


class LessonQuiz:
    """
    Generate several question into one solis quiz which will be used for
    handling language lessons.
    """

    def __init__(self, questions):
        self.questions = questions
        self.current_q_idx = 0
        self.score = 0

    def get_score(self) -> int:
        """
        Return user score after lesson

        :return: integer representing user score
        """
        return self.score

    def reset_lesson(self) -> None:
        """
        Reset score and question index

        :return: None
        """
        self.score = 0
        self.current_q_idx = 0

    def current_q(self) -> question.Question:
        """
        Return data of question with specific index to be displayed
        """
        return self.questions[self.current_q_idx]

    def check_answers(self, user_answer: str) -> bool:
        """
        Check user answers and change score according to results

        :param user_answer: user answer got from 'request.form'
        :return: True/False
        """
        if self.current_q().correct(user_answer):
            answer_result = True
            self.score += 1
        else:
            answer_result = False
        self.current_q_idx += 1
        return answer_result

    def is_finished(self) -> bool:
        """
        Check if user has answered all questions

        :return: True if all questions are answered, else False
        """
        return self.current_q_idx >= len(self.questions) or self.current_q_idx >= 10

    def to_dict(self) -> dict:
        """
        Convert questions data into dictionary for keeping data if needed.

        :return: dictionary with questions
        """
        return {
            "questions": [q.to_dict() for q in self.questions],
            "current_q_idx": self.current_q_idx,
            "score": self.score
        }
