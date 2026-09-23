# # # import redis

# # # import re

# # # def normalize_query(query):     #new
# # #     query = query.lower().strip()       #new
# # #     query = re.sub(r"[^\w\s]", "", query)       #new
# # #     return query        #new

# # # redis_client = redis.Redis(
# # #     host="localhost",
# # #     port=6379,
# # #     decode_responses=True
# # # )


# # # def get_cached_answer(question):
# # #     """
# # #     Returns cached answer if available.
# # #     Otherwise returns None.
# # #     """
# # #     question = normalize_query(question) #new
# # #     # return redis_client.get(question)
# # #     try:
# # #         return redis_client.get(question)
# # #     except redis.exceptions.ConnectionError:
# # #         return None

# # # def cache_answer(question, answer):
# # #     """
# # #     Store answer in Redis.
# # #     """
# # #     question = normalize_query(question) #new
# # #     # redis_client.set(question, answer, ex=3600)
# # #     try:
# # #         redis_client.set(question, answer, ex=3600)
# # #     except redis.exceptions.ConnectionError:
# # #         pass

# # # def clear_cache():
# # #     try:
# # #         redis_client.flushdb()
# # #     except redis.exceptions.ConnectionError:
# # #         pass


# # # def is_redis_alive():
# # #     try:
# # #         redis_client.ping()
# # #         return True
# # #     except redis.exceptions.ConnectionError:
# # #         return False






# # import re
# # import redis


# # # ==========================================================
# # # CONFIGURATION
# # # ==========================================================

# # REDIS_HOST = "localhost"
# # REDIS_PORT = 6379

# # CACHE_TTL = 3600  # 1 hour


# # # ==========================================================
# # # REDIS CLIENT
# # # ==========================================================

# # redis_client = redis.Redis(
# #     host=REDIS_HOST,
# #     port=REDIS_PORT,
# #     decode_responses=True,
# # )


# # # ==========================================================
# # # NORMALIZE QUERY
# # # ==========================================================

# # def normalize_query(query: str) -> str:
# #     """
# #     Normalize the user's question so that
# #     slightly different formatting produces
# #     the same cache key.
# #     """

# #     query = query.lower().strip()

# #     # Remove punctuation
# #     query = re.sub(r"[^\w\s]", "", query)

# #     # Remove multiple spaces
# #     query = re.sub(r"\s+", " ", query)

# #     return query


# # # ==========================================================
# # # GENERATE CACHE KEY
# # # ==========================================================

# # def get_cache_key(question: str) -> str:
# #     """
# #     Generate a dedicated Redis key for RAG answers.
# #     """

# #     normalized_question = normalize_query(question)

# #     return f"rag:answer:{normalized_question}"


# # # ==========================================================
# # # CHECK REDIS CONNECTION
# # # ==========================================================

# # def is_redis_alive() -> bool:
# #     """
# #     Check whether Redis is available.
# #     """

# #     try:

# #         redis_client.ping()

# #         return True

# #     except redis.exceptions.RedisError:

# #         return False


# # # ==========================================================
# # # GET CACHED ANSWER
# # # ==========================================================

# # def get_cached_answer(question: str):
# #     """
# #     Return cached answer if available.

# #     Returns:
# #         str: cached answer
# #         None: if no cached answer exists
# #               or Redis is unavailable
# #     """

# #     cache_key = get_cache_key(question)

# #     try:

# #         return redis_client.get(cache_key)

# #     except redis.exceptions.RedisError:

# #         return None


# # # ==========================================================
# # # CACHE ANSWER
# # # ==========================================================

# # def cache_answer(
# #     question: str,
# #     answer: str,
# # ):
# #     """
# #     Store the generated answer in Redis.

# #     Cache expires after CACHE_TTL seconds.
# #     """

# #     cache_key = get_cache_key(question)

# #     try:

# #         redis_client.set(
# #             cache_key,
# #             answer,
# #             ex=CACHE_TTL,
# #         )

# #     except redis.exceptions.RedisError:

# #         pass


# # # ==========================================================
# # # CLEAR CACHE
# # # ==========================================================

# # def clear_cache():
# #     """
# #     Clear all Redis cache entries.

# #     Useful during development/testing.
# #     """

# #     try:

# #         redis_client.flushdb()

# #         print("✅ Redis cache cleared.")

# #     except redis.exceptions.RedisError:

# #         print("⚠️ Could not clear Redis cache.")





# import re
# import redis


# # ==========================================================
# # REDIS CONNECTION
# # ==========================================================

# redis_client = redis.Redis(
#     host="localhost",
#     port=6379,
#     decode_responses=True
# )


# # ==========================================================
# # CONFIGURATION
# # ==========================================================

# CACHE_TTL = 3600
# CACHE_PREFIX = "rag:"


# # ==========================================================
# # NORMALIZE QUERY
# # ==========================================================

# def normalize_query(query: str) -> str:

#     query = query.lower().strip()

#     query = re.sub(
#         r"[^\w\s]",
#         "",
#         query
#     )

#     query = re.sub(
#         r"\s+",
#         " ",
#         query
#     )

#     return query


# # ==========================================================
# # CREATE REDIS KEY
# # ==========================================================

# def make_cache_key(question: str) -> str:

#     normalized_question = normalize_query(
#         question
#     )

#     return f"{CACHE_PREFIX}{normalized_question}"


# # ==========================================================
# # GET CACHED ANSWER
# # ==========================================================

