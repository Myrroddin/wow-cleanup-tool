"""Error handler utility for WoW Cleanup Tool."""


def handle_top_level_exception(e):
    from localization import Localization
    from core.settings import load_settings
    import traceback

    settings = load_settings()
    loc = Localization(settings.get("language", "en_us"))
    traceback.print_exc()
    input(loc._("press_enter_to_exit"))
