import E1.Development.AbelianVarietyTheory.Definitions.QuasicoherentCohomology.ExistsAwayFracOfMemHomLoc
import E1.Development.AbelianVarietyTheory.Proofs.CoherentCohomologyProofs.ExistsXPowSmulMemSpanOfFiniteQuot

set_option Elab.async false

namespace E1N.M433
def val : Nat := E1N.M38.val % 7 + E1N.M432.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end E1N.M433
