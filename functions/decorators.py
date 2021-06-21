from PyQt5.QtWidgets import QMessageBox


def track_error(func):
    def wrapper(self):
        try:
            func(self)
        except Exception as e:
            QMessageBox.information(self, 'Test Error', str(e), QMessageBox.Yes)
    return wrapper


def track_error_args(func):
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            QMessageBox.information(self, 'Test Error', str(e), QMessageBox.Yes)
    return wrapper


def finished_reminder(func):
    def wrapper(self):
        func(self)
        QMessageBox.information(self, 'Finished', 'Task finished.', QMessageBox.Yes)
    return wrapper


def finished_reminder_new(win_title, info):
    def deco_func(func):
        def wrapper(self):
            func(self)
            QMessageBox.information(self, win_title, info, QMessageBox.Yes)
        return wrapper
    return deco_func()


def not_finished_yet(func):
    def wrapper(self):
        func(self)
        QMessageBox.information(self, 'Information', 'NOT FINISHED YET...', QMessageBox.Yes)
    return wrapper
