"""Deterministic pedagogical policy: an explicit state machine over the session.

Takes the structured diagnosis of the LAST student message and the accumulated session state, and
decides WHAT the tutor may do this turn. The LLM that writes the reply never chooses the action or
the hint level. It only phrases the plan, and it only sees the content the plan allows.

Invariants (each has a test):
- Progress: a student who neither completes nor advances a step after a hint gets a higher level
  next time; every step-targeted action uses the same escalation rule.
- No oracle: a bare guess (no reasoning shown) is neither confirmed nor denied.
- Closing is terminal: after `tancar` the session stays closed.
- Non-hint actions (concept questions, redirections) never move the hint ladder.
- A regex never vetoes content the plan allows (completed or shown steps, the target's detail from
  level 3, the student's own words).
- Anti-gaming (help abuse, as in Cognitive Tutors): bare requests for help without any attempt climb
  the ladder at half speed, and the full step is only shown after the student has tried something.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field

from .fitxes import Exercici
from .schemas import Diagnosi
from .teoria import ItemTeoria, parse_ref

Accio = Literal[
    "redirigir",
    "tancar",
    "despres_de_tancar",
    "demanar_raonament",
    "demanar_intent",
    "demanar_justificacio",
    "demanar_conclusio",
    "mostrar_conclusio",
    "questionar_error",
    "questionar_resultat",
    "explicar_concepte",
    "validar_i_avancar",
    "pista",
    "mostrar_pas",
]

NIVELL_MAX_PISTA = 3  # 4 = show the full step
NIVELL_BASE = {"en_cami": 1, "dubte_puntual": 1, "encallat": 2, "perdut": 2}
TORNS_NIVELL3_PER_MOSTRAR = 2  # stuck turns at level 3 after which the step is shown without an explicit request
REPETICIONS_SI_TREBALLA = 2  # an on-track student mid-step gets this many turns at a level before it rises
ENCALLAT = ("demana_pista", "demana_solucio", "frustracio")

# Actions that deliver content of the target step: they move the hint ladder and count for escalation.
ACCIONS_PISTA = {"pista", "mostrar_pas", "questionar_error", "questionar_resultat", "demanar_justificacio", "validar_i_avancar"}
RANG_ESTAT = {"no_iniciat": 0, "erroni": 0, "en_curs": 1, "completat": 2}
TREBALL = ("mostra_treball", "proposa_resultat")  # intents that count as an attempt

# Teacher move of each action (MathDial taxonomy), for logs and the professor panel.
MOVIMENTS = {
    "redirigir": "Generic", "tancar": "Generic", "despres_de_tancar": "Generic", "demanar_raonament": "Probing",
    "demanar_intent": "Probing",
    "demanar_justificacio": "Probing", "mostrar_conclusio": "Telling", "demanar_conclusio": "Focus", "questionar_error": "Probing",
    "questionar_resultat": "Focus", "explicar_concepte": "Telling", "validar_i_avancar": "Focus",
    "pista": "Focus", "mostrar_pas": "Telling",
}

INSTRUCCIONS: dict[str, str] = {
    "redirigir": "L'alumne s'ha desviat del tema. Torna'l amablement a l'exercici amb una pregunta sobre on és.",
    "tancar": "L'alumne ha resolt l'exercici amb justificació. Felicita'l breument, confirma el resultat i destaca la idea clau que ha fet servir.",
    "despres_de_tancar": "L'exercici ja està resolt. Respon breument al que diu l'alumne (pots parlar del resultat i del raonament complet) i suggereix-li passar a un altre exercici.",
    "demanar_raonament": "L'alumne proposa un resultat sense haver mostrat cap raonament. NO diguis si és correcte o incorrecte (ni ho deixis entreveure): pregunta-li com hi ha arribat o com ho justificaria, orientant-lo cap a l'objectiu del pas objectiu.",
    "demanar_intent": "L'alumne demana ajuda sense haver intentat res, i ja té pistes de nivell alt. NO donis més contingut del pas: proposa-li UNA tasca molt petita i concreta que pugui fer ara mateix amb el que ja té (p. ex. escriure la primera expressió o substituir un cas concret) i demana-li que la provi i t'ensenyi el resultat.",
    "demanar_justificacio": "L'alumne ha proposat el resultat correcte i ja ha mostrat part del raonament. Reconeix que el valor és bo i ajuda'l a completar la justificació amb el pas objectiu, al nivell de pista indicat.",
    "demanar_conclusio": "L'alumne ha fet tots els passos però encara no ha formulat la conclusió. Demana-li que la formuli ell.",
    "mostrar_conclusio": "Tots els passos ja estan resolts però l'alumne no arriba a formular la conclusió. Formula-la tu breument a partir dels passos (dona el resultat) i pregunta-li si ho veu clar o vol repassar algun pas.",
    "questionar_error": "L'alumne ha comès l'error indicat. NO li diguis quin és l'error ni la correcció: fes-li una pregunta que el porti a detectar-lo ell mateix. Si el pla inclou contingut del pas objectiu, fes-lo servir per guiar-lo.",
    "questionar_resultat": "L'alumne proposa un resultat incorrecte després d'haver treballat. Digues-li que no és correcte (sense donar el bo) i pregunta-li per revisar el pas objectiu (o la conclusió, si no n'hi ha), al nivell de pista indicat.",
    "explicar_concepte": "L'alumne fa una pregunta conceptual. Explica el concepte en general en 2-3 frases a partir de la TEORIA PERMESA (cita l'ítem dels apunts: p. ex. «Teorema 12 del Tema 3»), SENSE aplicar-lo a aquest exercici, i acaba preguntant com el podria aplicar.",
    "validar_i_avancar": "L'alumne ha avançat correctament. Valida breument el que ha fet bé (concretament) i fes una pregunta que l'orienti cap a l'objectiu del pas següent.",
    "pista": "Dona una pista del nivell indicat per al pas objectiu, en forma de pregunta sempre que sigui possible.",
    "mostrar_pas": "L'alumne ha esgotat les pistes. Mostra NOMÉS el pas objectiu, complet i ben explicat, i acaba demanant-li que t'expliqui amb les seves paraules per què es fa així, o que continuï ell amb el pas següent.",
}

NIVELLS_DESCRIPCIO = {
    0: "Cap contingut del pas: només pots parlar del que l'alumne ja ha escrit.",
    1: "Nivell 1: una pregunta que apunti a l'OBJECTIU del pas, sense anomenar l'estratègia.",
    2: "Nivell 2: pots anomenar l'estratègia (la IDEA), però no fer-ne els càlculs.",
    3: "Nivell 3: pots començar el DETALL, però l'últim càlcul o conclusió del pas l'ha de fer l'alumne.",
    4: "Nivell 4: pots mostrar el DETALL complet del pas objectiu, i res més.",
}


class EstatSessio(BaseModel):
    completats: list[str] = Field(default_factory=list)
    nivell_per_pas: dict[str, int] = Field(default_factory=dict)  # highest level delivered per step
    torns: int = 0
    tancat: bool = False  # sticky: once closed, the session stays closed
    ultim_pas: str | None = None  # target of the last hint action
    ultima_accio: str | None = None
    estats: dict[str, str] = Field(default_factory=dict)  # step states after the last turn (to measure progress)
    mostrats: list[str] = Field(default_factory=list)  # steps the tutor has shown in full
    errors_vistos: dict[str, int] = Field(default_factory=dict)
    repeticions: dict[str, int] = Field(default_factory=dict)  # consecutive hint turns at the same level, per step
    resultat_confirmat: bool = False  # the tutor has already acknowledged the correct result
    intents_alumne: int = 0  # turns in which the student showed work or made progress (anti-gaming)


class Pla(BaseModel):
    accio: Accio
    motiu: str
    pas_objectiu: str | None
    nivell_pista: int
    error_objectiu: str | None = None
    error_text: str | None = None
    pregunta_suggerida: str | None = None
    pot_dir_resultat: bool = False
    resultat_dit_per_alumne: bool = False  # the student stated the correct result: it may be acknowledged
    requereix_pregunta: bool = True
    max_frases: int = 4
    regex_prohibides: list[str] = Field(default_factory=list)
    # Texts whose formulas the reply must not reproduce in any equivalent form (sympy check in the guard):
    # the result until it may be said, and the details of steps the plan does not open.
    textos_prohibits: list[str] = Field(default_factory=list)
    teoria_extra: list[str] = Field(default_factory=list)  # items answering a conceptual question
    to: Literal["normal", "empatic"] = "normal"  # empathetic opener for frustrated or lost students
    moviment: str = "Generic"  # teacher move (MathDial): Focus / Probing / Telling / Generic


def _merge_completats(ex: Exercici, previous: list[str], diag: Diagnosi) -> list[str]:
    now = {e.pas: e.estat for e in diag.estat_passos}
    return [s for s in ex.step_ids if (s in previous and now.get(s) != "erroni") or now.get(s) == "completat"]


def _nivell(current: int, desorientacio: str, escalar: bool) -> int:
    """The single escalation rule shared by every step-targeted action."""
    nivell = current + 1 if (current > 0 and escalar) else current
    return min(NIVELL_MAX_PISTA, max(NIVELL_BASE[desorientacio], nivell, 1))


def _allowed_texts(ex: Exercici, target: str | None, nivell: int, completats: list[str], mostrats: list[str],
                   textos_alumne: list[str], allow_result: bool) -> list[str]:
    texts = [ex.pas(s).detall for s in dict.fromkeys(list(completats) + list(mostrats))]
    if target is not None and nivell >= 3:
        texts.append(ex.pas(target).detall)
    if allow_result:
        texts.append(ex.resultat.valor)
    return texts + list(textos_alumne)


def _forbidden_regexes(
    ex: Exercici,
    target: str | None,
    nivell: int,
    allow_result: bool,
    completats: list[str] = (),
    mostrats: list[str] = (),
    textos_alumne: list[str] = (),
) -> list[str]:
    """Leak regexes for this turn, minus any that would veto content the plan allows."""
    regexes: list[str] = [] if allow_result else list(ex.resultat.fuites)
    if target is not None:
        idx = ex.step_ids.index(target)
        for later in ex.passos[idx + 1 :]:
            regexes += later.fuites
        if nivell < 3:
            regexes += ex.pas(target).fuites
    allowed = _allowed_texts(ex, target, nivell, completats, mostrats, textos_alumne, allow_result)
    return [r for r in dict.fromkeys(regexes) if not any(re.search(r, t, re.IGNORECASE) for t in allowed)]


def _forbidden_texts(ex: Exercici, target: str | None, nivell: int, allow_result: bool,
                     completats: list[str], mostrats: list[str]) -> list[str]:
    """Same gate as the regexes, as texts: their formulas are compared by value, not by spelling."""
    opened = set(completats) | set(mostrats)
    texts = [] if allow_result else [ex.resultat.valor]
    if target is not None:
        idx = ex.step_ids.index(target)
        texts += [p.detall for p in ex.passos[idx + 1:] if p.id not in opened]
        if nivell < 3:
            texts.append(ex.pas(target).detall)
    return texts


def _concept_items(ex: Exercici, diag: Diagnosi, target: str | None, current: int) -> list[str]:
    """Concept answers may not name a later step's theory early (that names the strategy)."""
    if target is None:
        return list(diag.teoria_pregunta)
    idx = ex.step_ids.index(target)
    gated = {parse_ref(r)[0] for p in ex.passos[idx + (1 if current >= 2 else 0):] for r in p.teoria}
    background = {parse_ref(r)[0] for r in ex.teoria}
    return [t for t in diag.teoria_pregunta if t not in gated or t in background]


