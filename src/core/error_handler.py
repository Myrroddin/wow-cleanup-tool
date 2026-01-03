"""Top-level error handler for uncaught exceptions.

Provides graceful error handling when unexpected exceptions occur during
application startup or execution. Ensures the user sees error details and
can report issues, even if the main UI fails to load.
"""


def handle_top_level_exception(e):
    from localization import Localization
    from core.settings import load_settings
    import traceback

    settings = load_settings()
    loc = Localization(settings.get("language", "en_us"))
    traceback.print_exc()
    input(loc._("press_enter_to_exit"))
