from django.db import models
from django.urls import reverse

class Category(models.Model):
	name = models.CharField(max_length=200,
							db_index=True)
	slug = models.SlugField(max_length=200,
							unique=True)
	index = models.IntegerField(null=True,
								default=1)

	class Meta:
		ordering = ("index",)
		verbose_name = "category"
		verbose_name_plural = "categories"

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		list_path_name = "product_list_by_category"
		return reverse(f"shop:{list_path_name}",
					   args=[self.slug])

class Genre(models.Model):
	name = models.CharField(max_length=200,
							db_index=True,
							default="Women")
	slug = models.SlugField(max_length=200,
							unique=True,
							default="women")
	index = models.IntegerField(null=True, default=1)

	class Meta:
		ordering = ("index",)

	def __str__(self):
		return self.name

class Season(models.Model):
	name = models.CharField(max_length=200,
							db_index=True,
							default="Spring")
	slug = models.SlugField(max_length=200,
							unique=True,
							default="spring")
	index = models.IntegerField(null=True, default=1)

	class Meta:
		ordering = ("index",)

	def __str__(self):
		return self.name

class Product(models.Model):
	COLORS = (
		("red", "紅"),
		("orange", "橙"),
		("yellow", "黃"),
		("pink", "粉紅"),
		("cyan", "青"),
		("blue", "藍"),
		("purple", "紫"),
		("green", "綠"),
		("gray", "灰"),
		("black", "黑"),
		("white", "白"),
		("brown", "咖啡")
	)
	BRANDS = (
		("Uniqlo", "Uniqlo"),
		("GU", "GU"),
		("NET", "NET"),
		("Lativ", "Lativ"),
		("H&M", "H&M"),
	)
	THICKNESSES = (
		("thick", "厚"),
		("average", "中"),
		("thin", "薄")
	)
	# category: product is 1:N
	# related_name: query 'products' by 'category'

	''' 服飾商品 - 基本屬性 '''
	category = models.ForeignKey(Category,
								 related_name="products",
								 on_delete=models.CASCADE)

	name = models.CharField(max_length=200,
							db_index=True)

	slug = models.SlugField(max_length=200,
							db_index=True)

	image = models.ImageField(upload_to="products/%Y/%m/%d",
							  blank=True)

	description = models.TextField(null=True,
                                   blank=True)

	price = models.DecimalField(max_digits=10,
								decimal_places=0)

	available = models.BooleanField(default=True)

	create_date = models.DateTimeField(auto_now_add=True)

	update_date = models.DateTimeField(auto_now=True)

	''' 服飾商品 - 進階屬性 '''
	### [可複選] 所屬客群/季節/顏色/風格/材質
	genres = models.ManyToManyField(Genre)

	seasons = models.ManyToManyField(Season)

	main_color = models.CharField(max_length=200,
								  choices=COLORS,
								  db_index=True,
								  null=True,
								  blank=True)

	styles = models.CharField(max_length=200,
							  db_index=True,
                              null=True,
							  blank=True)

	materials = models.CharField(max_length=200,
								 db_index=True,
                                 null=True,
								 blank=True)

	### [單選] 品牌/厚度
	brand = models.CharField(max_length=200,
							 db_index=True,
							 choices=BRANDS,
							 null=True,
							 blank=True)

	thickness = models.CharField(max_length=200,
								 db_index=True,
								 choices=THICKNESSES,
								 null=True,
								 blank=True)

	class Meta:
		ordering = ("name",)

	index_together = (("id", "slug"),)

	def __str__(self):
		return self.name

	def get_genres(self):
		return "、".join([genre.name for genre in self.genres.all()])

	def get_seasons(self):
		return "、".join([season.name for season in self.seasons.all()])

	def get_absolute_url(self):
		detail_path_name = "product_detail"
		return reverse(f"shop:{detail_path_name}",
					   args=[self.id, self.slug])

	""" 將傳入整數轉為具有千分號的字串並回傳 """
	def get_num_with_separators(self, n):
		n = str(n)
		prefix = n[:len(n)-3*(len(n)//3)]
		suffix = n[len(n)-3*(len(n)//3):]
		result = prefix + (',' if len(prefix)>0 and len(suffix)>0 else '')
		result += ','.join([suffix[3*i:3*(i+1)] for i in range(len(n)//3)])
		return result

	def get_price_str(self):
		return self.get_num_with_separators(self.price)
