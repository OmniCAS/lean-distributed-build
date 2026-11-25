import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.FlagStabilizerTensors.RootLatticeThresholds.LatDictZSt
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.FlagStabilizerTensors.RootLatticeThresholds.LatDictZZLoc
import E1.Formalism.SelfDualUnimodular.LocalLatticeDictionary.AlgebraMapNeZero
import E1.Formalism.SelfDualUnimodular.LocalLatticeDictionary.LocFin
import E1.Formalism.SelfDualUnimodular.LocalLatticeDictionary.SemiGenusLocal

set_option Elab.async false

namespace E1N.M1188
def val : Nat := E1N.M1159.val % 7 + E1N.M1160.val % 7 + E1N.M2236.val % 7 + E1N.M2238.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1188
