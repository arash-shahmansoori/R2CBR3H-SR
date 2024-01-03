import json
import time
from functools import partial

from rbhsr import brainstorm_concurrent, hypothesize_satisfice, refine
from settings import parse_args, parse_kwargs
from shared import create_openai_embedding


def main():
    args = parse_args()
    kwargs = parse_kwargs()

    subdoc_name = "subdoc_1_2"

    outputs = []

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

            brainstorm = partial(brainstorm_concurrent, args.top_n_rerank)

            iteration = args.iteration

            while True:
                iteration += 1
                print(f"{iteration=} started")

                ((new_queries, notes, top_note), elps_time), cb_bs = brainstorm(
                    user_query,
                    notes,
                    queries,
                    vector_store,
                    args.persist_dir,
                    embedding,
                    **kwargs["bs"],
                )
                queries += new_queries

                print(top_note)

                total_elapsed_time += elps_time
                cost += cb_bs.total_cost

                ((satisficed, feedback), hs_elps_time), cb_hs = hypothesize_satisfice(
                    user_query, notes, queries, **kwargs["st"]
                )

                print(f"{satisficed=}")
                print(f"{feedback=}")

                total_elapsed_time += hs_elps_time
                cost += cb_hs.total_cost

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
                f"top_note_{indx}": top_note,
            }

            outputs.append(output)

            time.sleep(60)  # Sleep 60 sec if using cohere free API

        # Store the JSON data in a file
        with open(f"results/{subdoc_name}/outputs.json", "w") as file:
            json.dump(outputs, file)

        print("Results stored successfully!")


if __name__ == "__main__":
    main()
