Message translates guide:
    Generate messages: pybabel extract webApps/ -o webApps/bot/locales/messages.pot
    Then: pybabel init -i webApps/bot/locales/messages.pot -d webApps/bot/locales -D messages -l en
    Then translate messages
    Then: pybabel compile -d webApps/bot/locales -D messages


Project Deployment:
    Fill out the sample.env file, then rename it to .env
    Then write in terminal: docker-compose up -d --build