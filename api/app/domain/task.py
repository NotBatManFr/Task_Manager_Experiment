"""Core domain entity definitions for tasks."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Domain representation of a task independent of transport/persistence layers."""

    id: str
    title: str
    status: str
    due_date: Optional[datetime] = None
