from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Menu(models.Model):
    name = models.CharField(
        'Тип меню',
        max_length=20
    )
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True,
        null=True,
        upload_to='images',
    )

    class Meta:
        verbose_name = 'Тип меню'
        verbose_name_plural = 'Типы меню'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    PERIOD_CHOICES = [
        ('1', '1 месяц'),
        ('3', '3 месяца'),
        ('6', '6 месяцев'),
        ('12', '12 месяцев')
    ]
    period = models.CharField(
        'Срок подписки',
        max_length=2,
        choices=PERIOD_CHOICES,
        unique=True
    )
    price = models.IntegerField(
        'Стоимость',
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.period} мес.: {self.price} руб.'

class Category(models.Model):
    name = models.CharField(
        'Название',
        db_index=True,
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='user_orders',
        on_delete=models.CASCADE
    )
    paid = models.BooleanField(
        'Оплачена',
        default=False,
        db_index=True
    )
    payment_date = models.DateField(
        'Дата оплаты',
        null=True,
        blank=True,
        db_index=True
    )
    menu_type = models.ForeignKey(
        Menu,
        verbose_name='Тип меню',
        related_name='orders',
        null=True,
        on_delete=models.SET_NULL
    )
    subscription = models.ForeignKey(
        Subscription,
        verbose_name='Подписка',
        related_name='orders',
        null=True,
        on_delete=models.SET_NULL
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='Категория',
        related_name='orders'
    )
    person_count = models.IntegerField(
        'Количество персон',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6)
        ]
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.user} - {self.subscription.period}'


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=100
    )
    quantity = models.IntegerField(
        'Количество',
        validators=[MinValueValidator(0)] # если 0, то значение "по вкусу"
    )
    unit = models.CharField(
        'Ед. измерения',
        max_length=10,
        blank=True
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}: {self.quantity} {self.unit}'


class Recipe(models.Model):
    free = models.BooleanField(
        'Бесплатный',
        default=False
    )
    name = models.CharField(
        'Название',
        max_length=100,
        unique=True
    )
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True,
        null=True,
        upload_to='images',
    )
    description = models.TextField(
        'Описание',
        max_length=200,
        blank=True
    )
    menu = models.ForeignKey(
        Menu,
        verbose_name='Тип меню',
        related_name='recipes',
        null=True,
        on_delete=models.SET_NULL
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='Категория',
        related_name='recipes'
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='recipes'
    )
    calories = models.IntegerField(
        'Калорийность',
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
