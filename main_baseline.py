import json

from rbhsr import brainstorm, hypothesize, refine, satisfice
from settings import parse_args, parse_kwargs
from shared import create_openai_embedding


def main():
    args = parse_args()
    kwargs = parse_kwargs()

    subdoc_name = "subdoc_1_2"

    outputs = []

    # Store the JSON data in a file
    with open(f"qa_db/{subdoc_name}/qa_dataset.json", "r") as file:
        qas = json.load(file)

        for indx, qa in enumerate(qas):
            print(qa["question"])

            user_query = qa["question"]

            notes = ""
            queries = ""

            total_elapsed_time = 0
            cost = 0

            vector_store = kwargs["vector_store"]

            embedding = create_openai_embedding()

            iteration = args.iteration
            hypotheses_feedback = "# FEEDBACK ON HYPOTHESES\n"

            while True:
                iteration += 1
                print(f"{iteration=} started")

                ((new_queries, notes), elps_time), cb_bs = brainstorm(
                    user_query,
                    notes,
                    queries,
                    vector_store,
                    args.persist_dir,
                    embedding,
                    **kwargs["bs"],
                )
                queries += new_queries

                total_elapsed_time += elps_time
                cost += cb_bs.total_cost

                (new_hypothesis, h_elps_time), cb_h = hypothesize(
                    user_query, notes, hypotheses_feedback, **kwargs["llm"]
                )

                total_elapsed_time += h_elps_time
                cost += cb_h.total_cost

                ((satisficed, feedback), s_elps_time), cb_s = satisfice(
                    user_query, notes, queries, new_hypothesis, **kwargs["st"]
                )

                hypotheses_feedback = f"""
                                {hypotheses_feedback}

                                ## HYPOTHESIS
                                {new_hypothesis}

                                ## FEEDBACK
                                {feedback}
                                """

                print(f"{new_hypothesis=}")
                print(f"{satisficed=}")
                print(f"{feedback=}")

                total_elapsed_time += s_elps_time
                cost += cb_s.total_cost

                if satisficed or args.max_iterations <= iteration:
                    print(f"satisficed after {iteration} iterations.")
                    break

                (notes, r_elps_time), cb_r = refine(notes, **kwargs["llm"])

                total_elapsed_time += r_elps_time
                cost += cb_r.total_cost

                print(f"{iteration=} completed")

            output = {
                f"cost_{indx}": cost,
                f"elapsed_time_{indx}": total_elapsed_time,
                f"satisficed_{indx}": satisficed,
                f"feedback_{indx}": feedback,
                f"original_question_{indx}": qa["question"],
                f"new_hypothesis_{indx}": new_hypothesis,
            }

            outputs.append(output)

        # Store the JSON data in a file
        with open(f"results_baseline/{subdoc_name}/outputs.json", "w") as file:
            json.dump(outputs, file)

        print("Results stored successfully!")


if __name__ == "__main__":
    main()
