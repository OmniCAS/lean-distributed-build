import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeylFormulaCompact.Assemble
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeylFormulaCompact.Blocks
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeylFormulaCompact.DimStep
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeylFormulaCompact.Formula
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeylFormulaCompact.Weights

set_option Elab.async false

namespace E1N.M1518
def val : Nat := E1N.M2063.val % 7 + E1N.M2064.val % 7 + E1N.M2065.val % 7 + E1N.M2068.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1518
