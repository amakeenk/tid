#!/usr/bin/python3
  
# Author: Alexander Makeenkov <amakeenk@altlinux.org>

import requests
import os
import bs4
import argparse


class Downloader():
    def __init__(self, url, outdir):
        self.url = url
        self.outdir_name = outdir
        self.telegraph_url = 'https://telegra.ph'

    def create_dir(self):
        if not os.path.exists(self.outdir_name):
            os.mkdir(self.outdir_name)

    def download(self):
        counter = 0
        response = requests.get(self.url)
        if response.status_code != 200:
            print(response.text)
            exit(1)
        images = bs4.BeautifulSoup(response.text, 'lxml').findAll('img')
        for img in images:
            counter += 1
            image_url = f'{self.telegraph_url}/{img["src"]}'
            response = requests.get(image_url)
            print(f'Downloading image {counter}/{len(images)}')
            try:
                with open(f'{self.outdir_name}/image_{counter}.jpg', 'wb') as file:
                    for data in response.iter_content(1024):
                        file.write(data)
            except requests.exceptions.RequestException as err:
                print(f'Some error occured: {err.strerror}')


def main():
    args = argparse.ArgumentParser()
    args.add_argument('url', help='album url')
    args.add_argument('outdir', help='directory for downloading')
    args_list = args.parse_args()
    url, outdir = args_list.url, args_list.outdir
    downloader = Downloader(url, outdir)
    downloader.create_dir()
    downloader.download()
    print(f'All done. Images dowloading to ./{downloader.outdir_name}')


if __name__ == '__main__':
    main()
