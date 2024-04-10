class MyDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'drugInfo':
            return 'mongodb'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'drugInfo':
            return 'mongodb'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
         if obj1._meta.app_label == 'drugInfo' or obj2._meta.app_label == 'drugInfo':
            return True
            return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
        if app_label == 'drugInfo':
            return db == 'mongodb'
        return None
