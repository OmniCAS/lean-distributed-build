import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.Cartan
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.Heckecomm
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.Satake
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.Spherical
import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.Tjcosets

set_option Elab.async false

namespace E1N.M2177
def val : Nat := E1N.M2161.val % 7 + E1N.M2196.val % 7 + E1N.M2207.val % 7 + E1N.M2213.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M2177
