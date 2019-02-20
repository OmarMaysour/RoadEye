def get_accelerometer_module_instance():
    if not _AccelerometerModule._AccelerometerModuleInstance:
        _AccelerometerModule._AccelerometerModuleInstance = _AccelerometerModule()
    return _AccelerometerModule._AccelerometerModuleInstance


class _AccelerometerModule:
    _AccelerometerModuleInstance = None

    def __init__(self):
        # todo: to be implemented
        return
