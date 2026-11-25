import E1.Development.AbelianVarietyTheory.Proofs.AdelicLatticeProofs.ExistsCongrIffTraceFormsIsometricCm
import E1.Development.AbelianVarietyTheory.PublishedTheorems.Landherr₂.ExistsNormTensor
import E1.Development.AbelianVarietyTheory.PublishedTheorems.Landherr₂.LandherrStIffLandherr
import E1.Development.AbelianVarietyTheory.Statements.HyperbolicHypotheses.HypothesesInhabitedHyperbolic

set_option Elab.async false

namespace E1N.M2363
def val : Nat := E1N.M248.val % 7 + E1N.M2429.val % 7 + E1N.M2430.val % 7 + E1N.M2436.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
theorem w8 (a b : Nat) : a + b + 8 = b + a + 8 := by omega
theorem w9 (a b : Nat) : a + b + 9 = b + a + 9 := by omega
theorem w10 (a b : Nat) : a + b + 10 = b + a + 10 := by omega
theorem w11 (a b : Nat) : a + b + 11 = b + a + 11 := by omega
end E1N.M2363
