from django.db import models



class Cities(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100, db_column='City_Name')

    class Meta:
        managed = False
        db_table = 'Cities'

    def __str__(self):
        return self.city_name


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, db_column='First_Name', blank=True, null=True)
    last_name = models.CharField(max_length=100, db_column='Last_Name', blank=True, null=True)
    email = models.EmailField(db_column='Email', unique=True)
    password = models.CharField(max_length=255, db_column='Password')

    city = models.ForeignKey(
        Cities,
        on_delete=models.SET_NULL,
        db_column='City_ID',
        null=True,
        blank=True
    )

    age = models.IntegerField(db_column='Age', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'

    def __str__(self):
        return self.email


class Pharmacies(models.Model):
    pharmacy_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=150, db_column='Branch_Name', blank=True, null=True)

    city = models.ForeignKey(
        Cities,
        on_delete=models.CASCADE,
        db_column='City_ID'
    )

    class Meta:
        managed = False
        db_table = 'Pharmacies'

    def __str__(self):
        return self.branch_name or "Pharmacy"


# =========================
# MEDICINE SYSTEM
# =========================

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, db_column='Category_Name')

    class Meta:
        managed = False
        db_table = 'Categories'


class ActiveIngredients(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=100, db_column='Ingredient_Name')

    class Meta:
        managed = False
        db_table = 'Active_Ingredients'


class Manufacturers(models.Model):
    manufacturer_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=150, db_column='Company_Name')
    country = models.CharField(max_length=100, db_column='Country')

    class Meta:
        managed = False
        db_table = 'Manufacturers'


class Medicines(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=150, db_column='Medicine_Name')

    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, db_column='Category_ID', null=True)
    ingredient = models.ForeignKey(ActiveIngredients, on_delete=models.SET_NULL, db_column='Ingredient_ID', null=True)
    manufacturer = models.ForeignKey(Manufacturers, on_delete=models.SET_NULL, db_column='Manufacturer_ID', null=True)

    class Meta:
        managed = False
        db_table = 'Medicines'


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)

    pharmacy = models.ForeignKey(Pharmacies, on_delete=models.CASCADE, db_column='Pharmacy_ID')
    medicine = models.ForeignKey(Medicines, on_delete=models.CASCADE, db_column='Medicine_ID')

    quantity = models.IntegerField(db_column='Quantity')
    price = models.FloatField(db_column='Price')

    class Meta:
        managed = False
        db_table = 'Inventory'


# =========================
# ORDERS SYSTEM
# =========================

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='User_ID')
    pharmacy = models.ForeignKey(Pharmacies, on_delete=models.CASCADE, db_column='Pharmacy_ID')

    order_date = models.DateTimeField(db_column='Order_Date')

    class Meta:
        managed = False
        db_table = 'Orders'


class OrderItems(models.Model):
    item_id = models.AutoField(primary_key=True)

    order = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='Order_ID')
    medicine = models.ForeignKey(Medicines, on_delete=models.CASCADE, db_column='Medicine_ID')

    quantity = models.IntegerField(db_column='Quantity')

    class Meta:
        managed = False
        db_table = 'Order_Items'


# =========================
# USER FEATURES
# =========================

class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='User_ID')
    pharmacy = models.ForeignKey(Pharmacies, on_delete=models.CASCADE, db_column='Pharmacy_ID')

    rating = models.IntegerField(db_column='Rating')

    class Meta:
        managed = False
        db_table = 'Reviews'


class UserSymptoms(models.Model):
    symptom_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='User_ID')
    symptom_name = models.CharField(max_length=255, db_column='Symptom_Name')

    class Meta:
        managed = False
        db_table = 'User_Symptoms'


class SearchLogs(models.Model):
    log_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='User_ID')
    searched_word = models.CharField(max_length=255, db_column='Searched_Word')

    class Meta:
        managed = False
        db_table = 'Search_Logs'


class MLRecommendations(models.Model):
    rec_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='User_ID')
    recommended_medicine = models.ForeignKey(Medicines, on_delete=models.CASCADE, db_column='Recommended_Medicine_ID')

    class Meta:
        managed = False
        db_table = 'ML_Recommendations'


class Prescriptions(models.Model):
    prescription_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='User_ID')
    doctor_name = models.CharField(max_length=150, db_column='Doctor_Name')

    class Meta:
        managed = False
        db_table = 'Prescriptions'


class DiscountCards(models.Model):
    card_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='User_ID')
    discount_percent = models.IntegerField(db_column='Discount_Percent')

    class Meta:
        managed = False
        db_table = 'Discount_Cards'


class Suppliers(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=150, db_column='Supplier_Name')

    class Meta:
        managed = False
        db_table = 'Suppliers'


