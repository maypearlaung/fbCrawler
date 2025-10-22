from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _ensure_selenium_stubs() -> None:
    if "selenium" in sys.modules:
        return

    selenium_module = ModuleType("selenium")

    webdriver_module = ModuleType("selenium.webdriver")
    chrome_module = ModuleType("selenium.webdriver.chrome")
    chrome_options_module = ModuleType("selenium.webdriver.chrome.options")

    class Options:
        def __init__(self) -> None:
            self.arguments: list[str] = []

        def add_argument(self, argument: str) -> None:
            self.arguments.append(argument)

    chrome_options_module.Options = Options
    webdriver_module.Chrome = MagicMock(name="Chrome")

    common_module = ModuleType("selenium.webdriver.common")
    by_module = ModuleType("selenium.webdriver.common.by")
    by_module.By = SimpleNamespace(LINK_TEXT="link text", XPATH="xpath")
    keys_module = ModuleType("selenium.webdriver.common.keys")
    keys_module.Keys = SimpleNamespace(COMMAND="CMD", CONTROL="CTRL", RETURN="ENTER")

    remote_module = ModuleType("selenium.webdriver.remote")
    remote_webdriver_module = ModuleType("selenium.webdriver.remote.webdriver")
    remote_webelement_module = ModuleType("selenium.webdriver.remote.webelement")
    remote_webdriver_module.WebDriver = type("WebDriver", (), {})
    remote_webelement_module.WebElement = type("WebElement", (), {})

    selenium_module.webdriver = webdriver_module
    webdriver_module.chrome = chrome_module
    chrome_module.options = chrome_options_module
    selenium_module.webdriver.common = common_module
    common_module.by = by_module
    common_module.keys = keys_module
    selenium_module.webdriver.remote = remote_module
    remote_module.webdriver = remote_webdriver_module
    remote_module.webelement = remote_webelement_module

    sys.modules["selenium"] = selenium_module
    sys.modules["selenium.webdriver"] = webdriver_module
    sys.modules["selenium.webdriver.chrome"] = chrome_module
    sys.modules["selenium.webdriver.chrome.options"] = chrome_options_module
    sys.modules["selenium.webdriver.common"] = common_module
    sys.modules["selenium.webdriver.common.by"] = by_module
    sys.modules["selenium.webdriver.common.keys"] = keys_module
    sys.modules["selenium.webdriver.remote"] = remote_module
    sys.modules["selenium.webdriver.remote.webdriver"] = remote_webdriver_module
    sys.modules["selenium.webdriver.remote.webelement"] = remote_webelement_module


_ensure_selenium_stubs()
