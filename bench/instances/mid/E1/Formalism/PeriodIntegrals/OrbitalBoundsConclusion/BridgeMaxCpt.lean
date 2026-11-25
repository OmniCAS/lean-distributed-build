import E1.Formalism.PeriodIntegrals.AdBridgeSteps
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.BridgeFinK
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.BridgeRealK
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MaximalCompactConjugacy.Assembly

set_option Elab.async false

namespace E1N.M1456
def val : Nat := E1N.M1407.val % 7 + E1N.M1455.val % 7 + E1N.M1458.val % 7 + E1N.M1836.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1456
