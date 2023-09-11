import csv
import json

import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import pytz


# create some basic values
headers = {
    "Accept":"text/plain, */*; q=0.01",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def get_pagination():
    """
    this function acesses to vistaauction, parse it and get the last pagination page
    :return:
    pagination index, as int
    """

    url = "https://vistaauction.com/Browse?page=0"
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    pagination = int(soup.find("ul", class_="pagination").find_all("li")[-2].find("a").text)
    return pagination


def parce_page(pag):
    with open("result.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Title",
            "MSRP",
            "BID",
            "Condition",
            "Time remaining",
            "Image url",
            "url"
        ])

    for i in range(0, pag+1):
        logging.info(f"working with page: {i}")

        url = f"https://vistaauction.com/Browse?page={i}"

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        lot_data = soup.find_all("section")

        result = []

        count = 0
        for item in lot_data:
            logging.info(f"working with item:{count}/{len(lot_data)}")
            try:
                count += 1
                lot_img_url = item.find(class_="img-responsive")["src"]
                lot_title = " ".join(item.find("h1").find_next("a").text.strip().strip().split())
                lot_url = "https://vistaauction.com" + item.find("a")["href"]
                subtitle = item.find("h2").find("a").text.strip()
                lot_msrp = float(subtitle.split(" - ")[0].split("MSRP: $")[1])
                lot_condition = subtitle.split(" - ")[1]
                lot_bid = float(item.find("a", class_="InlineQuickBid").find_next("span").text)
                lot_time = get_lot_time(lot_url)

                # requested conditions
                if lot_msrp > 25 and lot_bid < 25:
                    # result.append({
                    #     "lot_image": lot_img_url,
                    #     "lot_title": lot_title,
                    #     "lot_MSRP": lot_msrp,
                    #     "lot_bid": lot_bid,
                    #     "lot_condition": lot_condition,
                    #     "lot_time_remaining": lot_time,
                    #     "lot_url": lot_url
                    # })

                    with open("result.csv", "a") as f:
                        writer = csv.writer(f)
                        writer.writerow([lot_title, str(lot_msrp)+"$", str(lot_bid)+"$", lot_condition, lot_time, lot_img_url, lot_url])

            except Exception:
                logging.info(f"some error with item: {count}")

        # save the data to JSON
        # with open("result.json", "a") as f:
        #     json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"execution time was: {datetime.now()-start}")


def get_lot_time(url):
    """
    This function accesses to each lot url, parses a page and get finish_time. Then it compares it with current
    time and return a delta result, which is equal a remaining time for a lot
    :param url:
    as string
    :return: lot_time, as string - remaining time for a lot
    """

    # get a page via requests and parse it with BS
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    # get the data of auction finish
    finish_data = soup.find(class_="awe-rt-endingDTTM")["data-initial-dttm"]

    # Create a timezone object for GMT-4
    timezone = pytz.timezone('Etc/GMT+4')

    # Change finish data with correct timezone
    finish_datetime = timezone.localize(datetime.strptime(finish_data, '%m/%d/%Y %H:%M:%S'))

    # Get a current time and substruct it from finish time, so the'll be a remaining time for a lot
    current_datetime = datetime.now(timezone)
    lot_time = str((finish_datetime - current_datetime)).split(".")[0]
    return lot_time


if __name__ == '__main__':
    start = datetime.now()
    pag = get_pagination()
    parce_page(pag)
