
SYSTEM_PROMPT = """
You are a master of embedding, and you are working on a project to embed a video into a vector space.
You are given a video, and you need to extract the most important information from it and convert it into a vector.
You can use any tool you want to do this, but you need to make sure that the vector is as accurate as possible.
You can also use any programming language you want to do this, but you need to make sure that the code is well-written and easy to understand.
"""

USER_PROMPT = """
Please embed the following video for me:
{video_path}
"""

VIDEO_PROMPT = """
I have a video with the following frames:
{frames}

Please extract the most important information from these frames and convert it into a vector.
"""

EMBEDDING_PROMPT = """
I have the following information about a video:
{video_info}

Please convert this information into a vector.
"""

SEARCH_PROMPT = """
I have a vector that represents a video.
I want to find other videos that are similar to this one.
Please help me find similar videos.
"""

SIMILARITY_PROMPT = """
I have two vectors that represent two videos.
I want to know how similar these two videos are.
Please help me calculate the similarity between these two vectors.
"""

CLUSTER_PROMPT = """
I have a set of vectors that represent a set of videos.
I want to group these videos into clusters based on their similarity.
Please help me cluster these videos.
"""

CLASSIFY_PROMPT = """
I have a vector that represents a video.
I want to classify this video into one of the following categories:
{categories}

Please help me classify this video.
"""

RECOMMEND_PROMPT = """
I have a user who has watched the following videos:
{watched_videos}

Please recommend some other videos that this user might like.
"""
