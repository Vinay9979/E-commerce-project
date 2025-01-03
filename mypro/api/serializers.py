from rest_framework import serializers
from django.contrib.auth.models import User
from client.models import Subcategory,Toy,Category,Billingaddress,Cart
from adminside.models import Categoryphotos

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    increasedPrice = serializers.SerializerMethodField()
    categoryName = serializers.CharField(source='categoryId.categoryName')
    subcategoryName = serializers.CharField(source='subcategoryId.subcategoryName')

    class Meta:
        model = Toy
        fields= ['id','name','img_url','purchasePrice','description','increasedPrice','categoryName','subcategoryName','categoryId','subcategoryId']

    def get_increasedPrice(self,obj):
        return float(obj.purchasePrice)*1.2

    def __init__(self, *args, **kwargs):
        # Access the 'action' from the context passed from the viewset
        request = kwargs.get('context', {}).get('request', None)
        action = kwargs.get('context', {}).get('action', None)  # Get action from context

        if action != 'retrieve':
            # Remove the 'custom_field' if the action is not 'retrieve' (for list actions)
            self.fields.pop('description', None)

        super().__init__(*args, **kwargs)


class CategorySerializer(serializers.ModelSerializer):
    toyCount = serializers.SerializerMethodField()
    posterLink = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','categoryName','toyCount','posterLink']
    
    def get_toyCount(self,obj):
        return Toy.objects.filter(categoryId=obj.id).count()
    
    def get_posterLink(self,obj):
        posterLink = Categoryphotos.objects.filter(category=obj.id)
        print(posterLink)
        if posterLink:
            return posterLink[0].imgUrl
        else:
            return None

class BillingAddressSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    
    class Meta:
        model = Billingaddress
        fields = '__all__'

    def get_address(self,obj):
        address = obj.address.split('->')
        return address
    

class DeliveryaddressSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    
    class Meta:
        model = Billingaddress
        fields = '__all__'

    def get_address(self,obj):
        address = obj.address.split('->')
        return address

class CartSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    imgUrl = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','name','imgUrl','price','quantity','product','subTotal']


    def get_name(self, obj):
        return obj.product.name  

    def get_imgUrl(self, obj):
        return obj.product.img_url

    def get_price(self, obj):
        return obj.product.purchasePrice


class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

# class CartItemsSerializer(serializers.ModelSerializer):
#     cart_items = CartDetailSerializer()
#     total = serializers.DecimalField(max_digits=10,decimal_places=2)
#     # imgUrl = serializers.SerializerMethodField()
#     # price = serializers.SerializerMethodField()
#     class Meta:
#         model = Cart
#         fields = '__all__'


