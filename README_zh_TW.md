# Stagehand E2E 自動化測試框架

[English](README.md) | [繁體中文](README_zh_TW.md)

一個使用 [Stagehand](https://github.com/browserbase/stagehand-python) 和 pytest 構建的端到端測試框架，支援使用自然語言指令進行自動化瀏覽器測試。

## 概述

此框架結合 AI 驅動的自然語言指令與傳統程式碼測試，實現可靠的瀏覽器自動化。專為測試 TransGlobal 網站（https://www.transglobalus.com/）而配置，支援多種裝置類型、並行執行和自動重試機制。

> ⚠️ **重要瀏覽器限制**：Stagehand **僅**支援 Chromium/Chrome 瀏覽器。**不支援 Firefox 和 Safari**，無法與此框架配合使用。

## 功能特色

- **自然語言測試**：使用純英文指令撰寫測試
- **多裝置支援**：在手機、iPad 和桌面視窗大小上進行測試
- **並行執行**：使用 pytest-xdist 並行執行測試
- **自動重試**：失敗的測試會自動重試，可配置重試次數
- **靈活標籤**：使用自訂標記（標籤）組織測試
- **生產就緒**：專為可靠的 CI/CD 整合而設計

## 目錄

- [前置需求](#前置需求)
- [安裝](#安裝)
- [配置](#配置)
- [執行測試](#執行測試)
- [最佳實踐](#最佳實踐)
- [程式碼標準](#程式碼標準)
- [故障排除](#故障排除)

## 前置需求

開始之前，請確保已安裝以下項目：

- **Python 3.8+**（建議使用 Python 3.10+）
- **pip** 或 **uv**（套件管理器）
- **OpenAI API 金鑰**（Stagehand 所需）
- **Git**（用於克隆儲存庫）

### 系統需求

- macOS、Linux 或 Windows
- 至少 2GB 可用磁碟空間
- 用於 API 呼叫和瀏覽器下載的網路連線

## 安裝

### 步驟 1：克隆儲存庫

```bash
git clone <repository-url>
cd StageHand-E2E-Automation
```

### 步驟 2：建立虛擬環境

使用 `venv`（建議）：

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

或使用 `uv`（更快的替代方案）：

```bash
uv venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 步驟 3：安裝依賴套件

```bash
pip install -r requirements.txt
```

或使用 `uv`：

```bash
uv pip install -r requirements.txt
```

### 步驟 4：安裝 Playwright 瀏覽器

> ⚠️ **重要**：Stagehand **僅**支援 Chromium/Chrome 瀏覽器。**不支援 Firefox 和 Safari**。請勿嘗試安裝或使用其他瀏覽器。

安裝 Chromium 瀏覽器以進行本地執行：

```bash
python -m playwright install chromium
```

這將下載並安裝 Stagehand 進行瀏覽器自動化所需的 Chromium 瀏覽器。

### 步驟 5：配置環境變數

1. 複製範例環境檔案：

```bash
cp .env.example .env
```

2. 編輯 `.env` 並新增您的 OpenAI API 金鑰：

```env
OPENAI_API_KEY=your_actual_openai_api_key_here
```

**重要**：永遠不要將 `.env` 檔案提交到版本控制。它已包含在 `.gitignore` 中。

### 步驟 6：驗證安裝

執行簡單測試以驗證所有設定是否正確：

```bash
pytest tests/pages/homepage/test_homepage.py::test_homepage_loads -v
```

如果測試成功執行，您就可以開始使用了！🎉

## 配置

### 裝置類型

框架支援三種裝置配置：

- **mobile**：430x932（iPhone 15 Pro Max 大小）
- **ipad**：1024x1366（iPad Pro 12.9" 大小）
- **desktop**：1920x1080（預設）

### 瀏覽器支援

> ⚠️ **瀏覽器相容性警告**
> 
> **Stagehand 僅支援基於 Chromium 的瀏覽器：**
> - ✅ Chrome
> - ✅ Chromium
> - ✅ Microsoft Edge（基於 Chromium）
> 
> **不支援：**
> - ❌ Firefox
> - ❌ Safari
> - ❌ 任何其他非 Chromium 瀏覽器
> 
> 框架使用 Playwright 的 Chromium 瀏覽器執行所有測試。嘗試使用不支援的瀏覽器會導致錯誤。

### Pytest 配置

`pytest.ini` 檔案包含所有測試配置：

- **測試發現**：自動在 `tests/` 目錄中尋找測試
- **標記**：用於組織測試的自訂標籤（在 `pytest.ini` 中配置）
- **重試設定**：預設 2 次重試，延遲 1 秒
- **日誌記錄**：配置為詳細測試輸出

## 執行測試

### 基本測試執行

執行所有測試：

```bash
pytest
```

執行特定測試檔案：

```bash
pytest tests/pages/homepage/test_homepage.py
```

執行特定測試函數：

```bash
pytest tests/pages/homepage/test_homepage.py::test_homepage_loads
```

### 使用裝置選項

在手機裝置上執行測試：

```bash
pytest --device=mobile
```

在 iPad 上執行測試：

```bash
pytest --device=ipad
```

在桌面裝置上執行測試（預設）：

```bash
pytest --device=desktop
```

### 使用標籤（標記）

僅執行 smoke 測試：

```bash
pytest -m smoke
```

執行關鍵測試：

```bash
pytest -m critical
```

執行首頁測試：

```bash
pytest -m homepage
```

組合多個標籤（OR 邏輯）：

```bash
pytest -m "smoke or critical"
```

組合多個標籤（AND 邏輯）：

```bash
pytest -m "smoke and homepage"
```

排除特定標籤：

```bash
pytest -m "not regression"
```

### 無頭模式

在無頭模式下執行測試（無瀏覽器視窗）：

```bash
pytest --headless
```

### 並行執行

並行執行測試（更快的執行速度）：

```bash
pytest -n auto  # 自動偵測 CPU 核心數
pytest -n 4     # 使用 4 個工作程序
```

### 組合選項

在手機裝置上以無頭模式並行執行 smoke 測試：

```bash
pytest -m smoke --device=mobile --headless -n auto
```

### 模型選擇

使用不同的 Stagehand 模型：

```bash
pytest --stagehand-model=gpt-4o
```

### 詳細輸出

取得詳細的測試輸出：

```bash
pytest -v  # 詳細模式
pytest -vv  # 更詳細
pytest -s   # 顯示 print 語句
```

### 重試配置

預設重試配置在 `pytest.ini` 中設定（2 次重試，延遲 1 秒）。您可以覆蓋它：

```bash
pytest --reruns=3 --reruns-delay=2
```

## 最佳實踐

### 1. 使用描述性測試名稱

```python
# 好的
async def test_homepage_services_section_displays_correctly(stagehand_on_demand):
    pass

# 不好的
async def test1(stagehand_on_demand):
    pass
```

### 2. 新增適當的標記

始終適當地標記您的測試：

```python
@pytest.mark.homepage
@pytest.mark.smoke
async def test_homepage_loads(stagehand_on_demand):
    pass
```

### 3. 使用具體的自然語言指令

```python
# 好的 - 具體
await page.act("click the 'Get Started' button in the hero section")

# 不好的 - 模糊
await page.act("click button")
```

### 4. 優雅地處理錯誤

```python
try:
    await page.act("click the submit button")
except Exception as e:
    # 適當地記錄或處理錯誤
    print(f"Action failed: {e}")
    raise
```

### 5. 盡可能快取操作

使用 `observe` 預覽操作並快取它們：

```python
# 預覽操作
action = await page.observe("click the navigation menu")

# 執行而不需要額外的 LLM 呼叫
await page.act(action[0])
```

### 6. 使用結構化資料提取

對於複雜資料，使用 Pydantic 架構：

```python
from pydantic import BaseModel

class ServiceInfo(BaseModel):
    title: str
    description: str
    link: str

services = await page.extract("all services", schema=ServiceInfo)
```

### 7. 保持測試獨立

每個測試都應該能夠獨立執行：

```python
# 好的 - 每個測試都導航到頁面
async def test_a(stagehand_on_demand):
    await stagehand_on_demand.page.goto("https://www.transglobalus.com/")
    # 測試程式碼

async def test_b(stagehand_on_demand):
    await stagehand_on_demand.page.goto("https://www.transglobalus.com/")
    # 測試程式碼
```

### 8. 使用 BaseActions 進行常見操作

始終使用 `BaseActions` 進行標準 Playwright 操作，以保持一致性和可重用性：

```python
from tests.pages.base.base_action import BaseActions

base_actions = BaseActions(page)
await base_actions.open_url("https://www.transglobalus.com/")
await base_actions.wait_for_page_loaded()
is_visible = await base_actions.verify_element_visible('selector')
```

### 9. 驗證頁面內容，而不只是 URL

始終驗證頁面內容是否已實際載入，而不只是檢查 URL 是否改變：

```python
# 好的 - 驗證內容已載入
await base_actions.wait_for_page_loaded()
current_url = page.url
assert "contact" in current_url.lower()
body_text = await base_actions.get_element_text("body")
assert len(body_text.strip()) > 0, "Page appears to be blank"

# 不好的 - 只檢查 URL
current_url = page.url
assert "contact" in current_url.lower()
```

## 程式碼標準

此專案遵循 Python 最佳實踐和程式碼原則。詳細的程式碼規則，請參閱 [`.cursor/rules/stagehand_coding_rules.mdc`](.cursor/rules/stagehand_coding_rules.mdc)。

### PEP 8 風格指南

- **命名規範**：
  - 模組：`snake_case`（例如：`test_header.py`）
  - 類別：`PascalCase`（例如：`BaseActions`、`Device`）
  - 函數/方法：`snake_case`（例如：`navigate_homepage`）
  - 常數：`UPPER_SNAKE_CASE`（例如：`DEFAULT_TIMEOUT`）
  - 私有方法：使用 `_` 前綴（例如：`_resolve_locator`）

- **程式碼格式**：
  - 每行最多 100 個字元（軟限制）
  - 使用 4 個空格進行縮排（絕不使用 tab）
  - 頂層定義之間 2 個空行
  - 方法之間 1 個空行
  - 匯入分組：標準函式庫、第三方、本地

- **匯入組織**：
```python
# 標準函式庫
import asyncio
from typing import Union

# 第三方
import pytest
from playwright.async_api import Page
from stagehand import Stagehand

# 本地
from tests.pages.base.base_action import BaseActions
from config.devices import get_device_class
```

### SOLID 原則

- **單一職責**：每個類別/函數應該只有一個變更理由
- **開放封閉**：對擴展開放，對修改封閉
- **里氏替換**：子類型必須可以替換其基類型
- **介面隔離**：保持介面專注且最小
- **依賴反轉**：依賴抽象，而非具體實現

### DRY 原則

- 將常見功能提取到可重用的函數/類別中
- 使用 `BaseActions` 進行常見的 Playwright 操作
- 為重複模式建立輔助函數
- 使用 fixtures 進行共享測試設定

### Pytest-BDD 結構

#### Feature 檔案
- 位置：`features/{page_name}/{feature_name}.feature`
- 使用 Gherkin 語法（Given-When-Then）
- 適當地標記場景（例如：`@homepage`、`@header_visibility`）

#### 測試檔案
- 位置：`tests/pages/{page_name}/test_{feature_name}.py`
- 在頂部使用 `scenarios()` 函數載入 feature 檔案
- 將每個場景的所有步驟寫在一起
- **不要**在步驟定義函數前加上 `given_`、`when_`、`then_` 前綴

#### 範例結構：
```python
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from stagehand import Stagehand
from tests.pages.base.base_action import BaseActions

scenarios('../../../features/homepage/header.feature')

@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()

@when("I look at the header")
async def look_at_header_visibility(stagehand_on_demand: Stagehand):
    await stagehand_on_demand.page.wait_for_timeout(500)

@then("the TransGlobal logo should be visible")
async def logo_visible_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    is_visible = await base_actions.verify_element_visible('a[href*="transglobalus.com"]')
    assert is_visible
```

### Stagehand 使用指南

- **使用 BaseActions** 進行標準 Playwright 操作（點擊、等待、驗證）
- **使用 `page.act()`** 進行需要 AI 解釋的自然語言操作
- **使用 `page.observe()`** 僅在必要時使用（在執行前預覽操作）
- **使用 `page.extract()`** 僅在需要結構化資料提取時使用
- 在自然語言指令中要具體

### 測試組織

- **檔案結構**：按頁面/功能組織測試（例如：`tests/pages/homepage/test_header.py`）
- **命名**：測試檔案使用 `test_{feature_name}.py`，feature 檔案使用 `{feature_name}.feature`
- **標籤**：使用場景特定標籤（例如：`@header_visibility`、`@header_click_contact`）和頁面級別標籤（例如：`@homepage`）
- **獨立性**：每個測試都應該能夠獨立執行

### 程式碼品質標準

- **函數**：保持函數小而專注（最多 50 行，偏好更短）
- **變數**：使用描述性名稱，避免縮寫
- **型別提示**：為函數參數和返回值使用型別提示
- **註解**：註解「為什麼」，而不是「什麼」
- **常數**：在模組級別定義常數，避免魔術數字

### 常見模式

#### 導航模式
```python
@given("I navigate to the TransGlobal homepage")
async def navigate_homepage(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()
```

#### 點擊和導航模式
```python
@when("I click the menu item")
async def click_menu_item(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    await page.act(f'click the "{menu_item}" in the header')
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(2000)  # 等待內容載入

@then("I should be navigated to the page")
async def verify_navigation(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.wait_for_page_loaded()
    current_url = page.url
    assert "expected-path" in current_url.lower()
    # 驗證頁面內容已載入
    body_text = await base_actions.get_element_text("body")
    assert len(body_text.strip()) > 0, "Page appears to be blank"
```

### 應避免的反模式

❌ **不要這樣做**：
```python
# 魔術數字
await page.wait_for_timeout(2000)

# 通用名稱
def test1(stagehand):
    pass

# 程式碼重複
await page.locator('selector').wait_for(state="visible")
# 在多個地方重複

# 沒有頁面內容驗證
current_url = page.url
assert "contact" in current_url.lower()

# 使用 given/when/then 前綴
async def given_navigate_homepage(...):
    pass
```

✅ **應該這樣做**：
```python
# 命名常數或變數
PAGE_LOAD_DELAY = 2000
await page.wait_for_timeout(PAGE_LOAD_DELAY)

# 描述性名稱
async def test_header_logo_visibility(stagehand):
    pass

# 使用 BaseActions
base_actions = BaseActions(page)
is_visible = await base_actions.verify_element_visible('selector')

# 驗證頁面內容
base_actions = BaseActions(page)
await base_actions.wait_for_page_loaded()
body_text = await base_actions.get_element_text("body")
assert len(body_text.strip()) > 0, "Page appears to be blank"

# 不使用前綴
async def navigate_homepage(...):
    pass
```

完整的程式碼規則和詳細指南，請參閱 [`.cursor/rules/stagehand_coding_rules.mdc`](.cursor/rules/stagehand_coding_rules.mdc)。

## 故障排除

### 常見問題

#### 1. "OPENAI_API_KEY not found"

**問題**：`.env` 檔案中缺少或不正確的 API 金鑰。

**解決方案**：
- 驗證 `.env` 檔案存在於專案根目錄
- 檢查 `OPENAI_API_KEY` 是否正確設定
- 確保 `.env` 檔案未提交到 git

#### 2. "Browser not found" 或 "Chromium not installed"

**問題**：未安裝 Playwright 瀏覽器。

**解決方案**：
```bash
python -m playwright install chromium
```

> ⚠️ **警告**：僅支援 Chromium 瀏覽器。**請勿**嘗試安裝 Firefox 或 Safari 瀏覽器，因為 Stagehand 不支援它們。

#### 3. 並行執行中的連接埠衝突

**問題**：多個測試嘗試使用相同的連接埠。

**解決方案**：框架會自動使用隨機連接埠處理此問題。如果問題持續存在，請減少並行工作程序數量：

```bash
pytest -n 2  # 而不是 -n auto
```

#### 4. 測試超時

**問題**：測試執行時間過長或掛起。

**解決方案**：
- 檢查您的網路連線
- 驗證目標網站是否可訪問
- 如需要，在測試程式碼中增加超時時間
- 檢查 OpenAI API 速率限制

#### 5. "Module not found" 錯誤

**問題**：未安裝依賴套件。

**解決方案**：
```bash
pip install -r requirements.txt
```

#### 6. 無頭模式問題

**問題**：測試在無頭模式下失敗，但在有頭模式下通過。

**解決方案**：
- 某些網站在無頭模式下的行為不同
- 先嘗試不使用 `--headless` 標誌執行
- 檢查網站是否阻擋無頭瀏覽器

#### 7. 瀏覽器相容性問題

**問題**：嘗試使用 Firefox 或 Safari，或收到不支援瀏覽器的錯誤。

> ⚠️ **重要**：Stagehand **僅**支援 Chromium/Chrome 瀏覽器。Firefox 和 Safari **不支援**。

**解決方案**：
- ✅ 確保您已透過 `python -m playwright install chromium` 安裝 Chromium
- ❌ **請勿**配置框架使用 Firefox 或 Safari
- ❌ **請勿**嘗試安裝 Firefox 或 Safari 瀏覽器
- 如果您看到瀏覽器相容性錯誤，請驗證 Chromium 是否已正確安裝

### 取得幫助

1. 查看 [Stagehand 文件](https://github.com/browserbase/stagehand-python)
2. 使用 `-v` 或 `-vv` 標誌檢視 pytest 日誌
3. 使用 `-s` 標誌執行測試以查看 print 語句
4. 在非無頭模式下檢查瀏覽器控制台日誌

### 除錯模式

以最大詳細程度執行測試：

```bash
pytest -vvv -s --tb=long
```

這將顯示：
- 非常詳細的輸出
- Print 語句
- 失敗的完整追蹤

## 授權

此專案採用 MIT 授權。詳見 [LICENSE](LICENSE) 檔案。

## 資源

- [Stagehand Python 文件](https://github.com/browserbase/stagehand-python)
- [Pytest 文件](https://docs.pytest.org/)
- [Pytest-xdist 文件](https://pytest-xdist.readthedocs.io/)
- [Pytest-rerunfailures 文件](https://github.com/pytest-dev/pytest-rerunfailures)

---

**祝測試愉快！🚀**

