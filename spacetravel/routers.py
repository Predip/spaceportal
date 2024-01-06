class SpaceTravelRouter:
    """
    A router to control database operations for the News model.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read News models go to the 'neo' database.
        """
        if model._meta.app_label == 'spacetravel' and model._meta.model_name == 'news':
            return 'news'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the 'neo' database.
        """
        if obj1._state.db == 'news' and obj2._state.db == 'news':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the 'news' app only appears in the 'neo' database.
        """
        if app_label == 'spacetravel' and model_name == 'news':
            return db == 'news'
        return None
