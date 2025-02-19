from django.urls import path
from . import views

urlpatterns = [
 path('checklogin',views.checklogin,name='checklogin'),
 path('login/',views.login,name='login'),
 path('logout/',views.logout,name='logout'),
 path('index/',views.index,name="index"),
 path('addtoy/',views.addtoy,name='addtoy'),
 path('storetoy/',views.storetoy,name='storetoy'),
 path('showtoys/',views.showtoys,name='showtoys'),
 path('searchtoy/',views.searchtoy,name='searchtoy'),
 path('updatetoy/<int:id>',views.updatetoy,name='updatetoy'),
 path('deletetoy/<int:id>/',views.deletetoy,name='deletetoy'),
 path('addcategory/',views.addcategory,name='addcategory'),
 path('deletecategory/',views.deletecategory,name='deletecategory'),
 path('deletesubcategory/',views.deletesubcategory,name='deletesubcategory'),
 path('storecategory/',views.storecategory,name='storecategory'),
 path('edittoy/<int:id>',views.edittoy,name='edittoy'),
 path('storesubcategory/',views.storesubcategory,name='storesubcategory'),
 path('showcategory/',views.showcategory,name='showcategory'),
 path('showsubcategory/',views.showsubcategory,name='showsubcategory'),
 path('manageorders/',views.manageorders,name='manageorders'),
 path('showusers/',views.showusers,name='showusers'),
 path('edituser/',views.edituser,name='edituser'),
 path('addstore/',views.addstore,name="addstore"),
 path('showstores/',views.showstores,name='showstores'),
 path('storestore/',views.storestore,name='storestore'),
 path('addmanufacturer/',views.addmanufacturer,name='addmanufacturer'),
 path('storemanufacturer',views.storemanufacturer,name='storemanufacturer'),
 path('searchcategory/',views.searchcategory,name='searchcategory'),
 path('deletestore/<int:id>',views.deletestore,name='deletestore'),
 path('updatestore/<int:id>',views.updatestore,name='updatestore'),
 path('searchstore/',views.searchstore,name='searchstore'),
 path('showmanufacturers/',views.showmanufacturers,name='showmanufacturers'),
 path('searchmanufacturer/',views.searchmanufacturer,name='searchmanufacturer'),
 path('updatemanufacturer/<int:id>',views.updatemanufacturer,name='updatemanufacturer'),
 path('deletemanufacturer/<int:id>',views.deletemanufacturer,name='deletemanufacturer'),
 path('updatecategory/<int:id>',views.updatecategory,name='updatecategory'),
 path('updatesubcategory/<int:id>',views.updatesubcategory,name='updatesubcategory'),
 path('addcatphoto/',views.addcatphoto,name='addcatphoto'),
 path('storecatphoto/',views.storecatphoto,name='storecatphoto'),
 path('deleteorder/<int:id>',views.deleteorder,name='deleteorder'),
 path('orderdetails/<int:id>',views.editorder,name='editorder'),


]