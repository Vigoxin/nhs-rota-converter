import os
import json
import importlib

basedir = os.path.abspath(os.path.dirname(__file__))

def get_dirs(path='.'):
    dirs = next(os.walk(path))[1]
    drs_to_remove = ['__pycache__']
    for dr in drs_to_remove:
        if dr in dirs: dirs.remove(dr)
    return dirs

def get_files(path='.'):
    files = next(os.walk(path))[2]
    files_to_remove = ['.DS_Store']
    for file in files_to_remove:
        if file in files: files.remove(file)
    return list(map(lambda x: os.path.splitext(x)[0], files))

rotas = {}

for hosp in get_dirs():
    rotas[hosp] = {}
    for specialty in get_dirs(hosp):
        rotas[hosp][specialty] = {}
        rota = rotas[hosp][specialty]
        
        # imports converter function
        module = importlib.import_module(f'{hosp}.{specialty}.rota_to_csv', basedir)
        function = module.convert
        rota['converter'] = function
        rota['converter'] = 'function'

        # imports image path
        rota['img'] = f'./{hosp}/{specialty}/img.jpg'

rotas['nice_name_dict'] = {
    'ashford_kent': 'William Harvey Hospital, Ashford, Kent',
    'brighton': 'Brighton',
    'medicine': 'Medicine',
    'surgery': 'Surgery'
}

if __name__ == '__main__':
    print(json.dumps(rotas, indent=6))