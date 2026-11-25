import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.HaarTransversals.FoldBound
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.HaarTransversals.PoincareSeriesSquareIntegrable

set_option Elab.async false

namespace E1N.M1425
def val : Nat := E1N.M1200.val % 7 + E1N.M1203.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end E1N.M1425
