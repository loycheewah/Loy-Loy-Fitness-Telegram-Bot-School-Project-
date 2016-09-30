# Loy-Loy-Fitness-Telegram-Bot-School-Project-


# To Host App on Heroku
Deploy to heroic via GitHub

heroku buildpacks:add https://github.com/stomita/heroku-buildpack-phantomjs —app APP_NAME_IN_HEROKU

heroku ps:scale —app APP_NAME_IN_HEROKU worker=1