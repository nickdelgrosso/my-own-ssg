# Themes

This is where the general templates for your site goes.  A site only needs one theme, but having support multiple makes it easy to switch themes in the future.  

Requirements:
  - Use [jinja2's Template Designer](https://jinja.palletsprojects.com/en/3.1.x/templates/) syntax for the templates.
  - Every template should have a corresponding file or folder in the `content/` folder:
    - Example: `theme/mytheme/index.html` should also have a `content/index.md`
    - Example: `theme/mytheme/page.html` could have a `content/page/xxx.md`  (if it's a folder of content files, it doesn't matter what the individual files are named.)