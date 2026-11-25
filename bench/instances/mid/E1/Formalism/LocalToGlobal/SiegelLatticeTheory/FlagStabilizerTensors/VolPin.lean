import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GaugeLatticeShifts.Vanish
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.PairVal
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.RealObj
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.FlagStabilizerTensors.ParametersTermRelations

set_option Elab.async false

namespace E1N.M1193
def val : Nat := E1N.M1093.val % 7 + E1N.M1095.val % 7 + E1N.M1096.val % 7 + E1N.M1135.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
end E1N.M1193
