class SettingsPage:
    def __init__(self, page):
        self.page = page
        self.settings_menu = page.locator('#settings-menu')

    async def open_settings(self):
        await self.settings_menu.click()