import re
product_count_text = "381 Products found"
product_count_int = int(re.match("^(\d+).*", product_count_text).group(1))