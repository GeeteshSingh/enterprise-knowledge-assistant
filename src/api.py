from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from config.settings import settings
from src.rag_pipeline import RAGPipeline
from src.search_engine import SearchEngine
from utils.logger import get_logger


logger = get_logger(__name__)

# Module-level instances shared across all requests
_keyword_engine: SearchEngine | None = None
_rag_pipeline: RAGPipeline | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes search engines at startup and cleans up on shutdown.
    Both engines are built once and reused for all incoming requests.
    """
    global _keyword_engine, _rag_pipeline

    logger.info("API startup: initializing search engines.")

    _keyword_engine = SearchEngine(data_dir=settings.data_path)
    _keyword_engine.load_documents()
    _keyword_engine.build()

    _rag_pipeline = RAGPipeline(data_dir=settings.data_path)
    _rag_pipeline.build()

    logger.info("API startup complete.")
    yield
    logger.info("API shutdown.")


app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    description=(
        "A keyword and semantic search API for enterprise documents. "
        "The /ask endpoint requires GEMINI_API_KEY to be set in .env."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# --- Request and Response Models ---

class KeywordSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query string.")
    mode: str = Field(
        default="or",
        pattern="^(or|and)$",
        description="Search mode: 'or' returns any keyword match, 'and' requires all keywords.",
    )


class SemanticSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query string.")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return.")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Question to answer using RAG.")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of context paragraphs to retrieve.")


class SearchResultItem(BaseModel):
    paragraph: str
    source: str
    score: float | int


class KeywordSearchResponse(BaseModel):
    query: str
    mode: str
    result_count: int
    results: list[SearchResultItem]


class SemanticSearchResponse(BaseModel):
    query: str
    result_count: int
    results: list[SearchResultItem]


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SearchResultItem]


class HealthResponse(BaseModel):
    status: str
    llm_available: bool


class StatsResponse(BaseModel):
    keyword_engine_documents: int
    keyword_engine_paragraphs: int
    keyword_engine_keywords: int
    semantic_index_size: int
    llm_available: bool


# --- Endpoints ---

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    tags=["Monitoring"],
)
def health() -> HealthResponse:
    """
    Returns the current health status of the API.

    Always returns HTTP 200 if the server is running.
    llm_available indicates whether GEMINI_API_KEY is configured.
    """
    return HealthResponse(
        status="ok",
        llm_available=settings.llm_available,
    )


@app.get(
    "/stats",
    response_model=StatsResponse,
    summary="Index statistics",
    tags=["Monitoring"],
)
def stats() -> StatsResponse:
    """
    Returns statistics about the loaded document indexes.
    """
    return StatsResponse(
        keyword_engine_documents=_keyword_engine.document_count,
        keyword_engine_paragraphs=_keyword_engine.paragraph_count,
        keyword_engine_keywords=_keyword_engine.keyword_count,
        semantic_index_size=_rag_pipeline.vector_store_size,
        llm_available=settings.llm_available,
    )


@app.post(
    "/search",
    response_model=KeywordSearchResponse,
    summary="Keyword search",
    tags=["Search"],
)
def keyword_search(request: KeywordSearchRequest) -> KeywordSearchResponse:
    """
    Searches documents using keyword matching.

    - mode='or' returns paragraphs containing ANY query keyword.
    - mode='and' returns paragraphs containing ALL query keywords.

    Results are ranked by relevance score (number of matching keywords).
    """
    results = _keyword_engine.search(request.query, mode=request.mode)

    return KeywordSearchResponse(
        query=request.query,
        mode=request.mode,
        result_count=len(results),
        results=[
            SearchResultItem(
                paragraph=r.paragraph,
                source=r.source,
                score=r.score,
            )
            for r in results
        ],
    )


@app.post(
    "/semantic-search",
    response_model=SemanticSearchResponse,
    summary="Semantic search",
    tags=["Search"],
)
def semantic_search(request: SemanticSearchRequest) -> SemanticSearchResponse:
    """
    Searches documents using semantic similarity (FAISS + sentence-transformers).

    Returns paragraphs that are semantically related to the query, even if
    they do not share exact keywords. Results are scored by cosine similarity.

    No API key required.
    """
    results = _rag_pipeline.semantic_search(request.query, top_k=request.top_k)

    return SemanticSearchResponse(
        query=request.query,
        result_count=len(results),
        results=[SearchResultItem(**r) for r in results],
    )


@app.post(
    "/ask",
    response_model=AskResponse,
    summary="Ask a question (RAG)",
    tags=["RAG"],
)
def ask(request: AskRequest) -> AskResponse:
    """
    Answers a question using Retrieval-Augmented Generation.

    Retrieves the most relevant paragraphs using semantic search, then
    passes them as context to the Gemini LLM to generate a final answer.

    Requires GEMINI_API_KEY to be set in the .env file.
    Returns HTTP 503 if the API key is not configured.
    """
    try:
        result = _rag_pipeline.query(request.question, top_k=request.top_k)
    except ValueError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error))

    return AskResponse(
        question=request.question,
        answer=result["answer"],
        sources=[SearchResultItem(**s) for s in result["sources"]],
    )
