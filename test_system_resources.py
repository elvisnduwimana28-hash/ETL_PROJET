import psutil

def test_check_system_resources():
    # Mesurer l'utilisation de la mémoire RAM en pourcentage
    memory_usage = psutil.virtual_memory().percent
    print(f"Utilisation actuelle de la RAM : {memory_usage}%")

    # Mesurer l'utilisation globale du CPU (échantillon sur 1 seconde)
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"Utilisation actuelle du CPU : {cpu_usage}%")

    # Assertions : On vérifie que la RAM n'est pas saturée à plus de 90%
    assert memory_usage < 90.0, fitaire critique de la RAM : {memory_usage}%"
    
    # On peut aussi s'assurer que les valeurs retournées sont valides
    assert 0 <= cpu_usage <= 100
    assert 0 <= memory_usage <= 100
