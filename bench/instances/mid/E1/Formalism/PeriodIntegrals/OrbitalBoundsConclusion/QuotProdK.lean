import E1.Formalism.PeriodIntegrals.QuotProdK
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeilQuotientHaar.BruhatDecomposition
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeilQuotientHaar.ConjugationInvariantMeasure
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeilQuotientHaar.HaarMeasureUniqueness
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeilQuotientHaar.LocalWeilRepresentation
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeilQuotientHaar.ProdSetIsClosed
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeilQuotientHaar.QuotProdKOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeilQuotientHaar.SiegelMeasureDefinition
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeilQuotientHaar.WeilQuotientGlobalAssumptions

set_option Elab.async false

namespace E1N.M1496
def val : Nat := E1N.M1528.val % 7 + E1N.M2053.val % 7 + E1N.M2054.val % 7 + E1N.M2056.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1496
