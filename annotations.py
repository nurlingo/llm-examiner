from fastapi import Query
from typing import Annotated
from structures.GenericQuestion import QID_TYPE, Q_ANY


class Annotations:
    knowledge_base_id = Annotated[str, Query(
        description='Unique ID associated with knowledge database.'
    )]

    url = Annotated[str, Query(
        description='URL which is scrapped for knowledge database creation. Also scraps subpages recursively.'
    )]

    number_of_questions = Annotated[int, Query(
        description='Number of questions to return.'
    )]

    question_types = Annotated[list[str], Query(
        description='List of question types to return. See `QuestionType` for more information.'
    )]

    outcome = Annotated[str, Query(
        description='Intended learning outcome that is the basis for generating the activities'
    )]

    # q_filter = Annotated[QuestionFilter, Body(
    #     description='Parameters for selecting questions. See `QuestionFilter` for more information.'
    # )]

    qid = QID_TYPE
    any_question = Q_ANY

    # qid_list = Annotated[list[QID_TYPE], Body(
    #     description='List of question IDs. Command will be applied to each corresponding question.'
    # )]

    # token = Annotated[str, Header(
    #     description='Authentication token.'
    # )]

    tags_metadata = [
        {
            "name": "Learner",
            "description": "Commands for the learner."
        },
        {
            "name": "Learner",
            "description":
                "Commands for content and questions management. "
        }
    ]
