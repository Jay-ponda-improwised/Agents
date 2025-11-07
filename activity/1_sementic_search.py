import numpy as np
from constants.config import OLLAMA_HOST, MODEL_QUEN_EMBEDDINGS, ROOT_DIR
from langchain_ollama import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from utility.Console.VirtualMarkdownBoard import VirtualMarkdownBoard

md = VirtualMarkdownBoard()
if not MODEL_QUEN_EMBEDDINGS:
    raise ValueError("MODEL_QUEN_EMBEDDINGS must be set in constants.config")
if not ROOT_DIR:
    raise ValueError("ROOT_DIR must be set in constants.config")


month_facts = [
    # January
    "January is named after the Roman god Janus, the god of beginnings and endings",
    
    # February
    "February is the only month that can pass without a single full moon",
    
    # March
    "The expression 'Mad as a March Hare' comes from the hare's unusual behavior during its breeding season in March",
    
    # April
    "The diamond (April's birthstone) is one of the hardest natural substances on Earth",
    
    # May
    "The month of May is named for the Greek goddess Maia, who was the goddess of fertility",
    
    # June
    "June has the longest daylight hours of the year in the Northern Hemisphere (Summer Solstice)",
    
    # July
    "Before being named after Julius Caesar, July was called Quintilis, which is Latin for 'fifth'",
    
    # August
    "August was originally named Sextilis ('sixth') before being renamed for Augustus Caesar",
    
    # September
    "September comes from the Latin word septem, meaning 'seven', as it was the seventh month in the Roman calendar",
    
    # October
    "The first week of October is officially World Space Week",
    
    # November
    "Daylight Saving Time ends in November, giving everyone an 'extra' hour of sleep",
    
    # December
    "The Winter Solstice, the day with the shortest daylight in the Northern Hemisphere, occurs in December"
]
question = "which month's old name is in latin that represents a number?"

# Initialize Ollama embeddings
embeddings = OllamaEmbeddings(  # type: ignore[reportGeneralTypeIssues]
    model=MODEL_QUEN_EMBEDDINGS,
    base_url=OLLAMA_HOST,
)

# Test the embeddings
fact_embedding = embeddings.embed_documents(month_facts)  # type: ignore[reportGeneralTypeIssues]
question_embedding = embeddings.embed_query(question)  # type: ignore[reportGeneral]
print(len(fact_embedding), len(question_embedding))

# styler.print_markdown_panel(json.dumps(query_result))

md.topic("Semantic Search")

result = cosine_similarity(np.array([question_embedding]), np.array(fact_embedding))

md.list(
    [
        f"{x:.4f} ({month_facts[i]})"
        for rank, (i, x) in enumerate(
            sorted(enumerate(result.tolist()[0]), key=lambda y: y[1], reverse=True)[:3]
        )
    ],  # Format floats as strings
    ordered=True,
)
md.line(style="red")
md.text(f"Biggest semantic match is {result[0][0]:.2f} at index {np.argmax(result):d}.")
md.text(f"- Month is {month_facts[np.argmax(result)]}")
md.take_snapshot()
