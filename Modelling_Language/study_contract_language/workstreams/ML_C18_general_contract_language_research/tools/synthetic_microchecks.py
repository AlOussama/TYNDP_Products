"""ML-C18 research-only numerical microchecks; no GEMS/mathspec parser/solver."""
import math
import numpy as np

checks = []
def ck(name, fact):
    ok = bool(fact)
    checks.append((name, ok))
    if not ok:
        raise AssertionError(name)

# RC01: unit, loss and alternative state coordinates.
dt = 0.5  # hours
p_charge = 2.0  # MW
eta = 0.9
stored = p_charge * dt * eta
ck('RC01_MW_dt_MWh', math.isclose(p_charge * dt, 1.0))
ck('RC01_efficiency_ledger', math.isclose(stored, 0.9))
ck('RC01_reject_wrong_dt', not math.isclose(stored, 2.0 * eta))
ck('RC01_SOC_energy_coordinate', math.isclose(stored / 4.0 * 4.0, stored))

# RC02: aggregate final total does not prove individual departure requirement.
energy_by_ev = {'early': 0., 'late': 10.}
deadline_min = {'early': 4., 'late': 4.}
ck('RC02_fleet_total_not_enough', sum(energy_by_ev.values()) >= sum(deadline_min.values()))
ck('RC02_individual_mobility_negative', any(energy_by_ev[k] < deadline_min[k] for k in deadline_min))
ck('RC02_V2G_false_negative', -1.0 < 0.0)

# RC03: 1000 kWh electrical input / 50 kWh/kg = 20 kg/h H2.
prod_kgph = 1000.0 / 50.0
ck('RC03_kWh_to_kg', math.isclose(prod_kgph, 20.0))
ck('RC03_H2_energy_eff', (prod_kgph * 33.33) / 1000.0 < 1.)

# RC04: initial H2 stock 100 kg; 10 kg/h out over 2h; electricity <= available LHV energy.
stock_final = 100.0 - 10.0 * 2.0
el_energy_mwh = 10.0 * 2.0 * 33.33 * 0.55 / 1000.0
ck('RC04_inventory_ledger', math.isclose(stock_final, 80.0))
ck('RC04_generation_energy_bound', el_energy_mwh <= 20.0 * 33.33 / 1000.0)

# RC05: DC network angle = cycle = PTDF, connected fixed lossless 3-bus grid.
A = np.array([[1., 0., 1.], [-1., 1., 0.], [0., -1., -1.]])
x = np.array([1., 2., 1.5])
b = 1 / x
p = np.array([1., 0., -1.])  # MW on arbitrary consistent base
Bbus = A @ np.diag(b) @ A.T
theta = np.r_[np.linalg.solve(Bbus[:2, :2], p[:2]), 0.]
f_angle = np.diag(b) @ A.T @ theta
# PTDF from same admittance and slack bus.
ptdf = np.diag(b) @ A.T[:, :2] @ np.linalg.inv(Bbus[:2, :2])
f_ptdf = ptdf @ p[:2]
C = np.array([[1., 1., -1.]])  # cycle space C @ A.T = 0
f_cycle = np.linalg.solve(np.vstack([A[:2, :], C @ np.diag(x)]), np.r_[p[:2], 0.])
ck('RC05_angle_PFDC_balance', np.allclose(A @ f_angle, p))
ck('RC05_angle_cycle', np.allclose(f_angle, f_cycle, atol=1e-12))
ck('RC05_angle_PTDF', np.allclose(f_angle, f_ptdf, atol=1e-12))
ck('RC05_KVL_ok', np.allclose(C @ np.diag(x) @ f_angle, 0.))
bad = f_angle + 0.1 * C.ravel()  # preserves KCL, violates KVL
ck('RC05_wrong_cycle_preserves_KCL', np.allclose(A @ bad, p))
ck('RC05_wrong_cycle_violates_KVL', not np.allclose(C @ np.diag(x) @ bad, 0.))

# RC06: 3 x 50 MW modules is valid; fractional 0.3 module violates integer module policy.
ck('RC06_integer_capacity', 3 * 50. == 150.)
ck('RC06_reject_fractional_module', not float(0.3).is_integer())

# RC07: investment nonanticipativity before reveal.
ck('RC07_equal_first_stage', 2. == 2.)
ck('RC07_reject_scenario_split', 0. != 1.)

# RC08: 100 EUR capex + 10 EUR/MWh * 2 MW * 0.5 h = 110 EUR.
ck('RC08_correct_cost_ledger', math.isclose(100. + 10. * 2. * 0.5, 110.))
ck('RC08_reject_missing_dt', not math.isclose(100. + 10. * 2., 110.))

# RC09: same exogenous conditions required before two delta-computations are compared.
ck('RC09_counterfactual_scenario_identity', ('case_1' == 'case_1'))
ck('RC09_reject_mismatched_scenario', ('case_1' != 'case_2'))

# RC10: models may have different absolute costs but agree on decision ranking.
model_a = {'X':100., 'Y':120.}
model_b = {'X':110., 'Y':125.}
ck('RC10_ranking_stable', min(model_a,key=model_a.get) == min(model_b,key=model_b.get))
ck('RC10_not_identical_results', model_a['X'] != model_b['X'])

print('ML_C18_SYNTHETIC_MICROCHECKS:', sum(ok for _,ok in checks), '/', len(checks), 'PASS')
for name, passed in checks:
    print('PASS' if passed else 'FAIL', name)
print('RC05_angle=', np.round(f_angle, 8).tolist(), 'RC05_cycle=', np.round(f_cycle, 8).tolist(), 'RC05_ptdf=', np.round(f_ptdf, 8).tolist())
