ArticleCategory = ["love", "space", "kawaii"]

category_dict = dict()
for category in ArticleCategory:
	list= []
	for category in ArticleCategory:
		list.append(category)
	category_dict[category] = list
		
        
for category in category_dict:
	print(category)
	print(category_dict[category])