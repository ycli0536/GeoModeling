from PyQt5.QtCore import QSettings


def get_setting_values(module_name, variable_names):
    setting = QSettings('DL inv software', 'config')
    variables = []
    for i in range(len(variable_names)):
        variables.append(setting.value('%s/%s' % (module_name, variable_names[i])))
    return variables


def set_setting_values(module_name, variable_names, variables):
    setting = QSettings('DL inv software', 'config')
    assert len(variable_names) == len(variables)
    for i in range(len(variable_names)):
        setting.setValue('%s/%s' % (module_name, variable_names[i]), variables[i])
