import re


def text2object(text):
	# preprocess
	text = text.upper()
	text.replace("$", " ")

	# convert string into list
	lines = text.split('\n')

	# find lines that have an associated price
	products = []
	prices = []
	total = None
	name = None
	end_idx = None
	for i,line in enumerate(lines):
		if name is None and len(line) > 1:
			name = line
		if end_idx is None:
			# preprocess line text
			line = line.upper()
			line.replace("'", "")

			# check if the total has been displayed (only works for certain receipts).
			# if the total has been displayed, then the list of products has ended
			if line.__contains__('TOTAL'):
				end_idx = i
				#print(" ========= END OF PRODUCTS =========")

			# regular expression to check if the line ends in a decimal (price)
			re_end_in_num = "^.*[0-9][\.,][0-9][0-9]"
			x = re.search(re_end_in_num+"( .*)?$", line)
			if x is not None:
				units = line.split(" ")
				j = len(units)-1
				while j>0:
					if re.search(re_end_in_num+"$", units[j]) is not None:
						break
					else:
						j = j-1
				try:
					p = units[j].replace(",", ".").replace("$", " ")
					p = float(p)
					if end_idx is not None:
						total = p
					else:
						prices.append(p)
						products.append(" ".join(units[:j]))
				except(ValueError):
					print("ERROR: {} is not a number.".format(units[j]))

	# name = lines[0]
	if total is None:
		total = sum(prices)
	receipt = {'NAME':name, 'TOTAL':total, 'PRODUCTS':products, 'PRICES':prices}

	return receipt

