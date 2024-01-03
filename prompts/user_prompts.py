def create_user_prompt_brainstorm(
    user_query: str, queries: str, notes: str, chunks: str | None = None
) -> str:
    user_message_brainstorm = f"""
                                    # USER QUERY
                                    {user_query}

                                    # NOTES
                                    {notes}

                                    # PREVIOUS QUERIES
                                    {queries}

                                    # CONDITIONS
                                    Check the following conditions, respectively, during brainstorming phase to generate queries:
                                        (1) If there is ANY context under the # NOTES and # PREVIOUS QUERIES; Then, generate the queries according to the subject of them.
                                        (2) Else If the retrieved chunks of source document(s) are provided; Then, generate the queries according to the subject of {chunks}.
                                        (3) Else YOU MUST ASK the user about the required field or topic to generate queries.
                                    In any case, DO NOT generate queries about broader topics based on the initial naive user query.
                                    """
    return user_message_brainstorm


def create_user_prompt_brainstorm_baseline(
    user_query: str, queries: str, notes: str
) -> str:
    user_message_brainstorm = f"""
                                    # USER QUERY
                                    {user_query}

                                    # NOTES
                                    {notes}

                                    # PREVIOUS QUERIES
                                    {queries}
                                    """
    return user_message_brainstorm


def create_user_prompt_hypothesis(user_query: str, notes: str, hypotheses: str) -> str:
    user_message_hypothesis = f"""
                                # USER QUERY
                                {user_query}


                                # NOTES
                                {notes}


                                # PREVIOUS HYPOTHISES
                                {hypotheses}
                                """
    return user_message_hypothesis


def create_user_prompt_refine(notes: str) -> str:
    user_message_refine = f"""
                            # NOTES
                            {notes}
                            """
    return user_message_refine


def create_user_prompt_satisfice(
    user_query: str, notes: str, queries: str, hypothesis: str
) -> str:
    user_message_satisfice = f"""
                    # USER QUERY
                    {user_query}


                    # NOTES
                    {notes}


                    # QUERIES AND ANSWERS
                    {queries}


                    # FINAL HYPOTHESIS
                    {hypothesis}
                    """
    return user_message_satisfice


def create_user_prompt_hypothesize_satisfice(
    user_query: str, notes: str, queries: str
) -> str:
    user_message_satisfice = f"""
                    # USER QUERY
                    {user_query}

                    # NOTES
                    {notes}

                    # QUERIES AND ANSWERS
                    {queries}
                    """
    return user_message_satisfice


def create_user_prompt_qa(user_query: str, docs: str) -> str:
    user_message = f"""
                    # USER QUERY
                    {user_query}

                    # DOCUMENTS
                    {docs}
                    """
    return user_message
