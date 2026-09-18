# import os

# # ==========================================================
# # LIMIT BLAS THREADS
# # Prevents OpenBLAS memory allocation problems on Windows
# # ==========================================================

# os.environ["OPENBLAS_NUM_THREADS"] = "1"
# os.environ["OMP_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"


# # ==========================================================
# # IMPORTS
# # ==========================================================

# import pandas as pd

# from dotenv import load_dotenv

# from ragas import EvaluationDataset, SingleTurnSample, evaluate

# from ragas.metrics import (
#     Faithfulness,
#     ContextPrecision,
# )

# from langchain_google_genai import ChatGoogleGenerativeAI

# from retrieval import run_rag_for_evaluation


# # ==========================================================
# # LOAD ENVIRONMENT VARIABLES
# # ==========================================================

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if not GOOGLE_API_KEY:
#     raise ValueError(
#         "GOOGLE_API_KEY not found in .env file."
#     )


# # ==========================================================
# # TEST DATA
# # ==========================================================
# #
# # Add more questions here later.
# #
# # For now, keep only ONE question while testing
# # the evaluation pipeline. This saves Gemini API quota.
# # ==========================================================

# test_questions = [

#     {
#         "question": "What is the price of M Sand?",
#         "ground_truth": "The price of M-Sand is ₹1,250 per Cum.",
#     },

# ]


# # ==========================================================
# # RAGAS EVALUATOR LLM
# # ==========================================================
# #
# # IMPORTANT:
# # This model is ONLY used by RAGAS for evaluation.
# #
# # Your actual RAG model remains inside retrieval.py.
# #
# # Using a lighter evaluator helps reduce API usage.
# # ==========================================================

# evaluator_llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash-lite",
#     google_api_key=GOOGLE_API_KEY,
#     temperature=0,
# )


# # ==========================================================
# # RUN RAG
# # ==========================================================

# samples = []


# for item in test_questions:

#     question = item["question"]
#     ground_truth = item["ground_truth"]

#     print("\n")
#     print("=" * 70)
#     print("QUESTION")
#     print("=" * 70)

#     print(question)

#     try:

#         # --------------------------------------------------
#         # Run your existing RAG pipeline
#         # --------------------------------------------------

#         answer, contexts = run_rag_for_evaluation(
#             question
#         )


#         # ==================================================
#         # DISPLAY RETRIEVED CONTEXTS
#         # ==================================================

#         print("\n")
#         print("=" * 70)
#         print("RETRIEVED CONTEXTS")
#         print("=" * 70)

#         for i, context in enumerate(
#             contexts,
#             start=1
#         ):

#             print(f"\n--- Context {i} ---")

#             print(
#                 context[:1000]
#             )


#         # ==================================================
#         # DISPLAY GENERATED ANSWER
#         # ==================================================

#         print("\n")
#         print("=" * 70)
#         print("GENERATED ANSWER")
#         print("=" * 70)

#         print(answer)


#         # ==================================================
#         # DISPLAY GROUND TRUTH
#         # ==================================================

#         print("\n")
#         print("=" * 70)
#         print("GROUND TRUTH")
#         print("=" * 70)

#         print(ground_truth)


#         # ==================================================
#         # CREATE RAGAS SAMPLE
#         # ==================================================

#         sample = SingleTurnSample(

#             user_input=question,

#             retrieved_contexts=contexts,

#             response=answer,

#             reference=ground_truth,

#         )

#         samples.append(sample)


#     except Exception as e:

#         print("\n")
#         print("=" * 70)
#         print("❌ ERROR WHILE RUNNING RAG")
#         print("=" * 70)

#         print(str(e))


# # ==========================================================
# # CHECK SAMPLES
# # ==========================================================

# if not samples:

#     raise RuntimeError(
#         "No evaluation samples were created."
#     )


# # ==========================================================
# # CREATE RAGAS DATASET
# # ==========================================================

# dataset = EvaluationDataset(
#     samples=samples
# )


# # ==========================================================
# # DEFINE RAGAS METRICS
# # ==========================================================
# #
# # Start with TWO metrics.
# #
# # ContextPrecision:
# # Checks whether the retrieved contexts are relevant.
# #
# # Faithfulness:
# # Checks whether the generated answer is supported
# # by the retrieved context.
# #
# # We are intentionally NOT using:
# #
# # ContextRecall
# # ResponseRelevancy
# #
# # yet, because they require additional LLM calls and
# # can consume your Gemini quota quickly.
# # ==========================================================

# metrics = [

#     ContextPrecision(),

#     Faithfulness(),

# ]


# # ==========================================================
# # START EVALUATION
# # ==========================================================

# print("\n")
# print("=" * 70)
# print("STARTING RAGAS EVALUATION")
# print("=" * 70)

# print("\nMetrics being evaluated:")

# for metric in metrics:

#     print(
#         f" - {metric.__class__.__name__}"
#     )


# try:

#     result = evaluate(

#         dataset=dataset,

#         metrics=metrics,

#         llm=evaluator_llm,

#     )


# except Exception as e:

#     print("\n")
#     print("=" * 70)
#     print("❌ RAGAS EVALUATION FAILED")
#     print("=" * 70)

#     print(str(e))

#     print("\nPossible causes:")

#     print(
#         "1. Gemini API quota has been exhausted."
#     )

