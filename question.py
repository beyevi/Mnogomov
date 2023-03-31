"""
This module is a single question of a lesson
"""


class Question:
    """
    Take retrieved data from 'mnogomov' db and use it to form a question, which
    will be displayed during a lesson.
    """

    def __init__(self,
                 id_question: int,
                 question_text: str,
                 option1: str,
                 option2: str,
                 option3: str,
                 answer: str,
                 content: str):
        self.id = id_question
        self.text = question_text
        self.options = [option1, option2, option3]
        self.answer = answer
        self.content = content

    def correct(self, user_answer: str) -> bool:
        """
        Check if user has answered correctly

        :param user_answer: user choice, one of three possible options (1, 2 or 3)
        :return: True if correct, else False
        """
        return str(self.answer) == user_answer

    def to_dict(self) -> dict:
        """
        Convert question data into dictionary for keeping data if needed.

        :return: dictionary with question parameters
        """
        return {
            "id": self.id,
            "question text": self.text,
            "options": self.options,
            "correct answer": self.answer
        }
