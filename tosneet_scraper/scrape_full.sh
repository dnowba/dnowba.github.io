for spiderid in npcs skills attributes zones items
do
  echo "===================="
  echo "Scraping $spiderid.."
  echo "===================="
  fname="output_full/$spiderid.json"
  rm -f $fname
  scrapy crawl $spiderid -o $fname -a pfull_html=True
done