#     print(
#         "2. Gemini API request timed out."
#     )

#     print(
#         "3. Evaluator model is temporarily unavailable."
#     )

#     raise


# # ==========================================================
# # DISPLAY RESULTS
# # ==========================================================

# print("\n")
# print("=" * 70)
# print("RAGAS EVALUATION RESULTS")
# print("=" * 70)

# print(result)


# # ==========================================================
# # CONVERT RESULTS TO DATAFRAME
# # ==========================================================

# results_df = result.to_pandas()


# # ==========================================================
# # CREATE EVALUATION DIRECTORY
# # ==========================================================

# evaluation_dir = os.path.join(
#     os.path.dirname(
#         os.path.dirname(
#             os.path.abspath(__file__)
#         )
#     ),
#     "evaluation"
# )

# os.makedirs(
#     evaluation_dir,
#     exist_ok=True
# )


# # ==========================================================
# # SAVE RESULTS
# # ==========================================================

# results_path = os.path.join(
#     evaluation_dir,
#     "evaluation_results.csv"
# )


# results_df.to_csv(
#     results_path,
#     index=False
# )


# # ==========================================================
# # DISPLAY SAVED RESULTS
# # ==========================================================

# print("\n")
# print("=" * 70)
# print("RESULTS SAVED")
# print("=" * 70)

# print(results_path)


# # ==========================================================
# # DISPLAY INDIVIDUAL SCORES
# # ==========================================================

# print("\n")
# print("=" * 70)
# print("METRIC SCORES")
# print("=" * 70)

# for column in results_df.columns:

#     if column in [
#         "context_precision",
#         "faithfulness",
#         "context_recall",
#         "answer_relevancy",
#     ]:

#         value = results_df[column].iloc[0]

#         print(
#             f"{column}: {value}"
#         )


# # ==========================================================
# # COMPLETE
# # ==========================================================

# print("\n")
# print("=" * 70)
# print("EVALUATION COMPLETE")
# print("=" * 70)








# ============================================================
# evaluate_rag.py
# RAG EVALUATION PIPELINE
#
# Pipeline:
# Evaluation Dataset
#       ↓
# Qdrant Retrieval
#       ↓
# Gemini Answer Generation
#       ↓
# Save RAG Results
#       ↓
# RAGAS Evaluation
#       ↓
# Save Evaluation Results
#
# Current metrics:
#   1. Context Precision
#   2. Faithfulness
#
# These two metrics are intentionally used first to avoid
# exhausting Gemini free-tier quota.
# ============================================================

# import os
# import sys
# import time
# import traceback
# import pandas as pd

# from dotenv import load_dotenv

# # ============================================================
# # ENVIRONMENT
# # ============================================================

# load_dotenv()

# # Limit CPU threads to prevent OpenBLAS / MKL memory problems
# os.environ["OPENBLAS_NUM_THREADS"] = "1"
# os.environ["OMP_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"

# # ============================================================
# # RAGAS IMPORTS
# # ============================================================

# try:
#     from ragas import EvaluationDataset, SingleTurnSample, evaluate

#     # New RAGAS import location
#     try:
#         from ragas.metrics.collections import (
#             ContextPrecision,
#             Faithfulness,
#         )
#     except ImportError:
#         # Compatibility with older RAGAS versions
#         from ragas.metrics import (
#             ContextPrecision,
#             Faithfulness,
#         )

# except Exception as e:
#     print("\n❌ Could not import RAGAS.")
#     print("Error:", e)
#     sys.exit(1)


# # ============================================================
# # LANGCHAIN GEMINI
# # ============================================================

# try:
#     from langchain_google_genai import ChatGoogleGenerativeAI
# except ImportError:
#     print("\n❌ langchain-google-genai is not installed.")
#     print("Run:")
#     print("pip install -U langchain-google-genai")
#     sys.exit(1)


# # ============================================================
# # IMPORT YOUR EXISTING RAG FUNCTION
# # ============================================================

# try:
#     from retrieval import run_rag_for_evaluation
# except ImportError as e:
#     print("\n❌ Could not import run_rag_for_evaluation from retrieval.py")
#     print("Error:", e)
#     print("\nMake sure retrieval.py contains:")
#     print("run_rag_for_evaluation(question)")
#     sys.exit(1)


# # ============================================================
# # PATHS
# # ============================================================

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# EVALUATION_DIR = os.path.join(
#     BASE_DIR,
#     "evaluation"
# )

# DATASET_FILE = os.path.join(
#     EVALUATION_DIR,
#     "evaluation_dataset.csv"
# )

# RAG_RESULTS_FILE = os.path.join(
#     EVALUATION_DIR,
#     "rag_results.csv"
# )

# EVALUATION_RESULTS_FILE = os.path.join(
#     EVALUATION_DIR,
#     "evaluation_results.csv"
# )


# # ============================================================
# # CREATE EVALUATION DIRECTORY
# # ============================================================

# os.makedirs(EVALUATION_DIR, exist_ok=True)


# # ============================================================
# # GEMINI CONFIGURATION
# # ============================================================

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if not GOOGLE_API_KEY:
#     print("\n❌ GOOGLE_API_KEY not found.")
#     print("Check your .env file.")
#     sys.exit(1)


# # ============================================================
# # RAGAS EVALUATOR MODEL
# # ============================================================

