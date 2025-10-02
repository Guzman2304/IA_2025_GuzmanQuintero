import numpy as np # type: ignore
import random

# Lista de equipos y sus ratings Elo aproximados (basados en GPR octubre 2025)
teams_elo = {
    'Gen.G': 1627,
    'Hanwha Life Esports': 1569,
    'T1': 1538,
    'KT Rolster': 1480,
    "Anyone's Legend": 1508,
    'Bilibili Gaming': 1402,
    'Top Esports': 1396,
    'Invictus Gaming': 1350,
    'G2 Esports': 1450,
    'Movistar KOI': 1420,
    'Fnatic': 1350,
    'FlyQuest': 1420,
    'Vivo Keyd Stars': 1250,
    '100 Thieves': 1300,
    'CTBC Flying Oyster': 1350,
    'Team Secret Whales': 1250,
    'PSG Talon': 1300
}

teams = list(teams_elo.keys())
n_teams = len(teams)

# Función para probabilidad de victoria
def win_prob(elo1, elo2):
    return 1 / (1 + 10**((elo2 - elo1) / 400))

# Simular un torneo round-robin
def simulate_tournament():
    wins = {team: 0 for team in teams}
    for i in range(n_teams):
        for j in range(i+1, n_teams):
            team1 = teams[i]
            team2 = teams[j]
            elo1 = teams_elo[team1]
            elo2 = teams_elo[team2]
            if random.random() < win_prob(elo1, elo2):
                wins[team1] += 1
            else:
                wins[team2] += 1
    # Ordenar por victorias (top 3)
    sorted_teams = sorted(wins.items(), key=lambda x: x[1], reverse=True)
    return [team for team, _ in sorted_teams[:3]]

# Ejecutar simulaciones
n_sim = 10000
top3_counts = {team: 0 for team in teams}

for _ in range(n_sim):
    top3 = simulate_tournament()
    for team in top3:
        top3_counts[team] += 1

# Resultados
sorted_top3 = sorted(top3_counts.items(), key=lambda x: x[1], reverse=True)
print("Predicción top 3 (frecuencia en simulaciones):")
for i, (team, count) in enumerate(sorted_top3[:3], 1):
    prob = count / n_sim * 100
    print(f"{i}. {team}: {count} veces ({prob:.1f}%)")