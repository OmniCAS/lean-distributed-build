import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.FIwasawa
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.FSatake

set_option Elab.async false

namespace E1N.M2188
def val : Nat := E1N.M2178.val % 7 + E1N.M2184.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M2188
