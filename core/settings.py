
class Settings(object):

    def __init__(self):
        super().__init__()
        self._s = self.__load()

    def __load(self):

        from util.files import read_yaml, write_yaml, get_files
        from util.locations import get_locations, make_locations
        from util.structures import yaml_loc_join, yaml_str_join, dict_merge

        files = get_files()
        res = {
            'locations': get_locations(),
            'files': files
        }

        d = read_yaml(files['defaults'], add_constructor=[('!loc_join', yaml_loc_join,), ('!str_join', yaml_str_join,),])
        if d: res = dict_merge(res, d)

        make_locations()

        c = read_yaml(files['config'], add_constructor=('!loc_join', yaml_loc_join,))
        if c: return dict_merge(res, c)
        if c != res: write_yaml(files['config'], res)

    def get(self):
        return self._s
