"use strict";

/* Reads the functions of an exercise statement (LaTeX) so the visual tools can open with them:
   f(x,y)=…, limits at a point, maps F=(F1,F2), constraints and regions {(x,y) | …}.
   latexToExpr() turns LaTeX into math.js syntax; anything it cannot read is skipped, never guessed.
   Pure functions, no DOM: also loaded by node for tests (module.exports at the end). */

const LX_FUNCS = new Set(["sin", "cos", "tan", "exp", "log", "sqrt", "abs", "asin", "acos", "atan",
  "sinh", "cosh", "tanh", "nthRoot", "sec", "csc", "cot", "max", "min"]);
const LX_MACROS = {
  sin: "sin", cos: "cos", tan: "tan", tg: "tan", exp: "exp", log: "log", ln: "log", arcsin: "asin", arccos: "acos",
  arctan: "atan", arctg: "atan", sinh: "sinh", cosh: "cosh", tanh: "tanh", sec: "sec", csc: "csc", cot: "cot",
  pi: "pi", cdot: "*", times: "*", max: "max", min: "min",
};
const LX_VARS = new Set(["x", "y", "z", "e"]);

function lxGroup(s, i) {
  // s[i] === "{": returns [content, index after the closing brace].
  let depth = 0;
  for (let k = i; k < s.length; k++) {
    if (s[k] === "{") depth++;
    else if (s[k] === "}" && --depth === 0) return [s.slice(i + 1, k), k + 1];
  }
  throw new Error("claus desaparellades");
}

function lxArg(s, i) {
  // A macro argument: {group} or a single character/command.
  while (s[i] === " ") i++;
  if (s[i] === "{") return lxGroup(s, i);
  if (s[i] === "\\") { const m = /^\\[a-zA-Z]+/.exec(s.slice(i)); return [m[0], i + m[0].length]; }
  return [s[i], i + 1];
}

function lxStructure(s) {
  // LaTeX structure -> parenthesized text with function names, recursively.
  let out = "";
  for (let i = 0; i < s.length;) {
    const c = s[i];
    if (c === "\\") {
      const m = /^\\([a-zA-Z]+)/.exec(s.slice(i));
      if (!m) { i += 2; out += " "; continue; }  // \, \; \! \{ …
      const name = m[1];
      i += m[0].length;
      if (["frac", "dfrac", "tfrac"].includes(name)) {
        const [a, j] = lxArg(s, i); const [b, k] = lxArg(s, j);
        out += `((${lxStructure(a)})/(${lxStructure(b)}))`; i = k;
      } else if (name === "sqrt") {
        let n = null;
        if (s[i] === "[") { const e = s.indexOf("]", i); n = s.slice(i + 1, e); i = e + 1; }
        const [a, j] = lxArg(s, i);
        out += n ? ` nthRoot(${lxStructure(a)},${lxStructure(n)})` : ` sqrt(${lxStructure(a)})`; i = j;
      } else if (["mathrm", "operatorname", "text", "mathit"].includes(name)) {
        const [a, j] = lxArg(s, i);
        const w = a.trim();
        out += name === "text" ? " " : ` ${LX_MACROS[w] || w} `; i = j;
      } else if (name in LX_MACROS) out += ` ${LX_MACROS[name]} `;
      else if (["left", "right", "displaystyle", "big", "Big", "bigg", "Bigg", "quad", "qquad", "limits"].includes(name)) out += " ";
      else throw new Error(`no sé llegir \\${name}`);
    } else if (c === "^" || c === "_") {
      const [a, j] = lxArg(s, i + 1);
      if (c === "^") out += `^(${lxStructure(a)})`;
      // Subscripts are names (x_1); the tools only use x, y, z, so a subscript makes it unreadable.
      else throw new Error("subíndexs no suportats");
      i = j;
    } else if (c === "{") { const [a, j] = lxGroup(s, i); out += `(${lxStructure(a)})`; i = j; }
    else { out += c; i++; }
  }
  return out;
}