# # Use a lighter model for evaluation to reduce quota usage.
# #
# # IMPORTANT:
# # Your RAG system's generation model and the RAGAS evaluator
# # model do NOT have to be the same model.
# # ============================================================

# EVALUATOR_MODEL = os.getenv(
#     "RAGAS_EVALUATOR_MODEL",
#     "gemini-3.5-flash-lite"
# )

# print("\n============================================================")
# print("RAG EVALUATION")
# print("============================================================")
# print(f"Evaluator model: {EVALUATOR_MODEL}")


# # ============================================================
# # LOAD DATASET
# # ============================================================

# if not os.path.exists(DATASET_FILE):
#     print("\n❌ Evaluation dataset not found:")
#     print(DATASET_FILE)
#     sys.exit(1)


# try:
#     df = pd.read_csv(DATASET_FILE)
# except Exception as e:
#     print("\n❌ Could not read evaluation dataset.")
#     print("Error:", e)
#     sys.exit(1)


# # ============================================================
# # VALIDATE DATASET
# # ============================================================

# required_columns = [
#     "question",
#     "ground_truth"
# ]

# for column in required_columns:

#     if column not in df.columns:

#         print(
#             f"\n❌ Missing required column: {column}"
#         )

#         print(
#             "Required columns are:"
#         )

#         print(
#             required_columns
#         )

#         sys.exit(1)


# # Remove empty rows

# df = df.dropna(
#     subset=[
#         "question",
#         "ground_truth"
#     ]
# ).reset_index(drop=True)


# print(
#     f"\n✅ Loaded {len(df)} evaluation questions."
# )


# # ============================================================
# # HELPER:
# # NORMALIZE RAG OUTPUT
# # ============================================================

# def normalize_rag_output(result):
#     """
#     Converts different possible return formats from
#     run_rag_for_evaluation() into:

#         answer: str
#         contexts: list[str]

#     Supported formats:

#     1. {
#         "answer": "...",
#         "contexts": [...]
#        }

#     2. {
#         "response": "...",
#         "contexts": [...]
#        }

#     3. ("answer", ["context1", "context2"])

#     4. ("answer", "context")

#     5. Plain string answer
#     """

#     answer = ""
#     contexts = []

#     # --------------------------------------------------------
#     # Dictionary
#     # --------------------------------------------------------

#     if isinstance(result, dict):

#         answer = (
#             result.get("answer")
#             or result.get("response")
#             or result.get("generated_answer")
#             or result.get("text")
#             or ""
#         )

#         contexts = (
#             result.get("contexts")
#             or result.get("context")
#             or result.get("retrieved_contexts")
#             or []
#         )

#     # --------------------------------------------------------
#     # Tuple / List
#     # --------------------------------------------------------

#     elif isinstance(result, (tuple, list)):

#         if len(result) >= 1:

#             answer = result[0]

#         if len(result) >= 2:

#             contexts = result[1]

#     # --------------------------------------------------------
#     # String
#     # --------------------------------------------------------

#     elif isinstance(result, str):

#         answer = result

#     # --------------------------------------------------------
#     # Convert answer to string
#     # --------------------------------------------------------

#     if answer is None:
#         answer = ""

#     answer = str(answer)

#     # --------------------------------------------------------
#     # Normalize contexts
#     # --------------------------------------------------------

#     if contexts is None:

#         contexts = []

#     elif isinstance(contexts, str):

#         contexts = [contexts]

#     elif not isinstance(contexts, list):

#         contexts = list(contexts)

#     # Convert context objects to strings

#     cleaned_contexts = []

#     for context in contexts:

#         if context is None:
#             continue

#         if isinstance(context, str):

#             cleaned_contexts.append(context)

#         else:

#             # Try common document attributes

#             if hasattr(context, "text"):

#                 cleaned_contexts.append(
#                     str(context.text)
#                 )

#             elif hasattr(context, "page_content"):

#                 cleaned_contexts.append(
#                     str(context.page_content)
#                 )

#             else:

#                 cleaned_contexts.append(
#                     str(context)
#                 )

#     return answer.strip(), cleaned_contexts


# # ============================================================
# # RUN RAG ON DATASET
# # ============================================================

# print("\n============================================================")
# print("STEP 1: RUNNING RAG")
# print("============================================================")

# rag_rows = []


# for index, row in df.iterrows():

#     question = str(
#         row["question"]
#     ).strip()

#     ground_truth = str(
#         row["ground_truth"]
#     ).strip()

#     print("\n")
#     print("=" * 70)
#     print(
#         f"QUESTION {index + 1}/{len(df)}"
#     )
#     print("=" * 70)

#     print(
#         f"Question: {question}"
#     )

#     try:

#         # ----------------------------------------------------
#         # Run your existing RAG pipeline
#         # ----------------------------------------------------

#         result = run_rag_for_evaluation(
#             question
#         )

#         # ----------------------------------------------------
#         # Normalize output
#         # ----------------------------------------------------

#         answer, contexts = normalize_rag_output(
#             result
#         )

#         # ----------------------------------------------------
#         # Display
#         # ----------------------------------------------------

#         print("\nGENERATED ANSWER")
#         print("-" * 70)
#         print(answer)

#         print("\nRETRIEVED CONTEXTS")
#         print("-" * 70)

