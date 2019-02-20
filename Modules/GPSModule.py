def get_gps_module_instance():
    if not _GPSModule._GPSModuleInstance:
        _GPSModule._GPSModuleInstance = _GPSModule()
    return _GPSModule._GPSModuleInstance


class _GPSModule:
    _GPSModuleInstance = None

    def __init__(self):
        # todo: to be implemented
        return
