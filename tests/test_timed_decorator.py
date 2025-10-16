import asyncio
import logging
import pytest

from src.core.decorators import timed
from src.core.logging_config import configure_logging

configure_logging(level=logging.INFO)

def test_timed_sync_logs_and_returns(caplog):
    @timed("sync_test")
    def add(a, b):
        return a + b

    with caplog.at_level(logging.INFO):
        result = add(2, 3)

    assert result == 5
    # ensure at least one record mentions the label
    assert any("sync_test" in rec.message for rec in caplog.records)

@pytest.mark.asyncio
async def test_timed_async_logs_and_returns(caplog):
    @timed("async_test")
    async def delay():
        await asyncio.sleep(0.01)
        return "done"

    with caplog.at_level(logging.INFO):
        result = await delay()

    assert result == "done"
    assert any("async_test" in rec.message for rec in caplog.records)

def test_timed_raises_and_logs_error(caplog):
    @timed("error_test")
    def fail():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        with caplog.at_level(logging.ERROR):
            fail()

    assert any("error_test" in rec.message for rec in caplog.records)
    assert any("ERROR" in rec.levelname for rec in caplog.records)