#         if contexts:

#             for context_number, context in enumerate(
#                 contexts,
#                 start=1
#             ):

#                 print(
#                     f"\n--- Context {context_number} ---"
#                 )

#                 print(
#                     context[:2000]
#                 )

#         else:

#             print(
#                 "⚠️ No contexts returned."
#             )

#         # ----------------------------------------------------
#         # Save
#         # ----------------------------------------------------

#         rag_rows.append(
#             {
#                 "question": question,
#                 "ground_truth": ground_truth,
#                 "answer": answer,
#                 "contexts": contexts,
#                 "context_count": len(contexts),
#                 "status": "success"
#             }
#         )

#     except Exception as e:

#         print("\n❌ RAG failed.")

#         print(
#             "Error:",
#             str(e)
#         )

#         traceback.print_exc()

#         rag_rows.append(
#             {
#                 "question": question,
#                 "ground_truth": ground_truth,
#                 "answer": "",
#                 "contexts": [],
#                 "context_count": 0,
#                 "status": f"failed: {str(e)}"
#             }
#         )


# # ============================================================
# # SAVE RAG RESULTS
# # ============================================================

# rag_results_df = pd.DataFrame(
#     rag_rows
# )

# # Convert contexts list to a single string
# # because CSV cannot directly store Python lists.

# rag_results_df["contexts"] = (
#     rag_results_df["contexts"]
#     .apply(
#         lambda x: "\n\n--- CONTEXT SEPARATOR ---\n\n".join(x)
#         if isinstance(x, list)
#         else str(x)
#     )
# )


# rag_results_df.to_csv(
#     RAG_RESULTS_FILE,
#     index=False,
#     encoding="utf-8-sig"
# )


# print("\n")
# print("=" * 70)
# print("RAG RESULTS SAVED")
# print("=" * 70)

# print(
#     RAG_RESULTS_FILE
# )


# # ============================================================
# # CHECK SUCCESSFUL ROWS
# # ============================================================

# successful_df = rag_results_df[
#     rag_results_df["status"] == "success"
# ].copy()


# print(
#     f"\nSuccessful RAG responses: "
#     f"{len(successful_df)}/{len(rag_results_df)}"
# )


# if len(successful_df) == 0:

#     print(
#         "\n❌ No successful RAG responses."
#     )

#     print(
#         "RAGAS evaluation cannot continue."
#     )

#     sys.exit(1)


# # ============================================================
# # PREPARE RAGAS DATASET
# # ============================================================

# print("\n")
# print("=" * 70)
# print("STEP 2: PREPARING RAGAS DATASET")
# print("=" * 70)


# samples = []


# for _, row in successful_df.iterrows():

#     question = str(
#         row["question"]
#     )

#     answer = str(
#         row["answer"]
#     )

#     ground_truth = str(
#         row["ground_truth"]
#     )

#     # Reconstruct contexts

#     contexts_text = str(
#         row["contexts"]
#     )

#     if contexts_text.strip():

#         contexts = [
#             c.strip()
#             for c in contexts_text.split(
#                 "\n\n--- CONTEXT SEPARATOR ---\n\n"
#             )
#             if c.strip()
#         ]

#     else:

#         contexts = []

#     # --------------------------------------------------------
#     # Skip rows without contexts
#     # --------------------------------------------------------

#     if not contexts:

#         print(
#             f"⚠️ Skipping question because no context was retrieved:"
#         )

#         print(
#             question
#         )

#         continue

#     # --------------------------------------------------------
#     # Create RAGAS sample
#     # --------------------------------------------------------

#     sample = SingleTurnSample(
#         user_input=question,
#         response=answer,
#         retrieved_contexts=contexts,
#         reference=ground_truth
#     )

#     samples.append(
#         sample
#     )


# if not samples:

#     print(
#         "\n❌ No valid samples available for RAGAS."
#     )

#     sys.exit(1)


# evaluation_dataset = EvaluationDataset(
#     samples=samples
# )


# print(
#     f"\n✅ Prepared {len(samples)} samples for RAGAS."
# )


# # ============================================================
# # CREATE EVALUATOR LLM
# # ============================================================

# print("\n")
# print("=" * 70)
# print("STEP 3: CREATING RAGAS EVALUATOR")
# print("=" * 70)

# try:

#     evaluator_llm = ChatGoogleGenerativeAI(
#         model=EVALUATOR_MODEL,
#         google_api_key=GOOGLE_API_KEY,
#         temperature=0
#     )

#     print(
#         f"✅ Evaluator ready: {EVALUATOR_MODEL}"
#     )

# except Exception as e:

#     print(
#         "\n❌ Could not create evaluator."
#     )

#     print(
#         "Error:",
#         e
#     )

#     sys.exit(1)


# # ============================================================
# # METRICS
# # ============================================================

# print("\n")
# print("=" * 70)
# print("STEP 4: RAGAS EVALUATION")
# print("=" * 70)

# print(
#     "\nMetrics being evaluated:"
# )

# print(
#     " - Context Precision"
# )

# print(
#     " - Faithfulness"
# )


# metrics = [
#     ContextPrecision(),
#     Faithfulness()
# ]


# # ============================================================
# # RUN RAGAS
# # ============================================================

# try:

