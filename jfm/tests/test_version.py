def test_version_exposed() -> None:
    import jfm

    assert isinstance(jfm.__version__, str)
    assert jfm.__version__
