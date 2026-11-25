import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GaugeLatticeShifts.RegroupPfFrameCong
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GaugeLatticeShifts.RegroupPfModGOfAt
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GaugeLatticeShifts.RegroupPfRatIso
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GaugeLatticeShifts.RegroupPfTermCar

set_option Elab.async false

namespace E1N.M1072
def val : Nat := E1N.M1061.val % 7 + E1N.M1062.val % 7 + E1N.M1066.val % 7 + E1N.M1071.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1072
