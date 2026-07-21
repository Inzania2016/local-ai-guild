"""Tests for the harmless R0 command-line interface."""

from pytest import CaptureFixture

from local_ai_guild.cli import IMPLEMENTATION_STAGE, PROJECT_NAME, main


def test_status_prints_identity_and_stage(capsys: CaptureFixture[str]) -> None:
    """The status command reports only stable project metadata."""
    exit_code = main(["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == f"Project: {PROJECT_NAME}\nStage: {IMPLEMENTATION_STAGE}\n"
    assert captured.err == ""
