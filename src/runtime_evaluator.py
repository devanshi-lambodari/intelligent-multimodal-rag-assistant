# # import os

# # from dotenv import load_dotenv

# # from ragas import EvaluationDataset, SingleTurnSample, evaluate

# # from ragas.metrics import Faithfulness

# # try:
# #     from ragas.metrics import AnswerRelevancy

# #     AnswerRelevancyMetric = AnswerRelevancy
# #     ANSWER_RELEVANCY_NAME = "answer_relevancy"

# # except ImportError:

# #     from ragas.metrics import ResponseRelevancy

# #     AnswerRelevancyMetric = ResponseRelevancy
# #     ANSWER_RELEVANCY_NAME = "response_relevancy"


# # from langchain_google_genai import ChatGoogleGenerativeAI

# # from langchain_huggingface import HuggingFaceEmbeddings


# # # ==========================================================
# # # LOAD ENVIRONMENT
# # # ==========================================================

# # load_dotenv()


# # GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# # if not GOOGLE_API_KEY:

# #     raise ValueError(
# #         "GOOGLE_API_KEY is missing from your .env file."
# #     )


# # # ==========================================================
# # # RAGAS EVALUATOR MODEL
# # # ==========================================================

# # RAGAS_EVALUATOR_MODEL = os.getenv(
# #     "RAGAS_EVALUATOR_MODEL",
# #     "gemini-3.5-flash-lite"
# # )


# # # ==========================================================
# # # GEMINI EVALUATOR
# # # ==========================================================

# # evaluator_llm = ChatGoogleGenerativeAI(
# #     model=RAGAS_EVALUATOR_MODEL,
# #     google_api_key=GOOGLE_API_KEY,
# #     temperature=0,
# # )


# # # ==========================================================
# # # HUGGINGFACE EMBEDDINGS
# # # ==========================================================

# # # IMPORTANT:
# # #
# # # This prevents Answer Relevancy from trying to use
# # # OpenAI embeddings.
# # #
# # # We are using the same embedding family already used
# # # by your Qdrant RAG system.
# # # ==========================================================

# # evaluator_embeddings = HuggingFaceEmbeddings(
# #     model_name="BAAI/bge-small-en-v1.5"
# # )


# # # ==========================================================
# # # RAGAS METRICS
# # # ==========================================================

# # # ----------------------------------------------------------
# # # FAITHFULNESS
# # # ----------------------------------------------------------

# # faithfulness_metric = Faithfulness(
# #     llm=evaluator_llm
# # )


# # # ----------------------------------------------------------
# # # ANSWER RELEVANCY
# # # ----------------------------------------------------------

# # try:

# #     answer_relevancy_metric = AnswerRelevancyMetric(
# #         llm=evaluator_llm,
# #         embeddings=evaluator_embeddings,
# #     )

# # except TypeError:

# #     # Some RAGAS versions use a different constructor.
# #     #
# #     # Try the metric with the LLM only as a fallback.

# #     answer_relevancy_metric = AnswerRelevancyMetric(
# #         llm=evaluator_llm
# #     )


# # # ==========================================================
# # # RUNTIME EVALUATION FUNCTION
# # # ==========================================================

# # def evaluate_runtime_response(
# #     question: str,
# #     answer: str,
# #     contexts: list[str],
# # ) -> dict:
# #     """
# #     Evaluate one chatbot response during runtime.

# #     Runtime metrics:

# #         1. Faithfulness
# #         2. Answer Relevancy

# #     Context Precision is intentionally NOT used here
# #     because your installed RAGAS version requires a
# #     reference/ground-truth answer for that metric.
# #     """

# #     print("\n" + "=" * 60)
# #     print("RUNTIME RAGAS EVALUATION")
# #     print("=" * 60)


# #     # ======================================================
# #     # VALIDATE INPUT
# #     # ======================================================

# #     if not question or not question.strip():

# #         print("⚠️ Empty question.")

# #         return {
# #             "faithfulness": None,
# #             "context_precision": None,
# #             "answer_relevancy": None,
# #         }


# #     if not answer or not answer.strip():

# #         print("⚠️ Empty answer.")

# #         return {
# #             "faithfulness": None,
# #             "context_precision": None,
# #             "answer_relevancy": None,
# #         }


# #     if not contexts:

# #         print("⚠️ No contexts available.")

# #         return {
# #             "faithfulness": None,
# #             "context_precision": None,
# #             "answer_relevancy": None,
# #         }


# #     # ======================================================
# #     # CLEAN CONTEXTS
# #     # ======================================================

# #     cleaned_contexts = [
# #         str(context).strip()
# #         for context in contexts
# #         if context and str(context).strip()
# #     ]


# #     if not cleaned_contexts:

# #         print("⚠️ Contexts are empty after cleaning.")

# #         return {
# #             "faithfulness": None,
# #             "context_precision": None,
# #             "answer_relevancy": None,
# #         }


# #     # ======================================================
# #     # CREATE RAGAS SAMPLE
# #     # ======================================================

# #     sample = SingleTurnSample(
# #         user_input=str(question).strip(),
# #         response=str(answer).strip(),
# #         retrieved_contexts=cleaned_contexts,
# #     )


# #     # ======================================================
# #     # CONVERT SAMPLE TO DICTIONARY
# #     # ======================================================

# #     try:

# #         sample_dict = sample.model_dump(
# #             exclude_none=True
# #         )

