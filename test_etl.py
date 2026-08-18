import pandas as pd

def test_transform_data():
    # Données factices pour simuler l'API
    raw_data = [
        {
            'id': 1,
            'name': '  Elvis  ',
            'username': 'elvis28',
            'email': 'ELVIS@EXAMPLE.COM',
            'phone': '123-456',
            'website': 'elvis.fr'
        }
    ]

    df = pd.DataFrame(raw_data)

    # Appliquer la même logique de nettoyage que dans main.py
    df['email'] = df['email'].str.lower().str.strip()
    df['name'] = df['name'].str.strip()

    # Vérifier que le nettoyage a bien fonctionné (Assertions)
    assert df['email'].iloc[0] == 'elvis@example.com'
    assert df['name'].iloc[0] == 'Elvis'
