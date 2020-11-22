from tgbot.models import User, Category, UserToCategory

def update_user_categories(user_id, category):
  user_db = User.objects.filter(user_id__exact=str(user_id)).get()
  category_db = Category.objects.filter(name__exact=str(category)).get()
  user_categories = UserToCategory.objects.filter(user=user_db, category=category_db)
  has_category_added = user_categories.count() == 0

  if has_category_added:
    UserToCategory(
      user=user_db,
      category=category_db
    ).save()

  return has_category_added