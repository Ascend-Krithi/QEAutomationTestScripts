class ProfilePage:
    def __init__(self, page):
        self.page = page
        self.user_profile_icon = page.locator('#profile-icon')

    async def click_profile(self):
        await self.user_profile_icon.click()