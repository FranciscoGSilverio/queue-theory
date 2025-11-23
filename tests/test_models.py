import pytest
from calculator import calculate

def test_mm1_stable():
    """
    Exercise:
    Lambda = 10
    Mu = 15
    
    Expected:
    rho = 0.6667
    P0 = 0.3333
    L = 2.0
    Lq = 1.3333
    W = 0.2
    Wq = 0.1333
    """
    result = calculate("M/M/1", lmbda=10, mu=15)
    
    assert result["rho"] == pytest.approx(2/3, abs=1e-4)
    assert result["p0"] == pytest.approx(1/3, abs=1e-4)
    assert result["L"] == pytest.approx(2.0, abs=1e-4)
    assert result["Lq"] == pytest.approx(4/3, abs=1e-4)
    assert result["W"] == pytest.approx(0.2, abs=1e-4)
    assert result["Wq"] == pytest.approx(2/15, abs=1e-4)

def test_mm1_unstable():
    with pytest.raises(ValueError, match="Sistema instavel"):
        calculate("M/M/1", lmbda=20, mu=15)

def test_mms_stable():
    """
    Exercise:
    Lambda = 20
    Mu = 12
    s = 3
    
    Expected (approx):
    rho = 0.5556
    P0 = 0.1727
    Lq = 0.3746
    L = 2.0413
    Wq = 0.0187
    W = 0.1021
    """
    result = calculate("M/M/S", lmbda=20, mu=12, s=3)
    
    assert result["rho"] == pytest.approx(5/9, abs=1e-4)
    assert result["p0"] == pytest.approx(0.1727, abs=1e-3) 
    assert result["Lq"] == pytest.approx(0.3746, abs=1e-3)
    assert result["L"] == pytest.approx(2.0413, abs=1e-3)
    assert result["Wq"] == pytest.approx(0.0187, abs=1e-3)
    assert result["W"] == pytest.approx(0.1021, abs=1e-3)

def test_mms_unstable():
    with pytest.raises(ValueError, match="Sistema instavel"):
        calculate("M/M/S", lmbda=40, mu=12, s=3)

def test_mm1k_finite_capacity():
    """
    Exercise:
    Lambda = 1
    Mu = 2
    K = 2
    
    Expected:
    rho = 0.5
    P0 = 4/7 (~0.5714)
    L = 4/7 (~0.5714)
    lambda_eff = 6/7 (~0.8571)
    W = 2/3 (~0.6667)
    """
    result = calculate("M/M/1/K", lmbda=1, mu=2, K=2)
    
    assert result["rho"] == 0.5
    assert result["p0"] == pytest.approx(4/7, abs=1e-4)
    assert result["L"] == pytest.approx(4/7, abs=1e-4)
    assert result["lambda_eff"] == pytest.approx(6/7, abs=1e-4)
    assert result["W"] == pytest.approx(2/3, abs=1e-4)

def test_mm1n_finite_population():
    """
    Exercise:
    Lambda = 1 (per source)
    Mu = 2
    N = 2
    
    Expected:
    P0 = 4/9 (~0.4444)
    L = 2/3 (~0.6667)
    lambda_eff = 4/3 (~1.3333)
    W = 0.5
    """
    result = calculate("M/M/1/N", lmbda=1, mu=2, N=2)
    
    assert result["p0"] == pytest.approx(4/9, abs=1e-4)
    assert result["L"] == pytest.approx(2/3, abs=1e-4)
    assert result["lambda_eff"] == pytest.approx(4/3, abs=1e-4)
    assert result["W"] == pytest.approx(0.5, abs=1e-4)

def test_mg1_deterministic():
    """
    Exercise:
    Lambda = 3
    Mu = 4
    Distribution = deterministic (sigma=0)
    
    Expected:
    rho = 0.75
    Lq = 1.125
    L = 1.875
    Wq = 0.375
    W = 0.625
    """
    result = calculate("M/G/1", lmbda=3, mu=4, service_distribution="deterministic")
    
    assert result["rho"] == 0.75
    assert result["Lq"] == pytest.approx(1.125, abs=1e-4)
    assert result["L"] == pytest.approx(1.875, abs=1e-4)
    assert result["Wq"] == pytest.approx(0.375, abs=1e-4)
    assert result["W"] == pytest.approx(0.625, abs=1e-4)

def test_priority_non_preemptive():
    """
    Exercise:
    Lambda1 = 2, Lambda2 = 1
    Mu = 5
    
    Expected:
    rho1 = 0.4, rho2 = 0.2, rho_total = 0.6
    Wq1 = 0.2
    Wq2 = 0.5
    """
    # Note: The calculator expects 'arrival_rates' as a list
    result = calculate("M/M/1/PNP", arrival_rates=[2, 1], mu=5)
    
    # Check per-class metrics
    per_class = result["per_class"]
    # Class 1 (index 0)
    assert per_class[0]["Wq"] == pytest.approx(0.2, abs=1e-4)
    # Class 2 (index 1)
    assert per_class[1]["Wq"] == pytest.approx(0.5, abs=1e-4)


def test_priority_minimums_enforced():
    with pytest.raises(ValueError, match="pelo menos 3"):
        calculate("PRIORIDADE_PREEMPTIVA_3X3", arrival_rates=[0.2, 0.6], mu=3, s=3)

    with pytest.raises(ValueError, match="<= 3"):
        calculate("PRIORIDADE_PREEMPTIVA_3X3", arrival_rates=[0.2, 0.6, 1.2], mu=3, s=4)

    result = calculate("PRIORIDADE_NAO_PREEMPTIVA_3X3", arrival_rates=[0.2, 0.6, 1.2], mu=3, s=3)
    assert len(result["per_class"]) == 3
    assert result["rho"] < 1