def decide(
    ex: Exercici, diag: Diagnosi, state: EstatSessio, textos_alumne: list[str] = ()
) -> tuple[Pla, EstatSessio]:
    known_errors = [e for e in diag.errors_detectats if e in ex.error_ids]
    has_error = bool(known_errors) or ("altre" in diag.errors_detectats and diag.error_altre.strip())
    justified = diag.resultat_justificat and not has_error

    completats = _merge_completats(ex, state.completats, diag)
    new_steps = [s for s in completats if s not in state.completats]
    resolts = list(dict.fromkeys(completats + state.mostrats))  # a shown step no longer blocks the next one
    target = next((s for s in ex.step_ids if s not in resolts), None)
    estats_ara = {e.pas: e.estat for e in diag.estat_passos} | {s: "completat" for s in completats}
    current = state.nivell_per_pas.get(target, 0) if target else 0

    stuck = diag.intencio in ENCALLAT or diag.nivell_desorientacio in ("encallat", "perdut")
    progress = bool(target) and RANG_ESTAT.get(estats_ara.get(target, "no_iniciat"), 0) > RANG_ESTAT.get(
        state.estats.get(target, "no_iniciat"), 0
    )
    after_hint_here = state.ultim_pas == target and state.ultima_accio in ACCIONS_PISTA
    working = diag.nivell_desorientacio == "en_cami" and estats_ara.get(target) == "en_curs"
    # A student visibly working through a long step gets some room before the level rises.
    no_progress = (after_hint_here and not new_steps and not progress
                   and (not working or state.repeticions.get(target, 0) >= REPETICIONS_SI_TREBALLA))
    attempt = diag.intencio in TREBALL or bool(new_steps) or progress
    # Help abuse: without an attempt this turn, the level only climbs after repeating it once at the same level.
    earned = attempt or state.repeticions.get(target, 0) >= 2 or current == 0
    stuck = stuck and earned
    no_progress = no_progress and earned
    nivell = _nivell(current, diag.nivell_desorientacio, stuck or no_progress) if target else 0
    has_reasoning = bool(completats) or any(estats_ara.get(s) in ("en_curs", "completat") for s in ex.step_ids)
    # A result only drives the turn when this message is about it: a request for help, a question or
    # frustration is answered as such even if the diagnosis also reports a result.
    proposa = diag.resultat_proposat != "cap" and diag.intencio in ("proposa_resultat", "mostra_treball")
    already_said = state.resultat_confirmat

    pla: Pla
    if state.tancat:
        pla = Pla(accio="despres_de_tancar", motiu="L'exercici ja està tancat.", pas_objectiu=None, nivell_pista=0,
                  pot_dir_resultat=True, requereix_pregunta=False)

    elif diag.intencio == "fora_de_tema":
        pla = Pla(accio="redirigir", motiu="Missatge fora de tema.", pas_objectiu=target, nivell_pista=0)

    elif diag.resultat_proposat == "correcte" and not has_error and (justified or target is None):
        pla = Pla(accio="tancar", motiu="Resultat correcte i justificat.", pas_objectiu=None, nivell_pista=0,
                  pot_dir_resultat=True, requereix_pregunta=False)

    elif diag.intencio == "pregunta_conceptual" and target is not None:
        # A question is answered first; an error in the same message comes back when the student shows work.
        extra = _concept_items(ex, diag, target, current)
        pla = Pla(accio="explicar_concepte",
                  motiu="Pregunta conceptual." + (f" Teoria: {', '.join(extra)}." if extra else ""),
                  pas_objectiu=target, nivell_pista=current, teoria_extra=extra)

    elif has_error:
        err_id = known_errors[0] if known_errors else "altre"
        repeated = state.errors_vistos.get(err_id, 0) > 0
        err = ex.error(err_id) if known_errors else None
        lvl = _nivell(current, diag.nivell_desorientacio, True) if (target and repeated) else (current if target else 0)
        pla = Pla(
            accio="questionar_error",
            motiu=f"Error detectat: {err_id}" + (" (repetit: es puja el nivell)." if repeated else "."),
            pas_objectiu=target,
            nivell_pista=lvl,
            error_objectiu=err_id,
            error_text=err.descripcio if err else diag.error_altre,
            # A repeated error gets new content (the step at a higher level), not the same question again.
            pregunta_suggerida=err.pregunta if (err and not repeated) else None,
        )

    elif proposa and not has_reasoning and state.ultima_accio != "demanar_raonament":
        # Asked once; a second bare guess gets a hint on the step instead (handled by the branches below).
        pla = Pla(accio="demanar_raonament", motiu="Proposa un resultat sense raonament: no es confirma ni es desmenteix.",
                  pas_objectiu=target, nivell_pista=max(current, 1) if target else 0)

    elif proposa and has_reasoning and diag.resultat_proposat == "incorrecte":
        pla = Pla(accio="questionar_resultat", motiu="Resultat incorrecte després d'haver treballat.",
                  pas_objectiu=target, nivell_pista=nivell)

    elif proposa and has_reasoning and diag.resultat_proposat == "correcte":
        pla = Pla(accio="demanar_justificacio", motiu="Resultat correcte amb raonament parcial.",
                  pas_objectiu=target, nivell_pista=nivell, resultat_dit_per_alumne=True)

    elif target is None:
        if diag.intencio == "pregunta_conceptual":
            pla = Pla(accio="explicar_concepte", motiu="Pregunta conceptual amb tots els passos fets.", pas_objectiu=None,
                      nivell_pista=0, teoria_extra=list(diag.teoria_pregunta))
        elif stuck or state.ultima_accio == "demanar_conclusio":
            # Asked once already (or stuck): the conclusion follows from resolved steps, so the tutor states it.
            pla = Pla(accio="mostrar_conclusio", motiu="Tots els passos resolts; l'alumne no arriba a la conclusió.",
                      pas_objectiu=None, nivell_pista=0, pot_dir_resultat=True)
        else:
            pla = Pla(accio="demanar_conclusio", motiu="Tots els passos fets; falta la conclusió.", pas_objectiu=None,
                      nivell_pista=0)

    elif diag.intencio == "pregunta_conceptual":
        extra = _concept_items(ex, diag, target, current)
        pla = Pla(accio="explicar_concepte",
                  motiu="Pregunta conceptual." + (f" Teoria: {', '.join(extra)}." if extra else ""),
                  pas_objectiu=target, nivell_pista=current, teoria_extra=extra)

    elif (current >= NIVELL_MAX_PISTA and not attempt and state.intents_alumne == 0
          and state.repeticions.get(target, 0) >= 1 and state.ultima_accio != "demanar_intent"):
        # Help abuse at the top of the ladder: instead of repeating the same hint, ask for a tiny concrete attempt.
        pla = Pla(accio="demanar_intent", motiu="Demana ajuda al nivell màxim sense cap intent: es demana un intent concret.",
                  pas_objectiu=target, nivell_pista=current)

    elif current >= NIVELL_MAX_PISTA and (state.intents_alumne > 0 or attempt) and (
        diag.intencio == "demana_solucio" or (stuck and state.repeticions.get(target, 0) >= TORNS_NIVELL3_PER_MOSTRAR)
    ):
        pla = Pla(accio="mostrar_pas", motiu=f"Pistes esgotades al pas (nivell {current}).", pas_objectiu=target,
                  nivell_pista=4, max_frases=6)

    elif new_steps and diag.nivell_desorientacio in ("en_cami", "dubte_puntual") and diag.intencio not in ENCALLAT:
        pla = Pla(accio="validar_i_avancar", motiu=f"Ha completat: {', '.join(new_steps)}.", pas_objectiu=target,
                  nivell_pista=max(current, 1))

    else:
        motiu = f"Desorientació '{diag.nivell_desorientacio}', intenció '{diag.intencio}', nivell previ {current}"
        motiu += ", sense progrés des de l'última pista." if no_progress else "."
        pla = Pla(accio="pista", motiu=motiu, pas_objectiu=target, nivell_pista=nivell)

    if diag.intencio == "frustracio" or diag.nivell_desorientacio == "perdut":
        pla.to = "empatic"
    pla.moviment = "Telling" if (pla.accio == "pista" and pla.nivell_pista >= 3) else MOVIMENTS[pla.accio]

    # ---- state transition ----
    tancat = state.tancat or pla.accio in ("tancar", "mostrar_conclusio")
    if pla.accio in ("tancar", "mostrar_conclusio"):
        completats = list(ex.step_ids)
    mostrats = list(state.mostrats) + ([target] if pla.accio == "mostrar_pas" and target not in state.mostrats else [])
    confirmat = already_said or pla.accio in ("tancar", "demanar_justificacio")

    allow_result = pla.pot_dir_resultat or confirmat
    pla.regex_prohibides = _forbidden_regexes(
        ex, pla.pas_objectiu, pla.nivell_pista, allow_result, completats, mostrats, textos_alumne
    )
    pla.textos_prohibits = _forbidden_texts(ex, pla.pas_objectiu, pla.nivell_pista, allow_result, completats, mostrats)

    nivell_per_pas = dict(state.nivell_per_pas)
    repeticions = dict(state.repeticions)
    hint = pla.accio in ACCIONS_PISTA and pla.pas_objectiu is not None
    if hint:
        previ = nivell_per_pas.get(pla.pas_objectiu, 0)
        same = state.ultim_pas == pla.pas_objectiu and pla.nivell_pista == previ
        repeticions[pla.pas_objectiu] = repeticions.get(pla.pas_objectiu, 0) + 1 if same else 1
        nivell_per_pas[pla.pas_objectiu] = max(previ, pla.nivell_pista)
    errors_vistos = dict(state.errors_vistos)
    if pla.error_objectiu:
        errors_vistos[pla.error_objectiu] = errors_vistos.get(pla.error_objectiu, 0) + 1

    new_state = EstatSessio(
        completats=completats,
        nivell_per_pas=nivell_per_pas,
        torns=state.torns + 1,
        tancat=tancat,
        ultim_pas=pla.pas_objectiu if hint else state.ultim_pas,
        ultima_accio=pla.accio,
        estats=estats_ara,
        mostrats=mostrats,
        errors_vistos=errors_vistos,
        repeticions=repeticions,
        resultat_confirmat=confirmat,
        intents_alumne=state.intents_alumne + (1 if attempt else 0),
    )
    return pla, new_state


