# embeddings
# PhL 28jul26
########################################################################

# Std lib
from typing import Sequence

# 3rd party lib
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import (
    Normalize,
    Pooling,
    Transformer,
)

# Project lib
from explorer.config import MODEL_NAME

_model = None  # Cached SentenceTransformer instance


def configure_gpt2_padding(tokenizer, model_config):
    """Give GPT-2 a padding token for batched embedding requests."""

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        model_config.pad_token_id = tokenizer.pad_token_id


def load_gpt2_mean_pooling_model():
    """Build a fixed-size GPT-2 embedding model with mean pooling."""

    transformer = Transformer(MODEL_NAME)
    configure_gpt2_padding(transformer.tokenizer, transformer.model.config)

    pooling = Pooling(
        transformer.get_embedding_dimension(),
        pooling_mode="mean",
    )

    return SentenceTransformer(modules=[transformer, pooling, Normalize()])


def center_and_normalize_embeddings(embeddings):
    """Remove the scenario-wide common component from GPT-2 embeddings.

    This is an experimental visualisation post-processing step. It does not
    change GPT-2 itself and must only be used for the labelled GPT-2 test.
    """

    centered = embeddings - embeddings.mean(axis=0, keepdims=True)
    norms = np.linalg.norm(centered, axis=1, keepdims=True)

    return np.divide(centered, norms, out=np.zeros_like(centered), where=norms != 0)


def load_model():
    """Load the embedding model only once."""

    global _model

    if _model is None:
        print(f"Loading model: {MODEL_NAME}")

        if MODEL_NAME == "openai-community/gpt2":
            _model = load_gpt2_mean_pooling_model()
        else:
            _model = SentenceTransformer(MODEL_NAME)

    return _model


def compute_embeddings(concepts: str | Sequence[str]) -> np.ndarray:
    """
    Compute embeddings for one or more concepts or sentences.

    Parameters
    ----------
    concepts : str | Sequence[str]
        Input text(s).

    Returns
    -------
    numpy.ndarray
        One embedding vector per input text.
    """

    if isinstance(concepts, str):
        concepts = [concepts]

    model = load_model()

    embeddings = model.encode(
        concepts,
        convert_to_numpy=True,
    )

    if MODEL_NAME == "openai-community/gpt2":
        return center_and_normalize_embeddings(embeddings)

    return embeddings


def get_model():
    """Return the cached embedding model."""
    return load_model()
