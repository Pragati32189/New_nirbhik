from django.urls import path
from .views import SignupView, SigninView, GetAllUserTokensView, GetUserLocationsView, PostUserLocationView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('get-all-tokens/', GetAllUserTokensView.as_view(), name='get_all_tokens'),  # New route for all users' tokens
    path('post-location/', PostUserLocationView.as_view(), name='post_location'),
    path('get-locations/', GetUserLocationsView.as_view(), name='get_locations'),

]