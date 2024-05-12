from currency_converter import CurrencyConverter

def get_pair_price(usd):
	converter = CurrencyConverter()
	
	return int(converter.convert(usd, 'USD', 'IDR'))