import os
import json
import importlib

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

basedir = os.path.abspath(os.path.dirname(__file__))
rotas_dir = f'{basedir}/static/rotas'


rotas = {}

for hosp in [el for el in get_dirs(rotas_dir) if el != 'template_form_fields']:
    rotas[hosp] = {}
    for specialty in get_dirs(f'{rotas_dir}/{hosp}'):
        rotas[hosp][specialty] = {}
        rota = rotas[hosp][specialty]
        
        # imports converter function
        module = importlib.import_module(f'static.rotas.{hosp}.{specialty}.rota_to_csv', '.')
        function = module.convert
        rota['converter'] = function
        # rota['converter'] = 'function'

        # imports image path
        rota['img'] = f'/static/rotas/{hosp}/{specialty}/rota_screenshot.png'

nice_name_dict = {
    'ashford_kent': 'Ashford, Kent - William Harvey Hospital',
    'canterbury': 'Kent and Canterbury Hospital',
    'brighton': 'Brighton - Royal Sussex County Hospital',
    'oxford': 'Oxford - John Radcliffe Hospital',
    'frimley': 'Frimley - Frimley Park Hospital',

    'medicine': 'Medicine',
    'medicine-hcoop': 'Medicine and HCOOP',
    'respiratory': 'Respiratory Medicine',
    'surgery': 'Surgery',
    'gensurg': 'General Surgery',
    'paediatrics': 'Paediatrics',
    'urovasc': 'Urology and Vascular surgery',
    'gastro': 'Gastroenterology'
}

nice_name_dict_reversed = {v: k for k, v in nice_name_dict.items()}


if __name__ == '__main__':
    print(json.dumps(rotas, indent=4))
    print(json.dumps(nice_name_dict, indent=4))
    print(json.dumps(nice_name_dict_reversed, indent=4))