# #     except AttributeError:

# #         sample_dict = sample.dict(
# #             exclude_none=True
# #         )


# #     # ======================================================
# #     # CREATE DATASET
# #     # ======================================================

# #     dataset = EvaluationDataset.from_list(
# #         [sample_dict]
# #     )


# #     # ======================================================
# #     # RUNTIME METRICS
# #     # ======================================================

# #     metrics = [
# #         faithfulness_metric,
# #         answer_relevancy_metric,
# #     ]


# #     # ======================================================
# #     # RUN RAGAS
# #     # ======================================================

# #     try:

# #         result = evaluate(
# #             dataset=dataset,
# #             metrics=metrics,
# #         )


# #         # ==================================================
# #         # CONVERT RESULT
# #         # ==================================================

# #         result_df = result.to_pandas()


# #         print("\n📊 Runtime Evaluation Results")
# #         print("-" * 60)


# #         # ==================================================
# #         # FAITHFULNESS
# #         # ==================================================

# #         faithfulness = None


# #         if "faithfulness" in result_df.columns:

# #             value = result_df[
# #                 "faithfulness"
# #             ].iloc[0]


# #             if value == value:

# #                 faithfulness = float(value)


# #         # ==================================================
# #         # ANSWER RELEVANCY
# #         # ==================================================

# #         answer_relevancy = None


# #         if ANSWER_RELEVANCY_NAME in result_df.columns:

# #             value = result_df[
# #                 ANSWER_RELEVANCY_NAME
# #             ].iloc[0]


# #             if value == value:

# #                 answer_relevancy = float(value)


# #         # ==================================================
# #         # CONTEXT PRECISION
# #         # ==================================================

# #         # Not available during runtime because there is
# #         # no ground-truth/reference answer.

# #         context_precision = None


# #         # ==================================================
# #         # PRINT RESULTS
# #         # ==================================================

# #         print(
# #             "Faithfulness       : "
# #             + (
# #                 str(faithfulness)
# #                 if faithfulness is not None
# #                 else "N/A"
# #             )
# #         )


# #         print(
# #             "Context Precision  : "
# #             "N/A (requires reference)"
# #         )


# #         print(
# #             "Answer Relevancy   : "
# #             + (
# #                 str(answer_relevancy)
# #                 if answer_relevancy is not None
# #                 else "N/A"
# #             )
# #         )


# #         print("=" * 60)


# #         # ==================================================
# #         # RETURN
# #         # ==================================================

# #         return {
# #             "faithfulness": faithfulness,
# #             "context_precision": context_precision,
# #             "answer_relevancy": answer_relevancy,
# #         }


# #     # ======================================================
# #     # ERROR HANDLING
# #     # ======================================================

# #     except Exception as e:

# #         print("\n❌ RAGAS evaluation failed:")

# #         print(
# #             f"{type(e).__name__}: {e}"
# #         )


# #         return {
# #             "faithfulness": None,
# #             "context_precision": None,
# #             "answer_relevancy": None,
# #         }


# # # ==========================================================
# # # DIRECT TEST
# # # ==========================================================

# # if __name__ == "__main__":

# #     test_question = (
# #         "What is the price of M sand?"
# #     )


# #     test_answer = (
# #         "The price of M-Sand is "
# #         "₹1,250 per Cum."
# #     )


# #     test_contexts = [

# #         (
# #             "M-Sand is available at a rate "
# #             "of INR 1,250 per Cum."
# #         ),

# #         (
# #             "M-Sand quantity is 10 Cum."
# #         ),

# #         (
# #             "The amount for M-Sand is "
# #             "INR 12,500."
# #         ),

# #     ]


# #     scores = evaluate_runtime_response(
# #         question=test_question,
# #         answer=test_answer,
# #         contexts=test_contexts,
# #     )


# #     print("\nFinal Runtime Scores:")

# #     print(scores)







# import os
# import re
# import json

# from dotenv import load_dotenv

# from ragas import EvaluationDataset, SingleTurnSample, evaluate

# # ==========================================================
# # IMPORTANT:
# #
# # Your installed RAGAS version's COLLECTIONS metrics only
# # support InstructorLLM / OpenAI.
# #
# # Therefore we intentionally use the LEGACY metrics here.
# #
# # They work with ChatGoogleGenerativeAI.
# # ==========================================================

# from ragas.metrics import (
#     Faithfulness,
#     AnswerRelevancy,
# )

# from langchain_google_genai import ChatGoogleGenerativeAI

# from langchain_huggingface import HuggingFaceEmbeddings


# # ==========================================================
# # LOAD ENVIRONMENT
# # ==========================================================

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if not GOOGLE_API_KEY:
#     raise ValueError(
#         "GOOGLE_API_KEY is missing from your .env file."
#     )


# # ==========================================================
# # CONFIGURATION
# # ==========================================================

# RAGAS_EVALUATOR_MODEL = os.getenv(
#     "RAGAS_EVALUATOR_MODEL",
#     "gemini-3.5-flash-lite"
# )

# EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# # ==========================================================
# # GEMINI EVALUATOR
# # ==========================================================

# evaluator_llm = ChatGoogleGenerativeAI(
#     model=RAGAS_EVALUATOR_MODEL,
#     google_api_key=GOOGLE_API_KEY,
#     temperature=0,
# )


# # ==========================================================
# # HUGGINGFACE EMBEDDINGS
# # ==========================================================

