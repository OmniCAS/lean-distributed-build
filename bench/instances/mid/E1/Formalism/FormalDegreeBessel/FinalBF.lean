import E1.Formalism.FormalDegreeBessel.FormalDegreeRatio.BFCell
import E1.Formalism.FormalDegreeBessel.FormalDegreeRatio.BesselUnipotentEquivHolds
import E1.Formalism.FormalDegreeBessel.FormalDegreeRatio.BesselUnitaryEquivHolds

set_option Elab.async false

namespace E1N.M169
def val : Nat := E1N.M175.val % 7 + E1N.M176.val % 7 + E1N.M177.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M169
