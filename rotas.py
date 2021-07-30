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
    'canterbury': 'Canterbury - Kent and Canterbury Hospital',
    'brighton': 'Brighton - Royal Sussex County Hospital',
    'oxford': 'Oxford - John Radcliffe Hospital',
    'frimley': 'Frimley - Frimley Park Hospital',
    'gstt': "London - Guy's and St Thomas' Trust",
    'stgeorges': "London - St George's Hospital, Tooting",
    'woolwich': "London - Queen Elizabeth Hospital, Woolwich",
    'ashford_st_peters': "Ashford and St Peter's Trust, Chertsey",
    "lewisham": "London - Lewisham Hospital",
    "cardiff": "Cardiff - UHW / UHL",
    "forth_valley_royal": "Scotland - Forth Valley Royal Hospital, Larbert",
    "pruh": "London - Princess Royal University Hospital, Orpington",
    "colchester": "Colchester - Colchester General Hospital",

    'medicine': 'Medicine',
    "general_medicine": "General Medicine",
    'medicine-coe': "Medicine and Care of the Elderly",
    'medicine-hcoop': 'Medicine and HCOOP',
    'medicine_fy1': "Medicine (FY1 only)",
    'respiratory': 'Respiratory Medicine',
    'surgery': 'Surgery',
    'gensurg': 'General Surgery',
    'surgical_fy1': 'FY1 - Surgery only',
    'paediatrics': 'Paediatrics',
    'urovasc': 'Urology and Vascular surgery',
    'gastro': 'Gastroenterology',
    'cardio_sho': 'Cardiology (SHO/FY2/CMT only)',
    'medicine_sho': 'Medicine (SHO/FY2/CMT only)',
    'emergency_medicine': 'Emergency Medicine',
    'aande': 'Accident and Emergency',
    'aande_sho': 'Accident and Emergency (SHO)',
    'itu': "ITU"
}

nice_name_dict_reversed = {v: k for k, v in nice_name_dict.items()}


if __name__ == '__main__':
    print(json.dumps(rotas, indent=4))
    print(json.dumps(nice_name_dict, indent=4))
    print(json.dumps(nice_name_dict_reversed, indent=4))