# # Used by Answer Relevancy.
# #
# # This prevents RAGAS from attempting to use OpenAI
# # embeddings.
# # ==========================================================

# evaluator_embeddings = HuggingFaceEmbeddings(
#     model_name=EMBEDDING_MODEL
# )


# # ==========================================================
# # CREATE RAGAS METRICS
# # ==========================================================

# faithfulness_metric = Faithfulness(
#     llm=evaluator_llm
# )


# answer_relevancy_metric = AnswerRelevancy(
#     llm=evaluator_llm,
#     embeddings=evaluator_embeddings,
# )


# # ==========================================================
# # HELPER: CLEAN GEMINI JSON
# # ==========================================================

# def clean_json_response(text: str) -> str:
#     """
#     Remove Markdown code fences from Gemini JSON responses.

#     Example:

#         ```json
#         {
#             "statements": []
#         }
#         ```

#     becomes:

#         {
#             "statements": []
#         }
#     """

#     if not text:
#         return text

#     text = text.strip()

#     # ------------------------------------------------------
#     # Remove ```json ... ```
#     # ------------------------------------------------------

#     if text.startswith("```"):

#         text = re.sub(
#             r"^```(?:json)?\s*",
#             "",
#             text,
#             flags=re.IGNORECASE,
#         )

#         text = re.sub(
#             r"\s*```$",
#             "",
#             text,
#         )

#     return text.strip()


# # ==========================================================
# # HELPER: SAFE FLOAT
# # ==========================================================

# def safe_float(value):
#     """
#     Safely convert a RAGAS score to float.
#     """

#     try:

#         if value is None:
#             return None

#         value = float(value)

#         # NaN check
#         if value != value:
#             return None

#         return value

#     except Exception:

#         return None


# # ==========================================================
# # RUNTIME EVALUATION
# # ==========================================================

# def evaluate_runtime_response(
#     question: str,
#     answer: str,
#     contexts: list[str],
# ) -> dict:
#     """
#     Evaluate a single runtime chatbot response.

#     Runtime metrics:

#         1. Faithfulness
#         2. Answer Relevancy

#     Context Precision is intentionally excluded because
#     your installed RAGAS version requires a reference/
#     ground-truth answer for that metric.
#     """

#     print("\n" + "=" * 60)
#     print("RUNTIME RAGAS EVALUATION")
#     print("=" * 60)


#     # ======================================================
#     # VALIDATE QUESTION
#     # ======================================================

#     if not question or not question.strip():

#         print("⚠️ Empty question.")

#         return {
#             "faithfulness": None,
#             "context_precision": None,
#             "answer_relevancy": None,
#         }


#     # ======================================================
#     # VALIDATE ANSWER
#     # ======================================================

#     if not answer or not answer.strip():

#         print("⚠️ Empty answer.")

#         return {
#             "faithfulness": None,
#             "context_precision": None,
#             "answer_relevancy": None,
#         }


#     # ======================================================
#     # VALIDATE CONTEXTS
#     # ======================================================

#     if not contexts:

#         print("⚠️ No contexts available.")

#         return {
#             "faithfulness": None,
#             "context_precision": None,
#             "answer_relevancy": None,
#         }


#     # ======================================================
#     # CLEAN CONTEXTS
#     # ======================================================

#     cleaned_contexts = []

#     for context in contexts:

#         if context is None:
#             continue

#         context = str(context).strip()

#         if context:
#             cleaned_contexts.append(context)


#     if not cleaned_contexts:

#         print("⚠️ Contexts are empty.")

#         return {
#             "faithfulness": None,
#             "context_precision": None,
#             "answer_relevancy": None,
#         }


#     # ======================================================
#     # CREATE RAGAS SAMPLE
#     # ======================================================

#     sample = SingleTurnSample(
#         user_input=question.strip(),
#         response=answer.strip(),
#         retrieved_contexts=cleaned_contexts,
#     )


#     # ======================================================
#     # CONVERT SAMPLE TO DICTIONARY
#     # ======================================================

#     try:

#         sample_dict = sample.model_dump(
#             exclude_none=True
#         )

#     except AttributeError:

#         sample_dict = sample.dict(
#             exclude_none=True
#         )


#     # ======================================================
#     # CREATE DATASET
#     # ======================================================

#     dataset = EvaluationDataset.from_list(
#         [sample_dict]
#     )


#     # ======================================================
#     # RUN EVALUATION
#     # ======================================================

#     try:

#         result = evaluate(
#             dataset=dataset,
#             metrics=[
#                 faithfulness_metric,
#                 answer_relevancy_metric,
#             ],
#         )


#         # ==================================================
#         # CONVERT RESULT
#         # ==================================================

#         result_df = result.to_pandas()


#         print("\n📊 Runtime Evaluation Results")
#         print("-" * 60)


#         # ==================================================
#         # INITIALIZE SCORES
#         # ==================================================

#         faithfulness = None

#         answer_relevancy = None

#         context_precision = None


#         # ==================================================
#         # FAITHFULNESS
#         # ==================================================

#         if "faithfulness" in result_df.columns:

#             faithfulness = safe_float(
#                 result_df["faithfulness"].iloc[0]
#             )


#         # ==================================================
#         # ANSWER RELEVANCY
#         # ==================================================

#         if "answer_relevancy" in result_df.columns:

