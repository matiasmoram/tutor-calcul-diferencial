from typing import Literal

# How a document is reviewed: the whole text at once ("sencer") or one part at a time ("per_parts"). Part of the
# HTTP contract (`format`) and of the stored documents.
Layout = Literal["sencer", "per_parts"]
LAYOUTS: tuple[Layout, ...] = ("sencer", "per_parts")
