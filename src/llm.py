from utils.logger import get_logger


logger = get_logger(__name__)

GENERATION_CONFIG = {
    "temperature": 0.2,
    "top_p": 0.9,
    "max_output_tokens": 1024,
}

SYSTEM_PROMPT = (
    "You are an enterprise knowledge assistant. "
    "Answer the user's question using only the information provided in the context below. "
    "If the context does not contain enough information to answer the question, "
    "say so clearly. Do not make up information. "
    "At the end of your answer, mention which source documents you used."
)


class LLMClient:
    """
    Client for generating answers using the Gemini LLM.

    Reads the API key from the GEMINI_API_KEY environment variable via the
    application settings. Does not accept or store the API key directly in code.

    The LLM is used only for the RAG pipeline's answer generation step.
    All retrieval (keyword and semantic search) works without an API key.
    """

    def __init__(self, api_key: str) -> None:
        """
        Args:
            api_key: Gemini API key read from the GEMINI_API_KEY environment variable.

        Raises:
            ValueError: If api_key is empty or not set.
        """
        if not api_key or not api_key.strip():
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Add it to your .env file to enable LLM features.\n"
                "See .env.example for the required format."
            )

        import google.generativeai as genai

        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=GENERATION_CONFIG,
            system_instruction=SYSTEM_PROMPT,
        )
        logger.info("LLM client initialized with model: gemini-2.0-flash")

    def generate_answer(
        self,
        question: str,
        context_paragraphs: list[dict],
    ) -> str:
        """
        Generates an answer to the question using retrieved context paragraphs.

        The context is formatted as a numbered list of paragraphs with their
        source filenames so the model can cite sources in its answer.

        Args:
            question:          The user's raw question string.
            context_paragraphs: List of result dicts from semantic or keyword search.
                               Each dict must have "paragraph" and "source" keys.

        Returns:
            Generated answer string from the LLM.

        Raises:
            RuntimeError: If the LLM call fails.
        """
        if not context_paragraphs:
            return "No relevant context was found to answer this question."

        context_block = "\n\n".join(
            f"[Source: {item['source']}]\n{item['paragraph']}"
            for item in context_paragraphs
        )

        prompt = (
            f"Context:\n{context_block}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )

        logger.debug("Sending prompt to LLM (%d context paragraphs).", len(context_paragraphs))

        try:
            response = self._model.generate_content(prompt)
            answer = response.text.strip()
            logger.info("LLM generated answer successfully.")
            return answer
        except Exception as error:
            logger.error("LLM generation failed: %s", error)
            raise RuntimeError(f"LLM generation failed: {error}") from error