#             answer_relevancy = safe_float(
#                 result_df["answer_relevancy"].iloc[0]
#             )


#         # ==================================================
#         # CONTEXT PRECISION
#         # ==================================================

#         # Intentionally unavailable at runtime because
#         # your RAGAS version requires a reference answer.

#         context_precision = None


#         # ==================================================
#         # PRINT RESULTS
#         # ==================================================

#         if faithfulness is not None:

#             print(
#                 f"Faithfulness       : "
#                 f"{faithfulness:.4f}"
#             )

#         else:

#             print(
#                 "Faithfulness       : N/A"
#             )


#         print(
#             "Context Precision  : "
#             "N/A (requires reference)"
#         )


#         if answer_relevancy is not None:

#             print(
#                 f"Answer Relevancy   : "
#                 f"{answer_relevancy:.4f}"
#             )

#         else:

#             print(
#                 "Answer Relevancy   : N/A"
#             )


#         print("=" * 60)


#         # ==================================================
#         # RETURN RESULTS
#         # ==================================================

#         return {
#             "faithfulness": faithfulness,
#             "context_precision": context_precision,
#             "answer_relevancy": answer_relevancy,
#         }


#     # ======================================================
#     # ERROR HANDLING
#     # ======================================================

#     except Exception as e:

#         print("\n❌ RAGAS evaluation failed:")

#         print(
#             f"{type(e).__name__}: {e}"
#         )


#         return {
#             "faithfulness": None,
#             "context_precision": None,
#             "answer_relevancy": None,
#         }


# # ==========================================================
# # DIRECT TEST
# # ==========================================================

# if __name__ == "__main__":

#     print("\n" + "=" * 60)
#     print("RUNTIME RAGAS EVALUATOR TEST")
#     print("=" * 60)


#     # ------------------------------------------------------
#     # TEST QUESTION
#     # ------------------------------------------------------

#     test_question = (
#         "What is the price of M sand?"
#     )


#     # ------------------------------------------------------
#     # TEST ANSWER
#     # ------------------------------------------------------

#     test_answer = (
#         "The price of M-Sand is "
#         "₹1,250 per Cum."
#     )


#     # ------------------------------------------------------
#     # TEST CONTEXTS
#     # ------------------------------------------------------

#     test_contexts = [

#         (
#             "M-Sand is available at a rate "
#             "of INR 1,250 per Cum."
#         ),

#         (
#             "M-Sand quantity is 10 Cum."
#         ),

#         (
#             "The amount for M-Sand is "
#             "INR 12,500."
#         ),

#     ]


#     # ------------------------------------------------------
#     # RUN
#     # ------------------------------------------------------

#     scores = evaluate_runtime_response(
#         question=test_question,
#         answer=test_answer,
#         contexts=test_contexts,
#     )


#     # ------------------------------------------------------
#     # FINAL SCORES
#     # ------------------------------------------------------

#     print("\nFinal Runtime Scores:")

#     print(scores)

#     print("=" * 60)











# import os
# import re
# from typing import List, Dict, Any, Optional

# from dotenv import load_dotenv

# from ragas import EvaluationDataset, SingleTurnSample
# from ragas.metrics import AnswerRelevancy

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_huggingface import HuggingFaceEmbeddings


# # ==========================================================
# # LOAD ENVIRONMENT
# # ==========================================================

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if not GOOGLE_API_KEY:
#     raise ValueError(
#         "GOOGLE_API_KEY not found in .env file."
#     )


# # ==========================================================
# # CONFIGURATION
# # ==========================================================

# # Gemini model used for runtime evaluation
# EVALUATOR_MODEL = "gemini-3.5-flash-lite"

# # Local embedding model
# EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# # ==========================================================
# # RAGAS ANSWER RELEVANCY LLM
# # ==========================================================

# evaluator_llm = ChatGoogleGenerativeAI(
#     model=EVALUATOR_MODEL,
#     google_api_key=GOOGLE_API_KEY,
#     temperature=0,
# )


# # ==========================================================
# # HUGGINGFACE EMBEDDINGS
# # ==========================================================
# #
# # Important:
# # RAGAS AnswerRelevancy may otherwise try to use OpenAI
# # embeddings internally.
# #
# # Using the same local BGE embedding model avoids the need
# # for OPENAI_API_KEY.
# # ==========================================================

# evaluator_embeddings = HuggingFaceEmbeddings(
#     model_name=EMBEDDING_MODEL
# )


# # ==========================================================
# # RAGAS ANSWER RELEVANCY METRIC
# # ==========================================================

# answer_relevancy_metric = AnswerRelevancy(
#     llm=evaluator_llm,
#     embeddings=evaluator_embeddings,
# )


# # ==========================================================
# # GEMINI FAITHFULNESS JUDGE
# # ==========================================================
# #
# # We intentionally DO NOT use:
# #
# #     ragas.metrics.Faithfulness
# #
# # because RAGAS 0.4.3 + ChatGoogleGenerativeAI can produce
# # fenced JSON such as:
# #
# # ```json
# # {
# #     ...
# # }
# # ```
# #
# # which causes RAGAS's internal JSON parser to fail.
# #
# # Instead, Gemini returns a simple:
# #
# # SCORE: 0.95
# # REASON: ...
# #
# # This is much more robust.
# # ==========================================================


# def _extract_score(text: str) -> Optional[float]:
#     """
#     Extract SCORE: <number> from Gemini response.