# def get_cached_answer(question: str):

#     key = make_cache_key(question)

#     try:

#         return redis_client.get(key)

#     except redis.exceptions.ConnectionError:

#         return None


# # ==========================================================
# # CACHE ANSWER
# # ==========================================================

# def cache_answer(
#     question: str,
#     answer: str
# ):

#     key = make_cache_key(question)

#     try:

#         redis_client.set(
#             key,
#             answer,
#             ex=CACHE_TTL
#         )

#     except redis.exceptions.ConnectionError:

#         pass


# # ==========================================================
# # CLEAR CACHE
# # ==========================================================

# def clear_cache():

#     try:

#         redis_client.flushdb()

#     except redis.exceptions.ConnectionError:

#         pass


# # ==========================================================
# # CHECK REDIS
# # ==========================================================

# def is_redis_alive():

#     try:

#         redis_client.ping()

#         return True

#     except redis.exceptions.ConnectionError:

#         return False




# import redis
# import re
import os
import redis
import re
from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# REDIS CONFIGURATION
# ==========================================================

# REDIS_HOST = "localhost"
# REDIS_PORT = 6379
# REDIS_DB = 0

# CACHE_EXPIRATION = 3600  # 1 hour
REDIS_URL = os.getenv("REDIS_URL")

REDIS_DB = 0

CACHE_EXPIRATION = 3600  # 1 hour


# ==========================================================
# REDIS CLIENT
# ==========================================================

# redis_client = redis.Redis(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     db=REDIS_DB,
#     decode_responses=True,
# )
redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True
)

# ==========================================================
# NORMALIZE QUERY
# ==========================================================

def normalize_query(query: str) -> str:
    """
    Converts logically identical questions into the
    same Redis key.

    Example:

    "Who is Devanshi?"
    "WHO IS DEVANSHI?"
    " who is devanshi "
    "Who is Devanshi!!!"

    all become:

    "who is devanshi"
    """

    if not query:
        return ""

    # Convert to lowercase
    query = query.lower()

    # Remove punctuation
    query = re.sub(
        r"[^\w\s]",
        "",
        query
    )

    # Remove extra spaces
    query = re.sub(
        r"\s+",
        " ",
        query
    )

    # Remove leading/trailing spaces
    query = query.strip()

    return query


# ==========================================================
# CREATE REDIS KEY
# ==========================================================

def make_cache_key(question: str) -> str:
    """
    Creates a consistent Redis key for a question.
    """

    normalized = normalize_query(question)

    return f"rag:answer:{normalized}"


# ==========================================================
# GET CACHED ANSWER
# ==========================================================

def get_cached_answer(question: str):

    key = make_cache_key(question)

    print(f"🔑 Redis lookup key: {key}")

    try:

        answer = redis_client.get(key)

        if answer:

            print("🟢 Redis returned cached answer")

        else:

            print("🔴 Redis key does not exist")

        return answer

    except redis.exceptions.RedisError as e:

        print(
            f"⚠️ Redis GET error: {e}"
        )

        return None


# ==========================================================
# SAVE ANSWER
# ==========================================================

def cache_answer(
    question: str,
    answer: str,
):

    key = make_cache_key(question)

    print(f"🔑 Redis save key: {key}")

    try:

        redis_client.set(
            key,
            answer,
            ex=CACHE_EXPIRATION,
        )

        print(
            f"✅ Answer saved to Redis "
            f"(expires in {CACHE_EXPIRATION} seconds)"
        )

    except redis.exceptions.RedisError as e:

        print(
            f"⚠️ Redis SET error: {e}"
        )


# ==========================================================
# CHECK REDIS
# ==========================================================

def is_redis_alive():

    try:

        return redis_client.ping()

    except redis.exceptions.RedisError:

        return False


# ==========================================================
# DELETE ONE CACHE ENTRY
# ==========================================================

def delete_cached_answer(question: str):

    key = make_cache_key(question)

    try:

        deleted = redis_client.delete(key)

        if deleted:

            print(
                f"🗑️ Deleted cache: {key}"
            )

        else:

            print(
                f"⚠️ Cache not found: {key}"
            )

    except redis.exceptions.RedisError as e:

        print(
            f"⚠️ Redis DELETE error: {e}"
        )


# ==========================================================
# CLEAR ALL RAG CACHE
# ==========================================================

def clear_cache():

    try:

        keys = redis_client.keys(
            "rag:answer:*"
        )

        if keys:

            redis_client.delete(*keys)

            print(
                f"🗑️ Cleared {len(keys)} cached answers"
            )

        else:

            print(
                "ℹ️ No RAG cache entries found"
            )

    except redis.exceptions.RedisError as e:

        print(
            f"⚠️ Redis clear error: {e}"
        )


# ==========================================================
# SHOW CACHE
# ==========================================================

def show_cache():

    try:

        keys = redis_client.keys(
            "rag:answer:*"
        )

        if not keys:

            print(
                "ℹ️ Redis cache is empty"
            )

            return

        print("\n" + "=" * 60)
        print("REDIS CACHE")
        print("=" * 60)

        for key in keys:

            value = redis_client.get(key)

            ttl = redis_client.ttl(key)

            print("\nKEY:")
            print(key)

            print("\nTTL:")
            print(
                f"{ttl} seconds"
            )

            print("\nVALUE:")
            print(value)

            print("-" * 60)

    except redis.exceptions.RedisError as e:

        print(
            f"⚠️ Redis error: {e}"
        )