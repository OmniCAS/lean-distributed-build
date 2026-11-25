import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.ClassInjectiveOfSpanRecovery
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.ClassSetFiniteBoundedHolds
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsApprox
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsAsmHformSmulRight
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsCovol
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsDual
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsEasy
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsEquiv
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsGlob
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsScale
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsSpan
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.CsTrace

set_option Elab.async false

namespace E1N.M2163
def val : Nat := E1N.M2162.val % 7 + E1N.M2164.val % 7 + E1N.M2165.val % 7 + E1N.M2166.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end E1N.M2163
