from Pages.SettingsPage import SettingsPage

class TestSettings:
    def __init__(self, page):
        self.page = page
        self.settings_page = SettingsPage(page)

    async def test_open_settings_menu(self):
        await self.settings_page.open_settings()
