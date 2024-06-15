import requests
from bs4 import BeautifulSoup
import csv

def get_ebay_items(search_query, max_results=100):
    # eBayの検索結果ページの基本URL
    base_url = "https://www.ebay.com/sch/i.html"
    results = []
    page_number = 1
    
    while len(results) < max_results:
        # 検索結果ページのURLを作成
        url = f"{base_url}?_nkw={search_query.replace(' ', '+')}&_pgn={page_number}"
        
        # ページを取得
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーをチェック
        
        # BeautifulSoupを使用してHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 検索結果のアイテムを抽出
        items = soup.find_all('div', class_='s-item__info clearfix')
        
        if not items:
            break
        
        # 商品名と価格を取得
        for item in items:
            title = item.find('div', class_='s-item__title')
            price = item.find('span', class_='s-item__price')
            if title and price and ("Shop on eBay" not in title.get_text()):
                results.append((title.get_text(), price.get_text()))

                if (len(results) >= max_results):
                    break
        
        page_number += 1
    
    return results

#csvに書き込み
def save_to_csv(items, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer=csv.writer(file)
        writer.writerow(["商品名", "値段"])
        writer.writerows(items)

# 商品名を指定して検索
search_query = "laptop"
max_results = 100  # 取得したい最大件数を指定
items = get_ebay_items(search_query, max_results)

# 結果を表示
for i, (title, price) in enumerate(items, start=1):
    print(f"{i}. {title} - {price}")

csv_name="ebay_results.csv"
save_to_csv(items, csv_name)


