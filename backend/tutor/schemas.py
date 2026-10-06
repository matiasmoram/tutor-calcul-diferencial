"""Structured-output contracts for each LLM stage.

JSON schemas are built per exercise so step and error ids are closed enums:
the model cannot invent a step that doesn't exist in the sheet.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .fitxes import Exercici

EstatPas = Literal["no_iniciat", "en_curs", "completat", "erroni"]
Desorientacio = Literal["en_cami", "dubte_puntual", "encallat", "perdut"]
Intencio = Literal[
    "mostra_treball",
    "demana_pista",
    "demana_solucio",
    "pregunta_conceptual",
    "proposa_resultat",
    "fora_de_tema",
    "frustracio",
]
ResultatProposat = Literal["cap", "correcte", "incorrecte"]

DESORIENTACIO_ORDRE: list[str] = ["en_cami", "dubte_puntual", "encallat", "perdut"]

Infraccio = Literal[
    "revela_resultat",
    "revela_pas_futur",
    "excedeix_nivell_pista",
    "fa_la_feina_de_l_alumne",
    "afirmacio_matematica_falsa",
    "no_segueix_l_accio",
    "no_es_en_catala",
    "cita_teoria_incorrecta",
    "no_respon_a_l_alumne",
    "obeeix_l_alumne",
]


class EstatDePas(BaseModel):
    pas: str
    estat: EstatPas


class Diagnosi(BaseModel):
    evidencia: str
    resum_alumne: str
    estat_passos: list[EstatDePas]
    pas_actual: str
    errors_detectats: list[str]
    error_altre: str
    resultat_proposat: ResultatProposat
    resultat_justificat: bool
    nivell_desorientacio: Desorientacio
    intencio: Intencio
    teoria_pregunta: list[str] = []


class Resposta(BaseModel):
    missatge: str
    referencies: list[str] = []


class VeredicteGuardia(BaseModel):
    veredicte: Literal["ok", "rebutjat"]
    infraccions: list[Infraccio]
    explicacio: str


def _enum(values: list[str], description: str) -> dict:
    return {"type": "string", "enum": values, "description": description}


def _literal_values(lit) -> list[str]:
    return list(lit.__args__)


def diagnosi_schema(ex: Exercici, teoria_ids: list[str] | None = None) -> dict:
    """`teoria_ids`: theory items the diagnosis may point to when the student asks a conceptual question."""
    return {
        "type": "object",
        "additionalProperties": False,
        "required": list(Diagnosi.model_fields),
        "properties": {
            "evidencia": {
                "type": "string",
                "description": "Cita literal i breu del que ha escrit l'alumne que justifica la diagnosi. Buit si no ha escrit res rellevant.",
            },
            "resum_alumne": {
                "type": "string",
                "description": "Una frase: què ha fet l'alumne fins ara i on és.",
            },
            "estat_passos": {
                "type": "array",
                "description": "Un element per cada pas de la fitxa, en el mateix ordre.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["pas", "estat"],
                    "properties": {
                        "pas": _enum(ex.step_ids, "Id del pas."),
                        "estat": _enum(_literal_values(EstatPas), "Estat del pas segons el treball ESCRIT per l'alumne."),
                    },
                },
            },
            "pas_actual": _enum(
                ex.step_ids + ["cap"],
                "Primer pas que l'alumne encara no ha completat correctament ('cap' si els ha completat tots).",
            ),
            "errors_detectats": {
                "type": "array",
                "description": "Errors comuns de la fitxa presents a l'ÚLTIM missatge de l'alumne. 'altre' si n'hi ha un que no és a la llista.",
                "items": _enum(ex.error_ids + ["altre"], "Id de l'error."),
            },
            "error_altre": {
                "type": "string",
                "description": "Descripció breu de l'error si errors_detectats conté 'altre'; buit altrament.",
            },
            "resultat_proposat": _enum(
                _literal_values(ResultatProposat),
                "Si l'alumne ha afirmat un resultat final, si coincideix amb el de la fitxa.",
            ),
            "resultat_justificat": {
                "type": "boolean",
                "description": "Cert només si l'alumne ha donat una justificació rigorosa i completa del resultat.",
            },
            "nivell_desorientacio": _enum(
                DESORIENTACIO_ORDRE,
                "en_cami: avança bé. dubte_puntual: sap el camí però dubta en un detall. "
                "encallat: sap on és però no sap com continuar. perdut: no sap per on començar o falla un concepte base.",
            ),
            "intencio": _enum(_literal_values(Intencio), "Què vol l'alumne amb l'últim missatge."),
            "teoria_pregunta": _id_list(
                teoria_ids or [],
                "Si l'intenció és pregunta_conceptual: els ítems dels apunts (màxim 2) que responen la pregunta. Buit altrament.",
            ),
        },
    }


def _id_list(ids: list[str], description: str) -> dict:
    """Array of ids from a closed set. Length limits are enforced in code: not every provider supports maxItems."""
    if not ids:
        return {"type": "array", "description": "Sempre buit: no hi ha cap ítem disponible.", "items": {"type": "string"}}
    return {"type": "array", "description": description, "items": _enum(ids, "Id de l'ítem dels apunts.")}


def guardia_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["veredicte", "infraccions", "explicacio"],
        "properties": {
            "veredicte": _enum(["ok", "rebutjat"], "rebutjat si hi ha alguna infracció."),
            "infraccions": {
                "type": "array",
                "items": _enum(_literal_values(Infraccio), "Tipus d'infracció."),
            },
            "explicacio": {"type": "string", "description": "Una frase justificant el veredicte."},
        },
    }


def normalize_diagnosi(d: Diagnosi, ex: Exercici, teoria_ids: list[str] | None = None) -> Diagnosi:
    """Make the step list complete and ordered, whatever the model returned."""
    by_id = {e.pas: e.estat for e in d.estat_passos if e.pas in ex.step_ids}
    d.estat_passos = [EstatDePas(pas=s, estat=by_id.get(s, "no_iniciat")) for s in ex.step_ids]
    d.errors_detectats = list(dict.fromkeys(d.errors_detectats))
    # An uncatalogued error needs a description to be questioned. (Step states describe the whole
    # conversation and errors only the last message, so a step marked wrong is NOT turned into an error.)
    if "altre" in d.errors_detectats and not d.error_altre.strip():
        d.errors_detectats = [e for e in d.errors_detectats if e != "altre"]
    allowed = set(teoria_ids or [])
    d.teoria_pregunta = [t for t in dict.fromkeys(d.teoria_pregunta) if t in allowed][:2]
    return d
