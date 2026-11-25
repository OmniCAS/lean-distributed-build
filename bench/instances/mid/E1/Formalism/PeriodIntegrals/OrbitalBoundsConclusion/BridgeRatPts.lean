import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.FundamentalEquivalence.AdBridge
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.RationalPointsComparison.BridgeApplyEqOfComp

set_option Elab.async false

namespace E1N.M1457
def val : Nat := E1N.M1195.val % 7 + E1N.M1890.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1457
