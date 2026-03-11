class AddForm:
    def __init__(self, page):
        self.page = page
        self.add_form_button = page.get_by_role("button", name="Add Data")

    def click_add_form(self):
        self.add_form_button.click()

    def add_data(self):
        Entity_dropdown = self.page.get_by_placeholder("Select Entity")
        # Entity_dropdown.wait_for(state='visible', timeout=30000)
        Entity_dropdown.click()
        Entity = self.page.locator("//*[@id='cdk-overlay-2']/ul/li[1]")
        Entity.click() 
        print(Entity.inner_text())
    def select_entity(self):
        self.click_add_form()
        self.add_data()