import re

generic_urls = ["https://www.genericdoma;in.com/abc/def/1290aodwb23-ghi.img", "https://www.genericdomain.com/ab-c/31287bdwakj-jkl.img", "https://www.genericdomain.com/19unioawd02-jkl.img"]

for url in generic_urls:
    special_sequence = re.match(".*/(.*)-.*", url).group(1)