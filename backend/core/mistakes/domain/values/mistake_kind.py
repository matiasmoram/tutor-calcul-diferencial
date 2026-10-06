from typing import Literal

# The two activities: a worked solution of an exercise ("problema") or a result of the notes ("teoria").
SourceKind = Literal["problema", "teoria"]

# Catalan enum values of the generation schema (prompt contract) and of the stored documents.
PROBLEM_MISTAKE_KINDS: tuple[str, ...] = (
    "calcul",
    "logica",
    "hipotesi",
    "teorema_mal_aplicat",
    "conclusio",
    "desigualtat",
)
THEORY_MISTAKE_KINDS: tuple[str, ...] = (
    "hipotesi",  # a hypothesis dropped, weakened or changed
    "conclusio",  # a conclusion stronger than / different from what holds
    "quantificador",  # ∀/∃ swapped, order of quantifiers, "some" for "every"
    "implicacio",  # converse stated, "iff" where only one direction holds
    "desigualtat",
    "pas_injustificat",  # a proof step that does not follow
    "cas_oblidat",
    "calcul",
    "definicio",  # a definition used wrongly
)
# Items of the notes that make a theory document: a result with its proof.
THEORY_RESULT_KINDS: tuple[str, ...] = ("teorema", "proposicio", "lema", "corollari")
