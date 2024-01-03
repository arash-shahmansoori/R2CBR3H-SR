from shared import create_client

client = create_client()

query = "The Experiments"
# additional_requirement = "" # Use for Title
# additional_requirement = "The abstract should be maximum 200 words. At the end of the abstract you MUST mention that the proposed method outperforms the corresponding method from the literature in terms of computation speed and cost. DO NOT INCLUDE TITLE ONLY OUTPUT THE ABSTRACT." # Use for abstract
# additional_requirement = "The introduction should be maximum 700 words. You need to specifically mention the main contributions of the paper including: initial retrival and rerank phase based on the initial user query, concurrent brainstorming, hybrid hypothesis satisficing using a chain of thought based prompting, and any additional descriptions provided above for the proposed method with emphasis on the novel aspects of the proposed method. It is ideal to use the bulletpoints to emphasize on the novel aspects of the paper at the end of the introduction. DO NOT INCLUDE TITLE AND ABSTRACT ONLY OUTPUT THE INTRODUCTION."  # Use for introduction
# additional_requirement = "The proposed method should include a latex format algorithm to clearly describe this approach. In particular, the latex algorithm for the proposed method should describe clearly and easily all the steps in the proposed method in an easy-to-read way. I have provided a python code snippet to help you in the creation process of the latex algorithm and describing the proposed approach. DO NOT INCLUDE TITLE, ABSTRACT, AND INTRODUCTION ONLY OUTPUT THE PROPOSED METHOD. Finally, revise the main method section and make sure that it is coherent and very well written for a scientific publication."  # Use for the main method

additional_requirement = """The results section should include the following subsections. First, the setup including the types of models used for each phase. In particular, all different phases including the brainstorm, hypothesis-satisfying, and refine used "gpt-3.5-turbo-1106" model with the temperature set to 0 and max_tokens of 2000. The brainstorming and hypothesis-satisfying phases additionally used the response_format of type: "json_object". Finally, ChromaDB was used as the vector store during the simulations. Second, the baseline includes the method from the literature. In the result section, the main aim is to emphasize the fact that using concurrent brainstorming and hybrid hypothesis-satisfying results a faster and a more cost effective performance, satisfying user information needs in the retrival augmented generation process. DO NOT INCLUDE TITLE, ABSTRACT, INTRODUCTION, METHOD, AND CONCLUSION ONLY OUTPUT THE RESULTS."""  # Use for the Results

# additional_requirement = "The conclusion should include the summary of the main aspects of the process. It should emphasize on the cost effectiveness and speed of the proposed method compared to its available counterpart. The conclusion should be concise, easy to read, and follow and should not be more than 200 words in length. DO NOT INCLUDE TITLE, ABSTRACT, INTRODUCTION, AND THE PROPOSED METHOD ONLY OUTPUT THE CONCLUSION."  # Use for the conclusion

system_prompt = """You are a the best scientific artificial (general) intelligence researcher in the world. You provide the best suggestions for writing scientific papers related to artificial (general) intelligence, machine learning, and deep learning. You will be asked questions by the user for generating scientific suggestions for writing papers. The user asks your suggestions for writing different parts of a scientific paper, i.e., title, abstract, introduction, main methods, results, and conclusions. You only respond to what the user asks for and do not try to provide additional responses that are not related to the original user query."""

# user_prompt = f"""I have designed a system for retrieval augmented generation that: Rerank Brainstorm Rerank Hypothesize Satisfice and Refine. The system is iterative and described as follows.

# Here is a summary of the process:

# I have a system that brainstorms using the user question and available initial relevant documents retrieved from a vector database with highest possible similarity with user initial question, i.e., reranks the tope candidates from the vector database. The resulting brainstorming possibilities form a set of possible queries/questions that can be asked from the documents. Then in the hypothesize phase, the system hypothesize according to the user query, previous hypothesize, and relevant documents/notes. In this case, the hypothesis is a comprehensive answer to the user query or information need. Consequently in the satisfied phase, using the original user query, previous search queries, their results, notes, and a final hypothesis, the proposed method generates a decision as to whether or not the information need has been satisficed or not. Finally in the refine phase, the system writes a sparse prime representation as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors. The idea is to capture as much, conceptually, as possible but with as few words as possible. This process is iterative and iterates as: Retrieve -> Rerank -> Brainstorm -> Retrieve -> Rerank -> Refine -> Hypothesize Satisficing -> Refine -> ... Iterate Until satisficed.

# IMPORTANT: Please note that the brainstorming phase uses concurrency to generate relevant questions and to accelerate the recursive process for the retrival process. Please note that the hypothesis satisfice case is a hybrid process that combines hypothesizing and satisficing using a chain of thought based prompting approach to accelerate the entire process and reduce the overall cost.

# According to the above information, provide the best possible {query} for this research paper. The {query} should be smart, unique, concise, and capture all the key novel aspects of the aforementioned process above as much as possible. It should emphasize on the concurrency in brainstorming phase, it should emphesize on the hybrid hypothesize and satisfice step in one go using chain of thought based prompting, and include all the steps, i.e., Rerank, Brainstorm, Refine, Hypothesize Satisficing, and Refine, as well. Finally, it is very IMPORTANT to note the {query} will be potentially used for a top tier journal publication. {additional_requirement}
# """

user_prompt = """
Please edit the following text, do not add or remove information or change the values reported. Remain loyal to the original context provided as it is the results of a scientific publication. USE the term Information Need as it is a technical term used within the paper.

```Results
Table. summarizes the comparison study against the corresponding benchmark. It is observed that while both methods satisfy the information needs, the proposed approach results relative decrease of average cost by approximately 32.64 percent and relative decrease of the average elapsed time by approximately 58 percent compared to the benchmark. In other words, the absolute decrease of average cost per query is approximately 0.0017$ and the absolute decrease of the average elapsed time per query is approximately 14.1 sec compared to the benchmark.``` """


response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": user_prompt},
    ],
    stream=True,
)

# print(response.choices[0].message.content)


for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
