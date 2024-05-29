from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


# TODO: Reservation app under dev after users done


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("hall.urls")),
    path("api/", include("movies.urls")),
    path("api/", include("reservation.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