#     Example accepted responses:

#         SCORE: 0.95

#         SCORE: 1

#         SCORE: 0.72
#     """

#     if not text:
#         return None

#     match = re.search(
#         r"SCORE\s*:\s*([01](?:\.\d+)?)",
#         text,
#         flags=re.IGNORECASE,
#     )

#     if not match:
#         return None

#     try:
#         score = float(match.group(1))

#         # Safety clamp
#         score = max(0.0, min(1.0, score))

#         return score

#     except ValueError:
#         return None


# def _extract_reason(text: str) -> str:
#     """
#     Extract the reason from Gemini's response.
#     """

#     if not text:
#         return "No evaluation reason returned."

#     match = re.search(
#         r"REASON\s*:\s*(.+)",
#         text,
#         flags=re.IGNORECASE | re.DOTALL,
#     )

#     if match:
#         reason = match.group(1).strip()

#         # Remove unnecessary markdown/code fences if Gemini adds them
#         reason = reason.replace("```", "").strip()

#         return reason

#     return text.strip()


# def evaluate_faithfulness_with_gemini(
#     question: str,
#     answer: str,
#     contexts: List[str],
# ) -> Dict[str, Any]:
#     """
#     Evaluate whether the generated answer is supported by
#     the retrieved context.

#     Score:
#         1.0 = completely supported
#         0.0 = completely unsupported

#     The evaluator checks factual claims in the answer against
#     the supplied context.
#     """

#     if not answer.strip():
#         return {
#             "score": 0.0,
#             "reason": "The answer is empty.",
#         }

#     if not contexts:
#         return {
#             "score": 0.0,
#             "reason": "No context was provided for faithfulness evaluation.",
#         }

#     formatted_context = "\n\n".join(
#         [
#             f"[CONTEXT {i + 1}]\n{context}"
#             for i, context in enumerate(contexts)
#         ]
#     )

#     prompt = f"""
# You are a strict RAG faithfulness evaluator.

# Your job is to determine whether the factual claims made in the
# ANSWER are supported by the provided CONTEXT.

# Do NOT judge whether the answer is generally true from your own
# knowledge.

# Only use the supplied CONTEXT.

# Evaluation rules:

# 1. Identify the factual claims in the ANSWER.
# 2. Check whether each claim is directly supported by the CONTEXT.
# 3. If all factual claims are supported, give a score close to 1.0.
# 4. If some claims are unsupported, lower the score.
# 5. If most or all claims are unsupported, give a low score.
# 6. Do not penalize harmless wording differences.
# 7. Do not penalize concise summaries when they accurately represent
#    the context.
# 8. Do not use outside knowledge.

# Return EXACTLY this format:

# SCORE: <number between 0 and 1>
# REASON: <one concise sentence>

# Do not return JSON.
# Do not use Markdown.
# Do not use code fences.

# QUESTION:
# {question}

# CONTEXT:
# {formatted_context}

# ANSWER:
# {answer}
# """

#     try:
#         response = evaluator_llm.invoke(prompt)

#         # LangChain AIMessage normally has .content
#         raw_text = getattr(response, "content", response)

#         if isinstance(raw_text, list):
#             raw_text = " ".join(
#                 str(item)
#                 for item in raw_text
#             )

#         raw_text = str(raw_text).strip()

#         score = _extract_score(raw_text)
#         reason = _extract_reason(raw_text)

#         if score is None:
#             return {
#                 "score": None,
#                 "reason": (
#                     "Could not parse Gemini faithfulness score. "
#                     f"Raw response: {raw_text[:500]}"
#                 ),
#             }

#         return {
#             "score": score,
#             "reason": reason,
#         }

#     except Exception as e:

#         print(
#             f"Warning: Gemini faithfulness evaluation failed: {e}"
#         )

#         return {
#             "score": None,
#             "reason": f"Faithfulness evaluation failed: {e}",
#         }


# # ==========================================================
# # RAGAS ANSWER RELEVANCY
# # ==========================================================

# def evaluate_answer_relevancy(
#     question: str,
#     answer: str,
# ) -> Optional[float]:
#     """
#     Evaluate whether the answer is relevant to the question.

#     This metric does not require ground truth.
#     """

#     if not question.strip() or not answer.strip():
#         return None

#     try:

#         sample = SingleTurnSample(
#             user_input=question,
#             response=answer,
#         )

#         # Convert the sample into a normal dictionary.
#         #
#         # This is important because EvaluationDataset.from_list()
#         # expects dictionaries in this RAGAS version.
#         try:
#             sample_dict = sample.model_dump(
#                 exclude_none=True
#             )
#         except AttributeError:
#             sample_dict = sample.dict(
#                 exclude_none=True
#             )

#         dataset = EvaluationDataset.from_list(
#             [sample_dict]
#         )

#         result = answer_relevancy_metric.single_turn_score(
#             sample
#         )

#         return float(result)

#     except Exception as e:

#         print(
#             f"Warning: Answer Relevancy evaluation failed: {e}"
#         )

#         return None


# # ==========================================================
# # MAIN RUNTIME EVALUATOR
# # ==========================================================

# def evaluate_runtime_response(
#     question: str,
#     answer: str,
#     contexts: Optional[List[str]] = None,
# ) -> Dict[str, Any]:
#     """
#     Run runtime evaluation for one generated response.

#     Runtime metrics:

#         Faithfulness
#         Answer Relevancy