#     result = evaluate(
#         dataset=evaluation_dataset,
#         metrics=metrics,
#         llm=evaluator_llm
#     )

# except Exception as e:

#     print("\n")
#     print("=" * 70)
#     print("❌ RAGAS EVALUATION FAILED")
#     print("=" * 70)

#     print(
#         "\nError:",
#         str(e)
#     )

#     traceback.print_exc()

#     sys.exit(1)


# # ============================================================
# # CONVERT RESULTS TO DICTIONARY
# # ============================================================

# try:

#     result_dict = result.to_pandas().to_dict(
#         orient="records"
#     )

#     result_df = pd.DataFrame(
#         result_dict
#     )

# except Exception:

#     try:

#         result_df = pd.DataFrame(
#             result
#         )

#     except Exception:

#         result_df = pd.DataFrame(
#             [dict(result)]
#         )


# # ============================================================
# # DISPLAY RESULTS
# # ============================================================

# print("\n")
# print("=" * 70)
# print("RAGAS EVALUATION RESULTS")
# print("=" * 70)

# print(
#     result
# )


# # ============================================================
# # ADD QUESTIONS TO RESULT
# # ============================================================

# # RAGAS result normally has one row per sample.

# if len(result_df) == len(successful_df):

#     result_df.insert(
#         0,
#         "question",
#         successful_df["question"].values
#     )


# # ============================================================
# # SAVE EVALUATION RESULTS
# # ============================================================

# result_df.to_csv(
#     EVALUATION_RESULTS_FILE,
#     index=False,
#     encoding="utf-8-sig"
# )


# print("\n")
# print("=" * 70)
# print("RESULTS SAVED")
# print("=" * 70)

# print(
#     EVALUATION_RESULTS_FILE
# )


# # ============================================================
# # PRINT AVERAGE METRICS
# # ============================================================

# print("\n")
# print("=" * 70)
# print("AVERAGE METRIC SCORES")
# print("=" * 70)


# for metric_name in [
#     "context_precision",
#     "faithfulness"
# ]:

#     if metric_name in result_df.columns:

#         values = pd.to_numeric(
#             result_df[metric_name],
#             errors="coerce"
#         )

#         average = values.mean()

#         print(
#             f"{metric_name}: {average:.4f}"
#         )


# # ============================================================
# # COUNT SUCCESS / FAILURE
# # ============================================================

# print("\n")
# print("=" * 70)
# print("EVALUATION SUMMARY")
# print("=" * 70)

# print(
#     f"Total questions: {len(df)}"
# )

# print(
#     f"Successful RAG responses: {len(successful_df)}"
# )

# print(
#     f"RAGAS samples evaluated: {len(result_df)}"
# )


# # ============================================================
# # END
# # ============================================================

# print("\n")
# print("=" * 70)
# print("EVALUATION COMPLETE")
# print("=" * 70)










# import os
# import ast
# import pandas as pd

# from dotenv import load_dotenv

# # ============================================================
# # RAGAS IMPORTS
# # ============================================================

# from ragas import EvaluationDataset, SingleTurnSample, evaluate

# # IMPORTANT:
# # New RAGAS versions use metrics.collections
# from ragas.metrics.collections import (
#     ContextPrecision,
#     Faithfulness,
# )

# from langchain_google_genai import ChatGoogleGenerativeAI


# # ============================================================
# # CONFIGURATION
# # ============================================================

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if not GOOGLE_API_KEY:
#     raise ValueError(
#         "GOOGLE_API_KEY not found.\n"
#         "Please add GOOGLE_API_KEY=your_key_here to your .env file."
#     )


# # ============================================================
# # PATHS
# # ============================================================

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# EVALUATION_DIR = os.path.join(BASE_DIR, "evaluation")

# RAG_RESULTS_FILE = os.path.join(
#     EVALUATION_DIR,
#     "rag_results.csv"
# )

# EVALUATION_RESULTS_FILE = os.path.join(
#     EVALUATION_DIR,
#     "evaluation_results.csv"
# )


# # ============================================================
# # CREATE EVALUATION DIRECTORY
# # ============================================================

# os.makedirs(EVALUATION_DIR, exist_ok=True)


# # ============================================================
# # DISPLAY HEADER
# # ============================================================

# print()
# print("=" * 70)
# print("RAGAS EVALUATION")
# print("=" * 70)
# print()


# # ============================================================
# # CHECK RAG RESULTS FILE
# # ============================================================

# if not os.path.exists(RAG_RESULTS_FILE):

#     print("❌ rag_results.csv was not found.")
#     print()
#     print(f"Expected location:")
#     print(RAG_RESULTS_FILE)
#     print()

#     raise FileNotFoundError(
#         "rag_results.csv does not exist. "
#         "Run your RAG pipeline first."
#     )


# print("✅ Found RAG results:")
# print(RAG_RESULTS_FILE)
# print()


# # ============================================================
# # LOAD RAG RESULTS
# # ============================================================

# print("=" * 70)
# print("STEP 1: LOADING RAG RESULTS")
# print("=" * 70)

# df = pd.read_csv(RAG_RESULTS_FILE)

# print()
# print(f"Total rows found: {len(df)}")
# print()

# print("Columns found:")
# for column in df.columns:
#     print(f" - {column}")

# print()


# # ============================================================
# # HELPER FUNCTION
# # ============================================================

