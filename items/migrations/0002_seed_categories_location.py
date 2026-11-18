from django.db import migrations

CATEGORIES = ["Bags", "Phones", "IDs and Cards", "Keys", "Wallets",
              "Laptops and Gadgets", "Clothing", "Books and School Supplies",
              "Water Bottles", "Others"]
LOCATIONS = ["Library", "Canteen", "Main Gate", "Gymnasium",
             "Computer Laboratory", "Admin Building", "Parking Area",
             "Chapel", "Other"]


def seed(apps, schema_editor):
    Category = apps.get_model("items", "Category")
    Location = apps.get_model("items", "Location")
    for name in CATEGORIES:
        Category.objects.get_or_create(name=name)
    for name in LOCATIONS:
        Location.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]