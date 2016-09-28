from utils.page_objects import PageObject, PageElement


class DashboardPage(PageObject):
    """ To check Node status and System info on Virtualization panel."""
    add_btn = PageElement(id_="dashboard-add")
    enable_btn = PageElement(id_="dashboard-enable-edit")
    cpu_link = PageElement(link_text="CPU")
    memory_link = PageElement(link_text="Memory")
    network_link = PageElement(link_text="Network")
    disk_link = PageElement(link_text="Disk I/O")


    def __init__(self, *args, **kwargs):
        super(DashboardPage, self).__init__(*args, **kwargs)
        self.get("/dashboard")
        self.wait(period=5)

    def basic_check_elements_exists(self):
        assert self.cpu_link, "Cpu button not exist"
        assert self.memory_link, "Memory button not exist"
        assert self.network_link, "Network button not exist"
        assert self.disk_link, "Disk button not exist"
        assert self.add_btn, "Add button not exist"
        assert self.enable_btn, "Edit button not exist"
        self.wait()
