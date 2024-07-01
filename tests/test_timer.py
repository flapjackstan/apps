"""Test for all the apps."""

from argparse import Namespace

from timer import start_timers


def test_timers(mocker, capsys):
    """Timers test with mocks."""
    mock_play_sound = mocker.patch("timer.play_sound")
    mock_parse_args = mocker.patch(
        "timer.parse_args", return_value=Namespace(total="1:30", sub=["0:30", "1:00", "1:15"])
    )
    args = mock_parse_args(["--total", "1:30", "--sub", "0:30", "1:00", "1:15"])

    start_timers(args)

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert "Time Started at" in output_lines[0]
    assert "Subtimer 0 minute(s) and 30 second(s) elapsed" in output_lines[1]
    assert "Subtimer 1 minute(s) and 0 second(s) elapsed" in output_lines[2]
    assert "Subtimer 1 minute(s) and 15 second(s) elapsed" in output_lines[3]
    assert "Total time 1 minute(s) and 30 second(s) elapsed" in output_lines[4]

    assert mock_play_sound.call_count == 4