#     Context Precision is intentionally not calculated here
#     because RAGAS 0.4.3 requires a reference/ground truth.

#     Returns:

#         {
#             "faithfulness": ...,
#             "faithfulness_reason": ...,
#             "context_precision": None,
#             "answer_relevancy": ...,
#         }
#     """

#     if contexts is None:
#         contexts = []

#     # Make sure contexts are strings
#     cleaned_contexts = [
#         str(context).strip()
#         for context in contexts
#         if context is not None
#         and str(context).strip()
#     ]

#     print("\n" + "=" * 60)
#     print("RUNTIME RAGAS EVALUATION")
#     print("=" * 60)

#     # ======================================================
#     # 1. FAITHFULNESS
#     # ======================================================

#     print("\nEvaluating Faithfulness...")

#     faithfulness_result = evaluate_faithfulness_with_gemini(
#         question=question,
#         answer=answer,
#         contexts=cleaned_contexts,
#     )

#     faithfulness_score = faithfulness_result.get(
#         "score"
#     )

#     faithfulness_reason = faithfulness_result.get(
#         "reason"
#     )

#     if faithfulness_score is not None:

#         print(
#             f"Faithfulness       : "
#             f"{faithfulness_score:.4f}"
#         )

#         print(
#             f"Faithfulness Reason: "
#             f"{faithfulness_reason}"
#         )

#     else:

#         print(
#             "Faithfulness       : N/A"
#         )

#         print(
#             f"Faithfulness Reason: "
#             f"{faithfulness_reason}"
#         )

#     # ======================================================
#     # 2. CONTEXT PRECISION
#     # ======================================================
#     #
#     # Context Precision requires reference/ground truth
#     # in RAGAS 0.4.3.
#     #
#     # Therefore it remains an OFFLINE evaluation metric.
#     # ======================================================

#     context_precision_score = None

#     print(
#         "Context Precision  : "
#         "N/A (requires reference)"
#     )

#     # ======================================================
#     # 3. ANSWER RELEVANCY
#     # ======================================================

#     print("\nEvaluating Answer Relevancy...")

#     answer_relevancy_score = evaluate_answer_relevancy(
#         question=question,
#         answer=answer,
#     )

#     if answer_relevancy_score is not None:

#         print(
#             f"Answer Relevancy   : "
#             f"{answer_relevancy_score:.4f}"
#         )

#     else:

#         print(
#             "Answer Relevancy   : N/A"
#         )

#     # ======================================================
#     # FINAL RESULT
#     # ======================================================

#     results = {
#         "faithfulness": faithfulness_score,
#         "faithfulness_reason": faithfulness_reason,
#         "context_precision": context_precision_score,
#         "answer_relevancy": answer_relevancy_score,
#     }

#     print("\n" + "=" * 60)
#     print("FINAL RUNTIME SCORES")
#     print("=" * 60)

#     print(
#         f"Faithfulness       : "
#         f"{faithfulness_score if faithfulness_score is not None else 'N/A'}"
#     )

#     print(
#         "Context Precision  : "
#         "N/A (requires reference)"
#     )

#     print(
#         f"Answer Relevancy   : "
#         f"{answer_relevancy_score if answer_relevancy_score is not None else 'N/A'}"
#     )

#     print("=" * 60)

#     return results


# # ==========================================================
# # STANDALONE TEST
# # ==========================================================

# if __name__ == "__main__":

#     print("\n")
#     print("=" * 60)
#     print("RUNTIME RAGAS EVALUATOR TEST")
#     print("=" * 60)

#     test_question = (
#         "What is the price of M sand?"
#     )

#     test_answer = (
#         "The price of M sand is 1500 rupees."
#     )

#     test_contexts = [
#         "M sand price is 1500 rupees."
#     ]

#     scores = evaluate_runtime_response(
#         question=test_question,
#         answer=test_answer,
#         contexts=test_contexts,
#     )

#     print("\nReturned dictionary:")
#     print(scores)











import os
import re
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv

from ragas import EvaluationDataset, SingleTurnSample

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================================
# LOAD ENVIRONMENT
# ==========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file."
    )


# ==========================================================
# CONFIGURATION
# ==========================================================

# Gemini model used for runtime evaluation
EVALUATOR_MODEL = "gemini-3.5-flash-lite"

# Local embedding model
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# ==========================================================
# GEMINI EVALUATOR LLM
# ==========================================================

evaluator_llm = ChatGoogleGenerativeAI(
    model=EVALUATOR_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
)


# ==========================================================
# HUGGINGFACE EMBEDDINGS
# ==========================================================

# We keep the HuggingFace embedding model available because
# it is the same embedding model used by the RAG system.
#
# This avoids requiring OPENAI_API_KEY.
#
# NOTE:
# Answer Relevancy below is evaluated using Gemini directly,
# so we do not depend on RAGAS's internal JSON parser.
# ==========================================================

evaluator_embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


# ==========================================================
# HELPER: EXTRACT GEMINI TEXT
# ==========================================================

