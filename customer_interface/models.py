from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
import datetime

class CustomUser(AbstractUser):
    phone_number = PhoneNumberField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    profile_picture = models.ImageField(default='default.jpg', upload_to="profile_images")


class Orders(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "Pending"
        PROCESSING = "Processing"
        SHIPPED = "Shipped"
        DELIVERED = "Delivered"
        CANCELLED = "Cancelled"
   
    user_id_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now=True)
    order_status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    curr_date = datetime.date.today()
    end_date = curr_date + datetime.timedelta(days=7)
    delivery_date = models.DateField(default=end_date)

    @property
    def price_calculated(self):
        final_price = 0
        order_items = OrderItem.objects.filter(order_id_fk_id=self.id)
        for item in order_items:
            match item.category:
                case "Suit":
                    item_price = 90
                case "Dress":
                    item_price = 50
                case "Coat":
                    item_price  = 70
                case "Jacket":
                    item_price = 65
                case "Shirt":
                    item_price = 35
                case "Trousers":
                    item_price = 40
                case "Skirt":
                    item_price = 35
                case "Jeans":
                    item_price = 45
                case "Sweaters":
                    item_price = 55

            if item.special_instructions != "OTHER":
                final_price = final_price + item_price + 20
            else:
                final_price = final_price + item_price + 50
            
        return final_price

class OrderItem(models.Model):
    class CategoryType(models.TextChoices):
        SUIT = "Suit"
        DRESS = "Dress"
        COAT = "Coat"
        JACKET = "Jacket"
        BLAZER = "Blazer"
        SHIRT = "Shirt"
        TROUSERS = "Trousers"
        SKIRT = "Skirt"
        JEANS = "Jeans"
        SWEATER = "Sweaters"

    class SpecialInstructions(models.TextChoices):
        STAIN_REMOVAL = "Stain Removal"
        STARCH_SHIRTS = "Starch Shirts"
        DELICATES_HAND_WASH = "DELICATES HAND WASH"
        NEXT_DAY_SERVICE = "NEXT DAY SERVICE"
        OTHER = "OTHER"

    class ServiceType(models.TextChoices):
        DRY = "Dry Cleaning"
        WASH = "Wash and Dry"
    
    order_id_fk = models.ForeignKey(Orders, on_delete=models.CASCADE)
    service_type = models.CharField(
        choices=ServiceType.choices,
        default= ServiceType.WASH
    )
    
    special_instructions = models.CharField(
        choices=SpecialInstructions.choices,
        default=SpecialInstructions.OTHER
    )
    
    category = models.CharField(
        choices=CategoryType.choices,
        default=CategoryType.SHIRT
    )
    
    optional_instructions = models.TextField(blank=True, default="N/A")
    

class Sales(models.Model):
    class SalesStatus(models.TextChoices):
        FAILED = "Failed"
        SUCCESS = "Success"
        REVERSED = "Reversed"

    class SalesType(models.TextChoices):
        DEBIT = "DR"
        CREDIT = "CR"
    
    order_id_fk = models.ForeignKey(Orders, on_delete=models.CASCADE)
    status = models.CharField(
        choices=SalesStatus.choices,
        default=SalesStatus.SUCCESS
    )
    type = models.CharField(
        choices=SalesType.choices,
        default=SalesType.CREDIT
    )