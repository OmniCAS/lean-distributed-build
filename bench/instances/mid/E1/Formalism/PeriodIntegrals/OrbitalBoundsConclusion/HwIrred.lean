import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HighestWeightIrreducible.Assembly
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HighestWeightIrreducible.ConstructionA
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HighestWeightIrreducible.ConstructionB

set_option Elab.async false

namespace E1N.M1473
def val : Nat := E1N.M1672.val % 7 + E1N.M1675.val % 7 + E1N.M1676.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1473
