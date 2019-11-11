import app

try:
    config = app.Config()
    # satis = app.Satis(config)
    # satis.registry_login()
    # satis.image_check_exists()
    # satis.factory_satis()


except Exception as message:
    exit(message)
