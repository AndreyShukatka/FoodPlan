from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
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
    MENU_TYPE_CHOICES = [
        ('CLASSIC', 'Классическое'),
        ('LOW_CARB', 'Низкоуглеводное'),
        ('VEGETARIAN', 'Вегетарианское'),
        ('KETO', 'Кето')
    ]
    menu_type = models.CharField(
        'Тип меню',
        max_length=10,
        choices=MENU_TYPE_CHOICES
    )
    PERIOD_CHOICES = [
        ('1', '1 месяц'),
        ('3', '3 месяца'),
        ('6', '6 месяцев'),
        ('12', '12 месяцев')
    ]
    period = models.CharField(
        'Срок подписки',
        max_length=2,
        choices=PERIOD_CHOICES
    )
    breakfast = models.BooleanField(
        'Завтрак'
    )
    lunch = models.BooleanField(
        'Обед'
    )
    dinner = models.BooleanField(
        'Ужин'
    )
    dessert = models.BooleanField(
        'Десерт'
    )
    person_count = models.IntegerField(
        'Количество персон',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6)
        ]
    )
    FISH = 'f'
    MEAT = 'm'
    CEREAL = 'c'
    BEE_PRODUCTS = 'b'
    NUTS = 'n'
    DAIRY = 'd'
    ALLERGY_CHOICES = [
        (FISH, 'Рыба и морепродукты'),
        (MEAT, 'Мясо'),
        (CEREAL, 'Зерновые'),
        (BEE_PRODUCTS, 'Продукты пчеловодства'),
        (NUTS, 'Орехи и бобовые'),
        (DAIRY, 'Молочные продукты')
    ]
    allergy = models.CharField(
        'Аллергии',
        max_length=6,
        choices=ALLERGY_CHOICES
    )

    def __str__(self):
        return f'{self.user} - {self.period}'
