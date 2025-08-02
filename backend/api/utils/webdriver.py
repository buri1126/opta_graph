from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from typing import Dict, Any, List

class WebDriverHelper:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
    
    def _create_driver(self):
        """Chrome WebDriverを作成"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        
        # Dockerコンテナ内ではChromiumをChromeの代わりに使用
        chrome_options.binary_location = "/usr/bin/chromium"
        
        # ChromeDriverのサービスを明示的に指定
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def scrape_basic(self, url: str, wait_time: int = 3) -> Dict[str, Any]:
        """基本的なスクレイピング（タイトルとテキストのみ）"""
        try:
            self.driver = self._create_driver()
            self.driver.get(url)
            time.sleep(wait_time)
            
            # ページタイトルを取得
            title = self.driver.title
            
            # ページの基本情報を取得
            body_text = self.driver.find_element(By.TAG_NAME, "body").text[:1000]
            
            return {
                "success": True,
                "title": title,
                "url": url,
                "content": body_text,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "title": None,
                "url": url,
                "content": "",
                "error": str(e)
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def scrape_elements(self, url: str, selector: str, wait_time: int = 3) -> Dict[str, Any]:
        """指定されたセレクターで要素をスクレイピング"""
        try:
            self.driver = self._create_driver()
            self.driver.get(url)
            time.sleep(wait_time)
            
            title = self.driver.title
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            scraped_data = []
            for i, element in enumerate(elements):
                scraped_data.append({
                    "index": i,
                    "text": element.text.strip(),
                    "tag": element.tag_name,
                    "class": element.get_attribute("class"),
                    "id": element.get_attribute("id")
                })
            
            return {
                "success": True,
                "title": title,
                "url": url,
                "elements": scraped_data,
                "count": len(scraped_data),
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "title": None,
                "url": url,
                "elements": [],
                "count": 0,
                "error": str(e)
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def scrape_theanalyst_tottenham(self, wait_time: int = 10) -> Dict[str, Any]:
        """theanalyst.comでTottenhamのデータをスクレイピング"""
        url = "https://theanalyst.com/competition/premier-league/stats"
        
        try:
            self.driver = self._create_driver()
            self.driver.get(url)
            
            # ページ読み込み待機
            wait = WebDriverWait(self.driver, wait_time)
            
            # より多くのセレクターを試す
            search_input = None
            selectors = [
                "//input[contains(@placeholder, 'Search by player or team')]",
                "//input[contains(@placeholder, 'Search')]",
                "//input[@type='search']",
                "//input[contains(@class, 'search')]",
                "input[placeholder*='Search']",
                "input[type='search']"
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith("//"):
                        search_input = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    else:
                        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not search_input:
                # 検索なしで直接Tottenhamページに移動を試す
                tottenham_url = "https://theanalyst.com/team/premier-league/tottenham"
                self.driver.get(tottenham_url)
                time.sleep(5)
            else:
                search_input.clear()
                search_input.send_keys("tottenham")
                search_input.send_keys(Keys.RETURN)
            
            # 検索結果の読み込み待機
            time.sleep(8)
            
            # 複数のテーブルセレクターを試す
            table_selectors = [
                ".TableNew-module_data-table__Noo6s tbody tr",
                "table tbody tr",
                "[data-testid='player-stats-table'] tbody tr",
                ".stats-table tbody tr",
                "tbody tr"
            ]
            
            table_rows = []
            for selector in table_selectors:
                table_rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if len(table_rows) > 0:
                    break
            
            scraped_data = []
            for i, row in enumerate(table_rows):
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = {
                    "index": i,
                    "cells": []
                }
                
                for j, cell in enumerate(cells):
                    row_data["cells"].append({
                        "column": j,
                        "text": cell.text.strip(),
                        "class": cell.get_attribute("class")
                    })
                
                scraped_data.append(row_data)
            
            # ヘッダー情報も取得
            headers = []
            header_selectors = [
                ".TableNew-module_data-table__Noo6s thead th",
                "table thead th", 
                "thead th",
                "th"
            ]
            
            for selector in header_selectors:
                header_cells = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if len(header_cells) > 0:
                    for i, header in enumerate(header_cells):
                        headers.append({
                            "index": i,
                            "text": header.text.strip()
                        })
                    break
            
            # 画面の情報を詳細に取得
            page_content = self.driver.find_element(By.TAG_NAME, "body").text[:2000]
            
            # データを整形
            formatted_data = self._format_tottenham_data(headers, scraped_data)
            
            return {
                "success": True,
                "title": self.driver.title,
                "url": url,
                "search_term": "tottenham",
                "headers": headers,
                "data": scraped_data,
                "formatted_data": formatted_data,
                "count": len(scraped_data),
                "page_content": page_content,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "title": None,
                "url": url,
                "search_term": "tottenham",
                "headers": [],
                "data": [],
                "count": 0,
                "error": str(e)
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def _format_tottenham_data(self, headers: List[Dict], scraped_data: List[Dict]) -> Dict[str, Any]:
        """Tottenhamデータをフロントエンド向けに整形"""
        try:
            header_names = [h["text"] for h in headers]
            
            players = []
            for row in scraped_data:
                if len(row["cells"]) >= len(header_names):  # ヘッダー数と同じだけセルがあることを確認
                    cells = row["cells"]
                    player = {}
                    
                    # ヘッダーのインデックスと実際のデータを対応させる
                    for i, header_name in enumerate(header_names):
                        if i < len(cells):
                            player[str(i)] = cells[i]["text"]  # キーを数値文字列にして、値を実際のセルデータにする
                    
                    players.append(player)
            
            return {
                "success": True,
                "team": "tottenham",
                "total_players": len(players),
                "players": players,
                "headers": header_names,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "team": "tottenham",
                "total_players": 0,
                "players": [],
                "headers": [],
                "error": str(e)
            }
    
    def _is_float(self, value: str) -> bool:
        """文字列がfloatに変換可能かチェック"""
        try:
            float(value)
            return True
        except ValueError:
            return False