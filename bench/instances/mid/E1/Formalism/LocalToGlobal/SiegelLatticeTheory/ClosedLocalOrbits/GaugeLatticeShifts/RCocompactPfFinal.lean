import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GaugeLatticeShifts.RCocompactPfApproxFinal
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GaugeLatticeShifts.RCocompactPfMain
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GaugeLatticeShifts.RCocompactPfMem

set_option Elab.async false

namespace E1N.M1042
def val : Nat := E1N.M1040.val % 7 + E1N.M1044.val % 7 + E1N.M1045.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1042