function lxTokens(s) {
  const toks = [];
  const re = /\s*(?:(\d+(?:\.\d+)?|\.\d+)|([a-zA-Z]+)|(\*\*|[-+*/^(),|]))/y;
  let m;
  re.lastIndex = 0;
  while (re.lastIndex < s.length) {
    const at = re.lastIndex;
    m = re.exec(s);
    if (!m) { if (/^\s*$/.test(s.slice(at))) break; throw new Error(`caràcter inesperat «${s.slice(at).trim()[0]}»`); }
    if (m[1]) toks.push({ t: "num", v: m[1] });
    else if (m[2]) {
      const w = m[2];
      if (LX_FUNCS.has(w)) toks.push({ t: "fn", v: w });
      else if (w === "pi") toks.push({ t: "id", v: "pi" });
      else for (const ch of w) {  // implicit products of single-letter variables: xy -> x y
        if (!LX_VARS.has(ch)) throw new Error(`variable «${ch}»`);
        toks.push({ t: "id", v: ch });
      }
    } else toks.push({ t: "op", v: m[3] });
  }
  return toks;
}

function lxEmit(toks) {
  // Rebuild with explicit products, parenthesized function arguments and |…| as abs(…).
  const out = [];
  let absDepth = 0;
  const isValueEnd = (t) => t && (t.t === "num" || t.t === "id" || (t.t === "op" && t.v === ")"));
  const startsValue = (t) => t && (t.t === "num" || t.t === "id" || t.t === "fn" || (t.t === "op" && t.v === "("));
  // Operand of a function without parentheses: one atom, with an optional power (\sin x^2 -> sin(x^2)).
  const atomEnd = (i) => {
    if (toks[i]?.t === "op" && toks[i].v === "(") {
      let d = 0;
      for (let k = i; k < toks.length; k++) {
        if (toks[k].v === "(") d++;
        else if (toks[k].v === ")" && --d === 0) return k + 1;
      }
      return toks.length;
    }
    if (toks[i]?.t === "fn") return atomEnd(i + 1);
    let k = i + 1;
    // Implicit product in the argument, as written in the notes: \sin xy, \log 2x.
    while (toks[k] && (toks[k].t === "id" || toks[k].t === "num") && (toks[k - 1].t === "id" || toks[k - 1].t === "num")) k++;
    return k;
  };
  const withPower = (k) => (toks[k]?.v === "^" ? atomEnd(k + 1) : k);
  const fnArgs = new Map();  // token index of a function -> index where its operand ends
  for (let i = 0; i < toks.length; i++) {
    if (toks[i].t !== "fn") continue;
    let j = i + 1;
    if (toks[j]?.v === "^") { j = atomEnd(j + 1); fnArgs.set(i, { pow: [i + 2, j] }); }
    if (toks[j]?.v === "(") continue;
    fnArgs.set(i, { ...(fnArgs.get(i) || {}), argFrom: j, argTo: withPower(atomEnd(j)) });
  }
  const closeAt = new Map();
  let prev = null;
  for (let i = 0; i < toks.length; i++) {
    const t = toks[i];
    if (isValueEnd(prev) && startsValue(t)) out.push("*");
    if (t.v === "|") {
      const opening = !isValueEnd(prev) || absDepth === 0;
      if (opening) { if (isValueEnd(prev)) out.push("*"); out.push("abs("); absDepth++; prev = { t: "op", v: "(" }; }
      else { out.push(")"); absDepth--; prev = { t: "op", v: ")" }; }
      continue;
    }
    if (t.t === "fn") {
      const a = fnArgs.get(i);
      if (a?.pow) {
        // \sin^2 x -> (sin(x))^(2)
        const pow = toks.slice(a.pow[0], a.pow[1]);
        out.push(`(${t.v}(`);
        if (a.argFrom != null) {
          closeAt.set(a.argTo, (closeAt.get(a.argTo) || "") + `))^(${lxEmit(pow)})`);
          i = a.argFrom - 1;
        } else throw new Error("potència de funció amb parèntesis");
        prev = { t: "op", v: "(" };
        continue;
      }
      out.push(t.v);
      if (a) { out.push("("); closeAt.set(a.argTo, (closeAt.get(a.argTo) || "") + ")"); prev = { t: "op", v: "(" }; }
      else prev = t;
      continue;
    }
    out.push(t.v === "**" ? "^" : t.v);
    prev = t;
    if (closeAt.has(i + 1)) { out.push(closeAt.get(i + 1)); closeAt.delete(i + 1); prev = { t: "op", v: ")" }; }
  }
  for (const v of closeAt.values()) out.push(v);
  if (absDepth) throw new Error("valor absolut sense tancar");
  return out.join("");
}

