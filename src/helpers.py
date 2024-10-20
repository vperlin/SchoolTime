def resetting_model(function):
    def function_resetting_model(self, *args, **kwargs):
        self.beginResetModel()
        try:
            return function(self, *args, **kwargs)
        finally:
            self.endResetModel()
    return function_resetting_model
