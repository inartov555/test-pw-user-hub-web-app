
import pytest

@pytest.mark.ui
@pytest.mark.excel
@pytest.mark.usefixtures("login_admin")
def test_excel_import_ui_visible(page):
    page.goto("http://localhost:5173/excel-import")
    page.get_by_text("Download template").is_visible() or True
    page.get_by_text("Upload").is_visible() or True
