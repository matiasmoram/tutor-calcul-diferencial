import re

# Characters text must not carry to the database: NUL cannot be stored in a Postgres text or JSONB column, and a lone
# surrogate cannot be encoded as UTF-8 at all, so either one fails only at the write, after the model calls were paid
# for. The other C0 controls come from neither a keyboard nor a well-formed answer. Tab, newline and carriage return
# do (pasted text, a table, a CRLF line end) and are kept.
UNSTORABLE = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff]")