# def find_column(dataframe, possible_names):
#     """
#     Find a column using several possible names.
#     Matching is case-insensitive.
#     """

#     normalized_columns = {
#         str(column).strip().lower(): column
#         for column in dataframe.columns
#     }

#     for name in possible_names:

#         key = name.strip().lower()

#         if key in normalized_columns:
#             return normalized_columns[key]

#     return None


# # ============================================================
# # FIND REQUIRED COLUMNS
# # ============================================================

# QUESTION_COLUMN = find_column(
#     df,
#     [
#         "question",
#         "query",
#         "user_input",
#         "user question",
#     ]
# )

# ANSWER_COLUMN = find_column(
#     df,
#     [
#         "answer",
#         "response",
#         "generated_answer",
#         "generated answer",
#     ]
# )

# CONTEXT_COLUMN = find_column(
#     df,
#     [
#         "contexts",
#         "context",
#         "retrieved_contexts",
#         "retrieved contexts",
#         "retrieved_context",
#     ]
# )

# GROUND_TRUTH_COLUMN = find_column(
#     df,
#     [
#         "ground_truth",
#         "ground truth",
#         "reference",
#         "expected_answer",
#         "expected answer",
#     ]
# )


# # ============================================================
# # PRINT COLUMN MAPPING
# # ============================================================

# print("=" * 70)
# print("COLUMN MAPPING")
# print("=" * 70)

# print()
# print(f"Question column     : {QUESTION_COLUMN}")
# print(f"Answer column       : {ANSWER_COLUMN}")
# print(f"Context column      : {CONTEXT_COLUMN}")
# print(f"Ground truth column : {GROUND_TRUTH_COLUMN}")
# print()


# # ============================================================
# # VALIDATE REQUIRED COLUMNS
# # ============================================================

# missing_columns = []

# if QUESTION_COLUMN is None:
#     missing_columns.append("question")

# if ANSWER_COLUMN is None:
#     missing_columns.append("answer")

# if CONTEXT_COLUMN is None:
#     missing_columns.append("contexts")

# if GROUND_TRUTH_COLUMN is None:
#     missing_columns.append("ground_truth")


# if missing_columns:

#     print("❌ Required columns are missing:")
#     print()

#     for column in missing_columns:
#         print(f" - {column}")

#     print()
#     print("Actual CSV columns:")
#     print(list(df.columns))
#     print()

#     raise ValueError(
#         "rag_results.csv does not contain all required columns."
#     )


# # ============================================================
# # CONVERT CONTEXT INTO LIST
# # ============================================================

# def parse_contexts(value):
#     """
#     Convert contexts stored in CSV into a list of strings.

#     Handles:
#     - Python list strings
#     - JSON-like list strings
#     - single strings
#     - empty values
#     """

#     if pd.isna(value):
#         return []

#     # Already a Python list
#     if isinstance(value, list):
#         return [
#             str(item).strip()
#             for item in value
#             if str(item).strip()
#         ]

#     value = str(value).strip()

#     if not value:
#         return []

#     # Try Python literal parsing
#     try:

#         parsed = ast.literal_eval(value)

#         if isinstance(parsed, list):

#             return [
#                 str(item).strip()
#                 for item in parsed
#                 if str(item).strip()
#             ]

#     except Exception:
#         pass

#     # Try JSON-style parsing
#     try:

#         import json

#         parsed = json.loads(value)

#         if isinstance(parsed, list):

#             return [
#                 str(item).strip()
#                 for item in parsed
#                 if str(item).strip()
#             ]

#     except Exception:
#         pass

#     # If it is just one context
#     return [value]


# # ============================================================
# # PREPARE RAGAS DATASET
# # ============================================================

# print("=" * 70)
# print("STEP 2: PREPARING RAGAS DATASET")
# print("=" * 70)
# print()


# samples = []

# skipped_rows = 0


# for index, row in df.iterrows():

#     question = str(row[QUESTION_COLUMN]).strip()

#     answer = str(row[ANSWER_COLUMN]).strip()

#     ground_truth = str(
#         row[GROUND_TRUTH_COLUMN]
#     ).strip()

#     contexts = parse_contexts(
#         row[CONTEXT_COLUMN]
#     )


#     # --------------------------------------------------------
#     # Skip invalid rows
#     # --------------------------------------------------------

#     if not question:
#         skipped_rows += 1
#         continue

#     if not answer:
#         skipped_rows += 1
#         continue

#     if not contexts:
#         skipped_rows += 1
#         continue


#     # --------------------------------------------------------
#     # Create RAGAS sample
#     # --------------------------------------------------------

#     sample = SingleTurnSample(
#         user_input=question,
#         response=answer,
#         retrieved_contexts=contexts,
#         reference=ground_truth,
#     )

#     samples.append(sample)


# print(f"✅ Prepared {len(samples)} samples for RAGAS.")

# if skipped_rows:
#     print(
#         f"⚠️ Skipped {skipped_rows} invalid rows."
#     )

# print()


# # ============================================================
# # CHECK DATASET
# # ============================================================

# if len(samples) == 0:

#     raise ValueError(
#         "No valid samples were prepared for RAGAS."
#     )


# dataset = EvaluationDataset(samples)


# # ============================================================
# # CREATE RAGAS EVALUATOR
# # ============================================================

