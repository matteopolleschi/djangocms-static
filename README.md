# djangocms-static

__Static sites generator for Django CMS.__

This add-on saves a static copy of your Django CMS site in the file system so you can upload it to a server.

_This repo is in an early development stage. The current setup has been tested and requires Django CMS 3.8_

## How to test the add-on

1. Install the package `djangocms-static-0.1.tar.gz` into your Django CMS setup (single site).
1. Add `djangocms_static` to your installed apps.

```
INSTALLED_APPS = [
    'djangocms_static',
    ...
]
```

1. Add the static urls to your project `urls.py`:

```
urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path("static_generator/", include('djangocms_static.urls')),
]
```

You are ready to go. On the Django CMS admin you will see an additional button with the label `Create static site`.

## Customization

By default, the add-on saves the static HTMLs in a directory called static_files on the Django project's root directory.

You can change the location of the output HTMLs by adding the following line to your `settings.py`.

    STATIC_STORAGE_PATH = '/full/path/to/your/directory'