function latexToExpr(src) {
  let s = src.replace(/\\(?:displaystyle|left|right|big|Big|bigg|Bigg)(?![a-zA-Z])/g, "")
    .replace(/\\[,;:!]|\\q?quad(?![a-zA-Z])/g, " ")
    .replace(/[.,;]\s*$/, "").trim();
  if (/\\(?:int|sum|prod|lim|infty|in|mid|begin|to|neq|le|ge|leq|geq|leqslant|geqslant)(?![a-zA-Z])/.test(s)) throw new Error("no és una fórmula");
  const expr = lxEmit(lxTokens(lxStructure(s)));
  // A comma that does not separate the arguments of a function (max(a,b), nthRoot(a,n)) makes a vector
  // or a list, not one formula.
  const call = [];
  for (let i = 0; i < expr.length; i++) {
    if (expr[i] === "(") call.push(/[a-zA-Z]$/.test(expr.slice(0, i)));
    else if (expr[i] === ")") call.pop();
    else if (expr[i] === "," && !call[call.length - 1]) throw new Error("és un vector, no una fórmula");
  }
  return expr;
}

/* ---------- statements ---------- */

function lxMathSegments(text) {
  const segs = [];
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+)\$/g;
  let m;
  while ((m = re.exec(text))) segs.push((m[1] ?? m[2]).trim());
  return segs;
}

function lxSplitTop(s, sep) {
  // Split at `sep` characters that are not inside (), {}, [].
  const parts = [];
  let depth = 0, last = 0;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if ("({[".includes(c)) depth++;
    else if (")}]".includes(c)) depth--;
    else if (depth === 0 && sep.includes(c)) { parts.push(s.slice(last, i)); last = i + 1; }
  }
  parts.push(s.slice(last));
  return parts;
}

function lxCases(rhs) {
  // \begin{cases} A & \text{si …} \\ B & … \end{cases}: the non-constant branch, and the point where the other one applies.
  const m = /\\begin\{cases\}([\s\S]*?)\\end\{cases\}/.exec(rhs);
  if (!m) return null;
  const rows = m[1].split(/\\\\/).map((r) => r.split("&")).filter((r) => r[0].trim());
  let best = null, point = null, value = null;
  for (const [expr, cond = ""] of rows) {
    const p = /\(x,\s*y\)\s*=\s*\(([^)]*)\)/.exec(cond);
    if (p && !/[xy]/.test(expr)) {
      point = p[1].split(",").map((v) => Number(v));
      try { value = Number(latexToExpr(expr)); } catch { value = null; }
    } else if (/[xy]/.test(expr) && (!best || expr.length > best.length)) best = expr;
  }
  return best ? { expr: best, point, value } : null;
}

const LX_REL = [["\\leqslant", "<="], ["\\geqslant", ">="], ["\\leq", "<="], ["\\geq", ">="], ["\\le", "<="], ["\\ge", ">="], ["<", "<"], [">", ">"], ["=", "="]];

function lxRelation(s) {
  // "x^2+y^2\leq 1" -> "x^2 + y^2 <= 1" in tool syntax, or null.
  for (const [lt, op] of LX_REL) {
    const parts = s.split(lt);
    if (parts.length !== 2 || (lt === "=" && /[<>]/.test(s))) continue;
    try {
      const a = latexToExpr(parts[0]), b = latexToExpr(parts[1]);
      if (!/[xy]/.test(a + b)) return null;
      return `${a} ${op} ${b}`;
    } catch { return null; }
  }
  return null;
}

