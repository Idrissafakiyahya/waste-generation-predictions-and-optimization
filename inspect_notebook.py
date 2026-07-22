import json
from pathlib import Path
nb_path = Path('waste_prediction_model_best (1).ipynb')
nb = json.loads(nb_path.read_text(encoding='utf-8'))
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])
    if any(k in src for k in ['LabelEncoder','Timestamp','fit(','X_train','XGBClassifier','LGBMClassifier','RandomForestClassifier','pickle','dump','feature']):
        print('---CELL---')
        print(i)
        print(src)
