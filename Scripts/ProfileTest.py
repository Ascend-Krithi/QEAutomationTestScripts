from Pages.ProfilePage import ProfilePage

class TestProfile:
    def __init__(self, page):
        self.page = page
        self.profile_page = ProfilePage(page)

    async def test_click_profile_icon(self):
        await self.profile_page.click_profile()
