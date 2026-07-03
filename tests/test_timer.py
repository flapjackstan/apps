"""Tests for the timer app."""

from apps.timer import run_timers


def test_run_timers(mocker, capsys):
    """Timer test with mocked sound playback."""
    mock_play_sound = mocker.patch("apps.timer.play_sound")

    run_timers(total="0:03", sub=["0:01", "0:02"])

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert "Time Started at" in output_lines[0]
    assert "Subtimer 0 minute(s) and 1 second(s) elapsed" in output_lines[1]
    assert "Subtimer 0 minute(s) and 2 second(s) elapsed" in output_lines[2]
    assert "Total time 0 minute(s) and 3 second(s) elapsed" in output_lines[3]

    assert mock_play_sound.call_count == 3
