Developing a Python Pandas lesson with astrophys examples

Brain storming doc:

https://docs.google.com/document/d/1oA3D09GjzUnX2XRH-XCJ_X7g7fFEozJbt5hINTNv1qs/edit

To deploy on webserver with apache2 installed:

first follow the setup here:
https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/

on the webserver then run:

```bash
sudo bundle exec jekyll build --destination /var/www/html
```
