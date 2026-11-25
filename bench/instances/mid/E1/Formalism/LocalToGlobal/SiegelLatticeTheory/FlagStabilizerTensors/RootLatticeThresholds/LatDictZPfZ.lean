import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.FlagStabilizerTensors.RootLatticeThresholds.LatDictZGlue
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.FlagStabilizerTensors.RootLatticeThresholds.LatDictZPlane
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.FlagStabilizerTensors.RootLatticeThresholds.ZOrbitOfOpen

set_option Elab.async false

namespace E1N.M1157
def val : Nat := E1N.M1154.val % 7 + E1N.M1158.val % 7 + E1N.M1188.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1157
