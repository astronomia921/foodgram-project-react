# Generated by Django 4.2.2 on 2023-06-22 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0006_alter_favorite_options_alter_shoppingcart_options_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='favorite',
            name='foodgram_fa_user_id_5d2e53_idx',
        ),
        migrations.RemoveIndex(
            model_name='shoppingcart',
            name='foodgram_sh_user_id_b87924_idx',
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_favorite'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='shopping_recipe_user'),
        ),
    ]