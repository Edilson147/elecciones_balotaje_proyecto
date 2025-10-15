import numpy as np

# Parámetros por defecto (puedes sobreescribir vía POST /simular)
default_params = dict(
    n_trials=20000,
    margen_error=0.03,
    p_indecisos_a=0.55,
    p_indecisos_b=0.45,
)

def _clip01(x):
    return np.maximum(0.0, np.minimum(1.0, x))

def _perturb(p, me, rng, size):
    ruido = rng.normal(0.0, me, size=size)
    return np.clip(p * (1.0 + ruido), 0.0, 1.0)

def _observed_shares_from_db(conn):
    """
    Lee SOLO el agregado necesario sin pandas.
    Devuelve dict con proporciones de A, B, Blanco, Nulo, Indeciso.
    """
    with conn.cursor() as cur:
        # alias para no depender de 'COUNT(*)'
        cur.execute("""
            SELECT intencion_1v AS v, COUNT(*) AS c
            FROM encuestas
            GROUP BY intencion_1v
        """)
        rows = cur.fetchall()

    # PyMySQL con DictCursor => filas tipo {'v': 'A', 'c': 12}
    counts = {}
    total = 0
    for r in rows:
        key = (r.get('v') or '')
        cnt = int(r.get('c') or 0)
        counts[key] = counts.get(key, 0) + cnt
        total += cnt

    N = total if total > 0 else 1
    get = lambda k: counts.get(k, 0) / N
    return dict(
        A=get('A'),
        B=get('B'),
        Blanco=get('Blanco'),
        Nulo=get('Nulo'),
        Indeciso=get('Indeciso'),
    )

def run_simulation_from_db(conn_factory,
                           n_trials=20000,
                           margen_error=0.03,
                           p_indecisos_a=0.55,
                           p_indecisos_b=0.45):
    rng = np.random.default_rng(42)

    # 1) Cargar shares observados (agregado) desde MySQL
    conn = conn_factory()
    with conn:
        shares = _observed_shares_from_db(conn)

    # Normalizar por seguridad
    total = sum(shares.values())
    if total > 0:
        shares = {k: v / total for k, v in shares.items()}
    else:
        shares = {k: 0.0 for k in ['A','B','Blanco','Nulo','Indeciso']}

    # 2) Monte Carlo
    n = int(n_trials)
    me = float(margen_error)

    pA  = _perturb(shares['A'],      me, rng, n)
    pB  = _perturb(shares['B'],      me, rng, n)
    pBl = _perturb(shares['Blanco'], me, rng, n)
    pNu = _perturb(shares['Nulo'],   me, rng, n)

    # Reajuste por consistencia (indecisos = 1 - sum)
    pInd = _clip01(1.0 - (pA + pB + pBl + pNu))

    # Redistribución de indecisos para 2da vuelta
    indA = pInd * float(p_indecisos_a)
    indB = pInd * float(p_indecisos_b)

    # Totales “válidos” del balotaje (excluye blancos/nulos del denominador)
    totA = pA + indA
    totB = pB + indB
    den  = np.maximum(1e-9, totA + totB)

    shareA = totA / den
    shareB = totB / den

    ganaA  = (shareA > shareB).mean()
    ganaB  = (shareB > shareA).mean()
    empate = (np.abs(shareA - shareB) < 1e-9).mean()

    return dict(
        entradas=dict(observado=shares),  # proporciones observadas
        parametros=dict(
            n_trials=n,
            margen_error=me,
            p_indecisos_a=float(p_indecisos_a),
            p_indecisos_b=float(p_indecisos_b),
        ),
        balotaje=dict(
            prob_gana_A=float(ganaA),
            prob_gana_B=float(ganaB),
            prob_empate=float(empate),
            media_share_A=float(shareA.mean()),
            media_share_B=float(shareB.mean()),
            p5_A=float(np.percentile(shareA, 5)),
            p95_A=float(np.percentile(shareA, 95)),
            p5_B=float(np.percentile(shareB, 5)),
            p95_B=float(np.percentile(shareB, 95)),
        ),
    )