function extractVisual(text) {
  // { f, a, fa, limit, constraints[], map: [F1, F2], vars3 } read from the statement; fields absent when not found.
  const out = { constraints: [] };
  for (const raw of lxMathSegments(text)) {
    const seg = raw.replace(/\\(?:displaystyle|quad|qquad)(?![a-zA-Z])/g, " ").trim();
    const lim = /\\lim_\{?\s*\(x,\s*y\)\s*\\to\s*\(([^)]*)\)\s*\}?([\s\S]*)/.exec(seg);
    if (lim) {
      try {
        out.f ??= latexToExpr(lim[2]);
        out.a ??= lim[1].split(",").map((v) => Number(latexToExpr(v)));
        out.limit = true;
      } catch { /* unreadable limit */ }
      continue;
    }
    const def = /^([A-Za-z])(?:_?\{?([12])\}?)?\s*\(\s*x\s*,\s*y\s*(,\s*z\s*)?\)\s*=\s*([\s\S]+)$/.exec(seg);
    if (def) {
      if (def[3]) { out.vars3 = true; continue; }
      // "…,\quad\text{si }(x,y)\neq(1,0) \text{ i } f(1,0)=0": the formula, then where it is defined apart.
      let rhs = def[4];
      const tail = /,?\s*(?:\\q?quad\s*)?\\text\{\s*si[\s\S]*$/.exec(rhs);
      if (tail && !/\\begin\{cases\}/.test(rhs)) {
        const pv = /([A-Za-z])\s*\(([^)]*)\)\s*=\s*(-?[\d.]+)/.exec(tail[0]);
        if (pv) { out.a ??= pv[2].split(",").map(Number); out.fa ??= Number(pv[3]); }
        rhs = rhs.slice(0, tail.index);
      }
      const cs = lxCases(rhs);
      if (cs) { rhs = cs.expr; if (cs.point && !cs.point.some(Number.isNaN)) { out.a ??= cs.point; out.fa ??= cs.value; } }
      const vec = /^\s*(?:\\left)?\(([\s\S]*)(?:\\right)?\)\s*[.,;]?\s*$/.exec(rhs);
      const comps = vec ? lxSplitTop(vec[1].replace(/\\right$/, ""), ",") : null;
      try {
        if (comps && comps.length === 2) out.map ??= comps.map(latexToExpr);
        else if (def[2]) { out.map ??= [null, null]; out.map[Number(def[2]) - 1] = latexToExpr(rhs); }
        else out.f ??= latexToExpr(rhs);
      } catch { /* not readable: skip */ }
      continue;
    }
    // Region {(x,y) ∈ R² | conditions}.
    const reg = /\\\{\s*\(x,\s*y\)\s*(?:\\in[^|:]*?)?(?:\\mid|\||:)([\s\S]*)\\\}/.exec(seg);
    if (reg) {
      for (const cond of lxSplitTop(reg[1].replace(/\\text\{\s*i\s*\}/g, ","), ",")) {
        // Chains like 0 \le x \le 1 become two relations.
        const chain = cond.split(/(\\leqslant|\\geqslant|\\leq|\\geq|\\le|\\ge|<|>)/);
        if (chain.length === 5) {
          for (const r of [chain.slice(0, 3).join(""), chain.slice(2).join("")]) { const x = lxRelation(r); if (x) out.constraints.push(x); }
        } else { const x = lxRelation(cond); if (x) out.constraints.push(x); }
      }
      continue;
    }
    // A bare equation in x, y next to a function: a constraint (e.g. "$f(x,y)=x$, $x^2+2y^2=3$").
    if (out.f && /[xy]/.test(seg) && /=|\\le|\\ge|</.test(seg) && !/[A-Za-z]\s*\(/.test(seg.replace(/\\[a-z]+/g, ""))) {
      const x = lxRelation(seg);
      if (x) out.constraints.push(x);
    }
  }
  if (out.map && out.map.some((c) => c == null)) delete out.map;
  return out;
}

if (typeof module !== "undefined") module.exports = { latexToExpr, extractVisual };