# print("=" * 70)
# print("STEP 3: CREATING RAGAS EVALUATOR")
# print("=" * 70)
# print()


# # IMPORTANT:
# # This model is used ONLY for RAGAS evaluation.
# #
# # It does NOT regenerate your RAG answers.
# #
# # This avoids wasting your primary Gemini model quota.

# EVALUATOR_MODEL = "gemini-3.5-flash-lite"


# evaluator_llm = ChatGoogleGenerativeAI(
#     model=EVALUATOR_MODEL,
#     google_api_key=GOOGLE_API_KEY,
#     temperature=0,
# )


# print(
#     f"✅ Evaluator ready: {EVALUATOR_MODEL}"
# )

# print()


# # ============================================================
# # CREATE METRICS
# # ============================================================

# print("=" * 70)
# print("STEP 4: CREATING RAGAS METRICS")
# print("=" * 70)
# print()


# # IMPORTANT:
# #
# # Your current RAGAS version requires:
# #
# # ContextPrecision(llm=evaluator_llm)
# #
# # Faithfulness(llm=evaluator_llm)
# #
# # This fixes:
# #
# # TypeError:
# # ContextPrecision.__init__() missing
# # 1 required positional argument: 'llm'

# context_precision = ContextPrecision(
#     llm=evaluator_llm
# )

# faithfulness = Faithfulness(
#     llm=evaluator_llm
# )


# metrics = [
#     context_precision,
#     faithfulness,
# ]


# print("Metrics being evaluated:")
# print(" - Context Precision")
# print(" - Faithfulness")
# print()


# # ============================================================
# # RUN RAGAS
# # ============================================================

# print("=" * 70)
# print("STEP 5: RUNNING RAGAS EVALUATION")
# print("=" * 70)
# print()

# print(
#     f"Evaluating {len(samples)} samples..."
# )

# print()


# try:

#     result = evaluate(
#         dataset=dataset,
#         metrics=metrics,
#     )

# except Exception as error:

#     print()
#     print("=" * 70)
#     print("❌ RAGAS EVALUATION FAILED")
#     print("=" * 70)
#     print()

#     print("Error:")
#     print(error)

#     print()

#     raise


# # ============================================================
# # CONVERT RESULTS TO DICTIONARY
# # ============================================================

# print()
# print("=" * 70)
# print("STEP 6: RAGAS RESULTS")
# print("=" * 70)
# print()


# result_dict = result.to_pandas()


# # ============================================================
# # SAVE DETAILED RESULTS
# # ============================================================

# result_dict.to_csv(
#     EVALUATION_RESULTS_FILE,
#     index=False,
# )


# print(
#     f"✅ Detailed results saved to:"
# )

# print(
#     EVALUATION_RESULTS_FILE
# )

# print()


# # ============================================================
# # CALCULATE AVERAGE SCORES
# # ============================================================

# print("=" * 70)
# print("FINAL METRIC SCORES")
# print("=" * 70)
# print()


# metric_columns = [
#     "context_precision",
#     "faithfulness",
# ]


# average_scores = {}


# for metric in metric_columns:

#     if metric in result_dict.columns:

#         score = pd.to_numeric(
#             result_dict[metric],
#             errors="coerce",
#         ).mean()

#         average_scores[metric] = score

#         if pd.isna(score):

#             print(
#                 f"{metric}: NaN"
#             )

#         else:

#             print(
#                 f"{metric}: {score:.4f}"
#             )


# print()


# # ============================================================
# # SCORE INTERPRETATION
# # ============================================================

# print("=" * 70)
# print("SCORE INTERPRETATION")
# print("=" * 70)
# print()


# for metric, score in average_scores.items():

#     if pd.isna(score):
#         continue

#     if score >= 0.90:

#         interpretation = "Excellent"

#     elif score >= 0.75:

#         interpretation = "Good"

#     elif score >= 0.50:

#         interpretation = "Needs improvement"

#     else:

#         interpretation = "Poor"

#     print(
#         f"{metric}: {score:.4f} → {interpretation}"
#     )


# print()


# # ============================================================
# # FINAL SUMMARY
# # ============================================================

# print("=" * 70)
# print("EVALUATION COMPLETE")
# print("=" * 70)
# print()

# print(
#     f"RAG samples evaluated : {len(samples)}"
# )

# print(
#     f"Evaluator model       : {EVALUATOR_MODEL}"
# )

# print(
#     "Metrics               : Context Precision, Faithfulness"
# )

# print()

# print(
#     "Results file:"
# )

# print(
#     EVALUATION_RESULTS_FILE
# )

# print()

# print("=" * 70)










import os

# ==========================================================
# LIMIT BLAS THREADS
# Prevents OpenBLAS memory allocation problems on Windows
# ==========================================================

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"


# ==========================================================
# IMPORTS
# ==========================================================

import pandas as pd

from dotenv import load_dotenv

from ragas import EvaluationDataset, SingleTurnSample, evaluate

from ragas.metrics import (
    Faithfulness,
    ContextPrecision,
)

from langchain_google_genai import ChatGoogleGenerativeAI

from retrieval import run_rag_for_evaluation


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file."
    )


# ==========================================================
# TEST DATA
# ==========================================================
#
# Add more questions here later.
#
# For now, keep only ONE question while testing
# the evaluation pipeline. This saves Gemini API quota.
# ==========================================================

