from django.contrib import admin


from mainBlog.models import Category, Article, Comments, UserAccount


# автоматическое заполнение 
class ArticleAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comments)
admin.site.register(UserAccount)