import E1.Formalism.FormalDegreeBessel.StatementDS
import E1.Formalism.PeriodIntegrals.PhMeasCore
import E1.Formalism.PeriodIntegrals.UpqRep
import E1.Formalism.RealPlaceAnalysis.Complexify
import E1.Formalism.RealPlaceAnalysis.StatementE

set_option Elab.async false

namespace E1N.M1420
def val : Nat := E1N.M192.val % 7 + E1N.M1524.val % 7 + E1N.M2084.val % 7 + E1N.M2097.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
theorem w8 (a b : Nat) : a + b + 8 = b + a + 8 := by omega
end E1N.M1420
