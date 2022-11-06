










# class EmployeeSerializer(serializers.ModelSerializer):
#     owner = UserPublicSerializer(source='user', read_only=True)
#
#     title = serializers.CharField(validators=[validators.validate_title_no_hello, validators.unique_product_title])
#     body = serializers.CharField(source='content')
#     class Meta:
#         model = Product
#         fields = [
#             'owner',
#             'pk',
#             'title',
#             'body',
#             'price',
#             'sale_price',
#             'public',
#             'path',
#             'endpoint',
#         ]