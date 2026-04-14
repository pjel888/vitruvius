"""Stream Y1.2 — injects a source-identity prefix into a chat-completion message list.

This is the Vitruvius analogue of Gemma 4's Per-Layer Embeddings: instead
of conditioning every transformer layer with a learned vector, we
condition every LLM *call* with a deterministic prose reminder of the
document's identity. The model is explicitly told "you are reading
jurisdiction X's document type Y" on every invocation, so the Chain of
Thought cannot drift halfway through a long review session.
"""
from __future__ import annotations

import copy
from enum import Enum
from typing import Any, Sequence

from .context_vector import SourceIdentity


class PriorityLevel(str, Enum):
    NORMAL = "normal"
    HIGH = "high"


def inject_prefix(
    messages: Sequence[dict[str, Any]],
    *,
    identity: SourceIdentity,
    priority: PriorityLevel = PriorityLevel.NORMAL,
) -> list[dict[str, Any]]:
    """Return a copy of ``messages`` with an identity-priming prefix
    prepended to the system message.

    Never mutates the input. If no system message exists, a new one is
    inserted at position 0. The existing system message content (if
    any) is preserved, prepended with the identity block.

    When ``priority=PriorityLevel.HIGH``, an additional line reading
    ``CRITICAL: DO NOT DRIFT from this document's jurisdiction and
    type. Every verdict must be justifiable under this source's legal
    framework.`` is appended to the identity block.
    """
    new_messages = copy.deepcopy(list(messages))
    prefix_lines = [
        f"SOURCE_IDENTITY[{identity.fingerprint}]: {identity.prose}",
    ]
    if priority == PriorityLevel.HIGH:
        prefix_lines.append(
            "CRITICAL: DO NOT DRIFT from this document's jurisdiction and type. "
            "Every verdict must be justifiable under this source's legal framework."
        )
    prefix = "\n".join(prefix_lines) + "\n\n"

    if new_messages and new_messages[0].get("role") == "system":
        new_messages[0]["content"] = prefix + new_messages[0]["content"]
    else:
        new_messages.insert(0, {"role": "system", "content": prefix.rstrip()})

    return new_messages