test_questions = [

    {
        "question": "What is the price of M Sand?",
        "ground_truth": "The price of M-Sand is ₹1,250 per Cum.",
    },

]


# ==========================================================
# RAGAS EVALUATOR LLM
# ==========================================================
#
# IMPORTANT:
# This model is ONLY used by RAGAS for evaluation.
#
# Your actual RAG model remains inside retrieval.py.
#
# Using a lighter evaluator helps reduce API usage.
# ==========================================================

evaluator_llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
)


# ==========================================================
# RUN RAG
# ==========================================================

samples = []


for item in test_questions:

    question = item["question"]
    ground_truth = item["ground_truth"]

    print("\n")
    print("=" * 70)
    print("QUESTION")
    print("=" * 70)

    print(question)

    try:

        # --------------------------------------------------
        # Run your existing RAG pipeline
        # --------------------------------------------------

        answer, contexts = run_rag_for_evaluation(
            question
        )


        # ==================================================
        # DISPLAY RETRIEVED CONTEXTS
        # ==================================================

        print("\n")
        print("=" * 70)
        print("RETRIEVED CONTEXTS")
        print("=" * 70)

        for i, context in enumerate(
            contexts,
            start=1
        ):

            print(f"\n--- Context {i} ---")

            print(
                context[:1000]
            )


        # ==================================================
        # DISPLAY GENERATED ANSWER
        # ==================================================

        print("\n")
        print("=" * 70)
        print("GENERATED ANSWER")
        print("=" * 70)

        print(answer)


        # ==================================================
        # DISPLAY GROUND TRUTH
        # ==================================================

        print("\n")
        print("=" * 70)
        print("GROUND TRUTH")
        print("=" * 70)

        print(ground_truth)


        # ==================================================
        # CREATE RAGAS SAMPLE
        # ==================================================

        sample = SingleTurnSample(

            user_input=question,

            retrieved_contexts=contexts,

            response=answer,

            reference=ground_truth,

        )

        samples.append(sample)


    except Exception as e:

        print("\n")
        print("=" * 70)
        print("❌ ERROR WHILE RUNNING RAG")
        print("=" * 70)

        print(str(e))


# ==========================================================
# CHECK SAMPLES
# ==========================================================

if not samples:

    raise RuntimeError(
        "No evaluation samples were created."
    )


# ==========================================================
# CREATE RAGAS DATASET
# ==========================================================

dataset = EvaluationDataset(
    samples=samples
)


# ==========================================================
# DEFINE RAGAS METRICS
# ==========================================================
#
# Start with TWO metrics.
#
# ContextPrecision:
# Checks whether the retrieved contexts are relevant.
#
# Faithfulness:
# Checks whether the generated answer is supported
# by the retrieved context.
#
# We are intentionally NOT using:
#
# ContextRecall
# ResponseRelevancy
#
# yet, because they require additional LLM calls and
# can consume your Gemini quota quickly.
# ==========================================================

metrics = [

    ContextPrecision(),

    Faithfulness(),

]


# ==========================================================
# START EVALUATION
# ==========================================================

print("\n")
print("=" * 70)
print("STARTING RAGAS EVALUATION")
print("=" * 70)

print("\nMetrics being evaluated:")

for metric in metrics:

    print(
        f" - {metric.__class__.__name__}"
    )


try:

    result = evaluate(

        dataset=dataset,

        metrics=metrics,

        llm=evaluator_llm,

    )


except Exception as e:

    print("\n")
    print("=" * 70)
    print("❌ RAGAS EVALUATION FAILED")
    print("=" * 70)

    print(str(e))

    print("\nPossible causes:")

    print(
        "1. Gemini API quota has been exhausted."
    )

    print(
        "2. Gemini API request timed out."
    )

    print(
        "3. Evaluator model is temporarily unavailable."
    )

    raise


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print("\n")
print("=" * 70)
print("RAGAS EVALUATION RESULTS")
print("=" * 70)

print(result)


# ==========================================================
# CONVERT RESULTS TO DATAFRAME
# ==========================================================

results_df = result.to_pandas()


# ==========================================================
# CREATE EVALUATION DIRECTORY
# ==========================================================

evaluation_dir = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
    "evaluation"
)

os.makedirs(
    evaluation_dir,
    exist_ok=True
)


# ==========================================================
# SAVE RESULTS
# ==========================================================

results_path = os.path.join(
    evaluation_dir,
    "evaluation_results.csv"
)


results_df.to_csv(
    results_path,
    index=False
)


# ==========================================================
# DISPLAY SAVED RESULTS
# ==========================================================

print("\n")
print("=" * 70)
print("RESULTS SAVED")
print("=" * 70)

print(results_path)


# ==========================================================
# DISPLAY INDIVIDUAL SCORES
# ==========================================================

print("\n")
print("=" * 70)
print("METRIC SCORES")
print("=" * 70)

for column in results_df.columns:

    if column in [
        "context_precision",
        "faithfulness",
        "context_recall",
        "answer_relevancy",
    ]:

        value = results_df[column].iloc[0]

        print(
            f"{column}: {value}"
        )


# ==========================================================
# COMPLETE
# ==========================================================

print("\n")
print("=" * 70)
print("EVALUATION COMPLETE")
print("=" * 70)

