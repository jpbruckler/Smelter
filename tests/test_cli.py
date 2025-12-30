from typer.testing import CliRunner
import smelter.cli as cli

runner = CliRunner()

def test_root_command_writes_stdout(monkeypatch, tmp_path):
    fake_pdf = tmp_path / "fake.pdf"
    fake_pdf.write_text("not a real pdf", encoding="utf-8")

    def fake_extract_text(path, pages=None):
        assert path == fake_pdf
        return {1: "hello\n"}

    monkeypatch.setattr(cli, "extract_text", fake_extract_text)

    result = runner.invoke(cli.app, ["convert", str(fake_pdf)])
    assert result.exit_code == 0
    assert result.stdout == "hello\n"

def test_no_args_prints_help():
    result = runner.invoke(cli.app, [])
    assert result.exit_code == 0
    assert "Smelter CLI" in result.stdout
