import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# ✅ Extract value from a specific <td> based on label and table index
async def get_cell_text(page, label, table_index=0, value_index=2):
    try:
        # Target the specific table under <center> by index
        table = page.locator('center table').nth(table_index)
        # Find the <tr> with the label and get the value <td> (adjusted for HTML structure)
        element = table.locator(f'tr:has(td:has-text("{label}")) td:nth-child({value_index}) font')
        await element.wait_for(timeout=60000)  # Increased to 60s
        text = await element.text_content()
        return text.strip() if text else None
    except Exception as e:
        print(f"Error getting label {label} :: {e}")
        return None

# ✅ Extract parties from the dedicated parties table
async def extract_parties(page):
    try:
        # Target the parties table (third table under <center>, index 2)
        parties_table = page.locator('center table').nth(2)
        await parties_table.wait_for(timeout=60000)  # Increased to 60s
        # Extract text from both <tr> elements
        tr1 = parties_table.locator('tr:nth-child(1) td font')
        tr2 = parties_table.locator('tr:nth-child(2) td font')
        text1 = await tr1.text_content() or ""
        text2 = await tr2.text_content() or ""
        return f"{text1.strip()} vs. {text2.strip()}" if text1 and text2 else None
    except Exception as e:
        print(f"Error extracting parties: {e}")
        return None

# ✅ Judgment PDF link extractor (not present in this HTML)
async def extract_pdf_link(page):
    try:
        element = await page.wait_for_selector('a[href*=".pdf"]', timeout=120000)  # Increased to 120s
        return await element.get_attribute('href') if element else None
    except Exception as e:
        print(f"Error extracting PDF link: {e}")
        return None

# 🚀 Scraper main
async def scrape_court_data(court, case_type, case_number, filing_year):
    async with async_playwright() as p:
        max_retries = 3
        url = 'https://dhcmisc.nic.in/pcase/guiCaseWise.php'

        for attempt in range(max_retries):
            browser = None
            try:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                print(f"Attempt {attempt + 1}/{max_retries}: Navigating to {url}")
                await page.goto(url, wait_until='networkidle', timeout=120000)

                print(f"Filling form: case_type={case_type}, case_number={case_number}, year={filing_year}")
                await page.select_option('select#ctype', label=case_type)
                await page.fill('input#regno', case_number)
                await page.select_option('select#regyr', value=str(filing_year))

                print("Waiting for CAPTCHA...")
                await page.wait_for_selector('#cap', timeout=100000)
                captcha_text = await page.text_content('#cap')
                if not captcha_text or not captcha_text.strip().isdigit():
                    raise Exception("CAPTCHA not found or unreadable")
                await page.fill('input.form-control', captcha_text.strip())
                print(f"CAPTCHA entered: {captcha_text.strip()}")

                print("Submitting form...")
                await page.click('input[type="submit"]')
                await page.wait_for_url('**/case_history.php', timeout=150000)

                # Wait for page body and ensure network idle
                await page.wait_for_selector('body', timeout=100000)
                await page.wait_for_load_state('networkidle')

                # Debug: save screenshot and HTML separately
                await page.screenshot(path=f"debug_case_data_attempt{attempt+1}.png", full_page=True)
                html_content = await page.content()
                with open(f"debug_html_attempt{attempt+1}.html", "w", encoding="utf-8") as f:
                    f.write(html_content)

                # Check for server errors or no data
                if any(error in html_content.lower() for error in ["fatal error", "unable to connect", "no record found"]):
                    return {"error": "No case data found or server error detected."}

                print("Extracting case data...")

                data = {
                    'case_id': await get_cell_text(page, "Case No :", 2, 2) or "BAIL APPLN.-" + case_number + "/" + filing_year,
                    'cnr_number': await get_cell_text(page, "CNR No. :", 2, 2),
                    'status': await get_cell_text(page, "Status :", 2, 2),
                    'dealing_assistant': await get_cell_text(page, "Dealing Assistant :", 4, 2),
                    'filing_advocate': await get_cell_text(page, "Filing Advocate :", 4, 2),
                    'subject1': await get_cell_text(page, "Subject 1 :", 4, 2),
                    'subject2': await get_cell_text(page, "Subject2 :", 4, 2),
                    'filing_date': await get_cell_text(page, "Date of Filing :", 2, 5),
                    'registration_date': await get_cell_text(page, "Date of Registration :", 2, 5),
                    'next_hearing_date': None,  # Not present in this HTML
                    'order_date': None,  # Not present in this HTML
                    'parties': await extract_parties(page),
                    'judgment_pdf_link': await extract_pdf_link(page),
                }

                print(f"✅ Extracted data: {data}")

                return {
                    'court': court,
                    'case_type': case_type,
                    'case_number': case_number,
                    'filing_year': filing_year,
                    **data
                }

            except PlaywrightTimeoutError as e:
                print(f"⚠️ Timeout on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(5)
                    continue
                return {'error': 'Timeout occurred after retries.'}
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return {'error': str(e)}
            finally:
                if browser:
                    await browser.close()
                    print("Browser closed")

# 🧪 Test entrypoint
def get_court_data(court, case_type, case_number, filing_year):
    return asyncio.run(scrape_court_data(court, case_type, case_number, filing_year))

if __name__ == "__main__":
    result = get_court_data('Delhi High Court', 'BAIL APPLN.', '2872', '2025')
    print(result)