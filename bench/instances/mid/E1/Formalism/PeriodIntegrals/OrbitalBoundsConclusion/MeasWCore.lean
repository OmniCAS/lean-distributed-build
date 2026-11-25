import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeightedMeasureSplitting.HermitianMeasureSplitting

set_option Elab.async false

namespace E1N.M1482
def val : Nat := E1N.M2047.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1482
