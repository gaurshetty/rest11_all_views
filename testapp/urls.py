from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter
routerviewset = DefaultRouter()
routerviewset.register('', views.EmployeeViewset, basename='articleviewset')
routerviewset = SimpleRouter()
routerviewset.register('', views.EmployeeGenericViewSet, basename='Employeeviewset')
routers = DefaultRouter()
routers.register('', views.EmployeeCBViewSet)

urlpatterns = [
    # --------------------------------------------------------------
    # Normal FBV
    # --------------------------------------------------------------
    path('fbv/', views.employeeview),
    path('fbv/<int:id>/', views.employeedetailview),
    # --------------------------------------------------------------
    # decorator FBV
    # --------------------------------------------------------------
    path('decofbv/', views.employeedecoAPIView),
    path('decofbv/<int:id>/', views.employeedetaildecoAPIView),
    # -----------------------------------------------------
    # APIViews_CBV
    # -----------------------------------------------------
    path('APIViewsCBV/', views.EmployeeAPIView.as_view()),
    path('APIViewsCBV/<int:id>/', views.EmployeeDetailAPIView.as_view()),
    # --------------------------------------------------------------
    # Generic_APIViews_CBV
    # --------------------------------------------------------------
    path('genericAPIViewsCBV/', views.EmployeeListCreateAPIView.as_view()),
    path('genericAPIViewsCBV/<int:id>/', views.EmployeeRetrieveUpdateDestroyAPIView.as_view()),
    # --------------------------------------------------------------
    # Generic_APIViews_CBV_mixins
    # --------------------------------------------------------------
    path('genAPIViewsCBVMixin/', views.EmployeeListCreateModelMixin.as_view()),
    path('genAPIViewsCBVMixin/<int:pk>/', views.EmployeeRetrieveUpdateDistroyModelMixin.as_view()),
    # --------------------------------------------------------------
    # ViewSet
    # --------------------------------------------------------------
    path('viewset/', include(routerviewset.urls)),
    # --------------------------------------------------------------
    # ViewSet_modelmixins
    # --------------------------------------------------------------
    path('ViewSetMixins/', include(routerviewset.urls)),
    # --------------------------------------------------------------
    # ModelViewSet
    # --------------------------------------------------------------
    path('ModelViewSet/', include(routers.urls))
]