def allowed_content(ex: Exercici, pla: Pla, completats: list[str], mostrats: list[str] = ()) -> str:
    """The ONLY solution content the reply stage gets to see."""
    parts: list[str] = []
    done = [ex.pas(s) for s in dict.fromkeys(list(completats) + list(mostrats))]
    if done:
        parts.append("Passos que l'alumne JA té resolts (pots referir-t'hi):")
        parts += [f"  - {p.titol}: {p.detall}" for p in done]
    if pla.pas_objectiu:
        p = ex.pas(pla.pas_objectiu)
        parts.append(f"PAS OBJECTIU: {p.titol}")
        if pla.nivell_pista >= 1:
            parts.append(f"  objectiu: {p.objectiu}")
        if pla.nivell_pista >= 2:
            parts.append(f"  idea: {p.idea}")
        if pla.nivell_pista >= 3:
            parts.append(f"  detall: {p.detall}")
    if pla.error_text:
        parts.append(f"ERROR DE L'ALUMNE (no l'anomenis directament): {pla.error_text}")
    if pla.pregunta_suggerida:
        parts.append(f"Pregunta socràtica suggerida (pots adaptar-la): {pla.pregunta_suggerida}")
    if pla.pot_dir_resultat:
        parts.append(f"RESULTAT: {ex.resultat.valor}")
    return "\n".join(parts) if parts else "(cap contingut de la solució)"


def allowed_theory(
    ex: Exercici, pla: Pla, completats: list[str], teoria: dict[str, ItemTeoria]
) -> list[ItemTeoria]:
    """Theory items the reply stage may see and cite this turn.

    Naming a theorem names the strategy, so a step's theory follows the same gate as its idea
    (hint level >= 2). Items that solve this very exercise are never included.
    """
    refs = list(ex.teoria)
    if pla.accio in ("tancar", "despres_de_tancar"):
        refs += [r for p in ex.passos for r in p.teoria]
    else:
        refs += [r for s in completats for r in ex.pas(s).teoria]
        if pla.pas_objectiu and pla.nivell_pista >= 2:
            refs += ex.pas(pla.pas_objectiu).teoria
    refs += pla.teoria_extra
    reserved = ex.reserved_ids(teoria)
    ids = [i for i in dict.fromkeys(parse_ref(r)[0] for r in refs) if i in teoria and i not in reserved]
    return [teoria[i] for i in ids]