def _get_response_text(response: Any) -> str:
    """
    Safely extract plain text from a LangChain AIMessage.

    Gemini/LangChain responses can sometimes contain
    structured metadata. We only want the actual text.
    """

    raw_text = getattr(response, "content", response)

    # Normal text response
    if isinstance(raw_text, str):
        return raw_text.strip()

    # Some LangChain versions can return a list of blocks
    if isinstance(raw_text, list):
        text_parts = []

        for item in raw_text:
            if isinstance(item, str):
                text_parts.append(item)

            elif isinstance(item, dict):
                # Prefer the actual text field
                if "text" in item:
                    text_parts.append(str(item["text"]))

                elif "content" in item:
                    text_parts.append(str(item["content"]))

        return " ".join(text_parts).strip()

    return str(raw_text).strip()


# ==========================================================
# HELPER: EXTRACT SCORE
# ==========================================================

def _extract_score(text: str) -> Optional[float]:
    """
    Extract:

        SCORE: 0.95

    from Gemini's response.
    """

    if not text:
        return None

    match = re.search(
        r"SCORE\s*:\s*([01](?:\.\d+)?)",
        text,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    try:
        score = float(match.group(1))

        # Safety clamp
        score = max(0.0, min(1.0, score))

        return score

    except ValueError:
        return None


# ==========================================================
# HELPER: EXTRACT REASON
# ==========================================================

def _extract_reason(text: str) -> str:
    """
    Extract only the text after:

        REASON:

    from Gemini's response.

    This prevents Gemini metadata such as
    'extras' and 'signature' from appearing in the output.
    """

    if not text:
        return "No evaluation reason returned."

    match = re.search(
        r"REASON\s*:\s*(.+)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        reason = match.group(1).strip()

        # Remove markdown/code fences
        reason = reason.replace("```json", "")
        reason = reason.replace("```", "")
        reason = reason.strip()

        # Keep only the first meaningful line
        reason = reason.splitlines()[0].strip()

        return reason

    return text.strip()


# ==========================================================
# GEMINI FAITHFULNESS JUDGE
# ==========================================================

def evaluate_faithfulness_with_gemini(
    question: str,
    answer: str,
    contexts: List[str],
) -> Dict[str, Any]:
    """
    Evaluate whether the generated answer is supported
    by the retrieved context.

    Score:

        1.0 = completely supported
        0.0 = completely unsupported

    Only the supplied contexts are used.
    """

    if not answer.strip():
        return {
            "score": 0.0,
            "reason": "The answer is empty.",
        }

    if not contexts:
        return {
            "score": 0.0,
            "reason": (
                "No context was provided for faithfulness evaluation."
            ),
        }

    formatted_context = "\n\n".join(
        [
            f"[CONTEXT {i + 1}]\n{context}"
            for i, context in enumerate(contexts)
        ]
    )

    prompt = f"""
You are a strict RAG faithfulness evaluator.

Your job is to determine whether the factual claims made
in the ANSWER are supported by the provided CONTEXT.

Do NOT judge whether the answer is generally true from
your own knowledge.

Only use the supplied CONTEXT.

Evaluation rules:

1. Identify the factual claims in the ANSWER.
2. Check whether each claim is directly supported by CONTEXT.
3. If all factual claims are supported, give a score close to 1.0.
4. If some claims are unsupported, lower the score.
5. If most or all claims are unsupported, give a low score.
6. Do not penalize harmless wording differences.
7. Do not penalize concise summaries when they accurately represent
   the context.
8. Do not use outside knowledge.

Return EXACTLY this format:

SCORE: <number between 0 and 1>
REASON: <one concise sentence>

Do not return JSON.
Do not use Markdown.
Do not use code fences.

QUESTION:
{question}

CONTEXT:
{formatted_context}

ANSWER:
{answer}
"""

    try:
        response = evaluator_llm.invoke(prompt)

        raw_text = _get_response_text(response)

        score = _extract_score(raw_text)
        reason = _extract_reason(raw_text)

        if score is None:
            return {
                "score": None,
                "reason": (
                    "Could not parse Gemini faithfulness score."
                ),
            }

        return {
            "score": score,
            "reason": reason,
        }

    except Exception as e:

        print(
            f"Warning: Gemini faithfulness evaluation failed: {e}"
        )

        return {
            "score": None,
            "reason": (
                f"Faithfulness evaluation failed: {e}"
            ),
        }


# ==========================================================
# GEMINI ANSWER RELEVANCY JUDGE
# ==========================================================

def evaluate_answer_relevancy_with_gemini(
    question: str,
    answer: str,
) -> Dict[str, Any]:
    """
    Evaluate whether the answer directly addresses the question.

    Score:

        1.0 = highly relevant
        0.0 = completely irrelevant

    This intentionally uses Gemini directly instead of the
    RAGAS AnswerRelevancy parser because Gemini can sometimes
    return fenced JSON, which causes RAGAS parsing failures.
    """

    if not question.strip():
        return {
            "score": None,
            "reason": "The question is empty.",
        }

    if not answer.strip():
        return {
            "score": 0.0,
            "reason": "The answer is empty.",
        }

    prompt = f"""
You are a strict answer relevancy evaluator for a RAG chatbot.

Determine how directly the ANSWER addresses the QUESTION.

Evaluation rules:

1. Give a high score when the answer directly answers the question.
2. Give a lower score when the answer is only partially relevant.
3. Give a very low score when the answer does not address the question.
4. Do not judge factual correctness.
5. Do not use outside knowledge.
6. Focus only on whether the answer addresses what was asked.
7. Concise answers can receive a high score if they directly answer
   the question.

Scoring:

1.0 = completely relevant and directly answers the question
0.8 = highly relevant with minor unnecessary information
0.6 = mostly relevant but somewhat incomplete
0.4 = partially relevant
0.2 = mostly irrelevant
0.0 = completely irrelevant

Return EXACTLY this format:

SCORE: <number between 0 and 1>
REASON: <one concise sentence>

Do not return JSON.
Do not use Markdown.
Do not use code fences.

QUESTION:
{question}

ANSWER:
{answer}
"""

    try:
        response = evaluator_llm.invoke(prompt)

        raw_text = _get_response_text(response)

        score = _extract_score(raw_text)
        reason = _extract_reason(raw_text)

        if score is None:
            return {
                "score": None,
                "reason": (
                    "Could not parse Gemini answer relevancy score."
                ),
            }

        return {
            "score": score,
            "reason": reason,
        }

    except Exception as e:

        print(
            f"Warning: Gemini answer relevancy evaluation failed: {e}"
        )

        return {
            "score": None,
            "reason": (
                f"Answer relevancy evaluation failed: {e}"
            ),
        }


# ==========================================================
# MAIN RUNTIME EVALUATOR
# ==========================================================

def evaluate_runtime_response(
    question: str,
    answer: str,
    contexts: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Run runtime evaluation for one generated response.

    Runtime metrics:

        1. Faithfulness
        2. Context Precision -> intentionally N/A
        3. Answer Relevancy

    IMPORTANT:

    Context Precision from RAGAS 0.4.3 requires a reference/
    ground-truth answer, which is not available for a normal
    live chatbot question.

    Therefore Context Precision remains the ONLY intentional
    N/A metric during runtime.

    Offline evaluation continues to calculate Context Precision
    using the labeled evaluation dataset.
    """

    if contexts is None:
        contexts = []

    # Make sure contexts are strings
    cleaned_contexts = [
        str(context).strip()
        for context in contexts
        if context is not None
        and str(context).strip()
    ]

    print("\n" + "=" * 60)
    print("RUNTIME RAGAS EVALUATION")
    print("=" * 60)

    # ======================================================
    # 1. FAITHFULNESS
    # ======================================================

    print("\nEvaluating Faithfulness...")

    faithfulness_result = evaluate_faithfulness_with_gemini(
        question=question,
        answer=answer,
        contexts=cleaned_contexts,
    )

    faithfulness_score = faithfulness_result.get("score")
    faithfulness_reason = faithfulness_result.get("reason")

    if faithfulness_score is not None:

        print(
            f"Faithfulness       : "
            f"{faithfulness_score:.4f}"
        )

        print(
            f"Faithfulness Reason: "
            f"{faithfulness_reason}"
        )

    else:

        print(
            "Faithfulness       : N/A"
        )

        print(
            f"Faithfulness Reason: "
            f"{faithfulness_reason}"
        )

    # ======================================================
    # 2. CONTEXT PRECISION
    # ======================================================

    # RAGAS 0.4.3 Context Precision requires reference/
    # ground truth.
    #
    # Since a live user question normally has no reference,
    # this remains intentionally unavailable at runtime.
    #
    # This is the ONLY expected N/A in the runtime evaluator.
    # ======================================================

    context_precision_score = None

    print(
        "Context Precision  : "
        "N/A (requires reference)"
    )

    # ======================================================
    # 3. ANSWER RELEVANCY
    # ======================================================

    print("\nEvaluating Answer Relevancy...")

    answer_relevancy_result = (
        evaluate_answer_relevancy_with_gemini(
            question=question,
            answer=answer,
        )
    )

    answer_relevancy_score = answer_relevancy_result.get(
        "score"
    )

    answer_relevancy_reason = answer_relevancy_result.get(
        "reason"
    )

    if answer_relevancy_score is not None:

        print(
            f"Answer Relevancy   : "
            f"{answer_relevancy_score:.4f}"
        )

        print(
            f"Answer Relevancy Reason: "
            f"{answer_relevancy_reason}"
        )

    else:

        print(
            "Answer Relevancy   : N/A"
        )

        print(
            f"Answer Relevancy Reason: "
            f"{answer_relevancy_reason}"
        )

    # ======================================================
    # FINAL RESULT
    # ======================================================

    results = {
        "faithfulness": faithfulness_score,
        "faithfulness_reason": faithfulness_reason,
        "context_precision": context_precision_score,
        "answer_relevancy": answer_relevancy_score,
        "answer_relevancy_reason": answer_relevancy_reason,
    }

    print("\n" + "=" * 60)
    print("FINAL RUNTIME SCORES")
    print("=" * 60)

    print(
        f"Faithfulness       : "
        f"{faithfulness_score if faithfulness_score is not None else 'N/A'}"
    )

    print(
        "Context Precision  : "
        "N/A (requires reference)"
    )

    print(
        f"Answer Relevancy   : "
        f"{answer_relevancy_score if answer_relevancy_score is not None else 'N/A'}"
    )

    print("=" * 60)

    return results


# ==========================================================
# STANDALONE TEST
# ==========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("RUNTIME RAG EVALUATOR TEST")
    print("=" * 60)

    test_question = (
        "What is the price of M sand?"
    )

    test_answer = (
        "The price of M sand is 1500 rupees."
    )

    test_contexts = [
        "M sand price is 1500 rupees."
    ]

    scores = evaluate_runtime_response(
        question=test_question,
        answer=test_answer,
        contexts=test_contexts,
    )

    print("\nReturned dictionary:")
    print(scores)
