# embeddings
# PhL 28jul26
########################################################################

# Std lib
from typing import Sequence

# 3rd party lib
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import (
    Normalize,
    Pooling,
    Transformer,
)
from transformers import AutoModelForCausalLM, AutoTokenizer

# Project lib
from explorer.config import (
    MODEL_NAME,
    MODEL_TYPE,
    PREDICTIVE_STATE_SUFFIX,
    REPRESENTATION_MODE,
)

_model = None  # Cached SentenceTransformer instance


class PredictiveStateModel:
    """Expose causal-LM predictive states through the LlmExpl model interface."""

    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.tokenizer.padding_side = "right"

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype="auto",
        )
        self.model.eval()

        self.hidden_state_index = self.model.config.num_hidden_layers // 2
        self.last_raw_predictive_states = None
        self.reference_predictive_state = None
        self.reference_last_token_id = None

    def get_embedding_dimension(self):
        """Return the dimension of one predictive state."""

        return self.model.config.hidden_size

    def _extract_last_states(self, sentences):
        """Extract the selected hidden state and final token id for each input."""

        inputs = self.tokenizer(
            sentences,
            padding=True,
            return_tensors="pt",
        ).to(self.model.device)

        with torch.inference_mode():
            outputs = self.model(
                **inputs,
                output_hidden_states=True,
                use_cache=False,
                return_dict=True,
            )

        selected_hidden_states = outputs.hidden_states[self.hidden_state_index]
        last_token_indices = inputs["attention_mask"].sum(dim=1) - 1
        batch_indices = torch.arange(
            selected_hidden_states.shape[0],
            device=selected_hidden_states.device,
        )
        last_token_ids = inputs["input_ids"][batch_indices, last_token_indices]

        predictive_states = selected_hidden_states[
            batch_indices,
            last_token_indices,
        ]

        return predictive_states, last_token_ids

    def encode(self, sentences, convert_to_numpy=True):
        """Return each concept's variation from a suffix-only reference state."""

        prepared_sentences = [
            f"{sentence}{PREDICTIVE_STATE_SUFFIX}" for sentence in sentences
        ]
        predictive_states, last_token_ids = self._extract_last_states(
            prepared_sentences
        )

        if self.reference_predictive_state is None:
            reference_states, reference_token_ids = self._extract_last_states(
                [PREDICTIVE_STATE_SUFFIX]
            )
            self.reference_predictive_state = reference_states[0].detach()
            self.reference_last_token_id = reference_token_ids[0].detach()

        if (
            torch.unique(last_token_ids).numel() != 1
            or last_token_ids[0] != self.reference_last_token_id
        ):
            raise RuntimeError(
                "The PMG common suffix did not produce one shared final token."
            )

        self.last_raw_predictive_states = predictive_states.detach()
        predictive_state_deltas = (
            predictive_states - self.reference_predictive_state
        )

        if convert_to_numpy:
            return predictive_state_deltas.float().cpu().numpy()

        return predictive_state_deltas


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

        if MODEL_TYPE == "generative":
            if REPRESENTATION_MODE != "common_suffix_middle_delta":
                raise ValueError(
                    "Unsupported generative representation mode: "
                    f"{REPRESENTATION_MODE}"
                )

            _model = PredictiveStateModel(MODEL_NAME)
        elif MODEL_NAME == "openai-community/gpt2":
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
