from operator import countOf
from playwright.sync_api import sync_playwright,expect
import json
import csv

data_csv = []
data_json = []

def scrape_pages(page,page2):
         
        # Storing Xpath in variables
        stock_names = page.query_selector_all("//a[@data-anonymize='person-name']")
        stock_cmp = page.query_selector_all("//a[contains(@class,'ember-view t-black--light')]")
        # stock_link= page.locator("(//a[contains(@class,'ember-view t-black--light')])").click()
        stock_link = page.query_selector_all("//a[contains(@class,'ember-view t-black--light')]")
        stock_page = page.query_selector_all("//button[contains(@class,'artdeco-pagination__button artdeco-pagination__button--next')]")
        # print(stock_page.count())
        #To find number of rows
        rows = page.locator("(//a[@data-anonymize='person-name'])")
        count = rows.count()
        print(count)

        #To find number of pages
        pages = page.locator("(//li[contains(@class,'artdeco-pagination__indicator artdeco-pagination__indicator--number')]//button)")
        #pcount = pages.len()
        #qcount = stock_page.count()
        pcount = pages.count()
        # scount = stock_page.len()
        print(pcount)
        # y=0
        # next_page = pages[y].inner_text()
        # while next_page > 1:
        #     next_page
            
        #     print(y,next_page)
        #     y+=1


        #count = len(stock_codes)
        x=0
        for x in range(count):
            try:

                #code = stock_codes[x].inner_text()
                name = stock_names[x].inner_text()
                company = stock_cmp[x].inner_text()
                link = stock_link[x].get_attribute('href')


                if (link):
                  url = "https://www.linkedin.com/"+ link
            
                # obj.url = url
                if (url):
                    page2.goto(url)
                    page2.wait_for_load_state()
                    z = page2.locator('//a[contains(@class,"ember-view artdeco-button")]')

                    z.wait_for(timeout=5000)            
                    if (z.count() == 1):
                        url =  z.get_attribute("href");
                        # obj.website = url;
                        # obj.website = null;
                        print(url)
                    else:
                        print("null")



                print(x,name,company,link,url)
                if x == rows.count()-1:
                    x+=count
                    for y in range(pcount):
                        page.locator("//button[contains(@class,'artdeco-pagination__button artdeco-pagination__button--next')]").click()
                    
                    else:
                        print("NULL")
        
                   
            except Exception as e: 
                print(e)
                x += 1 
        
        # CSV            
            content_csv = [name, company,link,url]
            data_csv.append(content_csv)
            # JSON
            content_json = {
                
                'Name': name,
                'Company': company,
                'Link': link,
                'Url': url
                
            }
            data_json.append(content_json)

        page.locator("//button[@aria-label='Next']").click()
                

def scrape_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page2 = context.new_page()
        #page.keyboard.press("Control+Tab")
        
        page.goto("https://www.linkedin.com/uas/login?session_redirect=%2Fsales&_f=navigator&fromSignIn=true&trk=sales-home-page_nav-header-signin&src=or-search&veh=www.google.com")
        #email or phone fills
        page.locator('[aria-label="Email or Phone"]').fill("kewinsebrodriguez@gmail.com")
    
        #password fill
        page.locator('//input[@type="password"]').fill("starboy__3062")
    
        #sign in
        page.locator('[aria-label="Sign in"]').click()
        expect(page).to_have_url("https://www.linkedin.com/sales/index")
    
        #text=RPA-COE
        page.goto("https://www.linkedin.com/sales/search/people?page=&savedSearchId=50538485&sessionId=22IBRAl8TLWN2bk4XVaYEA%3D%3D")
        
        #scroll-down
        page.locator("#search-results-container").click()
        for index in range(0,500,1):
            page.locator("#search-results-container").press("ArrowDown")
            
        
            
        scrape_pages(page,page2)
        scrape_pages(page,page2)


            
        browser.close()

       

def storing_csv():
    with open('data.csv', mode='w', newline='', encoding="utf-8") as csv_file:
        # Create object
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write
        writer.writerow(["NAME", "COMPANY", "LINK","URL"])
        for d in data_csv:
            writer.writerow(d)
    print("Writing to CSV has been successful !")

def storing_json():
    # Serializing json
    json_object = json.dumps(data_json, indent=4)
    with open("data.json", "w") as outfile:
        outfile.write(json_object)
    print("Writing to JSON has been successful !")


scrape_data()
storing_csv()
storing_json()
