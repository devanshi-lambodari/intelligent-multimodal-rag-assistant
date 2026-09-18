from retrieval import run_rag_for_evaluation


question = "What is Python?"

answer, contexts = run_rag_for_evaluation(
    question
)


print("\n" + "=" * 60)
print("EVALUATION PIPELINE TEST")
print("=" * 60)


print("\nQUESTION:")
print(question)


print("\nRETRIEVED CONTEXTS:")

for i, context in enumerate(
    contexts,
    start=1
):

    print(f"\n--- Context {i} ---")

    print(context)


print("\nANSWER:")

print(answer)