"""Keep each pytest run's temporary files separate across Windows accounts."""
from uuid import uuid4


def pytest_configure(config):
    # Honour an explicitly supplied --basetemp. Otherwise choose a new sibling
    # directory each run, so pytest never clears another account's directory.
    if config.option.basetemp is None:
        config.option.basetemp = str(
            config.rootpath / f".pytest_tmp_{uuid4().hex}"
        )
