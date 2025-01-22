from rest_framework import serializers
from django.contrib.auth.models import User
from client.models import Subcategory,Toy,Category,Billingaddress,Cart
from rest_framework.authtoken.models import Token
from adminside.models import Categoryphotos
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class userDetailSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 100)
    password = serializers.CharField(max_length = 100)

    def validate(self,data):
            if User.objects.filter(username = data['username']).exists():
                raise ValidationError({"Details":"username already exists","username":data['username'],'password':data['password']})
            else:
                try:
                    validate_password(password=data['password'])
                    return data
                except ValidationError as e:
                    raise ValidationError({'username':data['username'],'password':data['password'],'details':e.messages})

    def create(self, validated_data):
       user =  User.objects.create_user(username = validated_data['username'],password = validated_data['password'])
       return  user
    
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
        fields = ['id','name','img_url','purchasePrice','description','categoryName','subcategoryName','increasedPrice']

    def get_increasedPrice(self,obj):
        return float(obj.purchasePrice)*1.2

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

# class CartSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()
#     imgUrl = serializers.SerializerMethodField()
#     price = serializers.SerializerMethodField()
#     class Meta:
#         model = Cart
#         fields = ['id','name','imgUrl','price','quantity','product','subTotal']


#     def get_name(self, obj):
#         return obj.product.name  

#     def get_imgUrl(self, obj):
#         return obj.product.img_url

#     def get_price(self, obj):
#         return obj.product.purchasePrice


class CartDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['product','sub_total']

    
    def get_sub_total(self,obj):
        return obj.product.purchasePrice * obj.quantity
        
class CartSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=10,decimal_places=2)
    cart_items = CartDetailSerializer(many=True)

    class meta:
        fields = ['cart_items','total','quantity']
    
   
   

