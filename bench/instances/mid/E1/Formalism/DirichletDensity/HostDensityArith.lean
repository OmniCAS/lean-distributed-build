import E1.Formalism.DirichletDensity.DirichletDensityProofs.APLogDensity
import E1.Formalism.DirichletDensity.DirichletDensityProofs.HostDensity
import E1.Formalism.DirichletDensity.DirichletDensityProofs.HostDensityArith
import E1.Formalism.DirichletDensity.DirichletDensityProofs.LogToDir
import E1.Formalism.DirichletDensity.DirichletDensityProofs.MQDiscr
import E1.Formalism.DirichletDensity.DirichletDensityProofs.QuadDiscr

set_option Elab.async false

namespace E1N.M81
def val : Nat := E1N.M75.val % 7 + E1N.M76.val % 7 + E1N.M77.val % 7 + E1N.M78.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M81
