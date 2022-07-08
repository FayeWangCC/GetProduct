import os.path
import datetime
import requests
from lxml import etree


# 获取商品信息
def get_product_msg(product_url):
	resp = requests.get(product_url, verify=False)
	resp.encoding = 'utf8'
	data = resp.text
	print(resp.status_code)
	return data


# 解析相应获取指定数据
def parse_data(data):
	# 将数据解析为HTML
	dom = etree.HTML(data)
	# 获取商品一级分类
	fir_sort = str(dom.xpath('//span[@class="brandCat"]/label[1]/span/a/label')[0].text)
	# 获取商品二级分类
	sec_sort = str(dom.xpath('//span[@class="brandCat"]/label[2]/span/a/label')[0].text)
	# 获取商品名称
	skuname = str(dom.xpath('//div[@class="name_info"]/h1')[0].text)
	# 获取商品平台价格
	pro_price = float(str(dom.xpath('//div[@class="normal_price"]/span[2]/b')[0].text).replace('￥', ''))
	# 将价格调高为平台价格的两倍
	pro_price = str(pro_price + pro_price)
	# 获取商品品牌
	brand = str(dom.xpath('//div[@class="summary"]/div[1]/div[2]/span')[0].text)
	# 获取商品规格
	specification = str(dom.xpath('//div[@class="summary"]/div[2]/div[2]/span')[0].text)
	# 定义需要替换的字符
	replace_list = ['(', ')', '（', '）', '/', '\\', '"', '\'', ' ','\r','\n']
	# 定义要替换的字符
	re_str = ''
	for re in replace_list:
		fir_sort = fir_sort.replace(re, re_str).replace('*', 'x')
		sec_sort = sec_sort.replace(re, re_str).replace('*', 'x')
		skuname = skuname.replace(re, re_str).replace('*', 'x')
		brand = brand.replace(re, re_str).replace('*', 'x')
		specification = specification.replace(re, re_str).replace('*', 'x')

	# 获取商品sku
	pro_sku = str(dom.xpath('//div[@class="summary"]/div[3]/div[2]/span')[0].text)
	# 获取商品图片列表对象
	el_li = dom.xpath('//div[@class="list"]/ul/li')
	img_list = []
	for li in el_li:
		img_src = li.xpath('./img/@src')[0]
		img_src = str(img_src).split('?x-oss-process=style/style')[0] + '?x-oss-process=style/style800'
		img_list.append(img_src)
	# 保存路径
	# 获取当天日期
	today = datetime.date.today()
	file_path = str(f'C:/Users/FayeWong/OneDrive/产品资料/产品素材/{today}/{fir_sort}/{sec_sort}/{skuname}')
	print(file_path)
	# 判断目录是否存在，不存在就创建
	if not os.path.exists(file_path):
		os.makedirs(file_path)
	# 保存商品信息到目录文件
	with open(f'{file_path}/{skuname}.txt', 'w') as fw:
		fw.write(f'{fir_sort}\n')
		fw.write(f'{sec_sort}\n')
		fw.write(f'{skuname}\n')
		fw.write(f'{pro_price}\n')
		fw.write(f'{brand}\n')
		fw.write(f'{specification}\n')
		fw.write(f'{pro_sku}')
		print(f'<{skuname}>信息保存完成！')
	num = 1
	# 保存商品图片到指定目录文件
	for img_url in img_list:
		# 获取商品图片
		resp_img = requests.get(img_url, verify=False)
		# 保存图片
		with open(f'{file_path}/{num}.jpg', 'wb') as fwi:
			fwi.write(resp_img.content)
		num += 1
	print(f'<{skuname}>图片保存完成')


if __name__ == '__main__':
	url = 'https://www.xfs.com/productsku/'
	# 从文件中读取产品sku
	with open('pro_sku_list.txt') as fr:

		# 定义存储抓取错误商品的SKU列表
		error_list = []
		while True:
			# 一次读一行
			product_sku = fr.readline()
			product_sku = product_sku.replace('\n', '')
			# 判断是否到达最后一行
			if product_sku:
				# product_sku = input('请输入产品SKU：')
				product_url = url + product_sku + '.html'
				# 调用方法获取网页数据
				data = get_product_msg(product_url)
				try:
					# 调用方法解析数据
					parse_data(data)
				except IndexError:
					# 将抓取错误的商品SKU保存到list中
					error_list.append(product_sku)
					print('--------------------------------')
					print(f'SKU为{product_sku}的商品抓取失败！')
					print(f'SKU为{product_sku}的商品抓取失败！')
					print(f'SKU为{product_sku}的商品抓取失败！')
					print('--------------------------------')
				continue
				print(f'SKU为{product_sku}的商品保存完成！')
			else:
				break
				print('所有商品保存完成！')
		print('以下商品信息抓取失败！！！')
		for sku in error_list:
			print(sku)
